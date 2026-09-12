// Author/Creator/Modifier: Neil Mitchell
using System;using System.IO;using System.Linq;using LauSetup;
public class HalionTestTests {
 static void Check(bool v,string m){if(!v)throw new Exception(m);}
 public static int Main(string[] a){try{
  string output=a[0],baseline=a[1],exe=a[2],payload=a[3];var old=HalionTest.Baseline();var current=Catalog.Embedded();Directory.CreateDirectory(output);int passed=0;
  foreach(var id in old.Assets.Keys.Where(k=>k.StartsWith("Y-"))){
   string root=Path.Combine(output,id);Directory.CreateDirectory(Path.Combine(root,"Data","enUS"));File.Copy(exe,Path.Combine(root,"WoW.exe"));File.WriteAllText(Path.Combine(root,"Data","common.mpq"),"fixture");File.WriteAllText(Path.Combine(root,"Data","enUS","locale-enUS.mpq"),"fixture");
   if(!id.StartsWith("Y-Non-HD")){File.WriteAllText(Path.Combine(root,"Data","patch-f.mpq"),"fixture");File.WriteAllText(Path.Combine(root,"Data","enUS","patch-enUS-F.MPQ"),"fixture");}
   var paths=new[]{Path.Combine(root,"Data","patch-y.mpq"),Path.Combine(root,"Data","enUS","patch-enUS-Y.MPQ")};foreach(var p in paths)File.Copy(Path.Combine(baseline,id+".mpq"),p);
   File.WriteAllText(Path.Combine(root,"personal-sentinel.txt"),"unchanged");
   Check(HalionTest.Plan(root,old,current).Operations.Count==2,"Missing upgrade");HalionTest.Apply(root,payload);
   Check(HalionTest.Apply(root,payload)==null,"Repeat not no-op");foreach(var p in paths)Check(Hash.Matches(p,current.Get(id).Sha256,current.Get(id).Bytes),"Wrong test bytes");
   string first=paths[0];var stamp=File.GetLastWriteTimeUtc(first);using(var s=new FileStream(first,FileMode.Open,FileAccess.ReadWrite)){s.Position=s.Length-1;int b=s.ReadByte();s.Position--;s.WriteByte((byte)(b^1));}File.SetLastWriteTimeUtc(first,stamp);
   bool rejected=false;try{HalionTest.Plan(root,old,current);}catch(IOException){rejected=true;}Check(rejected,"One byte drift was ignored");File.Copy(Path.Combine(payload,id+".mpq"),first,true);
   HalionTest.Undo(root);foreach(var p in paths)Check(Hash.Matches(p,old.Get(id).Sha256,old.Get(id).Bytes),"Restore mismatch");
   bool noBackup=false;try{HalionTest.Undo(root);}catch(IOException){noBackup=true;}Check(noBackup,"Restore should not select unrelated backup");Check(File.ReadAllText(Path.Combine(root,"personal-sentinel.txt"))=="unchanged","Unrelated file changed");
   // Testers already running v1 must receive v2 and restore their exact v1 bytes.
   foreach(var p in paths)File.Copy(Path.Combine(a[4],id+".mpq"),p,true);
   Check(HalionTest.Plan(root,old,current).Operations.Count==2,"V1 was mistaken for current test");HalionTest.Apply(root,payload);
   Check(HalionTest.Apply(root,payload)==null,"V2 repeat was not no-op");HalionTest.Undo(root);
   foreach(var p in paths)Check(Hash.FileHash(p)==HalionTest.V1()[id],"V1 rollback mismatch");
   Console.WriteLine("PASS base + v1 upgrade/restore "+id);passed++;
  }
  Json.Save(Path.Combine(output,"validation.json"),new{Author="Neil Mitchell",Creator="Neil Mitchell",LastModifiedBy="Neil Mitchell",passed,apply_repeat_single_byte_rejection_restore=true,v1_upgrade_and_exact_restore=true});return 0;
 }catch(Exception e){Console.Error.WriteLine(e);return 1;}}
}
