// Author/Creator/Modifier: Neil Mitchell
using System;using System.IO;using System.Linq;using System.Reflection;using System.Collections.Generic;using System.Threading;using System.Threading.Tasks;using System.Drawing;using System.Windows.Forms;
namespace LauSetup {
public static class LadyTest {
 public static Catalog Baseline(){using(var r=new StreamReader(Assembly.GetExecutingAssembly().GetManifestResourceStream("LauSetup.Baseline.json")))return Catalog.Load(r.ReadToEnd());}
 public static InstallPlan Plan(string root,Catalog old,Catalog test){
  var client=Client.Inspect(root,old);var paths=new[]{@"Data\patch-y.mpq",@"Data\"+client.Locale+@"\patch-"+client.Locale+"-Y.MPQ"};string edition=null;
  var plan=new InstallPlan{Root=client.Root,Locale=client.Locale};
  foreach(var path in paths){string target=SafePaths.Target(root,path,client.Locale);if(!File.Exists(target))throw new IOException("Install release 3.0.8 first. Both Patch-Y placements are required.");
   string hash=Hash.FileHash(target);string id=old.Assets.Keys.FirstOrDefault(k=>k.StartsWith("Y-")&&(old.Get(k).Sha256==hash||test.Get(k).Sha256==hash));
   if(id==null)throw new IOException("Patch-Y is modified or unsupported. This test only accepts original 3.0.8 or this exact Deathwhisper test build.");
   if(edition!=null&&edition!=id)throw new IOException("Root and locale Patch-Y editions differ. No files changed.");edition=id;
   if(hash!=test.Get(id).Sha256){plan.Operations.Add(new Operation{Relative=path,AssetId=id,Existed=true,OldHash=hash,OldBytes=new FileInfo(target).Length});plan.StageBytes+=test.Get(id).Bytes;}
  }
  if(client.Hd==edition.StartsWith("Y-Non-HD"))throw new IOException("The installed Patch-Y edition does not match the model pack. Repair with normal Setup first.");
  plan.Edition=edition.Substring(2);return plan;
 }
 public static string Undo(string root){
  var tx=new Transaction(Catalog.Embedded(),null,null);var test=Catalog.Embedded();string pending=Transaction.Pending(root);
  Func<string,bool> owned=p=>{var j=tx.ReadBackup(p);return j.Files.Count>0&&j.Files.All(f=>(f.Relative==@"Data\patch-y.mpq"||f.Relative==@"Data\"+j.Locale+@"\patch-"+j.Locale+"-Y.MPQ")&&test.Assets.Any(a=>a.Key.StartsWith("Y-")&&a.Value.Sha256==f.NewHash));};
  if(pending!=null&&!owned(pending))throw new IOException("An unrelated installation needs recovery with normal Lau Setup.");
  string journal=pending??Transaction.Journals(root).FirstOrDefault(p=>Transaction.Status(p)=="INSTALLED"&&owned(p));
  if(journal==null)throw new IOException("No Deathwhisper test backup is available. Other backups are untouched.");tx.Restore(journal);return journal;
 }
 public static string Apply(string root,string payload){var old=Baseline();var test=Catalog.Embedded();Client.AssertClosed(root);using(var lease=ClientLease.Acquire(root)){
  var plan=Plan(root,old,test);var files=plan.Operations.Select(o=>o.AssetId).Distinct().ToDictionary(id=>id,id=>SafePaths.Under(payload,id+".mpq"));
  return new Transaction(test,null,null).InstallWithLease(plan,files,CancellationToken.None,lease);
 }}
 [STAThread]public static int Main(string[] args){Application.EnableVisualStyles();using(var form=new TestForm()){if(args.Length==2&&args[0]=="--preview"){form.Show();Application.DoEvents();using(var bitmap=new Bitmap(form.Width,form.Height)){form.DrawToBitmap(bitmap,new Rectangle(0,0,form.Width,form.Height));bitmap.Save(args[1]);}return 0;}Application.Run(form);}return 0;}
}
public class TestForm:Form {
 TextBox folder=new TextBox{ReadOnly=true,Dock=DockStyle.Top};Label status=new Label{AutoSize=false,Height=100,Dock=DockStyle.Top};Button choose=new Button{Text="Choose WoW folder",AutoSize=true},install=new Button{Text="Apply Lady test",AutoSize=true},restore=new Button{Text="Restore previous Patch-Y",AutoSize=true};bool busy;
 public TestForm(){Text="Lau TEST ONLY - Lady Deathwhisper";Width=700;Height=340;MinimumSize=new Size(620,340);BackColor=Color.FromArgb(12,22,34);ForeColor=Color.White;Font=new Font("Segoe UI",10);Padding=new Padding(24);
  using(var stream=Assembly.GetExecutingAssembly().GetManifestResourceStream("LauSetup.Icon.ico"))Icon=new Icon(stream);
  var title=new Label{Text="LADY DEATHWHISPER — BANSHEE TEST 1\nBanshee +20%, blue ring, three red chevrons, Frost Beacon.\nRequires 3.0.8. Beacon is a summon cue, not confirmed chase targeting.",Height=85,Dock=DockStyle.Top};
  var buttons=new FlowLayoutPanel{Dock=DockStyle.Top,Height=52};foreach(var b in new[]{choose,install,restore}){b.ForeColor=Color.Black;b.BackColor=Color.FromArgb(225,190,120);b.UseVisualStyleBackColor=false;b.FlatStyle=FlatStyle.Flat;buttons.Controls.Add(b);}Controls.Add(status);Controls.Add(buttons);Controls.Add(folder);Controls.Add(title);install.Enabled=restore.Enabled=false;
  choose.Click+=(s,e)=>{using(var d=new FolderBrowserDialog()){if(d.ShowDialog()!=DialogResult.OK)return;folder.Text=d.SelectedPath;install.Enabled=restore.Enabled=true;status.Text="Close WoW before applying or restoring. Only the two Patch-Y files are affected.";}};
  install.Click+=async(s,e)=>await Run(false);restore.Click+=async(s,e)=>await Run(true);FormClosing+=(s,e)=>{if(busy)e.Cancel=true;};
 }
 async Task Run(bool undo){busy=true;choose.Enabled=install.Enabled=restore.Enabled=false;status.Text="Checking and verifying files…";try{string root=folder.Text;string result=await Task.Run(()=>{
  if(!undo)return LadyTest.Apply(root,Path.Combine(AppDomain.CurrentDomain.BaseDirectory,"payload"));
  return LadyTest.Undo(root);
 });status.Text=undo?"Previous Patch-Y restored and verified.":result==null?"This exact Deathwhisper test is already installed.":"Lady visual test installed and verified. /pyversion stays 3.0.8. Test in-game visibility; beacon duration is unchanged.";
 }catch(Exception ex){status.Text=ex.Message;}finally{busy=false;choose.Enabled=install.Enabled=restore.Enabled=true;}}
}
}
