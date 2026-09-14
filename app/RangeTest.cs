// Author/Creator/Modifier: Neil Mitchell
using System;using System.IO;using System.Linq;using System.Reflection;using System.Collections.Generic;using System.Threading;using System.Threading.Tasks;using System.Drawing;using System.Windows.Forms;
namespace LauSetup {
public static class RangeTest {
 public static Catalog Baseline(){using(var r=new StreamReader(Assembly.GetExecutingAssembly().GetManifestResourceStream("LauSetup.Baseline.json")))return Catalog.Load(r.ReadToEnd());}
 public static InstallPlan Plan(string root,Catalog baseline,Catalog test){
  var client=Client.Inspect(root,baseline);var paths=new[]{@"Data\patch-y.mpq",@"Data\"+client.Locale+@"\patch-"+client.Locale+"-Y.MPQ"};string edition=null;
  var plan=new InstallPlan{Root=client.Root,Locale=client.Locale};
  foreach(var relative in paths){string target=SafePaths.Target(client.Root,relative,client.Locale);if(!File.Exists(target))throw new IOException("Install Lau game 3.0.8 first. Both Patch-Y placements are required.");
   string hash=Hash.FileHash(target);string id=baseline.Assets.Keys.FirstOrDefault(k=>k.StartsWith("Y-")&&(baseline.Get(k).Sha256==hash||test.Get(k).Sha256==hash));
   if(id==null)throw new IOException("Patch-Y is modified, custom, or belongs to another test. This test only accepts the exact Lau game 3.0.8 baseline or this exact BPC floor-marker test.");
   if(edition!=null&&edition!=id)throw new IOException("Root and active-language Patch-Y editions differ. No files changed.");edition=id;
   var expected=test.Get(id);if(hash!=expected.Sha256||new FileInfo(target).Length!=expected.Bytes){plan.Operations.Add(new Operation{Relative=relative,AssetId=id,Existed=true,OldHash=hash,OldBytes=new FileInfo(target).Length});plan.StageBytes=checked(plan.StageBytes+expected.Bytes);}
  }
  if(client.Hd==edition.StartsWith("Y-Non-HD"))throw new IOException("The installed Patch-Y edition does not match the HD model-pack state. Repair with normal Lau Setup first.");
  plan.Edition=edition.Substring(2);return plan;
 }
 static bool Owns(Transaction tx,string record,Catalog test){try{var j=tx.ReadBackup(record);var allowed=new[]{@"Data\patch-y.mpq",@"Data\"+j.Locale+@"\patch-"+j.Locale+"-Y.MPQ"};return j.Files.Count>=1&&j.Files.Count<=2&&j.Files.Select(f=>f.Relative).Distinct(StringComparer.OrdinalIgnoreCase).Count()==j.Files.Count&&j.Files.All(f=>allowed.Contains(f.Relative,StringComparer.OrdinalIgnoreCase)&&test.Assets.Any(a=>a.Key.StartsWith("Y-")&&a.Value.Sha256==f.NewHash&&a.Value.Bytes==f.NewBytes));}catch{return false;}}
 public static string Undo(string root){var test=Catalog.Embedded();var tx=new Transaction(test,null,null);string pending=Transaction.Pending(root);
  if(pending!=null&&!Owns(tx,pending,test))throw new IOException("An unrelated installation needs recovery with normal Lau Setup. Its backup is untouched.");
  string journal=pending??Transaction.Journals(root).FirstOrDefault(p=>Transaction.Status(p)=="INSTALLED"&&Owns(tx,p,test));
  if(journal==null)throw new IOException("No BPC floor-marker test backup is available. Other Lau backups are untouched.");tx.Restore(journal);return journal;
 }
 public static string Apply(string root,string payload){var baseline=Baseline();var test=Catalog.Embedded();Client.AssertClosed(root);using(var lease=ClientLease.Acquire(root)){
  var plan=Plan(root,baseline,test);var files=plan.Operations.Select(o=>o.AssetId).Distinct().ToDictionary(id=>id,id=>SafePaths.Under(payload,id+".mpq"));
  return new Transaction(test,null,null).InstallWithLease(plan,files,CancellationToken.None,lease);
 }}
 [STAThread]public static int Main(string[] args){Application.EnableVisualStyles();using(var form=new RangeTestForm()){if(args.Length==2&&args[0]=="--preview"){form.Show();Application.DoEvents();using(var bitmap=new Bitmap(form.Width,form.Height)){form.DrawToBitmap(bitmap,new Rectangle(0,0,form.Width,form.Height));bitmap.Save(args[1]);}return 0;}Application.Run(form);}return 0;}
}
public class RangeTestForm:Form {
 TextBox folder=new TextBox{ReadOnly=true,Dock=DockStyle.Top};Label status=new Label{AutoSize=false,Height=92,Dock=DockStyle.Top};Button choose=new Button{Text="Choose WoW folder",AutoSize=true},install=new Button{Text="Apply BPC floor-marker test",AutoSize=true},restore=new Button{Text="Restore previous Patch-Y",AutoSize=true};bool busy;
 public RangeTestForm(){Text="Lau TEST ONLY - BPC floor markers";Width=760;Height=370;MinimumSize=new Size(760,370);BackColor=Color.FromArgb(12,22,34);ForeColor=Color.White;Font=new Font("Segoe UI",10);Padding=new Padding(24);
  using(var stream=Assembly.GetExecutingAssembly().GetManifestResourceStream("LauSetup.Icon.ico"))Icon=new Icon(stream);
  var title=new Label{Text="BLOOD PRINCE COUNCIL — FLOOR MARKERS TEST 2\n25 subtle, room-fixed markers: 10 melee stage points, 5 healer anchors, and 10 ranged points.\nNo player circles, spell edits, or gameplay changes. Validate visual clutter and placement in game.",Height=96,Dock=DockStyle.Top};
  var buttons=new FlowLayoutPanel{Dock=DockStyle.Top,Height=52};foreach(var b in new[]{choose,install,restore}){b.ForeColor=Color.Black;b.BackColor=Color.FromArgb(225,190,120);b.UseVisualStyleBackColor=false;b.FlatStyle=FlatStyle.Flat;buttons.Controls.Add(b);}Controls.Add(status);Controls.Add(buttons);Controls.Add(folder);Controls.Add(title);install.Enabled=restore.Enabled=false;
  choose.Click+=(s,e)=>{using(var d=new FolderBrowserDialog()){if(d.ShowDialog()!=DialogResult.OK)return;folder.Text=d.SelectedPath;install.Enabled=restore.Enabled=true;status.Text="Close WoW before applying or restoring. Only the root and active-language Patch-Y files are affected.";}};
  install.Click+=async(s,e)=>await Run(false);restore.Click+=async(s,e)=>await Run(true);FormClosing+=(s,e)=>{if(busy)e.Cancel=true;};
 }
 async Task Run(bool undo){busy=true;choose.Enabled=install.Enabled=restore.Enabled=false;status.Text="Checking and verifying files…";try{string root=folder.Text;string result=await Task.Run(()=>undo?RangeTest.Undo(root):RangeTest.Apply(root,Path.Combine(AppDomain.CurrentDomain.BaseDirectory,"payload")));status.Text=undo?"Previous Patch-Y restored and verified.":result==null?"This exact BPC floor-marker test is already installed.":"BPC floor-marker test installed and verified. /pyversion stays 3.0.8; validate the 25 points in-game.";}catch(Exception ex){status.Text=ex.Message;}finally{busy=false;choose.Enabled=install.Enabled=restore.Enabled=true;}}
}
}
