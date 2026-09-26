// Author: Neil Mitchell
// Creator: Neil Mitchell
// Last Modified By: Neil Mitchell
using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Threading;
using LauSetup;

public sealed class MapReleaseSourceIndex { public Dictionary<string,string> sources; }

public static class MapReleaseTests {
    static void Check(bool condition,string message){if(!condition)throw new Exception(message);}
    static string Target(string root,string relative){return Path.Combine(root,relative);}
    static void Copy(string source,string target){Directory.CreateDirectory(Path.GetDirectoryName(target));File.Copy(source,target,false);}
    static string HashOf(string path){return Hash.FileHash(path);}
    static void CheckNotReparsePoint(string path,string label){
        Check(Directory.Exists(path),label+" is missing: "+path);
        Check((new DirectoryInfo(path).Attributes&FileAttributes.ReparsePoint)==0,label+" must not be a reparse point: "+path);
    }
    static string FixtureRoot(){
        string project=Path.GetFullPath(Path.Combine(AppDomain.CurrentDomain.BaseDirectory,".."));
        string build=Path.GetFullPath(Path.Combine(project,"build"));
        CheckNotReparsePoint(project,"Project root");
        CheckNotReparsePoint(build,"Build directory");
        string fixture=Path.GetFullPath(Path.Combine(build,"raid-map-fixture"));
        string prefix=build.TrimEnd(Path.DirectorySeparatorChar,Path.AltDirectorySeparatorChar)+Path.DirectorySeparatorChar;
        Check(fixture.StartsWith(prefix,StringComparison.OrdinalIgnoreCase)&&Path.GetFileName(fixture)=="raid-map-fixture","Fixture must be the designated project-local build child: "+fixture);
        if(Directory.Exists(fixture))Check((new DirectoryInfo(fixture).Attributes&FileAttributes.ReparsePoint)==0,"Fixture must not be a reparse point: "+fixture);
        return fixture;
    }
    static string VerifiedSource(Dictionary<string,string> sources,Catalog catalog,string key){
        string path;
        Check(sources.TryGetValue(key,out path),"Missing source: "+key);
        var asset=catalog.Get(key);
        Check(Hash.Matches(path,asset.Sha256,asset.Bytes),"Source hash mismatch: "+key);
        return path;
    }
    public static int Main(string[] args){
        try {
            Check(args.Length==5,"Usage: MapReleaseTests <catalog.json> <source-index.json> <old-root-m.mpq> <old-enUS-T.MPQ> <evidence-dir>");
            string evidence=Path.GetFullPath(args[4]);
            Check(Directory.Exists(evidence),"Evidence directory must already exist");
            string fixture=FixtureRoot();
            Check(!Directory.Exists(fixture),"Fixture already exists: "+fixture);
            var catalog=Catalog.Load(File.ReadAllText(args[0]));
            var index=Json.Parse<MapReleaseSourceIndex>(File.ReadAllText(args[1]));
            Check(index.sources!=null,"Source index missing sources");
            string oldRoot=Path.GetFullPath(args[2]),oldT=Path.GetFullPath(args[3]);
            Check(HashOf(oldRoot)=="2eb1fde5691cc1e5dcfa9b45e4a2b50ed302b8afe619fe9dffd030854c6f8a8c","Old root M differs");
            Check(Hash.Matches(oldT,"de4b833b1d1ca1e98272e1ca79e73d941836d282ab9d33daed43eceb8bb8b2d2",69180155),"Old enUS T differs");
            string y="Y-HD-NewSpells-Off-Consecration-On";
            string newRoot=VerifiedSource(index.sources,catalog,"Maps");
            string newT=VerifiedSource(index.sources,catalog,"MapDetails-enUS");
            string newY=VerifiedSource(index.sources,catalog,y);
            var previous=catalog.PreviousMapRoots;
            Check(previous!=null&&previous.Any(p=>p.Sha256==HashOf(oldRoot)&&p.Bytes==new FileInfo(oldRoot).Length),"Old map root is not declared for upgrade");
            string client=Path.Combine(fixture,"client");
            Directory.CreateDirectory(client);
            string rootM=Target(client,@"Data\patch-m.mpq"),localeT=Target(client,@"Data\enGB\patch-enGB-T.MPQ");
            string rootY=Target(client,@"Data\patch-y.mpq"),localeY=Target(client,@"Data\enGB\patch-enGB-Y.MPQ");
            string inactive=Target(client,@"Data\enUS\patch-enUS-T.MPQ"),sentinel=Target(client,@"WTF\Account\private.lua");
            Copy(oldRoot,rootM);Copy(oldT,localeT);Copy(newY,rootY);Copy(newY,localeY);
            Directory.CreateDirectory(Path.GetDirectoryName(inactive));File.WriteAllText(inactive,"INACTIVE ENUS SENTINEL");
            Directory.CreateDirectory(Path.GetDirectoryName(sentinel));File.WriteAllText(sentinel,"KEEP USER DATA");
            foreach(var pair in MapAddons.Paths)Copy(VerifiedSource(index.sources,catalog,pair.Value),Target(client,pair.Key));
            string inactiveHash=HashOf(inactive),sentinelHash=HashOf(sentinel);
            var clientInfo=new ClientInfo{Root=client,Locale="enGB",Hd=true,NewSpells=false,MapsInstalled=Client.MapsRecognized(client,"enGB",catalog)};
            Check(clientInfo.MapsInstalled,"Old maps were not recognized");
            Check(!Client.MapsComplete(client,"enGB",catalog),"Old maps falsely reported complete");
            var plan=InstallPlan.Build(clientInfo,catalog,false,true,false,CancellationToken.None,false,false);
            var actual=plan.Operations.Select(o=>o.Relative).OrderBy(s=>s,StringComparer.OrdinalIgnoreCase).ToArray();
            var expected=new[]{@"Data\patch-m.mpq",@"Data\enGB\patch-enGB-T.MPQ"}.OrderBy(s=>s,StringComparer.OrdinalIgnoreCase).ToArray();
            Check(plan.Maps&&actual.SequenceEqual(expected),"Expected exactly root M and active enGB T: "+String.Join(",",actual));
            Check(plan.Operations.Single(o=>o.Relative==@"Data\patch-m.mpq").AssetId=="Maps","Wrong root M asset");
            Check(plan.Operations.Single(o=>o.Relative==@"Data\enGB\patch-enGB-T.MPQ").AssetId=="MapDetails-enUS","Wrong compatibility T asset");
            var tx=new Transaction(catalog,null,s=>{});
            string journal=tx.Install(plan,index.sources,CancellationToken.None);
            Check(journal!=null,"Upgrade did not create a restore journal");
            Check(Hash.Matches(rootM,catalog.Get("Maps").Sha256,catalog.Get("Maps").Bytes),"New root M hash differs");
            Check(Hash.Matches(localeT,catalog.Get("MapDetails-enUS").Sha256,catalog.Get("MapDetails-enUS").Bytes),"New enGB T hash differs");
            Check(Client.MapsComplete(client,"enGB",catalog),"Upgraded maps did not report complete");
            Check(HashOf(inactive)==inactiveHash&&HashOf(sentinel)==sentinelHash,"Inactive locale or unrelated user data changed");
            var repeat=InstallPlan.Build(clientInfo,catalog,false,true,false,CancellationToken.None,false,false);
            Check(repeat.Operations.Count==0,"Repeat map install is not a no-op");
            Check(tx.Install(repeat,index.sources,CancellationToken.None)==null,"No-op created a journal");
            tx.Restore(journal);
            Check(HashOf(rootM)==HashOf(oldRoot)&&HashOf(localeT)==HashOf(oldT),"Old map archives did not restore exactly");
            Check(HashOf(inactive)==inactiveHash&&HashOf(sentinel)==sentinelHash,"Inactive locale or unrelated user data changed on restore");
            Check(Hash.Matches(rootY,catalog.Get(y).Sha256,catalog.Get(y).Bytes)&&Hash.Matches(localeY,catalog.Get(y).Sha256,catalog.Get(y).Bytes),"Current Y changed");
            Check(Client.MapsRecognized(client,"enGB",catalog)&&!Client.MapsComplete(client,"enGB",catalog),"Restored maps state is wrong");
            Directory.CreateDirectory(evidence);
            Json.Save(Path.Combine(evidence,"enGB-map-upgrade-proof.json"),new{
                Author="Neil Mitchell",Creator="Neil Mitchell",LastModifiedBy="Neil Mitchell",Status="PASS",
                Fixture=fixture,Locale="enGB",VisualAssetLocale="enUS",Operations=actual,
                PreviousRootSha256=HashOf(oldRoot),CandidateRootSha256=HashOf(newRoot),
                PreviousLocaleSha256=HashOf(oldT),CandidateLocaleSha256=HashOf(newT),
                MapAddonsChecked=MapAddons.Paths.Count,UpgradeComplete=true,RepeatNoOp=true,RestoreExact=true,
                InactiveLocaleUnchanged=true,UnrelatedUserDataUnchanged=true,CurrentYUnchanged=true
            });
            // The fixture contains large archive copies. Remove only the exact,
            // verified project-local fixture after all assertions and proof save.
            Check(String.Equals(Path.GetFullPath(fixture),FixtureRoot(),StringComparison.OrdinalIgnoreCase),"Fixture cleanup boundary changed");
            Check((new DirectoryInfo(fixture).Attributes&FileAttributes.ReparsePoint)==0,"Fixture became a reparse point before cleanup");
            Directory.Delete(fixture,true);
            Console.WriteLine("ENGB_MAP_UPGRADE_RESTORE_PASS");
            return 0;
        } catch(Exception error) {Console.Error.WriteLine(error);return 1;}
    }
}
