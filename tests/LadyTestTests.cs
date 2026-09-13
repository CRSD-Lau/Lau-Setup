// Author/Creator/Modifier: Neil Mitchell
using System;using System.IO;using System.Linq;using LauSetup;
public class LadyTestTests {
 static void Check(bool v,string m){if(!v)throw new Exception(m);}
 public static int Main(string[] a){try{
  string output=a[0],baseline=a[1],exe=a[2],payload=a[3];var old=LadyTest.Baseline();var current=Catalog.Embedded();Directory.CreateDirectory(output);int passed=0;
  foreach(var id in old.Assets.Keys.Where(k=>k.StartsWith("Y-"))){
   string root=Path.Combine(output,id);Directory.CreateDirectory(Path.Combine(root,"Data","enUS"));File.Copy(exe,Path.Combine(root,"WoW.exe"));File.WriteAllText(Path.Combine(root,"Data","common.mpq"),"fixture");File.WriteAllText(Path.Combine(root,"Data","enUS","locale-enUS.mpq"),"fixture");
   if(!id.StartsWith("Y-Non-HD")){File.WriteAllText(Path.Combine(root,"Data","patch-f.mpq"),"fixture");File.WriteAllText(Path.Combine(root,"Data","enUS","patch-enUS-F.MPQ"),"fixture");}
   var paths=new[]{Path.Combine(root,"Data","patch-y.mpq"),Path.Combine(root,"Data","enUS","patch-enUS-Y.MPQ")};foreach(var p in paths)File.Copy(Path.Combine(baseline,id+".mpq"),p);
   File.WriteAllText(Path.Combine(root,"personal-sentinel.txt"),"unchanged");
   Check(LadyTest.Plan(root,old,current).Operations.Count==2,"Missing upgrade");
   string other=old.Assets.Keys.First(k=>k.StartsWith("Y-")&&k!=id);
   File.Copy(Path.Combine(baseline,other+".mpq"),paths[1],true);
   bool mixed=false;try{LadyTest.Plan(root,old,current);}catch(IOException){mixed=true;}Check(mixed,"Mixed editions accepted");
   File.Copy(Path.Combine(baseline,id+".mpq"),paths[1],true);
   string invalidPayload=Path.Combine(root,"invalid-payload");Directory.CreateDirectory(invalidPayload);File.WriteAllText(Path.Combine(invalidPayload,id+".mpq"),"corrupt");
   bool corrupt=false;try{LadyTest.Apply(root,invalidPayload);}catch(IOException){corrupt=true;}Check(corrupt,"Corrupt payload accepted");
   foreach(var p in paths)Check(Hash.Matches(p,old.Get(id).Sha256,old.Get(id).Bytes),"Corrupt payload changed client");
   LadyTest.Apply(root,payload);
   Check(LadyTest.Apply(root,payload)==null,"Repeat not no-op");foreach(var p in paths)Check(Hash.Matches(p,current.Get(id).Sha256,current.Get(id).Bytes),"Wrong test bytes");
   string first=paths[0];var stamp=File.GetLastWriteTimeUtc(first);using(var s=new FileStream(first,FileMode.Open,FileAccess.ReadWrite)){s.Position=s.Length-1;int b=s.ReadByte();s.Position--;s.WriteByte((byte)(b^1));}File.SetLastWriteTimeUtc(first,stamp);
   bool rejected=false;try{LadyTest.Plan(root,old,current);}catch(IOException){rejected=true;}Check(rejected,"One byte drift was ignored");File.Copy(Path.Combine(payload,id+".mpq"),first,true);
   LadyTest.Undo(root);foreach(var p in paths)Check(Hash.Matches(p,old.Get(id).Sha256,old.Get(id).Bytes),"Restore mismatch");
   bool noBackup=false;try{LadyTest.Undo(root);}catch(IOException){noBackup=true;}Check(noBackup,"Restore should not select unrelated backup");Check(File.ReadAllText(Path.Combine(root,"personal-sentinel.txt"))=="unchanged","Unrelated file changed");
   foreach(var prior in a.Skip(4)){
    string source=Path.Combine(prior,id+".mpq");string priorHash=Hash.FileHash(source);
    foreach(var p in paths)File.Copy(source,p,true);
    Check(LadyTest.Plan(root,old,current).Operations.Count==2,"Prior test was mistaken for current test");LadyTest.Apply(root,payload);
    Check(LadyTest.Apply(root,payload)==null,"V3 repeat was not no-op");LadyTest.Undo(root);
    foreach(var p in paths)Check(Hash.FileHash(p)==priorHash,"Prior test rollback mismatch");
   }
   Console.WriteLine("PASS baseline upgrade/restore "+id);passed++;
  }
  Json.Save(Path.Combine(output,"validation.json"),new{Author="Neil Mitchell",Creator="Neil Mitchell",LastModifiedBy="Neil Mitchell",passed,apply_repeat_single_byte_rejection_restore=true,baseline_upgrade_and_exact_restore=true});return 0;
 }catch(Exception e){Console.Error.WriteLine(e);return 1;}}
}
