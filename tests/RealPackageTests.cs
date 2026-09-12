// Author, Creator, Last Modified By: Neil Mitchell
using System;
using System.IO;
using System.Linq;
using System.Collections.Generic;
using System.Threading;
using LauSetup;
public static class RealPackageTests {
    static void Put(string root,string path,string text){string full=Path.Combine(root,path);Directory.CreateDirectory(Path.GetDirectoryName(full));File.WriteAllText(full,text);}
    static Dictionary<string,string> Snapshot(string root){return Directory.GetFiles(root,"*",SearchOption.AllDirectories).Where(p=>!p.Contains("\\LauSetupBackups\\")).ToDictionary(p=>p.Substring(root.Length+1),Hash.FileHash);}
    static void Same(Dictionary<string,string> expected,Dictionary<string,string> actual){if(expected.Count!=actual.Count||expected.Any(e=>!actual.ContainsKey(e.Key)||actual[e.Key]!=e.Value))throw new Exception("Client files did not restore exactly.");}
    public static int Main(string[] args){
        bool online=args.Length>2&&args[2]=="--online-core";
        bool offlineCore=args.Length>2&&args[2]=="--offline-core";
        string project=Path.GetFullPath(args[0]);var c=Catalog.Load(File.ReadAllText(Path.Combine(project,"build/catalog.json")));string output=Path.Combine(project,"reports",(online?"network-package-":"real-package-")+DateTime.UtcNow.ToString("yyyyMMdd-HHmmss"));Directory.CreateDirectory(output);var results=new List<object>();
        try{
            string root=Path.Combine(output,"client");Directory.CreateDirectory(root);File.Copy(args[1],Path.Combine(root,"WoW.exe"));
            foreach(string path in new[]{@"Data\common.mpq",@"Data\enUS\locale-enUS.mpq",@"Data\patch-f.mpq",@"Data\enUS\patch-enUS-F.MPQ"})Put(root,path,"Isolated file-layout fixture; not a runnable game client.");
            Put(root,@"WTF\Config.wtf","SET locale \"enUS\"\r\n");Put(root,@"WTF\Account\SavedVariables\private.lua","PRESERVE");Put(root,@"Interface\AddOns\ElvUI\private.lua","PRESERVE");Put(root,@"Data\patch-z.mpq","PRESERVE");Put(root,@"Data\frFR\patch-frFR-Q.MPQ","PRESERVE");
            Put(root,@"Data\patch-s.mpq.disabled","Older root S fixture - preserve");Put(root,@"Data\enUS\patch-enUS-S.MPQ.disabled","Older locale S fixture - preserve");
            var original=Snapshot(root);var records=new List<string>();var states=new List<Dictionary<string,string>>{original};
            foreach(var settings in (online||offlineCore)?new[]{new[]{true,true,false},new[]{false,true,false}}:new[]{new[]{true,true,false},new[]{true,true,true},new[]{false,false,true}}){
                var info=Client.Inspect(root,c);var plan=InstallPlan.Build(info,c,settings[0],settings[1],settings[2]);string record;
                using(var lease=ClientLease.Acquire(root)){
                    var d=new Downloader(Path.Combine(root,"LauSetupBackups/cache"),online?null:Path.Combine(project,"payload"),null);var files=new Dictionary<string,string>();
                    foreach(var id in plan.Operations.Where(o=>o.AssetId!=null).Select(o=>o.AssetId).Distinct())files[id]=d.Fetch(c.Get(id),CancellationToken.None);
                    record=new Transaction(c,null,null).InstallWithLease(plan,files,CancellationToken.None,lease);
                }
                foreach(var op in plan.Operations){string path=SafePaths.Target(root,op.Relative,info.Locale);if(op.SourceRelative!=null?!Hash.Matches(path,op.SourceHash,op.SourceBytes):op.AssetId==null?File.Exists(path):!Hash.Matches(path,c.Get(op.AssetId).Sha256,c.Get(op.AssetId).Bytes))throw new Exception("Installed bytes differ.");}
                if(InstallPlan.Build(info,c,settings[0],settings[1],settings[2]).Operations.Count!=0)throw new Exception("Repeat install was not a no-op");
                records.Add(record);states.Add(Snapshot(root));results.Add(new{edition=plan.Edition,maps=plan.Maps,operations=plan.Operations.Count,status="EXACT_RELEASE_ASSET_INSTALL_PASS"});Console.WriteLine("REAL_PACKAGE_PASS "+plan.Edition+" maps="+plan.Maps);
            }
            for(int i=records.Count-1;i>=0;i--){new Transaction(c,null,null).Restore(records[i]);Same(states[i],Snapshot(root));}
            Same(original,Snapshot(root));Json.Save(Path.Combine(output,"validation.json"),new{Author="Neil Mitchell",Creator="Neil Mitchell",LastModifiedBy="Neil Mitchell",status=online?"GITHUB_DOWNLOAD_INSTALL_AND_ROLLBACK_PASS":offlineCore?"WINE_CORE_INSTALL_AND_ROLLBACK_PASS":"RELEASE_ASSET_INSTALL_AND_STACKED_ROLLBACK_PASS",scope=offlineCore?"Final Wine core installation and exact rollback using previously verified GitHub parts, without a second download.":online?"Fresh anonymous GitHub downloads, enUS HD New Spells On then Off installation, exact disabled S preservation, repeat no-op and stacked rollback in an isolated file-layout fixture. No offline source or prepopulated cache.":"Exact Q/S/Y/M/executable payload bytes in an isolated file-layout fixture, using verified offline sources; public delivery and native game tests are separate gates",results});Console.WriteLine(output);return 0;
        }catch(Exception e){Console.Error.WriteLine(e);return 1;}
    }
}
