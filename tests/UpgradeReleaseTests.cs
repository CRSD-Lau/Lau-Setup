// Author/Creator/Modifier: Neil Mitchell
using System;using System.IO;using System.Linq;using System.Collections.Generic;using System.Threading;using LauSetup;
public class UpgradeReleaseTests {
 public class Index {public Dictionary<string,string> sources;}
 static void Check(bool ok,string why){if(!ok)throw new Exception(why);}
 public static int Main(string[] args){try{
 string project=args[0],build=Path.Combine(project,"build"),release=Path.Combine(build,"release-3.0.6");
 var old=Catalog.Load(File.ReadAllText(Path.Combine(release,"previous-catalog.json")));var current=Catalog.Load(File.ReadAllText(Path.Combine(build,"catalog.json")));
 var sources=Json.Parse<Index>(File.ReadAllText(Path.Combine(build,"source-index.json"))).sources;
 var prior=Json.Parse<Index>(File.ReadAllText(Path.Combine(release,"previous-source-index.json"))).sources;
 string output=Path.Combine(project,"reports","upgrade-3.0.6-"+DateTime.UtcNow.ToString("yyyyMMdd-HHmmss"));Directory.CreateDirectory(output);var results=new List<object>();
 foreach(string mode in new[]{"HD-NewSpells-On","HD-NewSpells-Off","Non-HD"})foreach(bool cons in new[]{true,false}){
 string root=Path.Combine(output,mode+"-"+cons);Directory.CreateDirectory(root);var client=new ClientInfo{Root=root,Locale="enUS",Hd=mode!="Non-HD"};bool spells=mode=="HD-NewSpells-On";
 var initial=InstallPlan.Build(client,old,spells,cons,false);
 foreach(var op in initial.Operations.Where(x=>x.AssetId!=null)){string f=SafePaths.Target(root,op.Relative,"enUS");Directory.CreateDirectory(Path.GetDirectoryName(f));File.Copy(prior[op.AssetId],f);}
 Check(InstallPlan.Build(client,old,spells,cons,false).Operations.Count==0,"Old fixture was not fully installed");
 var plan=InstallPlan.Build(client,current,spells,cons,false);
 Check(plan.Operations.Count==2&&plan.Operations.All(x=>x.AssetId=="Y-"+plan.Edition),"Old release incorrectly treated as installed or unrelated upgrade operations");
 var files=plan.Operations.Select(x=>x.AssetId).Distinct().ToDictionary(id=>id,id=>sources[id]);
 string record=new Transaction(current,null,null).Install(plan,files,CancellationToken.None);
 Check(record!=null,"Upgrade skipped");
 Check(InstallPlan.Build(client,current,spells,cons,false).Operations.Count==0,"Repeat upgrade was not a no-op");
 foreach(var op in plan.Operations)Check(Hash.Matches(SafePaths.Target(root,op.Relative,"enUS"),current.Get(op.AssetId).Sha256,current.Get(op.AssetId).Bytes),"Wrong installed payload");
 // Size and timestamp are deliberately unchanged: only hashing can detect this.
 foreach(var originalOp in plan.Operations){
  string target=SafePaths.Target(root,originalOp.Relative,"enUS");DateTime stamp=File.GetLastWriteTimeUtc(target);
  using(var stream=new FileStream(target,FileMode.Open,FileAccess.ReadWrite)){stream.Position=stream.Length-1;int value=stream.ReadByte();stream.Position--;stream.WriteByte((byte)(value^1));}
  File.SetLastWriteTimeUtc(target,stamp);
  var repair=InstallPlan.Build(client,current,spells,cons,false);
  Check(repair.Operations.Count==1 && repair.Operations[0].Relative==originalOp.Relative,"Same-size same-time one-byte change not detected");
  new Transaction(current,null,null).Install(repair,files,CancellationToken.None);
  Check(InstallPlan.Build(client,current,spells,cons,false).Operations.Count==0,"Repair did not restore matching bytes");
 }
 new Transaction(current,null,null).Restore(record);
 Check(InstallPlan.Build(client,old,spells,cons,false).Operations.Count==0,"Prior release did not restore exactly");
 results.Add(new{edition=plan.Edition,update_operations=2,old_release_detected=true,repeat_noop=true,one_byte_same_size_same_timestamp_detected_in_both_placements=true,rollback_exact=true});Console.WriteLine("UPGRADE_PASS "+plan.Edition);
 }
 Json.Save(Path.Combine(output,"validation.json"),new{Author="Neil Mitchell",Creator="Neil Mitchell",LastModifiedBy="Neil Mitchell",status="SIX_EDITION_305_TO_306_UPGRADE_ONE_BYTE_REPEAT_AND_ROLLBACK_PASS",results});Console.WriteLine(output);return 0;
 }catch(Exception e){Console.Error.WriteLine(e);return 1;}}
}
