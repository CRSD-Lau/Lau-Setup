// Author/Creator/Modifier: Neil Mitchell
using System;using System.IO;using System.Linq;using System.Collections.Generic;using System.Threading;using LauSetup;

// Exercises only disposable fixtures below the caller-supplied artifact directory.
public static class RaidReleaseTests {
    public class Index { public Dictionary<string,string> sources; }
    static void Check(bool ok,string why){if(!ok)throw new Exception(why);}
    static string Target(string root,string relative,string locale){return SafePaths.Target(root,relative,locale);}
    static Dictionary<string,string> Snapshot(string root){return Directory.GetFiles(root,"*",SearchOption.AllDirectories).Where(p=>!p.StartsWith(Path.Combine(root,"LauSetupBackups")+"\\",StringComparison.OrdinalIgnoreCase)).ToDictionary(p=>p.Substring(root.Length+1),Hash.FileHash,StringComparer.OrdinalIgnoreCase);}
    static void Same(Dictionary<string,string> expected,Dictionary<string,string> actual,string message){Check(expected.Count==actual.Count,message+" (file count)");foreach(var pair in expected)Check(actual.ContainsKey(pair.Key)&&actual[pair.Key]==pair.Value,message+": "+pair.Key);}
    static void CopyAsset(Dictionary<string,string> sources,Operation op,string root,string locale){if(op.AssetId==null)return;string target=Target(root,op.Relative,locale);Directory.CreateDirectory(Path.GetDirectoryName(target));File.Copy(sources[op.AssetId],target,true);}
    static Dictionary<string,string> Required(Catalog catalog,Index index,InstallPlan plan){var files=new Dictionary<string,string>();foreach(string id in plan.Operations.Where(x=>x.AssetId!=null).Select(x=>x.AssetId).Distinct()){Check(index.sources.ContainsKey(id),"Source index missing "+id);Check(File.Exists(index.sources[id]),"Source missing "+id+": "+index.sources[id]);files[id]=index.sources[id];}return files;}
    static void CorruptAndRepair(ClientInfo client,Catalog current,Dictionary<string,string> files,Operation installed){string target=Target(client.Root,installed.Relative,client.Locale);DateTime stamp=File.GetLastWriteTimeUtc(target);using(var stream=new FileStream(target,FileMode.Open,FileAccess.ReadWrite,FileShare.None)){stream.Position=stream.Length-1;int value=stream.ReadByte();Check(value>=0,"Empty Y archive");stream.Position--;stream.WriteByte((byte)(value^1));}File.SetLastWriteTimeUtc(target,stamp);var repair=InstallPlan.Build(client,current,client.NewSpells,true,false,default(CancellationToken),false,false);Check(repair.Operations.Count==1&&repair.Operations[0].Relative.Equals(installed.Relative,StringComparison.OrdinalIgnoreCase),"One-byte same-size/same-time corruption was not isolated at "+installed.Relative);new Transaction(current,null,null).Install(repair,files,CancellationToken.None);Check(InstallPlan.Build(client,current,client.NewSpells,true,false,default(CancellationToken),false,false).Operations.Count==0,"Repair did not restore "+installed.Relative);}
    static void VerifyAliases(Catalog catalog,Index sources){foreach(string mode in new[]{"HD-NewSpells-On","HD-NewSpells-Off","Non-HD"}){string on="Y-"+mode+"-Consecration-On",off="Y-"+mode+"-Consecration-Off";var active=catalog.Get(on);var alias=catalog.Get(off);Check(active!=null&&alias!=null,"Current catalog does not retain "+on+" and "+off);Check(active.Bytes==alias.Bytes&&active.Sha256==alias.Sha256,"Off edition is not an alias of On for "+mode);foreach(string id in new[]{on,off}){Check(sources.sources.ContainsKey(id)&&File.Exists(sources.sources[id]),"Current source index missing alias source "+id);Check(Hash.Matches(sources.sources[id],catalog.Get(id).Sha256,catalog.Get(id).Bytes),"Alias source does not match catalog "+id);}}}
    public static int Main(string[] args){
        try{
            Check(args.Length==6,"Usage: RaidReleaseTests <project> <previous-catalog> <previous-source-index> <current-catalog> <current-source-index> <artifact-root>");
            string project=Path.GetFullPath(args[0]),artifact=Path.GetFullPath(args[5]),fixtureRoot=Path.Combine(project,"build","r");
            var old=Catalog.Load(File.ReadAllText(args[1]));var previous=Json.Parse<Index>(File.ReadAllText(args[2]));var current=Catalog.Load(File.ReadAllText(args[3]));var sources=Json.Parse<Index>(File.ReadAllText(args[4]));
            Check(current.Version=="3.1.0","Expected current catalog version 3.1.0");VerifyAliases(current,sources);Directory.CreateDirectory(fixtureRoot);
            var results=new List<object>();int repairs=0,caseNumber=0;
            foreach(string locale in current.ClientLocales)foreach(string mode in new[]{"HD-NewSpells-On","HD-NewSpells-Off","Non-HD"})foreach(bool priorConsecration in new[]{false,true}){
                string root=Path.Combine(fixtureRoot,(++caseNumber).ToString("D3"));Directory.CreateDirectory(root);
                try{
                    bool hd=mode!="Non-HD",spells=mode=="HD-NewSpells-On";var client=new ClientInfo{Root=root,Locale=locale,Hd=hd,NewSpells=spells};
                    // Sentinels cover an inactive locale and unsupported/user-owned patch content.
                    string inactive=locale.Equals("enUS",StringComparison.OrdinalIgnoreCase)?"deDE":"enUS";
                    foreach(string relative in new[]{@"Data\patch-v.mpq",@"Data\"+inactive+@"\patch-"+inactive+"-Y.MPQ",@"Interface\AddOns\Sentinel\keep.lua"}){string path=Path.Combine(root,relative);Directory.CreateDirectory(Path.GetDirectoryName(path));File.WriteAllText(path,"preserve "+relative);}
                    // An HD/New Spells fixture already has the released 3.0.9 S pair.
                    // This release only validates Y, so its upgrade must leave S untouched.
                    foreach(var op in InstallPlan.Build(client,old,spells,priorConsecration,false,default(CancellationToken),false,false).Operations.Where(x=>x.AssetId=="SpellAssets"||x.AssetId=="SpellTables"))CopyAsset(previous.sources,op,root,locale);
                    var oldPlan=InstallPlan.Build(client,old,spells,priorConsecration,false,default(CancellationToken),false,false);Check(oldPlan.Operations.Count==2,"Prior fixture did not target exactly two Y placements");foreach(var op in oldPlan.Operations)CopyAsset(previous.sources,op,root,locale);
                    Check(InstallPlan.Build(client,old,spells,priorConsecration,false,default(CancellationToken),false,false).Operations.Count==0,"Prior edition not installed: "+locale+" "+mode);
                    var before=Snapshot(root);var update=InstallPlan.Build(client,current,spells,true,false,default(CancellationToken),false,false);
                    string expectedEdition=(hd?(spells?"HD-NewSpells-On":"HD-NewSpells-Off"):"Non-HD")+"-Consecration-On";
                    Check(update.Edition==expectedEdition&&update.Operations.Count==2&&update.Operations.All(x=>x.AssetId=="Y-"+expectedEdition),"Upgrade did not select the current On payload");
                    string localeTarget=@"Data\"+locale+@"\patch-"+locale+"-Y.MPQ";Check(update.Operations.Any(x=>x.Relative.Equals(localeTarget,StringComparison.OrdinalIgnoreCase)),"Active client locale path was not used: "+locale);Check(!update.Operations.Any(x=>x.Relative.IndexOf(inactive,StringComparison.OrdinalIgnoreCase)>=0),"Inactive locale was targeted");
                    string record=new Transaction(current,null,null).Install(update,Required(current,sources,update),CancellationToken.None);Check(record!=null,"Upgrade skipped");Check(InstallPlan.Build(client,current,spells,true,false,default(CancellationToken),false,false).Operations.Count==0,"Repeat upgrade was not a no-op");
                    bool repair=locale=="enUS"&&priorConsecration; if(repair){foreach(var op in update.Operations)CorruptAndRepair(client,current,Required(current,sources,update),op);repairs++;}
                    new Transaction(current,null,null).Restore(record);Same(before,Snapshot(root),"Exact prior 3.0.9 restore failed");
                    results.Add(new{locale,mode,prior_consecration=priorConsecration,active_locale_path=localeTarget,upgrade_operations=2,repeat_noop=true,repair_both_y_placements=repair,exact_restore=true});Console.WriteLine("RAID_RELEASE_PASS "+locale+" "+mode+" old-consecration-"+priorConsecration);
                } finally {
                    string expectedPrefix=Path.GetFullPath(fixtureRoot).TrimEnd(Path.DirectorySeparatorChar,Path.AltDirectorySeparatorChar)+Path.DirectorySeparatorChar;
                    string resolvedRoot=Path.GetFullPath(root);
                    Check(resolvedRoot.StartsWith(expectedPrefix,StringComparison.OrdinalIgnoreCase),"Fixture cleanup escaped artifact root: "+resolvedRoot);
                    if(Directory.Exists(resolvedRoot))Directory.Delete(resolvedRoot,true);
                }
            }
            Check(results.Count==current.ClientLocales.Count*6,"Unexpected matrix size");Check(repairs==3,"Expected one both-placement repair per mode");
            Json.Save(Path.Combine(artifact,"raid-release-tests.json"),new{Author="Neil Mitchell",Creator="Neil Mitchell",LastModifiedBy="Neil Mitchell",status="PASS",fixtures="project build\\r with path-bound cleanup; report only under artifact root",matrix_cases=results.Count,repairs,results});return 0;
        }catch(Exception e){Console.Error.WriteLine(e);return 1;}
    }
}
