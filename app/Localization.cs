// Author, Creator, Last Modified By: Neil Mitchell
using System;
using System.Collections.Generic;
using System.Globalization;
using System.IO;
using System.Reflection;
using System.Text;
using System.Web.Script.Serialization;

namespace LauSetup {
public sealed class LanguageOption {
    readonly string name;
    public string Code { get; private set; }
    public string Name { get { return Code=="auto"?Ui.T("Automatic (system language)"):name; } }
    public LanguageOption(string code,string name){Code=code;this.name=name;}
}

public static class Ui {
    const string ResourceName="LauSetup.Translations.json";
    const int PreferenceLimit=128;
    static readonly LanguageOption[] languageOptions=new[]{
        new LanguageOption("auto","Automatic (system language)"),new LanguageOption("en-US","English (US)"),
        new LanguageOption("de-DE","Deutsch"),new LanguageOption("fr-FR","Français"),
        new LanguageOption("es-ES","Español (España)"),new LanguageOption("es-MX","Español (México)"),
        new LanguageOption("ko-KR","한국어"),new LanguageOption("ru-RU","Русский"),
        new LanguageOption("zh-CN","简体中文"),new LanguageOption("zh-TW","繁體中文"),
        new LanguageOption("pt-BR","Português (Brasil)")};
    static Dictionary<string,Dictionary<string,string>> translations;
    static bool attemptedLoad;
    static string preferencePathForTests;

    public static string Locale { get; private set; }
    public static string Choice { get; private set; }
    public static string LastPreferenceError { get; private set; }
    public static bool ResourceLoaded { get { EnsureTranslations();return translations!=null; } }
    public static LanguageOption[] Languages { get { return (LanguageOption[])languageOptions.Clone(); } }

    static Ui(){Locale="en-US";Choice="auto";}

    // This method exists solely for isolated tests. Production always uses user-local app data.
    public static void SetPreferencePathForTests(string path) {
        if(String.IsNullOrEmpty(path)) { preferencePathForTests=null; return; }
        preferencePathForTests=Path.GetFullPath(path);
    }

    public static void Initialize(string requested=null,bool readPreference=true) {
        LastPreferenceError=null;
        if(requested!=null) {
            string explicitChoice=NormalizeChoice(requested);
            if(explicitChoice==null) { Choice="auto";Locale="en-US";return; }
            Apply(explicitChoice);if(readPreference)WritePreference(explicitChoice);return;
        }
        string choice=NormalizeChoice(requested);
        if(choice==null && readPreference) choice=ReadPreference();
        if(choice==null) choice="auto";
        Apply(choice);
    }

    public static bool Select(string choice,bool persist=true) {
        string normalized=NormalizeChoice(choice);
        if(normalized==null) throw new ArgumentException("Unsupported interface language.","choice");
        Apply(normalized);
        if(!persist) { LastPreferenceError=null; return true; }
        return WritePreference(normalized);
    }

    static void Apply(string choice) {
        Choice=choice;
        Locale=choice=="auto" ? ResolveAutomatic() : choice;
    }

    static string ResolveAutomatic() {
        string current;
        try { current=CultureInfo.CurrentUICulture.Name; } catch(CultureNotFoundException) { current=null; }
        return ResolveAutomatic(Environment.GetEnvironmentVariable("LAU_UI_LANGUAGE"),current,WineHost.Active);
    }

    internal static string ResolveAutomatic(string hostHint,string systemCulture,bool wine) {
        if(wine) {
            if(!String.IsNullOrWhiteSpace(hostHint)) {
                string hostResolved=Resolve(hostHint,true);
                return hostResolved ?? "en-US";
            }
            string resolved=Resolve(hostHint,true);
            if(resolved!=null) return resolved;
        }
        return Resolve(systemCulture,false) ?? "en-US";
    }

    // Pure resolver retained for test coverage of launcher preference ordering.
    public static string Resolve(string value,bool preferenceList) {
        if(String.IsNullOrEmpty(value)) return null;
        string[] candidates=preferenceList ? value.Split(':') : new[]{value};
        foreach(string candidate in candidates) {
            string resolved=NormalizeLocale(candidate);
            if(resolved!=null) return resolved;
        }
        return null;
    }

    static string NormalizeChoice(string value) {
        if(String.IsNullOrEmpty(value)) return null;
        string candidate=Clean(value);
        if(candidate=="auto") return "auto";
        return NormalizeLocale(candidate);
    }

    static string NormalizeLocale(string value) {
        string candidate=Clean(value);
        if(String.IsNullOrEmpty(candidate)) return null;
        string[] pieces=candidate.Split('-');
        string language=pieces[0].ToLowerInvariant();
        if(language=="en") return "en-US";
        if(language=="de") return "de-DE";
        if(language=="fr") return "fr-FR";
        if(language=="ko") return "ko-KR";
        if(language=="ru") return "ru-RU";
        if(language=="pt") return "pt-BR";
        if(language=="es") {
            foreach(string item in pieces) if(item.Equals("mx",StringComparison.OrdinalIgnoreCase)||item=="419"||IsLatinAmericanSpanishRegion(item)) return "es-MX";
            return "es-ES";
        }
        if(language=="zh") {
            foreach(string item in pieces) if(item.Equals("hans",StringComparison.OrdinalIgnoreCase)) return "zh-CN";
            foreach(string item in pieces) if(item.Equals("hant",StringComparison.OrdinalIgnoreCase)) return "zh-TW";
            foreach(string item in pieces) if(item.Equals("cn",StringComparison.OrdinalIgnoreCase)||item.Equals("sg",StringComparison.OrdinalIgnoreCase)) return "zh-CN";
            foreach(string item in pieces) if(item.Equals("tw",StringComparison.OrdinalIgnoreCase)||item.Equals("hk",StringComparison.OrdinalIgnoreCase)||item.Equals("mo",StringComparison.OrdinalIgnoreCase)) return "zh-TW";
            return null; // Bare Chinese has no safe script choice.
        }
        return null;
    }

    static bool IsLatinAmericanSpanishRegion(string value) {
        return Array.IndexOf(new[]{"ar","bo","br","bz","cl","co","cr","cu","do","ec","sv","gt","hn","ni","pa","py","pe","pr","uy","ve"},value.ToLowerInvariant())>=0;
    }

    static string Clean(string value) {
        if(value==null) return null;
        string candidate=value.Trim();
        try { candidate=Uri.UnescapeDataString(candidate); } catch(UriFormatException) { return null; }
        int modifier=candidate.IndexOf('@');if(modifier>=0) candidate=candidate.Substring(0,modifier);
        int encoding=candidate.IndexOf('.');if(encoding>=0) candidate=candidate.Substring(0,encoding);
        return candidate.Replace('_','-').Trim().ToLowerInvariant();
    }

    public static string T(string english) {
        if(english==null) return null;
        EnsureTranslations();
        Dictionary<string,string> language;
        string translated;
        if(translations!=null && translations.TryGetValue(Locale,out language) && language!=null && language.TryGetValue(english,out translated) && !String.IsNullOrEmpty(translated)) return translated;
        return english;
    }

    public static string F(string english,params object[] args) {
        return Format(T(english),english,args);
    }

    public static string Message(string english) {
        return Message(english,0);
    }

    static string Message(string english,int depth) {
        if(english==null) return null;
        string exact=T(english);
        if(!String.Equals(exact,english,StringComparison.Ordinal) || HasExactKey(english)) return exact;
        EnsureTranslations();
        if(translations==null) return english;
        Dictionary<string,string> language;
        if(!translations.TryGetValue(Locale,out language) || language==null) return english;
        foreach(string template in language.Keys) {
            object[] values;
            if(TryCapture(template,english,out values)) {
                if(depth<4) for(int i=0;i<values.Length;i++) if(values[i]!=null) values[i]=Message(values[i].ToString(),depth+1);
                return Format(language[template],template,values);
            }
        }
        return english;
    }

    static bool HasExactKey(string english) {
        EnsureTranslations();
        Dictionary<string,string> language;
        return translations!=null && translations.TryGetValue(Locale,out language) && language!=null && language.ContainsKey(english);
    }

    static string Format(string translated,string fallback,object[] args) {
        try { return String.Format(CultureInfo.CurrentCulture,translated,args??new object[0]); }
        catch(FormatException) { return String.Format(CultureInfo.CurrentCulture,fallback,args??new object[0]); }
    }

    static bool TryCapture(string template,string message,out object[] values) {
        values=null;
        var parts=new List<string>();var indexes=new List<int>();int cursor=0,max=-1;
        while(cursor<template.Length) {
            int open=template.IndexOf('{',cursor);if(open<0) break;
            int close=template.IndexOf('}',open+1);if(close<0) return false;
            int index;
            if(!Int32.TryParse(template.Substring(open+1,close-open-1),out index)||index<0||index>31) return false;
            parts.Add(template.Substring(cursor,open-cursor));indexes.Add(index);if(index>max)max=index;cursor=close+1;
        }
        if(indexes.Count==0) return false;
        parts.Add(template.Substring(cursor));
        if(parts[0].Length==0) return false; // A diagnostic needs a literal leading anchor.
        int position=0;values=new object[max+1];
        for(int i=0;i<indexes.Count;i++) {
            string prefix=parts[i];
            if(message.IndexOf(prefix,position,StringComparison.Ordinal)!=position) return false;
            position+=prefix.Length;
            string suffix=parts[i+1];int end;
            if(suffix.Length==0) end=i==indexes.Count-1?message.Length:position;
            else { end=message.IndexOf(suffix,position,StringComparison.Ordinal);if(end<0)return false; }
            if(values[indexes[i]]!=null) return false;
            values[indexes[i]]=message.Substring(position,end-position);position=end;
        }
        return position==message.Length-parts[parts.Count-1].Length && message.EndsWith(parts[parts.Count-1],StringComparison.Ordinal);
    }

    static string PreferencePath {
        get {
            if(preferencePathForTests!=null) return preferencePathForTests;
            string basePath=Environment.GetFolderPath(Environment.SpecialFolder.LocalApplicationData);
            if(String.IsNullOrEmpty(basePath)||!Path.IsPathRooted(basePath))throw new IOException("Local application data is unavailable.");
            return Path.Combine(basePath,"LauSetup","interface-language.txt");
        }
    }

    static string ReadPreference() {
        try {
            string path=PreferencePath;if(!File.Exists(path))return null;
            var info=new FileInfo(path);if(info.Length<0||info.Length>PreferenceLimit) return null;
            using(var reader=new StreamReader(new FileStream(path,FileMode.Open,FileAccess.Read,FileShare.Read),Encoding.UTF8,true)) {
                char[] buffer=new char[PreferenceLimit+1];int count=reader.Read(buffer,0,buffer.Length);if(count>PreferenceLimit)return null;
                return NormalizeChoice(new string(buffer,0,count));
            }
        } catch(Exception error) { LastPreferenceError=error.Message; return null; }
    }

    static bool WritePreference(string choice) {
        string temporary=null;
        try {
            string path=PreferencePath;string directory=Path.GetDirectoryName(path);Directory.CreateDirectory(directory);
            temporary=Path.Combine(directory,"interface-language."+Guid.NewGuid().ToString("N")+".new");
            File.WriteAllText(temporary,choice+Environment.NewLine,new UTF8Encoding(false));
            if(File.Exists(path)) File.Replace(temporary,path,null); else File.Move(temporary,path);
            LastPreferenceError=null;return true;
        } catch(Exception error) { LastPreferenceError=error.Message; return false; }
        finally { if(temporary!=null)try{if(File.Exists(temporary))File.Delete(temporary);}catch(Exception){} }
    }

    static void EnsureTranslations() {
        if(attemptedLoad)return;attemptedLoad=true;
        try {
            using(Stream stream=Assembly.GetExecutingAssembly().GetManifestResourceStream(ResourceName)) {
                if(stream==null)return;
                using(var reader=new StreamReader(stream,Encoding.UTF8,true)) {
                    var document=new JavaScriptSerializer{MaxJsonLength=2*1024*1024}.Deserialize<TranslationDocument>(reader.ReadToEnd());
                    string error;if(!ValidateDocument(document,out error))return;
                    translations=document.languages;
                }
            }
        } catch(Exception) { translations=null; }
    }

    public static bool ValidateTranslations(out string error) {
        EnsureTranslations();
        if(translations==null){error="Translations resource is missing or invalid.";return false;}
        error=null;return true;
    }

    static bool ValidateDocument(TranslationDocument document,out string error) {
        if(document==null||document.Author!="Neil Mitchell"||document.Creator!="Neil Mitchell"||document.LastModifiedBy!="Neil Mitchell"||document.languages==null){error="Translations metadata is invalid.";return false;}
        Dictionary<string,string> source;
        if(!document.languages.TryGetValue("en-US",out source)||source==null||source.Count==0){error="English translations are missing.";return false;}
        foreach(LanguageOption option in languageOptions) {
            if(option.Code=="auto")continue;
            Dictionary<string,string> language;
            if(!document.languages.TryGetValue(option.Code,out language)||language==null){error="Translations are incomplete: "+option.Code;return false;}
            foreach(string key in source.Keys) {
                string translated;
                if(!language.TryGetValue(key,out translated)||String.IsNullOrEmpty(translated)){error="Translations are incomplete: "+option.Code+" / "+key;return false;}
            }
        }
        error=null;return true;
    }

    sealed class TranslationDocument {
        public string Author { get; set; }
        public string Creator { get; set; }
        public string LastModifiedBy { get; set; }
        public Dictionary<string,Dictionary<string,string>> languages { get; set; }
    }
}
}
