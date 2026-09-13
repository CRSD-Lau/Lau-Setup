// Author, Creator, Last Modified By: Neil Mitchell
using System;
using System.IO;
using System.Windows.Forms;
using LauSetup;

public static class LocalizationTests {
    static void Check(bool value,string message){if(!value)throw new Exception(message);}
    static Label FindLabel(Control parent,string text){
        foreach(Control control in parent.Controls){var label=control as Label;if(label!=null&&label.Text==text)return label;var found=FindLabel(control,text);if(found!=null)return found;}return null;
    }
    public static void Run(string work) {
        Check(Ui.Resolve("de_DE.UTF-8@euro",false)=="de-DE","locale modifier was not normalized");
        Check(Ui.Resolve("xx:pt_BR:de_DE",true)=="pt-BR","preference list fallback failed");
        Check(Ui.Resolve("es_419",false)=="es-MX"&&Ui.Resolve("es_AR",false)=="es-MX"&&Ui.Resolve("es_ES",false)=="es-ES","Spanish regional selection failed");
        Check(Ui.Resolve("zh_Hant_CN",false)=="zh-TW"&&Ui.Resolve("zh_Hans_TW",false)=="zh-CN"&&Ui.Resolve("zh",false)==null,"Chinese script selection failed");
        Check(Ui.Resolve("xx_YY",false)==null&&Ui.Resolve("%",false)==null,"unsupported locale was accepted");
        Check(Ui.ResolveAutomatic("ru:de-DE","fr-FR",true)=="ru-RU"&&Ui.ResolveAutomatic("ru:de-DE","fr-FR",false)=="fr-FR","Wine host language priority failed");
        Check(Ui.ResolveAutomatic("C","de-DE",true)=="en-US"&&Ui.ResolveAutomatic("POSIX","de-DE",true)=="en-US"&&Ui.ResolveAutomatic(null,"de-DE",true)=="de-DE","Wine C/POSIX precedence failed");
        var wineFonts=new[]{"Liberation Sans","Noto Sans CJK SC","Noto Sans CJK TC","Noto Sans CJK KR"};
        Check(SetupForm.SelectFont("zh-CN",wineFonts,true)=="Noto Sans CJK SC"&&SetupForm.SelectFont("zh-TW",wineFonts,true)=="Noto Sans CJK TC"&&SetupForm.SelectFont("ko-KR",wineFonts,true)=="Noto Sans CJK KR"&&SetupForm.SelectFont("en-US",wineFonts,true)=="Noto Sans CJK SC","Wine CJK font preference failed");

        string preference=Path.Combine(work,"localization-fixture","interface-language.txt");Ui.SetPreferencePathForTests(preference);
        try {
            Ui.Initialize("de-DE",false);Check(Ui.Locale=="de-DE"&&Ui.Choice=="de-DE","requested language was not selected");
            Check(Ui.Select("fr_FR",true),"preference was not written");Ui.Initialize(null,true);Check(Ui.Locale=="fr-FR"&&Ui.Choice=="fr-FR","saved manual choice did not win");
            Ui.Initialize("xx-YY",true);Check(Ui.Locale=="en-US"&&Ui.Choice=="auto"&&File.ReadAllText(preference).Trim()=="fr-FR","invalid explicit request did not safely fall back");
            Ui.Initialize("auto",true);Ui.Initialize(null,true);Check(Ui.Choice=="auto","automatic reset was not saved");
            Check(File.ReadAllText(preference).Trim()=="auto","automatic reset used an unexpected preference value");

            Check(Ui.ResourceLoaded,"compiled test build did not embed translations");string resourceError;Check(Ui.ValidateTranslations(out resourceError),resourceError);
            Ui.Initialize("de-DE",false);string path=@"C:\Games\WoW\WTF\Config.wtf";
            string sourceException="Linked folders are not supported: "+path;
            string translated=Ui.Message(sourceException);
            Check(translated!=sourceException&&translated.Contains(path),"localized exception changed its diagnostic path or remained English");
            string download=Ui.F("Download up to {0}  ·  {1}","123.4 MB","Existing maps kept");
            Check(download.Contains("123.4 MB")&&download.Contains("Existing maps kept"),"localized format removed a dynamic value");

            // Initial selection happens before its event is bound, so opening the form must not create a preference.
            File.Delete(preference);Ui.Initialize("auto",false);
            using(var form=new SetupForm(new Catalog{Version="3.0.8"})) {
                form.StartPosition=FormStartPosition.Manual;form.Location=new System.Drawing.Point(-32000,-32000);form.ShowInTaskbar=false;form.Show();form.PerformLayout();Application.DoEvents();
                var picker=(ComboBox)form.Controls.Find("interfaceLanguage",true)[0];var label=FindLabel(form,Ui.T("Interface language"));
                Check(!File.Exists(preference)&&picker.Visible&&picker.Width>100&&form.ClientSize.Width>=840,"language picker initialization changed preferences or broke layout");
                Check(label!=null,"interface language label is missing");
                picker.SelectedIndex=2; // de-DE, after the Automatic and en-US entries.
                Check(Ui.Locale=="de-DE"&&File.ReadAllText(preference).Trim()=="de-DE","manual picker selection was not saved");
                Check(label.Text==Ui.T("Interface language"),"live language switch did not update static UI text");
            }
        } finally { Ui.SetPreferencePathForTests(null);Ui.Initialize("en-US",false); }
    }
}
