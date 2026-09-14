// Author, Creator, Last Modified By: Neil Mitchell
using System;
using System.IO;
using System.Linq;
using System.Text;
using System.Net;
using System.Net.Sockets;
using System.Diagnostics;
using System.Collections.Generic;
using System.Threading;
using System.Threading.Tasks;
using System.Reflection;
using System.Runtime.InteropServices;
using System.Windows.Forms;
using LauSetup;

public static class Tests {
    [DllImport("kernel32.dll",CharSet=CharSet.Unicode,SetLastError=true)] static extern bool CreateHardLink(string link,string existing,IntPtr reserved);
    static string work,realExe;static int passed;static List<object> results=new List<object>();
    static void Check(bool condition,string message){if(!condition)throw new Exception(message);}
    static void Fails(Action action,string fragment=null){try{action();}catch(Exception e){if(fragment!=null)Check(e.ToString().Contains(fragment),"Wrong error: "+e);return;}throw new Exception("Expected rejection.");}
    static string Put(string path,byte[] bytes){Directory.CreateDirectory(Path.GetDirectoryName(path));File.WriteAllBytes(path,bytes);return path;}
    static string Put(string path,string value){return Put(path,Encoding.UTF8.GetBytes(value));}
    static readonly string startAt=Environment.GetEnvironmentVariable("LAU_TEST_START_AT");static bool testStarted=String.IsNullOrEmpty(startAt);
    static void Test(string name,Action run){if(!testStarted){if(name!=startAt)return;testStarted=true;}var start=DateTime.UtcNow;try{run();passed++;results.Add(new{name,status="PASS",seconds=(DateTime.UtcNow-start).TotalSeconds});Console.WriteLine("PASS "+name);}catch(Exception e){results.Add(new{name,status="FAIL",error=e.ToString()});throw;}}
    static void Guard(string root){}
    static byte[] ScanFixture(params string[] names){return ScanFixtureSize(8,false,names);}
    static byte[] ScanFixtureSize(int count,bool invalidTail,params string[] names){
        uint[] table=new uint[count*4];for(int i=0;i<table.Length;i++)table[i]=0xFFFFFFFF;
        for(int i=0;i<names.Length;i++){int slot=(count-1-i)*4;table[slot]=MpqScan.NameHash(names[i],1);table[slot+1]=MpqScan.NameHash(names[i],2);table[slot+2]=0;table[slot+3]=(uint)i;}
        if(invalidTail)table[table.Length-1]=(uint)names.Length;
        uint key=MpqScan.NameHash("(hash table)",3),seed=0xEEEEEEEE;uint[] crypt=new uint[1280];uint z=0x100001;
        for(int i=0;i<256;i++)for(int j=0;j<5;j++){z=(z*125+3)%0x2AAAAB;uint hi=(z&65535)<<16;z=(z*125+3)%0x2AAAAB;crypt[i+j*256]=hi|(z&65535);}
        using(var m=new MemoryStream())using(var w=new BinaryWriter(m)){w.Write(0x1A51504Du);w.Write(32u);w.Write((uint)(32+count*16));w.Write((ushort)0);w.Write((ushort)3);w.Write(32u);w.Write((uint)(32+count*16));w.Write((uint)count);w.Write((uint)names.Length);
        unchecked{foreach(uint plain in table){seed+=crypt[1024+(key&255)];w.Write(plain^(key+seed));key=((~key<<21)+0x11111111)|(key>>11);seed=plain+seed+(seed<<5)+3;}}return m.ToArray();}
    }

    sealed class Fixture {
        public string Root;public Catalog Catalog;public ClientInfo Client;public Dictionary<string,string> Files;public Dictionary<string,string> Before;
        public Fixture(string locale="enUS",bool hd=true,bool originals=true){
            Root=Path.Combine(work,Guid.NewGuid().ToString("N"));Directory.CreateDirectory(Root);Files=new Dictionary<string,string>();
            Catalog=new Catalog{Version="3.0.4",InstallerVersion="1.0.0",Locales=new List<string>{"enUS","deDE","frFR","esES","esMX","koKR","ruRU","zhCN","zhTW"},Assets=new Dictionary<string,Asset>()};
            var ids=new List<string>{"Executable","Maps","SpellAssets","SpellTables"};
            foreach(var l in Catalog.Locales){ids.Add("LoadingQ-"+l);ids.Add("MapsQ-"+l);}
            foreach(var mode in new[]{"Non-HD","HD-NewSpells-On","HD-NewSpells-Off"})foreach(var c in new[]{"On","Off"})ids.Add("Y-"+mode+"-Consecration-"+c);
            foreach(var id in ids){string p=Put(Path.Combine(Root,"sources",id),"VERIFIED ASSET "+id);Files[id]=p;long length=new FileInfo(p).Length;string sha=Hash.FileHash(p);Catalog.Assets[id]=new Asset{Id=id,Bytes=length,Sha256=sha,Parts=new List<Part>{new Part{Sha256=sha,Bytes=length,FileName=sha+".bin",Url="https://github.com/CRSD-Lau/Lau-Setup/releases/download/payload-3.0.4/"+sha+".bin"}}};}
            Catalog.Validate();Client=new ClientInfo{Root=Root,Locale=locale,Hd=hd};
            var scoped=new[]{"WoW.exe",@"Data\patch-q.mpq",@"Data\patch-y.mpq",@"Data\patch-s.mpq",@"Data\patch-m.mpq",@"Data\"+locale+@"\patch-"+locale+"-Q.MPQ",@"Data\"+locale+@"\patch-"+locale+"-Y.MPQ",@"Data\"+locale+@"\patch-"+locale+"-S.MPQ",@"Data\"+locale+@"\patch-"+locale+"-M.MPQ"};
            if(originals)foreach(var relative in scoped)Put(Path.Combine(Root,relative),"ORIGINAL "+relative);
            foreach(var relative in new[]{@"Data\patch-z.mpq",@"Data\patch-a.mpq",@"Interface\AddOns\ElvUI\ElvUI.lua",@"WTF\Account\private.lua",@"Fonts\private.ttf",@"Data\xxXX\patch-xxXX-Q.MPQ"})Put(Path.Combine(Root,relative),"PRESERVE "+relative);
            foreach(var mpq in new[]{@"Data\patch-z.mpq",@"Data\patch-a.mpq"})Put(Path.Combine(Root,mpq),ScanFixture());
            Before=Snapshot();
        }
        public Dictionary<string,string> Snapshot(){return Directory.GetFiles(Root,"*",SearchOption.AllDirectories).Where(p=>!p.StartsWith(Path.Combine(Root,"LauSetupBackups")+"\\")).ToDictionary(p=>p.Substring(Root.Length+1),Hash.FileHash);}
        public void Original(){var now=Snapshot();Check(now.Count==Before.Count,"Original file count changed.");foreach(var x in Before)Check(now.ContainsKey(x.Key)&&now[x.Key]==x.Value,"Original not preserved: "+x.Key);}
        public InstallPlan Plan(bool spells=true,bool cons=true,bool maps=true){return InstallPlan.Build(Client,Catalog,spells,cons,maps);}
        public Transaction Tx(){return new Transaction(Catalog,null,Guard);}
        public void Installed(InstallPlan p){foreach(var o in p.Operations){var path=SafePaths.Target(Root,o.Relative,Client.Locale,o.ExtraPatch);Check(o.SourceRelative!=null?Hash.Matches(path,o.SourceHash,o.SourceBytes):o.AssetId==null?!File.Exists(path):Hash.Matches(path,Catalog.Get(o.AssetId).Sha256,Catalog.Get(o.AssetId).Bytes),"Wrong installed bytes "+o.Relative);}foreach(var b in Before.Where(x=>!p.Operations.Any(o=>o.Relative.Equals(x.Key,StringComparison.OrdinalIgnoreCase))))Check(File.Exists(Path.Combine(Root,b.Key))&&Hash.FileHash(Path.Combine(Root,b.Key))==b.Value,"Unrelated file changed: "+b.Key);}
    }
    static void EnableMapPack(Fixture f){
        f.Catalog.MapPackVersion="WDM-2.4.5";
        foreach(string id in f.Catalog.Locales.Select(l=>"MapDetails-"+l).Concat(MapAddons.Paths.Values)){
            string path=Put(Path.Combine(f.Root,"sources",id),"MAP FIXTURE "+id);string sha=Hash.FileHash(path);long bytes=new FileInfo(path).Length;
            f.Files[id]=path;f.Catalog.Assets[id]=new Asset{Id=id,Sha256=sha,Bytes=bytes,Parts=new List<Part>{new Part{Sha256=sha,Bytes=bytes,FileName=sha+".bin",Url="https://github.com/CRSD-Lau/Lau-Setup/releases/download/payload-maps-1.4.0/"+sha+".bin"}}};
        }
        f.Catalog.Validate();f.Before=f.Snapshot();
    }
    static void AutoConflict(Fixture f){f.Before=f.Snapshot();var p=f.Plan();Check(p.Operations.Count(o=>o.ExtraPatch)==1,"Expected one automatic backup");string j=f.Tx().Install(p,f.Files,CancellationToken.None);f.Installed(p);f.Tx().Restore(j);f.Original();}
    sealed class Server:IDisposable {
        TcpListener listener;Task task;public Uri Url;public string Request;
        public Server(Func<string,byte[]> response){listener=new TcpListener(IPAddress.Loopback,0);listener.Start();Url=new Uri("http://127.0.0.1:"+((IPEndPoint)listener.LocalEndpoint).Port+"/file");task=Task.Run(()=>{using(var c=listener.AcceptTcpClient())using(var stream=c.GetStream()){c.ReceiveTimeout=5000;c.SendTimeout=5000;var header=new StringBuilder();while(!header.ToString().EndsWith("\r\n\r\n")&&header.Length<16384){int b=stream.ReadByte();if(b<0)break;header.Append((char)b);}Request=header.ToString();byte[] result=response(Request);try{stream.Write(result,0,result.Length);}catch(IOException){}}});}
        public void Dispose(){listener.Stop();try{task.Wait(6000);}catch(AggregateException){} }
    }
    static byte[] Response(byte[] body,string status="200 OK",string headers="",long? length=null){return Encoding.ASCII.GetBytes("HTTP/1.1 "+status+"\r\nConnection: close\r\nContent-Type: application/octet-stream\r\nContent-Length: "+(length??body.Length)+"\r\n"+headers+"\r\n").Concat(body).ToArray();}
    static void DownloadTest(string mode){
        var f=new Fixture();var a=f.Catalog.Get("Executable");var part=a.Parts[0];byte[] bytes=File.ReadAllBytes(f.Files[a.Id]);var cache=Path.Combine(f.Root,"cache");Directory.CreateDirectory(cache);string partial=Path.Combine(cache,part.Sha256+".partial");
        if(new[]{"resume","ignored-range","bad-range","interrupted"}.Contains(mode))Put(partial,bytes.Take(7).ToArray());
        using(var server=new Server(request=>{
            if(mode=="quota")return Encoding.ASCII.GetBytes("HTTP/1.1 200 OK\r\nContent-Type: text/html\r\nConnection: close\r\n\r\nToo many users have downloaded this file. Quota exceeded.");
            if(mode=="resume")return Response(bytes.Skip(7).ToArray(),"206 Partial Content","Content-Range: bytes 7-"+(bytes.Length-1)+"/"+bytes.Length+"\r\n");
            if(mode=="bad-range")return Response(bytes.Skip(7).ToArray(),"206 Partial Content","Content-Range: bytes 8-"+(bytes.Length-1)+"/"+bytes.Length+"\r\n");
            if(mode=="interrupted")return Response(bytes.Skip(7).Take(3).ToArray(),"206 Partial Content","Content-Range: bytes 7-"+(bytes.Length-1)+"/"+bytes.Length+"\r\n",bytes.Length-7);
            if(mode=="wrong-size")return Response(bytes.Concat(new byte[]{1}).ToArray());
            if(mode=="bad-hash"){var wrong=(byte[])bytes.Clone();wrong[0]^=1;return Response(wrong);}
            return Response(bytes);
        })){
            var cancel=new CancellationTokenSource();var d=new Downloader(cache,null,p=>{if(mode=="cancel")cancel.Cancel();});d.TestUrl=p=>server.Url;
            if(new[]{"quota","bad-range","interrupted","wrong-size","bad-hash","cancel"}.Contains(mode)){
                Fails(()=>d.Fetch(a,cancel.Token));Check(!File.Exists(Path.Combine(cache,a.Sha256+".asset")),"Failed download was accepted.");
                if(mode=="quota"||mode=="wrong-size")Check(!File.Exists(partial),"Error page was saved as payload.");
                if(mode=="bad-range")Check(File.ReadAllBytes(partial).SequenceEqual(bytes.Take(7)),"Bad range modified cache.");
                if(mode=="bad-hash")Check(!File.Exists(partial),"Bad hash retained as completed partial.");
            }else{
                Check(Hash.Matches(d.Fetch(a,CancellationToken.None),a.Sha256,a.Bytes),"Download incorrect.");
                if(mode=="resume"||mode=="ignored-range")Check(server.Request.Contains("Range: bytes=7-"),"Resume header absent.");
                Check(Hash.Matches(d.Fetch(a,CancellationToken.None),a.Sha256,a.Bytes),"Verified cache not reused.");
            }
        }
    }
    static object Field(object value,string name){return value.GetType().GetField(name,BindingFlags.Instance|BindingFlags.NonPublic).GetValue(value);}
    static void Call(object value,string name,params object[] args){value.GetType().GetMethod(name,BindingFlags.Instance|BindingFlags.NonPublic).Invoke(value,args);}
    static void Pump(Task task){var until=DateTime.UtcNow.AddSeconds(90);while(!task.IsCompleted&&DateTime.UtcNow<until){Application.DoEvents();Thread.Sleep(10);}Check(task.IsCompleted,"UI task timed out");task.GetAwaiter().GetResult();}
    static void Idle(SetupForm form){var until=DateTime.UtcNow.AddSeconds(90);while((bool)Field(form,"busy")&&DateTime.UtcNow<until){Application.DoEvents();Thread.Sleep(10);}Check(!(bool)Field(form,"busy"),"UI operation timed out");Application.DoEvents();}
    [STAThread] public static int Main(string[] args){
        if(args.Length==1&&args[0]=="--hold"){Thread.Sleep(20000);return 0;}
        work=Path.GetFullPath(args[0]);realExe=Path.GetFullPath(args[1]);Directory.CreateDirectory(work);
        try {
            Application.EnableVisualStyles();Application.SetCompatibleTextRenderingDefault(false);
            Test("Interface locale resolution, persistence and live switching",()=>LocalizationTests.Run(work));
            Ui.Initialize("en-US",false);
            Test("Interface language does not change game locale or install plan",()=>{
                var f=new Fixture("frFR");var original=Json.Text(f.Plan());
                foreach(var option in Ui.Languages.Where(x=>x.Code!="auto")){
                    Ui.Select(option.Code,false);Check(f.Client.Locale=="frFR","UI language changed the client locale.");
                    Check(Json.Text(f.Plan())==original,"UI language changed patch selection.");
                }
                f.Original();Ui.Initialize("en-US",false);
            });
            Test("108 locale / edition / map install plans",()=>{
                foreach(var loc in new Fixture().Catalog.Locales)foreach(int mode in new[]{0,1,2})foreach(bool cons in new[]{false,true})foreach(bool maps in new[]{false,true}){
                    var f=new Fixture(loc,mode>0);var p=f.Plan(mode==2,cons,maps);
                    var q=p.Operations.Where(x=>x.AssetId!=null&&x.AssetId.Contains("Q-")).ToArray();var y=p.Operations.Where(x=>x.AssetId!=null&&x.AssetId.StartsWith("Y-")).ToArray();
                    Check(q.Length==2&&q[0].AssetId==q[1].AssetId,"Q duplication incorrect.");Check(y.Length==2&&y[0].AssetId==y[1].AssetId,"Y duplication incorrect.");
                    Check(q.All(x=>x.AssetId=="LoadingQ-"+loc),"Wrong regional/core Q.");
                    Check(p.Operations.Count(x=>x.AssetId=="Maps")== (maps?1:0),"Wrong map install.");
                    var s=p.Operations.Where(x=>x.Relative.EndsWith("s.mpq",StringComparison.OrdinalIgnoreCase)).ToArray();Check(s.Length==2&&s.All(x=>(x.AssetId!=null)==(mode==2)),"S switch wrong.");
                    string journal=f.Tx().Install(p,f.Files,CancellationToken.None);f.Installed(p);f.Tx().Restore(journal);f.Original();
                }
            });
            Test("Install without prior patches and exact rollback",()=>{var f=new Fixture(originals:false);var p=f.Plan();string j=f.Tx().Install(p,f.Files,CancellationToken.None);f.Installed(p);f.Tx().Restore(j);f.Original();});
            Test("Repeat install is a no-op",()=>{var f=new Fixture();f.Tx().Install(f.Plan(),f.Files,CancellationToken.None);var p=f.Plan();Check(p.Operations.Count==0,"Repeated install changes files.");Check(f.Tx().Install(p,f.Files,CancellationToken.None)==null,"No-op created backup.");});
            Test("Edition switch and stacked rollback",()=>{var f=new Fixture();string first=f.Tx().Install(f.Plan(),f.Files,CancellationToken.None);var secondPlan=f.Plan(false,false);Check(secondPlan.Operations.Count==6,"Switch should change two Y, disable two S, and preserve two disabled copies.");string second=f.Tx().Install(secondPlan,f.Files,CancellationToken.None);f.Tx().Restore(second);Check(f.Plan().Operations.Count==0,"Previous edition not restored.");f.Tx().Restore(first);f.Original();});
            Test("Patch-S off preserves disabled files and exact rollback",()=>{foreach(var loc in new Fixture().Catalog.Locales){var f=new Fixture(loc);var p=f.Plan(false);string j=f.Tx().Install(p,f.Files,CancellationToken.None);f.Installed(p);foreach(var rel in new[]{@"Data\patch-s.mpq",@"Data\"+loc+@"\patch-"+loc+"-S.MPQ"})Check(Hash.FileHash(Path.Combine(f.Root,rel+".disabled"))==f.Before[rel],"Disabled S differs from original");Check(f.Plan(false).Operations.Count==0,"Off repeat was not a no-op");f.Tx().Restore(j);f.Original();}});
            Test("Disabled Patch-S collisions preserve old copy and use plain name",()=>{var f=new Fixture();string active=Path.Combine(f.Root,@"Data\patch-s.mpq"),disabled=active+".disabled";Put(disabled,"KEEP DIFFERENT DISABLED S");f.Before=f.Snapshot();string oldHash=Hash.FileHash(disabled),current=Hash.FileHash(active);string j=f.Tx().Install(f.Plan(false),f.Files,CancellationToken.None);Check(Hash.FileHash(disabled)==current,"Current S did not receive plain disabled name");Check(Hash.FileHash(disabled+"."+oldHash.Substring(0,12))==oldHash,"Old disabled copy lost");f.Tx().Restore(j);f.Original();var g=new Fixture();Directory.CreateDirectory(Path.Combine(g.Root,@"Data\patch-s.mpq.disabled"));Fails(()=>g.Plan(false),"directory");});
            Test("All three flags on then spells off with older locale disabled copy",()=>{foreach(var loc in new Fixture().Catalog.Locales){var f=new Fixture(loc);foreach(var rel in new[]{@"Data\patch-s.mpq",@"Data\"+loc+@"\patch-"+loc+"-S.MPQ"})Put(Path.Combine(f.Root,rel+".disabled"),"OLDER DISABLED "+rel);f.Before=f.Snapshot();string on=f.Tx().Install(f.Plan(true,true,true),f.Files,CancellationToken.None);var onState=f.Snapshot();string off=f.Tx().Install(f.Plan(false,true,true),f.Files,CancellationToken.None);foreach(var rel in new[]{@"Data\patch-s.mpq",@"Data\"+loc+@"\patch-"+loc+"-S.MPQ"}){Check(!File.Exists(Path.Combine(f.Root,rel)),"S still active");Check(Hash.FileHash(Path.Combine(f.Root,rel+".disabled"))==onState[rel],"Current S not at plain disabled path");string oldHash=f.Before[rel+".disabled"];Check(Directory.GetFiles(Path.Combine(f.Root,"LauSetupBackups"),"*",SearchOption.AllDirectories).Any(x=>Hash.FileHash(x)==oldHash),"Old disabled S not backed up");}Check(f.Plan(false,true,true).Operations.Count==0,"Repeat off not a no-op");string again=f.Tx().Install(f.Plan(true,true,true),f.Files,CancellationToken.None);string offAgain=f.Tx().Install(f.Plan(false,true,true),f.Files,CancellationToken.None);f.Tx().Restore(offAgain);f.Tx().Restore(again);f.Tx().Restore(off);Check(onState.OrderBy(x=>x.Key).SequenceEqual(f.Snapshot().OrderBy(x=>x.Key)),"On state not restored");f.Tx().Restore(on);f.Original();}});
            Test("Re-enable reuses matching disabled S without downloads and restores exactly",()=>{foreach(var loc in new Fixture().Catalog.Locales){var f=new Fixture(loc);f.Tx().Install(f.Plan(),f.Files,CancellationToken.None);f.Tx().Install(f.Plan(false),f.Files,CancellationToken.None);var before=f.Snapshot();f.Before=before;var p=f.Plan();Check(p.Operations.Count(o=>o.SourceRelative!=null&&o.AssetId!=null)==2,"Both S copies should reuse local files");var files=new Dictionary<string,string>(f.Files);files.Remove("SpellAssets");files.Remove("SpellTables");string j=f.Tx().Install(p,files,CancellationToken.None);f.Installed(p);Check(f.Plan().Operations.Count==0,"Repeat on not a no-op");f.Tx().Restore(j);Check(before.OrderBy(x=>x.Key).SequenceEqual(f.Snapshot().OrderBy(x=>x.Key)),"Re-enable rollback differs");}});
            Test("Re-enable cleans duplicate even when active release already matches",()=>{var f=new Fixture();f.Tx().Install(f.Plan(),f.Files,CancellationToken.None);File.Copy(Path.Combine(f.Root,@"Data\patch-s.mpq"),Path.Combine(f.Root,@"Data\patch-s.mpq.disabled"));var before=f.Snapshot();f.Before=before;var p=f.Plan();Check(p.Operations.Count==1&&p.DownloadBytes==0,"Duplicate cleanup was skipped or downloads added");string j=f.Tx().Install(p,new Dictionary<string,string>(),CancellationToken.None);f.Installed(p);f.Tx().Restore(j);Check(before.OrderBy(x=>x.Key).SequenceEqual(f.Snapshot().OrderBy(x=>x.Key)),"Duplicate rollback differs");});
            Test("Re-enable source drift is rejected",()=>{var f=new Fixture();f.Tx().Install(f.Plan(),f.Files,CancellationToken.None);f.Tx().Install(f.Plan(false),f.Files,CancellationToken.None);var p=f.Plan();Put(Path.Combine(f.Root,@"Data\patch-s.mpq.disabled"),"CHANGED");Fails(()=>f.Tx().Install(p,f.Files,CancellationToken.None),"changed");});
            Test("Re-enable interruptions preserve disabled copies and exact rollback",()=>{foreach(bool matching in new[]{true,false})for(int i=0;i<6;i++){var f=new Fixture();f.Tx().Install(f.Plan(),f.Files,CancellationToken.None);f.Tx().Install(f.Plan(false),f.Files,CancellationToken.None);if(!matching)Put(Path.Combine(f.Root,@"Data\patch-s.mpq.disabled"),"OLDER ORIGINAL S");var before=f.Snapshot();var p=f.Plan();Check(p.Operations.Count==6,"Expected six re-enable operations");int fail=i;var tx=f.Tx();tx.AfterMove=n=>{if(n==fail)throw new IOException("enable interruption");};Fails(()=>tx.Install(p,f.Files,CancellationToken.None),"enable interruption");Check(before.OrderBy(x=>x.Key).SequenceEqual(f.Snapshot().OrderBy(x=>x.Key)),"Failed enable changed files");string j=f.Tx().Install(f.Plan(),f.Files,CancellationToken.None);var restore=f.Tx();restore.AfterRestore=n=>{if(n==fail)throw new IOException("restore interruption");};Fails(()=>restore.Restore(j),"restore interruption");f.Tx().Restore(j);Check(before.OrderBy(x=>x.Key).SequenceEqual(f.Snapshot().OrderBy(x=>x.Key)),"Interrupted restore changed files");}});
            Test("Tampered hash-named disabled copy is never overwritten",()=>{var f=new Fixture();string active=Path.Combine(f.Root,@"Data\patch-s.mpq");Put(active+".disabled","OLDER");Put(active+".disabled."+Hash.FileHash(active+".disabled").Substring(0,12),"TAMPERED");f.Before=f.Snapshot();Fails(()=>f.Plan(false),"hash-named");f.Original();});
            Test("Identical disabled Patch-S is preserved through off on rollback",()=>{var f=new Fixture();foreach(var rel in new[]{@"Data\patch-s.mpq",@"Data\enUS\patch-enUS-S.MPQ"})File.Copy(Path.Combine(f.Root,rel),Path.Combine(f.Root,rel+".disabled"));f.Before=f.Snapshot();string off=f.Tx().Install(f.Plan(false),f.Files,CancellationToken.None);string on=f.Tx().Install(f.Plan(true),f.Files,CancellationToken.None);foreach(var x in f.Before.Where(x=>x.Key.EndsWith(".disabled")))Check(!File.Exists(Path.Combine(f.Root,x.Key)),"On left disabled file in Data");f.Tx().Restore(on);f.Tx().Restore(off);f.Original();});
            Test("Disable failure after each move restores original client",()=>{for(int i=0;i<12;i++){int fail=i;var f=new Fixture();foreach(var rel in new[]{@"Data\patch-s.mpq.disabled",@"Data\enUS\patch-enUS-S.MPQ.disabled"})Put(Path.Combine(f.Root,rel),"OLDER "+rel);f.Before=f.Snapshot();var plan=f.Plan(false);Check(plan.Operations.Count==12,"Expected twelve operations");var tx=f.Tx();tx.AfterMove=n=>{if(n==fail)throw new IOException("disable interruption");};Fails(()=>tx.Install(plan,f.Files,CancellationToken.None),"disable interruption");f.Original();}});
            Test("Disabled-file rollback interruption recovers every step",()=>{for(int i=0;i<12;i++){int fail=i;var f=new Fixture();foreach(var rel in new[]{@"Data\patch-s.mpq.disabled",@"Data\enUS\patch-enUS-S.MPQ.disabled"})Put(Path.Combine(f.Root,rel),"OLDER "+rel);f.Before=f.Snapshot();string j=f.Tx().Install(f.Plan(false),f.Files,CancellationToken.None);var tx=f.Tx();tx.AfterRestore=n=>{if(n==fail)throw new IOException("restore interruption");};Fails(()=>tx.Restore(j),"restore interruption");f.Tx().Restore(j);f.Original();}});
            Test("Disabled copy drift blocks rollback without losing files",()=>{var f=new Fixture();string j=f.Tx().Install(f.Plan(false),f.Files,CancellationToken.None);Put(Path.Combine(f.Root,@"Data\patch-s.mpq.disabled"),"USER CHANGED DISABLED FILE");var before=f.Snapshot();Fails(()=>f.Tx().Restore(j),"changed");Check(before.OrderBy(x=>x.Key).SequenceEqual(f.Snapshot().OrderBy(x=>x.Key)),"Rollback changed drifted files");});
            Test("Previously installed map upgrade is retained",()=>{var f=new Fixture();f.Client.MapsInstalled=true;Check(f.Plan(maps:false).Maps,"Maps disabled despite previous upgrade.");});
            Test("Failure after each backup move rolls back",()=>{for(int i=0;i<8;i++){int fail=i;var f=new Fixture();var t=f.Tx();t.AfterMove=n=>{if(n==fail)throw new IOException("injected interruption");};Fails(()=>t.Install(f.Plan(),f.Files,CancellationToken.None),"injected");f.Original();Check(Transaction.Pending(f.Root)==null,"Recovery incorrectly left pending.");}});
            Test("Restore survives interruption after every step",()=>{for(int i=0;i<8;i++){int fail=i;var f=new Fixture();string j=f.Tx().Install(f.Plan(),f.Files,CancellationToken.None);var t=f.Tx();t.AfterRestore=n=>{if(n==fail)throw new IOException("simulated shutdown");};Fails(()=>t.Restore(j),"simulated");Check(Transaction.Pending(f.Root)==j,"Interrupted restore not discoverable.");f.Tx().Restore(j);f.Original();}});
            Test("Corrupt source cannot reach client and staging is cleared",()=>{var f=new Fixture();var p=f.Plan();Put(f.Files["Maps"],"corrupt");Fails(()=>f.Tx().Install(p,f.Files,CancellationToken.None),"verification");Check(Directory.GetFiles(Transaction.StateRoot(f.Root),"*",SearchOption.AllDirectories).All(x=>!x.Contains("\\staged\\")),"Aborted staging was retained.");foreach(var o in p.Operations)Check(Hash.Matches(SafePaths.Target(f.Root,o.Relative,f.Client.Locale),o.OldHash,o.OldBytes),"Original changed.");});
            Test("Game file drift before install is preserved",()=>{var f=new Fixture();var p=f.Plan();Put(Path.Combine(f.Root,"WoW.exe"),"another update");Fails(()=>f.Tx().Install(p,f.Files,CancellationToken.None),"changed");Check(File.ReadAllText(Path.Combine(f.Root,"WoW.exe"))=="another update","Drift overwritten.");});
            Test("Rollback preflight preserves external updates",()=>{var f=new Fixture();string j=f.Tx().Install(f.Plan(),f.Files,CancellationToken.None);Put(Path.Combine(f.Root,@"Data\patch-q.mpq"),"another update");var snapshot=f.Snapshot();Fails(()=>f.Tx().Restore(j),"changed");Check(snapshot.OrderBy(x=>x.Key).SequenceEqual(f.Snapshot().OrderBy(x=>x.Key)),"Rollback changed files before rejecting drift.");});
            Test("Corrupted original backup blocks rollback",()=>{var f=new Fixture();string j=f.Tx().Install(f.Plan(),f.Files,CancellationToken.None);Put(Path.Combine(Path.GetDirectoryName(j),@"before\WoW.exe"),"corrupt");Fails(()=>f.Tx().Restore(j),"backup has changed");});
            Test("Locked client file is preserved",()=>{var f=new Fixture();var p=f.Plan();using(var handle=File.Open(Path.Combine(f.Root,"WoW.exe"),FileMode.Open,FileAccess.Read,FileShare.Read))Fails(()=>f.Tx().Install(p,f.Files,CancellationToken.None));f.Original();});
            Test("Cancellation during commit restores originals",()=>{var f=new Fixture();var c=new CancellationTokenSource();var t=f.Tx();t.AfterMove=i=>c.Cancel();Fails(()=>t.Install(f.Plan(),f.Files,c.Token));f.Original();});
            Test("Process guard repeats and stops commit",()=>{var f=new Fixture();int calls=0;var t=new Transaction(f.Catalog,null,r=>{if(++calls>=4)throw new IOException("client started");});Fails(()=>t.Install(f.Plan(),f.Files,CancellationToken.None));Check(Transaction.Pending(f.Root)!=null,"Blocked recovery not recorded.");f.Tx().Restore(Transaction.Pending(f.Root));f.Original();});
            Test("Install locks exclude concurrent operations",()=>{var f=new Fixture();var state=Transaction.StateRoot(f.Root);Directory.CreateDirectory(state);using(var h=File.Open(Path.Combine(state,"installer.lock"),FileMode.Create,FileAccess.ReadWrite,FileShare.None))Fails(()=>f.Tx().Install(f.Plan(),f.Files,CancellationToken.None));f.Original();});
            Test("Unsafe destinations and tampered journal rejected",()=>{var f=new Fixture();foreach(var path in new[]{@"..\escape",@"Data\..\WoW.exe",@"Data/patch-q.mpq",@"Data\patch-q.mpq:evil",@"Data\patch-z.mpq",@"WTF\Config.wtf",@"Data\enUS\patch-enUS-F.MPQ"})Fails(()=>SafePaths.Target(f.Root,path,"enUS"));string j=f.Tx().Install(f.Plan(),f.Files,CancellationToken.None);var record=Json.Parse<Journal>(File.ReadAllText(j));record.Files[0].Relative=@"WTF\Account\private.lua";Json.Save(j,record);Fails(()=>f.Tx().Restore(j),"outside the install scope");});
            Test("Tampered backup root causes no other-folder writes",()=>{var f=new Fixture();var other=new Fixture();Directory.CreateDirectory(Transaction.StateRoot(other.Root));string j=f.Tx().Install(f.Plan(),f.Files,CancellationToken.None);var record=Json.Parse<Journal>(File.ReadAllText(j));record.Root=other.Root;Json.Save(j,record);Fails(()=>f.Tx().Restore(j),"Invalid backup");Check(!File.Exists(Path.Combine(Transaction.StateRoot(other.Root),"installer.lock")),"Foreign lock created.");});
            Test("Junction client rejected",()=>{var path=Environment.GetEnvironmentVariable("LAU_TEST_JUNCTION");Check(Directory.Exists(path),"Junction fixture missing.");Fails(()=>SafePaths.Root(path),"Linked folders");});
            Test("Hardlinked resume file cannot change another file",()=>{var f=new Fixture();var a=f.Catalog.Get("Executable");var cache=Path.Combine(f.Root,"cache");Directory.CreateDirectory(cache);string victim=Put(Path.Combine(f.Root,"unrelated"),"KEEP");Check(CreateHardLink(Path.Combine(cache,a.Sha256+".partial"),victim,IntPtr.Zero),"Hardlink fixture failed.");using(var server=new Server(q=>Response(File.ReadAllBytes(f.Files[a.Id])))){var d=new Downloader(cache,null,null);d.TestUrl=p=>server.Url;Fails(()=>d.Fetch(a,CancellationToken.None),"linked to another file");}Check(File.ReadAllText(victim)=="KEEP","Unrelated file modified.");});
            Test("Journal temporary hardlink is not overwritten",()=>{var f=new Fixture();string victim=Put(Path.Combine(f.Root,"unrelated"),"KEEP"),record=Path.Combine(f.Root,"record.json");Check(CreateHardLink(record+".new",victim,IntPtr.Zero),"Hardlink fixture failed.");Json.Save(record,new{value=1});Check(File.ReadAllText(victim)=="KEEP","Unrelated journal-linked file modified.");});
            Test("Recovery UI works with missing WoW.exe",()=>{var f=new Fixture();string j=f.Tx().Install(f.Plan(),f.Files,CancellationToken.None);File.Delete(Path.Combine(f.Root,"WoW.exe"));var record=Json.Parse<Journal>(File.ReadAllText(j));record.Status="COMMITTING";Json.Save(j,record);using(var form=new SetupForm(f.Catalog)){Pump(form.SelectRoot(f.Root));Call(form,"SetBusy",false);Check(((Button)Field(form,"restore")).Enabled,"Restore unavailable without executable.");Check(!((Button)Field(form,"install")).Enabled,"Install enabled during recovery.");Check(!((Button)Field(form,"next")).Enabled,"Next enabled during recovery.");Check(((ComboBox)Field(form,"language")).Enabled,"Manual language unavailable during recovery.");}f.Tx().Restore(j);f.Original();});
            Test("GUI install and restore use the real executable safely",()=>{
                var f=new Fixture();File.Copy(realExe,Path.Combine(f.Root,"WoW.exe"),true);File.Copy(realExe,f.Files["Executable"],true);
                var exe=f.Catalog.Get("Executable");exe.Bytes=new FileInfo(realExe).Length;exe.Sha256=Hash.FileHash(realExe);exe.Parts=new List<Part>{new Part{Bytes=exe.Bytes,Sha256=exe.Sha256,FileName=exe.Sha256+".bin"}};
                foreach(var rel in new[]{@"Data\common.mpq",@"Data\enUS\locale-enUS.mpq",@"Data\patch-f.mpq",@"Data\enUS\patch-enUS-F.MPQ"})Put(Path.Combine(f.Root,rel),ScanFixture());Put(Path.Combine(f.Root,@"WTF\Config.wtf"),"SET locale \"enUS\"\r\n");f.Before=f.Snapshot();
                File.Copy(f.Files["Y-HD-NewSpells-Off-Consecration-On"],Path.Combine(f.Root,@"Data\Y-HD-NewSpells-Off-Consecration-On.mpq"));f.Before=f.Snapshot();
                Put(Path.Combine(f.Root,@"Data\patch-v.mpq"),ScanFixture(@"DBFilesClient\Spell.dbc"));f.Before=f.Snapshot();
                string offline=Path.Combine(AppDomain.CurrentDomain.BaseDirectory,"payload");Directory.CreateDirectory(offline);
                foreach(var a in f.Catalog.Assets.Values)File.Copy(f.Files[a.Id],Path.Combine(offline,a.Parts[0].FileName),true);
                using(var form=new SetupForm(f.Catalog)){
                    form.StartPosition=FormStartPosition.Manual;form.Location=new System.Drawing.Point(-32000,-32000);form.ShowInTaskbar=false;form.Show();Application.DoEvents();WindowsFormsSynchronizationContext.AutoInstall=false;SynchronizationContext.SetSynchronizationContext(new WindowsFormsSynchronizationContext());Control.CheckForIllegalCrossThreadCalls=true;
                    Pump(form.SelectRoot(f.Root));Call(form,"SetBusy",false);Call(form,"RefreshPlan",null,EventArgs.Empty);Idle(form);
                    var readyButton=(Button)Field(form,"install");
                    Check(!readyButton.Enabled&&((Button)Field(form,"next")).Enabled,"Folder step must offer Next, not Install. status="+((Label)Field(form,"status")).Text+"; install="+readyButton.Enabled+"; next="+((Button)Field(form,"next")).Enabled+"; step="+Field(form,"step")+"; busy="+Field(form,"busy")+"; recovery="+Field(form,"recoveryOnly")+"; blocked="+Field(form,"navigationBlocked")+"; plan="+(Field(form,"plan")!=null)+"; parent="+((Button)Field(form,"next")).Parent.Enabled);
                    f.Original();Check(!Directory.Exists(Transaction.StateRoot(f.Root)),"Folder check wrote installer state.");
                    ((Button)Field(form,"next")).PerformClick();Check((int)Field(form,"step")==1,"Next did not open options.");
                    Check(((CheckBox)Field(form,"basePatch")).Checked&&!((CheckBox)Field(form,"basePatch")).Enabled&&((CheckBox)Field(form,"basePatch")).Text=="Patch-Y HD","Detected base flag incorrect.");
                    Check(!((CheckBox)Field(form,"cons")).Checked&&!((CheckBox)Field(form,"spells")).Checked&&!((CheckBox)Field(form,"maps")).Checked,"Optional extras did not start off.");Check(!((CheckBox)Field(form,"executable")).Checked&&!((CheckBox)Field(form,"artwork")).Checked,"EXE and artwork must default off");
                    for(int mask=0;mask<32;mask++){
                        form.GetType().GetField("refreshing",BindingFlags.Instance|BindingFlags.NonPublic).SetValue(form,true);
                        ((CheckBox)Field(form,"cons")).Checked=(mask&1)!=0;((CheckBox)Field(form,"spells")).Checked=(mask&2)!=0;((CheckBox)Field(form,"maps")).Checked=(mask&4)!=0;((CheckBox)Field(form,"executable")).Checked=(mask&8)!=0;((CheckBox)Field(form,"artwork")).Checked=(mask&16)!=0;
                        form.GetType().GetField("refreshing",BindingFlags.Instance|BindingFlags.NonPublic).SetValue(form,false);Call(form,"RefreshPlan",null,EventArgs.Empty);Idle(form);
                        string expected="Your choices: Patch-Y (Lau’s version)"+((mask&1)!=0?" + Enhanced Consecration":"")+((mask&2)!=0?" + New Spells":"")+((mask&4)!=0?" + Map Upgrade":"")+((mask&8)!=0?" + Install compatible WoW.exe":"")+((mask&16)!=0?" + Loading screens and artwork (Patch-Q)":"");
                        Check(((Label)Field(form,"reviewChoices")).Text==expected,"Summary does not match selected options.");var uiPlan=(InstallPlan)Field(form,"plan");Check((mask&8)!=0||!uiPlan.Operations.Any(o=>o.AssetId=="Executable"),"Unchecked EXE scheduled for replacement");Check(((Label)Field(form,"reviewIncluded")).Text.Contains("WoW.exe: "+((mask&8)!=0?"Install":"Keep existing")),"EXE choice missing from review");Check(uiPlan.Operations.Any(o=>o.AssetId!=null&&(o.AssetId.StartsWith("MapsQ-")||o.AssetId.StartsWith("LoadingQ-")))==((mask&16)!=0),"Artwork checkbox ignored");f.Original();
                    }
                    for(int page=0;page<4;page++){
                        Call(form,"ShowStep",page);
                        foreach(var locale in new[]{"de-DE","fr-FR","es-ES","es-MX","pt-BR","ko-KR","ru-RU","zh-CN","zh-TW","en-US"}){
                            form.ChangeLanguage(locale,false);Check((int)Field(form,"step")==page&&((ComboBox)Field(form,"language")).Enabled,"Language switch changed step or lost selector.");
                            Check(((Label)Field(form,"reviewChoices")).Text.Contains(Ui.T("Patch-Y (Lau’s version)")),"Summary did not translate live.");
                        }
                    }
                    Call(form,"ShowStep",1);((CheckBox)Field(form,"spells")).Checked=false;Idle(form);((CheckBox)Field(form,"cons")).Checked=false;Idle(form);
                    Check(((Label)Field(form,"reviewIncluded")).Text.Contains("WoW.exe")&&((Label)Field(form,"reviewIncluded")).Text.Contains("Patch-Q"),"Default files missing from review.");

                    ((Button)Field(form,"back")).PerformClick();Check((int)Field(form,"step")==0&&((CheckBox)Field(form,"maps")).Checked,"Back lost selections.");
                    ((Button)Field(form,"next")).PerformClick();((Button)Field(form,"next")).PerformClick();
                    Check((int)Field(form,"step")==2&&readyButton.Enabled,"Review did not enable install.");Check(((Label)Field(form,"reviewWarning")).Visible&&((Label)Field(form,"reviewWarning")).Text.Contains("You can continue"),"Patch-V warning missing from review");
                    f.Original();Check(!Directory.Exists(Transaction.StateRoot(f.Root)),"Navigation wrote installer state.");
                    Check(!((InstallPlan)Field(form,"plan")).Operations.Any(o=>o.Relative.Contains("custom")),"Renamed copy should remain untouched");readyButton.PerformClick();Idle(form);Check(((Label)Field(form,"status")).Text.StartsWith("Installed and verified"),((Label)Field(form,"status")).Text);
                    Check((int)Field(form,"step")==3&&((Button)Field(form,"next")).Text=="Finish","Success did not reach Finish.");Check(((ComboBox)Field(form,"language")).Enabled,"Language unavailable on Finish.");
                    Check(!((CheckBox)Field(form,"maps")).Enabled&&((CheckBox)Field(form,"maps")).Checked,"Installed map state not refreshed.");
                    string j=Transaction.Journals(f.Root).First();Pump(form.RestoreRecord(j));Check(((Label)Field(form,"status")).Text=="Previous install restored and verified.","GUI restore failed.");
                    Check(((CheckBox)Field(form,"maps")).Enabled&&!((CheckBox)Field(form,"maps")).Checked,"Restored map state stale.");Check((int)Field(form,"step")==0&&Field(form,"plan")!=null,"Restore did not reset wizard with a fresh plan.");f.Original();
                }
            });
            Test("Catalog rejects size, hash and language tampering",()=>{var f=new Fixture();string json=Json.Text(f.Catalog);Fails(()=>Catalog.Load(json.Replace("enUS","xxXX")));f.Catalog.Get("Maps").Bytes++;Fails(()=>f.Catalog.Validate(),"sizes");f=new Fixture();f.Catalog.Get("Maps").Sha256="../evil";Fails(()=>f.Catalog.Validate(),"Invalid asset");});
            Test("Optional executable and artwork exclude writes and downloads and restore exactly",()=>{
                foreach(string locale in new[]{"enUS","frFR"})for(int mask=0;mask<8;mask++){
                    var f=new Fixture(locale);var p=InstallPlan.Build(f.Client,f.Catalog,false,false,(mask&4)!=0,default(CancellationToken),(mask&1)!=0,(mask&2)!=0);
                    Check(p.Operations.Any(o=>o.AssetId=="Executable")==((mask&1)!=0),"Executable selection ignored");Check(p.Operations.Any(o=>o.Relative.EndsWith("q.mpq",StringComparison.OrdinalIgnoreCase))==((mask&2)!=0),"Artwork selection ignored");
                    var selected=p.Operations.Where(o=>o.AssetId!=null).Select(o=>o.AssetId).Distinct().ToDictionary(id=>id,id=>f.Files[id]);Check(p.DownloadBytes==selected.Keys.Sum(id=>f.Catalog.Get(id).Bytes),"Unselected asset counted for download");
                    string j=f.Tx().Install(p,selected,CancellationToken.None);f.Installed(p);f.Tx().Restore(j);f.Original();
                }
            });
            Test("Unrecognized nonempty Patch V warns without blocking or changing the file",()=>{
                foreach(var bytes in new[]{Encoding.UTF8.GetBytes("unknown format"),ScanFixture(@"DBFilesClient\Spell.dbc")}){
                    var f=new Fixture();Put(Path.Combine(f.Root,@"Data\patch-v.mpq"),bytes);f.Before=f.Snapshot();var p=f.Plan();Check(p.Warnings.SequenceEqual(new[]{@"Data\patch-v.mpq"}),"Missing V compatibility warning");Check(!p.Operations.Any(o=>o.ExtraPatch),"Unknown V scheduled for removal");string j=f.Tx().Install(p,f.Files,CancellationToken.None);f.Installed(p);f.Tx().Restore(j);f.Original();
                }
            });
            Test("Configured locale casing resolves every supported language without editing settings",()=>{
                foreach(var loc in new Fixture().Catalog.Locales){var f=new Fixture(loc);File.Copy(realExe,Path.Combine(f.Root,"WoW.exe"),true);Put(Path.Combine(f.Root,@"Data\common.mpq"),"fixture");Put(Path.Combine(f.Root,@"Data\"+loc+@"\locale-"+loc+".mpq"),"fixture");
                    foreach(var value in new[]{loc.ToLowerInvariant(),loc.ToUpperInvariant(),loc}){string config=Put(Path.Combine(f.Root,@"WTF\Config.wtf"),"SET locale \""+value+"\"\r\n");string hash=Hash.FileHash(config);Check(Client.Inspect(f.Root,f.Catalog).Locale==loc,"Locale not canonicalized: "+value);Check(Hash.FileHash(config)==hash,"Config changed");}
                    Put(Path.Combine(f.Root,@"WTF\Config.wtf"),"SET locale \"xxXX\"\r\n");Fails(()=>Client.Inspect(f.Root,f.Catalog),"matching language files");
                }
            });
            Test("Only empty Patch V backs up while nonempty V stays",()=>{
                foreach(var bytes in new[]{new byte[0]}){var f=new Fixture();Put(Path.Combine(f.Root,@"Data\PaTcH-V.MpQ"),bytes);AutoConflict(f);}
                var unrelated=new Fixture();Put(Path.Combine(unrelated.Root,@"Data\patch-v.mpq"),ScanFixture(@"DBFilesClient\Spell.dbc"));Check(!unrelated.Plan().Operations.Any(o=>o.ExtraPatch),"Unrelated V was moved by filename");
            });
            Test("Retired Patch V policy excludes lookalikes disabled and inactive locale files",()=>{
                Check(!MpqScan.IsRetiredPatch(@"Data\patch-v2.mpq")&&!MpqScan.IsRetiredPatch(@"Data\enUS\patch-v.mpq")&&!MpqScan.IsRetiredPatch(@"Data\patch-v.mpq.disabled"),"Retired scope broadened");
                var f=new Fixture();Put(Path.Combine(f.Root,@"Data\deDE\patch-v.mpq"),new byte[0]);Put(Path.Combine(f.Root,@"Data\patch-v.mpq.disabled"),new byte[0]);f.Plan();Put(Path.Combine(f.Root,@"Data\patch-v2.mpq"),new byte[0]);f.Plan();
            });
            Test("Retired Patch V drift and backup tampering remain protected",()=>{
                var f=new Fixture();string path=Put(Path.Combine(f.Root,@"Data\patch-v.mpq"),new byte[0]);var plan=f.Plan();Put(path,ScanFixture(@"Interface\AddOns\!PYAndre\!PYAndre.toc"));f.Before=f.Snapshot();Fails(()=>f.Tx().Install(plan,f.Files,CancellationToken.None),"Game files changed");f.Original();
                Put(path,new byte[0]);string record=f.Tx().Install(f.Plan(),f.Files,CancellationToken.None);Put(Path.Combine(Path.GetDirectoryName(record),@"before\Data\patch-v.mpq"),"tampered");Fails(()=>f.Tx().Restore(record),"backup has changed");Check(!File.Exists(path),"Tampered backup restored");
            });
            Test("Empty retired Patch V recovers from an interrupted installation",()=>{
                var f=new Fixture();Put(Path.Combine(f.Root,@"Data\patch-v.mpq"),new byte[0]);f.Before=f.Snapshot();var tx=f.Tx();tx.AfterMove=n=>{throw new IOException("V interruption");};Fails(()=>tx.Install(f.Plan(),f.Files,CancellationToken.None),"V interruption");f.Original();
            });
            Test("Correct client build, locale and HD detection",()=>{var f=new Fixture();File.Copy(realExe,Path.Combine(f.Root,"WoW.exe"),true);Put(Path.Combine(f.Root,@"Data\common.mpq"),"fixture");Put(Path.Combine(f.Root,@"Data\enUS\locale-enUS.mpq"),"fixture");Put(Path.Combine(f.Root,@"WTF\Config.wtf"),"SET locale \"enUS\"\r\n");Check(!Client.Inspect(f.Root,f.Catalog).Hd,"NonHD misdetected.");Put(Path.Combine(f.Root,@"Data\patch-f.mpq"),"fixture");Fails(()=>Client.Inspect(f.Root,f.Catalog),"incomplete");Put(Path.Combine(f.Root,@"Data\enUS\patch-enUS-F.MPQ"),"fixture");Check(Client.Inspect(f.Root,f.Catalog).Hd,"HD not detected.");Put(Path.Combine(f.Root,@"WTF\Config.wtf"),"SET locale \"enUS\"\r\nSET locale \"deDE\"");Fails(()=>Client.Inspect(f.Root,f.Catalog),"ambiguous");});
            Test("Exact running client is refused; another folder allowed",()=>{var f=new Fixture();File.Copy(System.Reflection.Assembly.GetExecutingAssembly().Location,Path.Combine(f.Root,"WoW.exe"),true);using(var p=Process.Start(new ProcessStartInfo(Path.Combine(f.Root,"WoW.exe"),"--hold"){UseShellExecute=false,CreateNoWindow=true})){try{Thread.Sleep(300);Fails(()=>Client.AssertClosed(f.Root),WineHost.Active?"Close all WoW":"Close this WoW client");if(WineHost.Active)Fails(()=>Client.AssertClosed(Path.Combine(f.Root,"other")));else Client.AssertClosed(Path.Combine(f.Root,"other"));}finally{if(!p.HasExited)p.Kill();p.WaitForExit();}}});
            Test("Catalog pins the repository, release and filename",()=>{var f=new Fixture();var p=f.Catalog.Get("Executable").Parts[0];string valid=p.Url;foreach(string bad in new[]{valid.Replace("https:","http:"),valid.Replace("CRSD-Lau","other"),valid.Replace("payload-3.0.4","latest"),valid+"?redirect=1",valid.Replace(p.Sha256,new string('0',64))}){p.Url=bad;Fails(()=>f.Catalog.Validate());}p.Url=null;f.Catalog.PublicReady=true;Fails(()=>f.Catalog.Validate(),"URL is missing");});
            Test("Every catalog payload tag passes the real downloader destination check",()=>{
                var f=new Fixture();var d=new Downloader(Path.Combine(f.Root,"cache"),null,null);string sha=f.Catalog.Get("Maps").Sha256;
                foreach(string tag in Catalog.DownloadTags){var part=new Part{Sha256=sha,Url="https://github.com/CRSD-Lau/Lau-Setup/releases/download/"+tag+"/"+sha+".bin"};Check(Catalog.ValidDownloadUrl(part),"Catalog tag rejected");d.CheckHost(new Uri(part.Url));}
                foreach(string bad in new[]{"payload-maps-1.4.0-evil","payload-maps-1.4.1","latest"})Fails(()=>d.CheckHost(new Uri("https://github.com/CRSD-Lau/Lau-Setup/releases/download/"+bad+"/"+sha+".bin")),"Unexpected download destination");
            });
            if(!String.IsNullOrEmpty(Environment.GetEnvironmentVariable("LAU_TEST_PUBLIC_CATALOG")))Test("Real published map downloads pass without test URL override",()=>{
                var catalog=Catalog.Load(File.ReadAllText(Environment.GetEnvironmentVariable("LAU_TEST_PUBLIC_CATALOG")));var f=new Fixture();var d=new Downloader(Path.Combine(f.Root,"public-cache"),null,null);
                foreach(var asset in new[]{catalog.Get("MapDetails-enUS"),catalog.Assets.Values.Where(a=>a.Id.StartsWith("MapAddon-")).OrderBy(a=>a.Bytes).First()}){string downloaded=d.Fetch(asset,CancellationToken.None);Check(Hash.Matches(downloaded,asset.Sha256,asset.Bytes),"Public map download failed hash verification");}
            });
            Test("Downloader follows a validated redirect and preserves resume",()=>{var f=new Fixture();var a=f.Catalog.Get("Executable");byte[] bytes=File.ReadAllBytes(f.Files[a.Id]);string cache=Path.Combine(f.Root,"cache");Put(Path.Combine(cache,a.Sha256+".partial"),bytes.Take(7).ToArray());using(var destination=new Server(q=>Response(bytes.Skip(7).ToArray(),"206 Partial Content","Content-Range: bytes 7-"+(bytes.Length-1)+"/"+bytes.Length+"\r\n")))using(var redirect=new Server(q=>Response(new byte[0],"302 Found","Location: "+destination.Url+"\r\n"))){var d=new Downloader(cache,null,null);d.TestUrl=p=>redirect.Url;Check(Hash.Matches(d.Fetch(a,CancellationToken.None),a.Sha256,a.Bytes),"Redirect download mismatch.");Check(destination.Request.Contains("Range: bytes=7-"),"Redirect lost resume.");}});
            Test("Downloader rejects unsafe redirects before requesting them",()=>{foreach(string location in new[]{"http://github.com/CRSD-Lau/Lau-Setup/releases/download/payload-3.0.4/file","https://github.com.evil.example/file","https://release-assets.githubusercontent.com:444/file","https://user:password@release-assets.githubusercontent.com/file","https://github.com/login"}){var f=new Fixture();var a=f.Catalog.Get("Executable");using(var redirect=new Server(q=>Response(new byte[0],"302 Found","Location: "+location+"\r\n"))){var d=new Downloader(Path.Combine(f.Root,"cache"),null,null);d.TestUrl=p=>redirect.Url;Fails(()=>d.Fetch(a,CancellationToken.None),"Unexpected download destination");}}});
            foreach(var mode in new[]{"normal","resume","ignored-range","bad-range","wrong-size","bad-hash","interrupted","quota","cancel"}){string m=mode;Test("Downloader: "+m,()=>DownloadTest(m));}
            Test("Offline segmented assembly and corruption rejection",()=>{var f=new Fixture();var a=f.Catalog.Get("Maps");byte[] bytes=File.ReadAllBytes(f.Files[a.Id]);a.Parts.Clear();string offline=Path.Combine(f.Root,"offline");foreach(var b in new[]{bytes.Take(8).ToArray(),bytes.Skip(8).ToArray()}){string temp=Put(Path.Combine(f.Root,Guid.NewGuid().ToString()),b);string sha=Hash.FileHash(temp);Put(Path.Combine(offline,sha+".bin"),b);a.Parts.Add(new Part{Bytes=b.Length,Sha256=sha,FileName=sha+".bin"});}var d=new Downloader(Path.Combine(f.Root,"cache"),offline,null);Check(Hash.Matches(d.Fetch(a,CancellationToken.None),a.Sha256,a.Bytes),"Assembly mismatch.");Put(Path.Combine(offline,a.Parts[0].FileName),"damaged");Fails(()=>new Downloader(Path.Combine(f.Root,"other-cache"),offline,null).Fetch(a,CancellationToken.None),"damaged");});
            Test("Merged map pack installs independently and restores all support files",()=>{
                var f=new Fixture();EnableMapPack(f);
                foreach(string relative in MapAddons.Paths.Keys)Put(Path.Combine(f.Root,relative),"EXISTING "+relative);
                Put(Path.Combine(f.Root,@"Data\enUS\patch-enUS-T.MPQ"),"OLD MAP T");Put(Path.Combine(f.Root,@"Data\enUS\patch-enUS-N.MPQ"),"KEEP N");Put(Path.Combine(f.Root,@"Interface\AddOns\WDM\custom.lua"),"KEEP CUSTOM");f.Before=f.Snapshot();
                var p=InstallPlan.Build(f.Client,f.Catalog,false,false,true,default(CancellationToken),false,false);
                Check(!p.Operations.Any(o=>o.AssetId=="Executable"||(o.AssetId!=null&&o.AssetId.Contains("Q-"))),"Maps pulled EXE or loading screens");
                Check(p.Operations.Count(o=>o.AssetId!=null&&o.AssetId.StartsWith("MapAddon-"))==MapAddons.Paths.Count,"Support addon files missing");
                string j=f.Tx().Install(p,f.Files,CancellationToken.None);f.Installed(p);Check(Client.MapsComplete(f.Root,"enUS",f.Catalog),"Complete map pack not detected");
                Check(InstallPlan.Build(f.Client,f.Catalog,false,false,true,default(CancellationToken),false,false).Operations.Count==0,"Map reinstall not a no-op");
                f.Tx().Restore(j);f.Original();
            });
            Test("Unselected map pack has no map or addon operations",()=>{var f=new Fixture();EnableMapPack(f);var p=InstallPlan.Build(f.Client,f.Catalog,false,false,false,default(CancellationToken),false,false);Check(!p.Operations.Any(o=>o.AssetId!=null&&o.AssetId.StartsWith("Map")),"Unselected maps were installed");});
            Test("Partial map pack is detected and repaired only when selected",()=>{
                var f=new Fixture();EnableMapPack(f);f.Tx().Install(InstallPlan.Build(f.Client,f.Catalog,false,false,true,default(CancellationToken),false,false),f.Files,CancellationToken.None);
                var first=MapAddons.Paths.First();Put(Path.Combine(f.Root,first.Key),"USER EDIT");Check(!Client.MapsComplete(f.Root,"enUS",f.Catalog),"Partial maps shown complete");
                var repair=InstallPlan.Build(f.Client,f.Catalog,false,false,true,default(CancellationToken),false,false);Check(repair.Operations.Count==1&&repair.Operations[0].Relative==first.Key,"Repair scope incorrect");f.Before=f.Snapshot();string j=f.Tx().Install(repair,f.Files,CancellationToken.None);f.Tx().Restore(j);f.Original();
            });
            Test("Map addon commit interruptions roll back exactly",()=>{
                foreach(int fail in new[]{3,60,118}){var f=new Fixture();EnableMapPack(f);var p=InstallPlan.Build(f.Client,f.Catalog,false,false,true,default(CancellationToken),false,false);f.Before=f.Snapshot();var tx=f.Tx();tx.AfterMove=n=>{if(n==fail)throw new IOException("map interruption");};Fails(()=>tx.Install(p,f.Files,CancellationToken.None),"map interruption");f.Original();}
            });
            Test("Map path scope rejects unlisted addons and inactive locale T",()=>{var f=new Fixture();foreach(string path in new[]{@"Interface\AddOns\WDM\unknown.lua",@"WTF\Account\WDM.lua",@"Data\deDE\patch-deDE-T.MPQ",@"Data\patch-t.mpq"})Fails(()=>SafePaths.Target(f.Root,path,"enUS"));});
            Test("Unrelated MPQs including renamed Lau copies are never parsed or moved",()=>{
                var f=new Fixture();
                var samples=new[]{Encoding.UTF8.GetBytes("unsupported layout"),new byte[0],ScanFixture(@"Interface\AddOns\!PYAndre\!PYAndre.toc"),ScanFixtureSize(8,true),File.ReadAllBytes(f.Files["SpellAssets"])};
                int n=0;foreach(var bytes in samples){Put(Path.Combine(f.Root,@"Data\patch-other-"+(n++)+".mpq"),bytes);Put(Path.Combine(f.Root,@"Data\enUS\patch-other-"+n+".mpq"),bytes);}
                string locked=Put(Path.Combine(f.Root,@"Data\patch-w.mpq"),"unreadable while locked");f.Before=f.Snapshot();
                InstallPlan p;using(var handle=new FileStream(locked,FileMode.Open,FileAccess.ReadWrite,FileShare.None)){p=f.Plan();Check(!p.Operations.Any(o=>o.ExtraPatch),"Unrelated patch scheduled for backup");MpqScan.ValidatePlan(p,f.Catalog,CancellationToken.None);}
                string j=f.Tx().Install(p,f.Files,CancellationToken.None);f.Installed(p);f.Tx().Restore(j);f.Original();
            });
            Test("Other patches introduced after planning do not block install",()=>{var f=new Fixture();var p=f.Plan();Put(Path.Combine(f.Root,@"Data\patch-late.mpq"),"unsupported");f.Before=f.Snapshot();string j=f.Tx().Install(p,f.Files,CancellationToken.None);f.Installed(p);f.Tx().Restore(j);f.Original();});
            Test("Nonempty recognized Patch V is also preserved without parsing",()=>{var f=new Fixture();Put(Path.Combine(f.Root,@"Data\patch-v.mpq"),ScanFixture(@"Interface\AddOns\!PYAndre\!PYAndre.toc"));f.Before=f.Snapshot();var p=f.Plan();Check(p.Warnings.Count==1&&!p.Operations.Any(o=>o.ExtraPatch),"Nonempty V policy violated");string j=f.Tx().Install(p,f.Files,CancellationToken.None);f.Installed(p);f.Tx().Restore(j);f.Original();});
            Test("Patch policy cancellation",()=>{var f=new Fixture();var c=new CancellationTokenSource();c.Cancel();Fails(()=>MpqScan.Check(f.Root,f.Client.Locale,f.Catalog,c.Token));});
            Test("Extra path resolver retains historical restore boundaries",()=>{var f=new Fixture();foreach(string path in new[]{@"Data\patch-y.mpq",@"Data\enUS\patch-enUS-Q.mpq",@"Data\deDE\extra.mpq",@"Data\nested\extra.mpq",@"Data\..\extra.mpq",@"WTF\extra.mpq",@"Data\extra.mpq:stream"})Fails(()=>SafePaths.ExtraPatch(f.Root,path,"enUS"));});
            Test("Historical renamed patch backup restores without a new scan",()=>{
                var f=new Fixture();string rel=@"Data\old-renamed.mpq";string path=Put(Path.Combine(f.Root,rel),ScanFixture(@"Interface\AddOns\!PYAndre\!PYAndre.toc"));f.Before=f.Snapshot();
                string record=f.Tx().Install(f.Plan(),f.Files,CancellationToken.None);var journal=Json.Parse<Journal>(File.ReadAllText(record));
                journal.Files.Add(new JournalEntry{Relative=rel,Existed=true,ExtraPatch=true,OldBytes=new FileInfo(path).Length,OldHash=Hash.FileHash(path)});
                string backup=Path.Combine(Path.GetDirectoryName(record),"before",rel);Directory.CreateDirectory(Path.GetDirectoryName(backup));File.Move(path,backup);Json.Save(record,journal);
                f.Tx().Restore(record);f.Original();
            });
            Check(passed>0,"No tests matched the requested starting group.");Console.WriteLine("ALL PASS "+passed);return 0;
        }catch(Exception e){Console.Error.WriteLine(e);return 1;}
        finally{Json.Save(Path.Combine(work,"results.json"),new{Author="Neil Mitchell",Creator="Neil Mitchell",LastModifiedBy="Neil Mitchell",StartAt=startAt,passed,results});}
    }
}
