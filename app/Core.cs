// Author, Creator, Last Modified By: Neil Mitchell
using System;
using System.IO;
using System.Linq;
using System.Collections.Generic;
using System.Diagnostics;
using System.Reflection;
using System.Security.Cryptography;
using System.Text;
using System.Text.RegularExpressions;
using System.Threading;
using System.Web.Script.Serialization;
using System.Runtime.InteropServices;
using Microsoft.Win32.SafeHandles;

namespace LauSetup {
// Wine translates Windows paths, but its process and lock namespaces are per-prefix.
// Require the supervised Linux helper for native inspection; never silently downgrade.
public static class WineHost {
    [DllImport("ntdll.dll",CallingConvention=CallingConvention.Cdecl)] static extern IntPtr wine_get_version();
    [DllImport("kernel32.dll",CharSet=CharSet.Unicode,CallingConvention=CallingConvention.Cdecl)] static extern IntPtr wine_get_unix_file_name(string path);
    [DllImport("kernel32.dll")] static extern IntPtr GetProcessHeap();
    [DllImport("kernel32.dll")] static extern bool HeapFree(IntPtr heap,uint flags,IntPtr memory);
    public static readonly bool Active=Detect();
    sealed class HostLease { public string Token,NativePath; }
    static readonly Dictionary<string,HostLease> leases=new Dictionary<string,HostLease>(StringComparer.OrdinalIgnoreCase);
    static bool Detect(){try{return wine_get_version()!=IntPtr.Zero;}catch(EntryPointNotFoundException){return false;}}
    static string Native(string path) {
        string mapped=Path.GetFullPath(path);var suffix=new List<string>();
        IntPtr value=wine_get_unix_file_name(mapped);
        // New backup/staging directories do not exist yet. Map their nearest
        // existing ancestor, then let native no-follow checks inspect the suffix.
        while(value==IntPtr.Zero){string parent=Path.GetDirectoryName(mapped);if(String.IsNullOrEmpty(parent))throw new IOException("Wine could not map this folder to Linux: "+path);suffix.Insert(0,Path.GetFileName(mapped));mapped=parent;value=wine_get_unix_file_name(mapped);}
        try{var bytes=new List<byte>();for(int i=0;i<32768;i++){byte b=Marshal.ReadByte(value,i);if(b==0){string result=Encoding.UTF8.GetString(bytes.ToArray());return suffix.Count==0?result:result.TrimEnd('/')+"/"+String.Join("/",suffix);}bytes.Add(b);}throw new IOException("Wine path is too long.");}
        finally{HeapFree(GetProcessHeap(),0,value);}
    }
    static Dictionary<string,object> Request(string operation,string path,string lease=null) {
        int port;string secret=Environment.GetEnvironmentVariable("LAU_WINE_GUARD_TOKEN");
        if(!Int32.TryParse(Environment.GetEnvironmentVariable("LAU_WINE_GUARD_PORT"),out port)||port<1||port>65535||String.IsNullOrEmpty(secret))
            throw new IOException("On Linux, start Lau Setup using the supplied Wine launcher. Its host safety checks are required.");
        try {
            var request=(System.Net.HttpWebRequest)System.Net.WebRequest.Create("http://127.0.0.1:"+port+"/guard");
            request.Proxy=null;request.Method="POST";request.AllowAutoRedirect=false;request.Timeout=10000;request.ReadWriteTimeout=10000;
            request.ServicePoint.Expect100Continue=false;
            request.Headers["X-Lau-Token"]=secret;request.ContentType="application/json";
            byte[] body=Encoding.UTF8.GetBytes(Json.Text(new{operation,path=operation=="release"?path:Native(path),lease}));request.ContentLength=body.Length;
            using(var output=request.GetRequestStream())output.Write(body,0,body.Length);
            using(var response=request.GetResponse())using(var reader=new StreamReader(response.GetResponseStream())) {
                var result=Json.Parse<Dictionary<string,object>>(reader.ReadToEnd());
                if(!result.ContainsKey("ok")||!(result["ok"] is bool)||(bool)result["ok"]==false)
                    throw new IOException(result.ContainsKey("error")?result["error"].ToString():"Invalid Linux safety response.");
                return result;
            }
        }catch(System.Net.WebException error){throw new IOException("The Linux safety helper is unavailable. Reopen the Wine launcher; any pending backup will remain available for recovery.",error);}
    }
    public static void PathCheck(string path){if(Active)Request("path",path);}
    public static void Check(string root){if(Active){HostLease lease;lock(leases)leases.TryGetValue(root,out lease);Request("check",root,lease==null?null:lease.Token);}}
    public static long AvailableBytes(string root){if(!Active)return new DriveInfo(Path.GetPathRoot(root)).AvailableFreeSpace;HostLease lease;lock(leases)leases.TryGetValue(root,out lease);return Convert.ToInt64(Request("space",root,lease==null?null:lease.Token)["availableBytes"]);}
    public static void Acquire(string root){if(Active){lock(leases){if(leases.ContainsKey(root))throw new IOException("Another installer may be using this client.");var result=Request("acquire",root);leases.Add(root,new HostLease{Token=result["lease"].ToString(),NativePath=result["path"].ToString()});}}}
    public static void Release(string root){if(Active){HostLease lease;lock(leases){if(!leases.TryGetValue(root,out lease))return;leases.Remove(root);}try{Request("release",lease.NativePath,lease.Token);}catch(IOException){/* Launcher owns final lock cleanup if its channel has failed. */}}}
}
public sealed class Part { public string Sha256; public long Bytes; public string Url; public string FileName; }
public sealed class Asset { public string Id; public string Sha256; public long Bytes; public List<Part> Parts; }
public sealed class Catalog {
    public string Author, Creator, LastModifiedBy, Version, InstallerVersion;
    public bool PublicReady;
    public List<string> Locales;
    public Dictionary<string,Asset> Assets;
    public static Catalog Load(string json) {
        var c=Json.Parse<Catalog>(json); c.Validate(); return c;
    }
    public static Catalog Embedded() {
        using(var s=Assembly.GetExecutingAssembly().GetManifestResourceStream("LauSetup.Catalog.json"))
        using(var r=new StreamReader(s)) return Load(r.ReadToEnd());
    }
    public void Validate() {
        if((Version!="3.0.4" && Version!="3.0.5" && Version!="3.0.6" && Version!="3.0.7" && Version!="3.0.8") || Locales==null || Assets==null || Assets.Count>64 || Locales.Count!=9 || Locales.Distinct().Count()!=9) throw new InvalidDataException("Invalid release catalog.");
        foreach(string locale in Locales) if(!Regex.IsMatch(locale,@"^(enUS|deDE|frFR|esES|esMX|koKR|ruRU|zhCN|zhTW)$")) throw new InvalidDataException("Unsupported language.");
        foreach(var entry in Assets) {
            var a=entry.Value;
            if(a==null || entry.Key!=a.Id || !Regex.IsMatch(a.Id,@"^[A-Za-z0-9-]+$") || !Hash.Valid(a.Sha256) || a.Bytes<=0 || a.Bytes>8L*1024*1024*1024 || a.Parts==null || a.Parts.Count==0 || a.Parts.Count>64) throw new InvalidDataException("Invalid asset.");
            long total=0;
            foreach(var p in a.Parts) {
                if(!Hash.Valid(p.Sha256) || p.FileName!=p.Sha256+".bin" || p.Bytes<=0 || p.Bytes>512L*1024*1024 || (!String.IsNullOrEmpty(p.Url) && !ValidDownloadUrl(p))) throw new InvalidDataException("Invalid download segment.");
                if(PublicReady && String.IsNullOrEmpty(p.Url)) throw new InvalidDataException("Public download URL is missing.");
                total=checked(total+p.Bytes);
            }
            if(total!=a.Bytes) throw new InvalidDataException("Download sizes do not match.");
        }
        Get("Executable");Get("Maps");Get("SpellAssets");Get("SpellTables");
        foreach(var loc in Locales) { Get("LoadingQ-"+loc); Get("MapsQ-"+loc); }
        foreach(var mode in new[]{"Non-HD","HD-NewSpells-On","HD-NewSpells-Off"}) foreach(var cons in new[]{"On","Off"}) Get("Y-"+mode+"-Consecration-"+cons);
    }
    public static bool ValidDownloadUrl(Part part) { return new[]{"payload-3.0.4","payload-3.0.5","payload-3.0.6","payload-3.0.7","payload-3.0.8"}.Any(tag=>part.Url=="https://github.com/CRSD-Lau/Lau-Setup/releases/download/"+tag+"/"+part.Sha256+".bin"); }
    public Asset Get(string id) { Asset a; if(!Assets.TryGetValue(id,out a)) throw new InvalidDataException("Missing release component: "+id); return a; }
}
public static class Json {
    public static T Parse<T>(string value) { if(value.Length>8*1024*1024) throw new InvalidDataException("Record too large."); return new JavaScriptSerializer{MaxJsonLength=8*1024*1024}.Deserialize<T>(value); }
    public static string Text(object value) { return new JavaScriptSerializer{MaxJsonLength=8*1024*1024}.Serialize(value); }
    public static void Save(string path,object value) {
        SafePaths.Plain(path);
        var temp=path+"."+Guid.NewGuid().ToString("N")+".new"; SafePaths.Plain(temp);
        using(var fs=new FileStream(temp,FileMode.CreateNew,FileAccess.Write,FileShare.None)) {
            var bytes=Encoding.UTF8.GetBytes(Text(value));fs.Write(bytes,0,bytes.Length);fs.Flush(true);
        }
        if(File.Exists(path)) File.Replace(temp,path,null); else File.Move(temp,path);
    }
}
public static class Hash {
    public static bool Valid(string hash) { return hash!=null && Regex.IsMatch(hash,@"^[a-f0-9]{64}$"); }
    public static string FileHash(string file) {
        using(var s=new FileStream(file,FileMode.Open,FileAccess.Read,FileShare.Read)) using(var hash=SHA256.Create()) return BitConverter.ToString(hash.ComputeHash(s)).Replace("-","").ToLowerInvariant();
    }
    public static bool Matches(string file,string hash,long bytes) { return File.Exists(file) && new FileInfo(file).Length==bytes && FileHash(file)==hash; }
}
public static class SafePaths {
    [StructLayout(LayoutKind.Sequential)] struct FileInformation {
        public uint Attributes;public System.Runtime.InteropServices.ComTypes.FILETIME Creation,Access,Write;
        public uint Volume,SizeHigh,SizeLow,Links,IndexHigh,IndexLow;
    }
    [DllImport("kernel32.dll",SetLastError=true)] static extern bool GetFileInformationByHandle(SafeFileHandle handle,out FileInformation info);
    public static void SingleLink(FileStream stream) {
        FileInformation info;
        if(!GetFileInformationByHandle(stream.SafeFileHandle,out info)||info.Links!=1)throw new IOException("A download cache file is linked to another file. Choose a normal local folder.");
    }
    public static string Root(string root) {
        if(String.IsNullOrWhiteSpace(root) || root.StartsWith(@"\\") || !Path.IsPathRooted(root)) throw new IOException("Choose a local WoW folder.");
        string full=Path.GetFullPath(root).TrimEnd(Path.DirectorySeparatorChar);
        if(full.Length<4 || full.Equals(Path.GetPathRoot(full).TrimEnd('\\'),StringComparison.OrdinalIgnoreCase)) throw new IOException("Choose the game folder, not a drive.");
        Plain(full);return full;
    }
    public static void Plain(string path) {
        string full=Path.GetFullPath(path);
        WineHost.PathCheck(full);
        foreach(string part in full.Substring(Path.GetPathRoot(full).Length).Split('\\')) if(part.EndsWith(".") || part.EndsWith(" ")) throw new IOException("Folder names ending in a dot or space are not supported.");
        string walk=full;
        while(!String.IsNullOrEmpty(walk)) {
            // Wine's drive root itself is a dosdevices mapping. The host helper has
            // already checked its native target and every real path component.
            if(WineHost.Active && walk.Equals(Path.GetPathRoot(full),StringComparison.OrdinalIgnoreCase))break;
            if(File.Exists(walk)||Directory.Exists(walk)) if((File.GetAttributes(walk)&FileAttributes.ReparsePoint)!=0) throw new IOException("Linked folders are not supported: "+walk);
            walk=Path.GetDirectoryName(walk);
        }
    }
    public static string Under(string root,string relative) {
        if(String.IsNullOrWhiteSpace(relative) || relative.IndexOfAny(new[]{':','/','\0'})>=0 || Path.IsPathRooted(relative) || relative.Split('\\').Any(x=>x==".."||x=="."||x.Length==0||x.EndsWith(".")||x.EndsWith(" "))) throw new IOException("Unsafe relative path.");
        string full=Path.GetFullPath(Path.Combine(root,relative));
        if(!full.StartsWith(Path.GetFullPath(root).TrimEnd('\\')+"\\",StringComparison.OrdinalIgnoreCase)) throw new IOException("Path escapes the selected folder.");
        Plain(full);return full;
    }
    public static string Target(string root,string relative,string locale) {
        string expression=@"^(WoW\.exe|Data\\patch-[qmsy]\.mpq|Data\\"+Regex.Escape(locale)+@"\\patch-"+Regex.Escape(locale)+@"-[qmsy]\.mpq)$";
        string disabled=@"^(Data\\patch-s\.mpq\.disabled(?:\.[a-f0-9]{12})?|Data\\"+Regex.Escape(locale)+@"\\patch-"+Regex.Escape(locale)+@"-s\.mpq\.disabled(?:\.[a-f0-9]{12})?)$";
        if(!Regex.IsMatch(relative,expression,RegexOptions.IgnoreCase)&&!Regex.IsMatch(relative,disabled,RegexOptions.IgnoreCase)) throw new IOException("File is outside the install scope: "+relative);
        return Under(root,relative);
    }
    public static void DirectoryFor(string file) { Plain(file); Directory.CreateDirectory(Path.GetDirectoryName(file)); }
}
public sealed class ClientInfo { public string Root,Locale; public bool Hd,NewSpells,MapsInstalled; }
public static class Client {
    public static ClientInfo Inspect(string input,Catalog catalog) {
        string root=SafePaths.Root(input);var exe=SafePaths.Under(root,"WoW.exe");
        if(!File.Exists(exe)) throw new IOException("Choose the folder containing WoW.exe.");
        var v=FileVersionInfo.GetVersionInfo(exe);
        if(v.FileMajorPart!=3 || v.FileMinorPart!=3 || v.FileBuildPart!=5 || v.FilePrivatePart!=12340) throw new IOException("This upgrade requires WoW 3.3.5a build 12340.");
        using(var f=new BinaryReader(File.OpenRead(exe))) {
            if(f.ReadUInt16()!=0x5a4d) throw new IOException("The game executable is invalid.");
            f.BaseStream.Position=0x3c; int pe=f.ReadInt32();if(pe<64 || pe>f.BaseStream.Length-6) throw new IOException("The game executable is invalid.");
            f.BaseStream.Position=pe;if(f.ReadUInt32()!=0x4550 || f.ReadUInt16()!=0x14c) throw new IOException("This upgrade requires the 32-bit WoW client.");
        }
        string config=SafePaths.Under(root,@"WTF\Config.wtf");string locale=null;
        if(File.Exists(config)) {
            var matches=Regex.Matches(File.ReadAllText(config),"(?m)^SET locale \"([A-Za-z]{4})\"\\s*$");
            if(matches.Count>1) throw new IOException("The client language settings are ambiguous.");
            if(matches.Count==1) locale=matches[0].Groups[1].Value;
        }
        if(locale==null) {
            var candidates=catalog.Locales.Where(l=>File.Exists(SafePaths.Under(root,@"Data\"+l+@"\locale-"+l+".mpq"))).ToArray();
            if(candidates.Length!=1) throw new IOException("Launch WoW once to choose its language, then close it and try again.");locale=candidates[0];
        }
        if(!catalog.Locales.Contains(locale) || !File.Exists(SafePaths.Under(root,@"Data\"+locale+@"\locale-"+locale+".mpq"))) throw new IOException("The selected client is missing its matching language files.");
        if(!File.Exists(SafePaths.Under(root,@"Data\common.mpq"))) throw new IOException("This is not a complete existing WoW client. Select its game folder.");
        bool rootF=File.Exists(SafePaths.Under(root,@"Data\patch-f.mpq")),localeF=File.Exists(SafePaths.Under(root,@"Data\"+locale+@"\patch-"+locale+"-F.MPQ"));
        if(rootF!=localeF) throw new IOException("The HD model patches are incomplete. Enable the matching model pack in your client before installing.");
        bool s=File.Exists(SafePaths.Under(root,@"Data\patch-s.mpq"));
        return new ClientInfo{Root=root,Locale=locale,Hd=rootF,NewSpells=rootF&&s,MapsInstalled=Hash.Matches(SafePaths.Under(root,@"Data\patch-m.mpq"),catalog.Get("Maps").Sha256,catalog.Get("Maps").Bytes)};
    }
    public static void AssertClosed(string root) {
        WineHost.Check(root);
        foreach(var p in Process.GetProcesses()) {
            using(p) {
                string name;try{name=p.ProcessName;}catch{continue;}
                if(!new[]{"wow","wow-64","wowclassic"}.Contains(name.ToLowerInvariant())) continue;
                string exe;try{exe=p.MainModule.FileName;}catch{throw new IOException("A WoW process could not be identified. Close WoW before installing.");}
                if(Path.GetDirectoryName(exe).Equals(root,StringComparison.OrdinalIgnoreCase)) throw new IOException("Close this WoW client, then try again.");
            }
        }
    }
}
public sealed class Operation { public string Relative,AssetId,OldHash,SourceRelative,SourceHash; public long OldBytes,SourceBytes; public bool Existed; }
public sealed class InstallPlan {
    public string Root,Locale,Edition;public bool Maps;public List<Operation> Operations=new List<Operation>();
    public long DownloadBytes,StageBytes;
    public static InstallPlan Build(ClientInfo client,Catalog catalog,bool newSpells,bool consecration,bool maps) {
        if(newSpells&&!client.Hd) throw new IOException("New spell visuals require an existing HD model client.");
        maps=maps||client.MapsInstalled;
        string edition=(client.Hd ? (newSpells?"HD-NewSpells-On":"HD-NewSpells-Off") : "Non-HD")+"-Consecration-"+(consecration?"On":"Off");
        var plan=new InstallPlan{Root=SafePaths.Root(client.Root),Locale=client.Locale,Edition=edition,Maps=maps};
        if(!catalog.Locales.Contains(client.Locale)) throw new InvalidDataException("Unsupported language.");
        string loc=@"Data\"+client.Locale+@"\patch-"+client.Locale+"-";
        Action<string,string> add=(path,id)=>{
            var target=SafePaths.Target(plan.Root,path,plan.Locale);bool exists=File.Exists(target);string old=exists?Hash.FileHash(target):null;
            var a=id==null?null:catalog.Get(id);
            if(a==null&&!exists || a!=null&&exists&&old==a.Sha256&&new FileInfo(target).Length==a.Bytes)return;
            plan.Operations.Add(new Operation{Relative=path,AssetId=id,Existed=exists,OldHash=old,OldBytes=exists?new FileInfo(target).Length:0});
            if(a!=null)plan.StageBytes=checked(plan.StageBytes+a.Bytes);
        };
        add("WoW.exe","Executable");
        var q=(maps?"MapsQ-":"LoadingQ-")+client.Locale;
        add(@"Data\patch-q.mpq",q);add(loc+"Q.MPQ",q);
        add(@"Data\patch-y.mpq","Y-"+edition);add(loc+"Y.MPQ","Y-"+edition);
        if(maps){add(@"Data\patch-m.mpq","Maps");add(loc+"M.MPQ",null);}
        if(newSpells) {
            foreach(var pair in new[]{new[]{@"Data\patch-s.mpq","SpellAssets"},new[]{loc+"S.MPQ","SpellTables"}}) {
                string active=pair[0],disabled=active+".disabled";var asset=catalog.Get(pair[1]);
                add(active,pair[1]);
                string disabledPath=SafePaths.Target(plan.Root,disabled,plan.Locale);
                if(Directory.Exists(disabledPath))throw new IOException("The disabled Patch-S destination is a directory: "+disabled);
                if(File.Exists(disabledPath)) {
                    var install=plan.Operations.FirstOrDefault(o=>o.Relative.Equals(active,StringComparison.OrdinalIgnoreCase));
                    if(install!=null&&Hash.Matches(disabledPath,asset.Sha256,asset.Bytes)) {
                        install.SourceRelative=disabled;install.SourceHash=asset.Sha256;install.SourceBytes=asset.Bytes;
                    }
                    // Transaction moves this copy into its verified before backup, including when active S already matches.
                    add(disabled,null);
                }
            }
        }
        else foreach(string active in new[]{@"Data\patch-s.mpq",loc+"S.MPQ"}) {
            string source=SafePaths.Target(plan.Root,active,plan.Locale);
            if(!File.Exists(source))continue;
            string digest=Hash.FileHash(source);long bytes=new FileInfo(source).Length;
            if(bytes==0)throw new IOException("An empty Patch-S file needs checking: "+active);
            string disabled=active+".disabled",target=SafePaths.Target(plan.Root,disabled,plan.Locale);
            if(Directory.Exists(target))throw new IOException("The disabled Patch-S destination is a directory: "+disabled);
            bool exists=File.Exists(target);string oldHash=exists?Hash.FileHash(target):null;long oldBytes=exists?new FileInfo(target).Length:0;
            if(exists&&oldHash!=digest){
                if(oldBytes==0)throw new IOException("An empty disabled Patch-S file needs checking: "+disabled);
                string archived=disabled+"."+oldHash.Substring(0,12),archivePath=SafePaths.Target(plan.Root,archived,plan.Locale);
                if(Directory.Exists(archivePath)||File.Exists(archivePath)&&!Hash.Matches(archivePath,oldHash,oldBytes))throw new IOException("A hash-named disabled Patch-S was changed. Keep it and check this file before retrying: "+archived);
                if(!File.Exists(archivePath)){
                    plan.Operations.Add(new Operation{Relative=archived,SourceRelative=disabled,SourceHash=oldHash,SourceBytes=oldBytes});
                    plan.StageBytes=checked(plan.StageBytes+oldBytes);
                }
            }
            // The just-disabled active file always receives the plain .disabled name.
            if(!exists||oldHash!=digest){
                plan.Operations.Add(new Operation{Relative=disabled,Existed=exists,OldHash=oldHash,OldBytes=oldBytes,SourceRelative=active,SourceHash=digest,SourceBytes=bytes});
                plan.StageBytes=checked(plan.StageBytes+bytes);
            }
            add(active,null);
        }
        foreach(var id in plan.Operations.Where(o=>o.AssetId!=null&&o.SourceRelative==null).Select(o=>o.AssetId).Distinct())plan.DownloadBytes=checked(plan.DownloadBytes+catalog.Get(id).Bytes);
        return plan;
    }
}
public sealed class JournalEntry { public string Relative,OldHash,NewHash;public long OldBytes,NewBytes;public bool Existed; }
public sealed class Journal {
    public string Author="Neil Mitchell",Creator="Neil Mitchell",LastModifiedBy="Neil Mitchell";
    public string Root,Locale,Edition,Status,CreatedUtc; public List<JournalEntry> Files;
}
public sealed class ClientLease:IDisposable {
    readonly string root;FileStream stream;
    ClientLease(string root,FileStream stream){this.root=root;this.stream=stream;}
    public static ClientLease Acquire(string root){
        root=SafePaths.Root(root);WineHost.Acquire(root);
        try{string state=Transaction.StateRoot(root);Directory.CreateDirectory(state);return new ClientLease(root,new FileStream(SafePaths.Under(state,"installer.lock"),FileMode.OpenOrCreate,FileAccess.ReadWrite,FileShare.None));}
        catch{WineHost.Release(root);throw;}
    }
    public void Assert(string selected){if(stream==null||!root.Equals(SafePaths.Root(selected),StringComparison.OrdinalIgnoreCase))throw new IOException("The client operation lock is no longer held.");WineHost.Check(root);}
    public void Dispose(){if(stream!=null){stream.Dispose();stream=null;WineHost.Release(root);}}
}
public sealed class Transaction {
    readonly Catalog catalog;readonly Action<string> report;readonly Action<string> guard;
    internal Action<int> AfterMove { get; set; }
    internal Action<int> AfterRestore { get; set; }
    public Transaction(Catalog catalog,Action<string> report,Action<string> processGuard) { this.catalog=catalog;this.report=report??(s=>{});guard=processGuard??Client.AssertClosed; }
    public static string StateRoot(string root) { return SafePaths.Under(root,"LauSetupBackups"); }
    public static string[] Journals(string root) {
        string path=SafePaths.Under(StateRoot(root),"transactions");
        if(!Directory.Exists(path))return new string[0];
        return Directory.GetDirectories(path).Select(d=>SafePaths.Under(d,"install.json")).Where(File.Exists).OrderByDescending(x=>x,StringComparer.Ordinal).ToArray();
    }
    public static string Status(string record) {
        SafePaths.Plain(record);
        if(new FileInfo(record).Length>8*1024*1024)throw new IOException("A backup record is damaged. Keep the backups and contact support.");
        var j=Json.Parse<Journal>(File.ReadAllText(record));
        if(j==null||j.Status==null)throw new IOException("A backup record is damaged. Keep the backups and contact support.");
        return j.Status;
    }
    public static string Pending(string root) { return Journals(root).FirstOrDefault(f=>new[]{"STAGING","COMMITTING","RESTORING","RECOVERY_REQUIRED"}.Contains(Status(f))); }
    public string Install(InstallPlan plan,Dictionary<string,string> assets,CancellationToken token) {
        using(var lease=ClientLease.Acquire(plan.Root))return InstallWithLease(plan,assets,token,lease);
    }
    public string InstallWithLease(InstallPlan plan,Dictionary<string,string> assets,CancellationToken token,ClientLease lease) {
        lease.Assert(plan.Root);
        guard(plan.Root);if(Pending(plan.Root)!=null)throw new IOException("An interrupted install needs restoring first. Click Restore previous install.");
        string state=StateRoot(plan.Root);Directory.CreateDirectory(state);
        {
            if(plan.Operations.Count==0){report("This release is already installed.");return null;}
            if(WineHost.AvailableBytes(plan.Root)<plan.StageBytes+256L*1024*1024)throw new IOException("Not enough free space to stage this update safely.");
            var seen=new HashSet<string>(StringComparer.OrdinalIgnoreCase);
            foreach(var op in plan.Operations) {
                if(!seen.Add(op.Relative))throw new IOException("Duplicate install destination.");
                var path=SafePaths.Target(plan.Root,op.Relative,plan.Locale);
                if(op.SourceRelative!=null){
                    bool disable=op.SourceRelative.EndsWith("s.mpq",StringComparison.OrdinalIgnoreCase)&&op.Relative.Equals(op.SourceRelative+".disabled",StringComparison.OrdinalIgnoreCase);
                    bool archive=op.SourceRelative.EndsWith("s.mpq.disabled",StringComparison.OrdinalIgnoreCase)&&op.Relative.Equals(op.SourceRelative+"."+(op.SourceHash??"").Substring(0,Math.Min(12,(op.SourceHash??"").Length)),StringComparison.OrdinalIgnoreCase)&&!op.Existed;
                    bool enable=op.AssetId!=null&&(op.AssetId=="SpellAssets"&&op.Relative.Equals(@"Data\patch-s.mpq",StringComparison.OrdinalIgnoreCase)||op.AssetId=="SpellTables"&&op.Relative.Equals(@"Data\"+plan.Locale+@"\patch-"+plan.Locale+"-S.MPQ",StringComparison.OrdinalIgnoreCase))&&op.SourceRelative.Equals(op.Relative+".disabled",StringComparison.OrdinalIgnoreCase)&&op.SourceHash==catalog.Get(op.AssetId).Sha256&&op.SourceBytes==catalog.Get(op.AssetId).Bytes;
                    if((op.AssetId!=null&&!enable)||(!disable&&!archive&&!enable)||!Hash.Valid(op.SourceHash)||op.SourceBytes<=0)throw new IOException("Invalid disabled Patch-S operation.");
                    var source=SafePaths.Target(plan.Root,op.SourceRelative,plan.Locale);
                    if(!Hash.Matches(source,op.SourceHash,op.SourceBytes)||!plan.Operations.Any(x=>x.Relative.Equals(op.SourceRelative,StringComparison.OrdinalIgnoreCase)&&x.AssetId==null&&x.Existed&&x.OldHash==op.SourceHash&&x.OldBytes==op.SourceBytes&&(disable||enable?x.SourceRelative==null:x.SourceRelative!=null)))throw new IOException("Patch-S changed after the install was prepared.");
                }
                if(Directory.Exists(path))throw new IOException("An install destination is a directory: "+op.Relative);
                if(op.Existed ? !Hash.Matches(path,op.OldHash,op.OldBytes) : File.Exists(path))throw new IOException("A game file changed after the install was prepared. Please choose the folder again.");
            }
            string dir=SafePaths.Under(state,@"transactions\"+DateTime.UtcNow.ToString("yyyyMMdd-HHmmss-fffffff")+"-"+Guid.NewGuid().ToString("N"));Directory.CreateDirectory(dir);
            var journal=new Journal{Root=plan.Root,Locale=plan.Locale,Edition=plan.Edition,CreatedUtc=DateTime.UtcNow.ToString("o"),Status="STAGING",Files=new List<JournalEntry>()};
            string record=SafePaths.Under(dir,"install.json");
            foreach(var op in plan.Operations) {
                var a=op.AssetId==null?null:catalog.Get(op.AssetId);
                journal.Files.Add(new JournalEntry{Relative=op.Relative,Existed=op.Existed,OldHash=op.OldHash,OldBytes=op.OldBytes,NewHash=a==null?op.SourceHash:a.Sha256,NewBytes=a==null?op.SourceBytes:a.Bytes});
            }
            Json.Save(record,journal);
            try {
            foreach(var op in plan.Operations) {
                token.ThrowIfCancellationRequested();var a=op.AssetId==null?null:catalog.Get(op.AssetId);
                if(a!=null||op.SourceRelative!=null) {
                    string src,expectedHash;long expectedBytes;
                    if(a!=null&&op.SourceRelative==null){expectedHash=a.Sha256;expectedBytes=a.Bytes;if(!assets.TryGetValue(a.Id,out src))throw new IOException("Downloaded file verification failed.");}
                    else {src=SafePaths.Target(plan.Root,op.SourceRelative,plan.Locale);expectedHash=op.SourceHash;expectedBytes=op.SourceBytes;}
                    if(!Hash.Matches(src,expectedHash,expectedBytes))throw new IOException("Source file verification failed.");
                    string stage=SafePaths.Under(dir,@"staged\"+op.Relative);SafePaths.DirectoryFor(stage);File.Copy(src,stage);
                    if(!Hash.Matches(stage,expectedHash,expectedBytes))throw new IOException("Staged file verification failed.");
                }
            }
            guard(plan.Root);token.ThrowIfCancellationRequested();
            foreach(var op in plan.Operations) {
                string path=SafePaths.Target(plan.Root,op.Relative,plan.Locale);
                if(op.Existed ? !Hash.Matches(path,op.OldHash,op.OldBytes) : File.Exists(path))throw new IOException("Game files changed while downloading. No install was applied.");
            }
            } catch { CleanupStages(dir,journal);journal.Status="ABORTED";Json.Save(record,journal);throw; }
            journal.Status="COMMITTING";Json.Save(record,journal);
            try {
                for(int i=0;i<journal.Files.Count;i++) {
                    token.ThrowIfCancellationRequested();guard(plan.Root);var entry=journal.Files[i];string path=SafePaths.Target(plan.Root,entry.Relative,plan.Locale);
                    if(entry.Existed?!Hash.Matches(path,entry.OldHash,entry.OldBytes):File.Exists(path))throw new IOException("A game file changed before installation. Restoring your backup.");
                    report("Installing "+entry.Relative+"…");
                    if(entry.Existed) { var before=SafePaths.Under(dir,@"before\"+entry.Relative);SafePaths.DirectoryFor(before);File.Move(path,before);if(!Hash.Matches(before,entry.OldHash,entry.OldBytes))throw new IOException("Backup verification failed."); }
                    if(AfterMove!=null)AfterMove(i);
                    if(entry.NewHash!=null){SafePaths.DirectoryFor(path);File.Move(SafePaths.Under(dir,@"staged\"+entry.Relative),path);}
                }
                foreach(var entry in journal.Files) {
                    var path=SafePaths.Target(plan.Root,entry.Relative,plan.Locale);
                    if(entry.NewHash==null ? File.Exists(path) : !Hash.Matches(path,entry.NewHash,entry.NewBytes))throw new IOException("Final install verification failed.");
                }
                journal.Status="INSTALLED";Json.Save(record,journal);report("Installed and verified. Your backup is ready.");return record;
            } catch(Exception original) {
                try{RestoreInternal(record);report("The install did not finish. Your previous files were restored.");}
                catch(Exception recovery){journal.Status="RECOVERY_REQUIRED";Json.Save(record,journal);throw new IOException("Installation stopped. Close WoW and use Restore previous install. Backup: "+dir+". "+recovery.Message,original);}
                throw;
            }
        }
    }
    public void Restore(string record) {
        var j=ReadBackup(record);string root=SafePaths.Root(j.Root);guard(root);
        using(var gate=ClientLease.Acquire(root))RestoreInternal(record);
    }
    public Journal ReadBackup(string record) {
        Status(record);var j=Json.Parse<Journal>(File.ReadAllText(record));string root=SafePaths.Root(j.Root);
        string expected=SafePaths.Under(StateRoot(root),"transactions")+"\\";
        if(!Path.GetFullPath(record).StartsWith(expected,StringComparison.OrdinalIgnoreCase)||!String.Equals(Path.GetDirectoryName(Path.GetDirectoryName(record))+"\\",expected,StringComparison.OrdinalIgnoreCase)||Path.GetFileName(record)!="install.json"||!catalog.Locales.Contains(j.Locale)||j.Files==null||j.Files.Count>13||j.Files.Count==0)throw new IOException("Invalid backup record.");
        if(!new[]{"INSTALLED","STAGING","COMMITTING","RESTORING","RECOVERY_REQUIRED"}.Contains(j.Status))throw new IOException("This backup has already been restored or was not installed.");
        var seen=new HashSet<string>(StringComparer.OrdinalIgnoreCase);
        foreach(var e in j.Files) {
            if(e==null||!seen.Add(e.Relative)||e.OldBytes<0||(e.Existed&&!Hash.Valid(e.OldHash))||(!e.Existed&&(e.OldHash!=null||e.OldBytes!=0))||(e.NewHash!=null&&(!Hash.Valid(e.NewHash)||e.NewBytes<=0))||(e.NewHash==null&&e.NewBytes!=0))throw new IOException("Invalid backup entry.");
            SafePaths.Target(root,e.Relative,j.Locale);
        }
        return j;
    }
    static void CleanupStages(string dir,Journal journal) {
        foreach(var e in journal.Files) {
            var stage=SafePaths.Under(dir,@"staged\"+e.Relative);
            if(File.Exists(stage))File.Delete(stage);
        }
    }
    void CheckRestoreEntry(string root,string dir,Journal j,JournalEntry e,bool strict) {
        var path=SafePaths.Target(root,e.Relative,j.Locale);var before=SafePaths.Under(dir,@"before\"+e.Relative);
        if(e.Existed&&File.Exists(before)&&!Hash.Matches(before,e.OldHash,e.OldBytes))throw new IOException("An original backup has changed: "+e.Relative);
        if(e.Existed&&!File.Exists(before)&&!Hash.Matches(path,e.OldHash,e.OldBytes))throw new IOException("An original backup is missing: "+e.Relative);
        if(File.Exists(path)&&!((e.Existed&&Hash.Matches(path,e.OldHash,e.OldBytes))||(e.NewHash!=null&&Hash.Matches(path,e.NewHash,e.NewBytes))))throw new IOException("A game file was changed by another update. Restore stopped to preserve it: "+e.Relative);
        if(strict&&(e.NewHash==null?File.Exists(path):!Hash.Matches(path,e.NewHash,e.NewBytes)))throw new IOException("Installed files changed since this backup. Restore stopped.");
    }
    void RestoreInternal(string record) {
        var j=ReadBackup(record);string root=SafePaths.Root(j.Root);
        var dir=Path.GetDirectoryName(record);guard(root);
        foreach(var e in j.Files) {
            CheckRestoreEntry(root,dir,j,e,j.Status=="INSTALLED");
        }
        j.Status="RESTORING";Json.Save(record,j);int restored=0;
        foreach(var e in j.Files.AsEnumerable().Reverse()) {
            guard(root);var path=SafePaths.Target(root,e.Relative,j.Locale);var before=SafePaths.Under(dir,@"before\"+e.Relative);
            CheckRestoreEntry(root,dir,j,e,false);
            if(e.Existed&&File.Exists(before)) {
                if(File.Exists(path))File.Delete(path);
                File.Move(before,path);
            } else if(!e.Existed&&File.Exists(path))File.Delete(path);
            if(AfterRestore!=null)AfterRestore(restored);restored++;
        }
        foreach(var e in j.Files){var path=SafePaths.Target(root,e.Relative,j.Locale);if(e.Existed?!Hash.Matches(path,e.OldHash,e.OldBytes):File.Exists(path))throw new IOException("Restored file verification failed.");}
        CleanupStages(dir,j);j.Status="RESTORED";Json.Save(record,j);report("Previous install restored and verified.");
    }
}
}
