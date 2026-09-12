// Author, Creator, Last Modified By: Neil Mitchell
using System;
using System.IO;
using System.Linq;
using System.Collections.Generic;
using System.Drawing;
using System.Windows.Forms;
using System.Threading;
using System.Threading.Tasks;
using System.Diagnostics;

namespace LauSetup {
// Windows' default disabled text can turn nearly black on a dark control.
// Keep real Enabled semantics and paint only the disabled appearance ourselves.
public sealed class ReadableButton:Button {
    protected override void OnPaint(PaintEventArgs e) {
        if(Enabled){base.OnPaint(e);return;}
        Color background=Color.FromArgb(35,47,64),text=Color.FromArgb(196,207,223);
        using(var fill=new SolidBrush(background))e.Graphics.FillRectangle(fill,ClientRectangle);
        using(var border=new Pen(Color.FromArgb(114,133,157)))e.Graphics.DrawRectangle(border,0,0,Math.Max(0,Width-1),Math.Max(0,Height-1));
        TextRenderer.DrawText(e.Graphics,Text,Font,ClientRectangle,text,background,TextFormatFlags.HorizontalCenter|TextFormatFlags.VerticalCenter|TextFormatFlags.EndEllipsis);
    }
}
public sealed class ReadableCheckBox:CheckBox {
    protected override void OnPaint(PaintEventArgs e) {
        if(Enabled&&!WineHost.Active){base.OnPaint(e);return;}
        Color background=Parent==null?BackColor:Parent.BackColor,text=Enabled?ForeColor:Color.FromArgb(196,207,223);
        using(var fill=new SolidBrush(background))e.Graphics.FillRectangle(fill,ClientRectangle);
        int size=Math.Max(14,Font.Height-1),left=2,top=(Height-size)/2;
        using(var fill=new SolidBrush(Color.FromArgb(35,47,64)))e.Graphics.FillRectangle(fill,left,top,size,size);
        using(var pen=new Pen(Color.FromArgb(154,173,197)))e.Graphics.DrawRectangle(pen,left,top,size,size);
        if(Checked)using(var pen=new Pen(text,2F))e.Graphics.DrawLines(pen,new[]{new Point(left+3,top+size/2),new Point(left+size/2,top+size-4),new Point(left+size-3,top+3)});
        var bounds=new Rectangle(left+size+8,0,Math.Max(0,Width-left-size-8),Height);
        TextRenderer.DrawText(e.Graphics,Text,Font,bounds,text,background,TextFormatFlags.Left|TextFormatFlags.VerticalCenter|TextFormatFlags.WordBreak);
        if(Enabled&&Focused&&ShowFocusCues)ControlPaint.DrawFocusRectangle(e.Graphics,bounds,text,background);
    }
}
public sealed class SetupForm:Form {
    static readonly string UiFont=ChooseFont();
    static string ChooseFont() {
        using(var fonts=new System.Drawing.Text.InstalledFontCollection()) {
            var names=fonts.Families.Select(f=>f.Name).ToArray();
            foreach(string candidate in WineHost.Active?new[]{"Liberation Sans","DejaVu Sans","Tahoma","Arial"}:new[]{"Segoe UI","Tahoma","Liberation Sans","DejaVu Sans","Arial"})
                if(names.Contains(candidate,StringComparer.OrdinalIgnoreCase))return candidate;
        }
        throw new InvalidOperationException("No supported interface font was found. Install Liberation Sans fonts in your Wine environment, then reopen Lau Setup.");
    }
    readonly Catalog catalog;
    readonly Color ink=Color.FromArgb(241,245,251),muted=Color.FromArgb(190,204,224),surface=Color.FromArgb(23,33,49),gold=Color.FromArgb(224,179,98);
    TextBox folder;Label detected,download,status;CheckBox cons,spells,maps;Button browse,install,restore,cancel;ProgressBar progress;
    ClientInfo client;InstallPlan plan;CancellationTokenSource cancellation;bool busy,refreshing,recoveryOnly;
    public SetupForm(Catalog catalog) {
        this.catalog=catalog;Text="Lau Setup";Font=new Font(UiFont,10F);ForeColor=ink;BackColor=Color.FromArgb(12,20,33);ClientSize=new Size(820,630);MinimumSize=new Size(770,665);StartPosition=FormStartPosition.CenterScreen;AutoScaleMode=AutoScaleMode.Dpi;
        using(var icon=typeof(SetupForm).Assembly.GetManifestResourceStream("LauSetup.Icon.ico"))if(icon!=null)Icon=new Icon(icon);
        var grid=new TableLayoutPanel{Dock=DockStyle.Fill,Padding=new Padding(34,25,34,24),ColumnCount=1,RowCount=10};Controls.Add(grid);
        foreach(int h in new[]{39,42,28,44,52,45,45,45,43,1})grid.RowStyles.Add(new RowStyle(h==1?SizeType.Percent:SizeType.Absolute,h==1?100:h));
        grid.Controls.Add(Label("LAU  /  WRATH VISUAL UPGRADE",18,FontStyle.Bold,ink));
        grid.Controls.Add(Label("Your client. Your language. One simple install.",11,FontStyle.Regular,muted));
        grid.Controls.Add(Label("1   Choose your existing WoW 3.3.5a folder",10,FontStyle.Bold,ink));
        var row=new TableLayoutPanel{Dock=DockStyle.Fill,ColumnCount=2,Margin=new Padding(0)};row.ColumnStyles.Add(new ColumnStyle(SizeType.Percent,100));row.ColumnStyles.Add(new ColumnStyle(SizeType.Absolute,142));
        folder=new TextBox{ReadOnly=true,Dock=DockStyle.Fill,BackColor=surface,ForeColor=ink,BorderStyle=BorderStyle.FixedSingle,Margin=new Padding(0,5,12,3)};row.Controls.Add(folder);
        browse=Button("Choose folder…",false);browse.Dock=DockStyle.Fill;browse.Click+=Choose;row.Controls.Add(browse);grid.Controls.Add(row);
        detected=Label("Language and model setup will be detected automatically.",10,FontStyle.Regular,muted);detected.Padding=new Padding(0,11,0,0);grid.Controls.Add(detected);
        cons=Check("Enhanced Consecration",true);grid.Controls.Add(cons);
        spells=Check("New spell visuals  ·  available with HD models",false);spells.Enabled=false;grid.Controls.Add(spells);
        maps=Check("Upgrade maps and minimap  ·  optional extra download",false);grid.Controls.Add(maps);
        download=Label("Select your folder to see the download size.",10,FontStyle.Regular,muted);download.Padding=new Padding(0,10,0,0);grid.Controls.Add(download);
        var bottom=new TableLayoutPanel{Dock=DockStyle.Fill,ColumnCount=1,RowCount=5,Margin=new Padding(0,8,0,0)};
        bottom.RowStyles.Add(new RowStyle(SizeType.Absolute,48));bottom.RowStyles.Add(new RowStyle(SizeType.Absolute,30));bottom.RowStyles.Add(new RowStyle(SizeType.Percent,100));bottom.RowStyles.Add(new RowStyle(SizeType.Absolute,28));bottom.RowStyles.Add(new RowStyle(SizeType.Absolute,26));
        var actions=new FlowLayoutPanel{Dock=DockStyle.Fill,FlowDirection=FlowDirection.LeftToRight,WrapContents=false,Margin=new Padding(0)};
        install=Button("Install upgrade",true);install.Width=182;install.Enabled=false;install.Click+=Install;actions.Controls.Add(install);
        cancel=Button("Cancel",false);cancel.Width=164;cancel.Visible=false;cancel.Click+=(s,e)=>{if(cancellation!=null)cancellation.Cancel();};actions.Controls.Add(cancel);
        restore=Button("Restore previous install",false);restore.Width=205;restore.Enabled=false;restore.Click+=Restore;actions.Controls.Add(restore);bottom.Controls.Add(actions);
        progress=new ProgressBar{Dock=DockStyle.Fill,Maximum=1000,Visible=false,Margin=new Padding(0,8,0,8)};bottom.Controls.Add(progress);
        status=Label("",10,FontStyle.Regular,ink);status.Padding=new Padding(0,6,0,0);bottom.Controls.Add(status);
        bottom.Controls.Add(Label("Automatic backups. Existing addons and personal settings are preserved.",10,FontStyle.Regular,muted));
        bottom.Controls.Add(Label("Release 3.0.6 Lau  •  "+(WineHost.Active?"Wine 11 on Linux":"Windows 10 / 11")+"  •  Existing build 12340 required",10,FontStyle.Regular,muted));grid.Controls.Add(bottom);
        cons.CheckedChanged+=RefreshPlan;spells.CheckedChanged+=RefreshPlan;maps.CheckedChanged+=RefreshPlan;
        FormClosing+=(s,e)=>{if(busy){e.Cancel=true;status.Text="Please wait for this operation to finish, or use Cancel.";}};
        AcceptButton=install;
    }
    Label Label(string text,float size,FontStyle style,Color color) { return new Label{Text=text,Font=new Font(UiFont,size,style),ForeColor=color,Dock=DockStyle.Fill,AutoEllipsis=false,Margin=new Padding(0),TextAlign=ContentAlignment.MiddleLeft}; }
    Button Button(string text,bool primary) { var b=new ReadableButton{Text=text,Height=40,FlatStyle=FlatStyle.Flat,BackColor=primary?gold:surface,ForeColor=primary?Color.FromArgb(12,20,33):ink,Cursor=Cursors.Hand,Margin=new Padding(0,0,10,0),Font=new Font(UiFont,10,primary?FontStyle.Bold:FontStyle.Regular)};b.FlatAppearance.BorderColor=primary?gold:Color.FromArgb(114,133,157);return b; }
    CheckBox Check(string text,bool check) { return new ReadableCheckBox{Text=text,Checked=check,Dock=DockStyle.Fill,AutoSize=false,Margin=new Padding(0),Padding=new Padding(0,2,0,2),ForeColor=ink}; }
    async void Choose(object sender,EventArgs args) {
        using(var dialog=new FolderBrowserDialog{Description="Select your World of Warcraft folder (the folder containing WoW.exe).",ShowNewFolderButton=false,SelectedPath=client==null?"":client.Root}) {
            if(dialog.ShowDialog(this)!=DialogResult.OK)return;
            SetBusy(true);status.Text="Checking your client…";
            try {
                await SelectRoot(dialog.SelectedPath);
            }catch(Exception ex){client=null;plan=null;detected.Text="Client could not be prepared.";status.Text=ex.Message;}
            finally{SetBusy(false);}
            if(client!=null&&!recoveryOnly)RefreshPlan(null,EventArgs.Empty);
        }
    }
    internal async Task SelectRoot(string selected) {
        string root=SafePaths.Root(selected);Client.AssertClosed(root);string pending=Transaction.Pending(root);
        plan=null;recoveryOnly=pending!=null;
        if(recoveryOnly){
            var record=new Transaction(catalog,null,null).ReadBackup(pending);
            if(!root.Equals(record.Root,StringComparison.OrdinalIgnoreCase))throw new IOException("This backup belongs to another client.");
            client=new ClientInfo{Root=root,Locale=record.Locale};folder.Text=root;
            detected.Text=Language(client.Locale)+"  ·  Interrupted installation found";
            download.Text="Restore is available even if the game executable is missing.";
            status.Text="Click Restore previous install to recover your game files.";return;
        }
        client=await Task.Run(()=>Client.Inspect(root,catalog));UpdateClientDisplay();
        status.Text="Ready. A verified backup is created before any game files change.";
    }
    void UpdateClientDisplay(){
        folder.Text=client.Root;refreshing=true;spells.Checked=client.NewSpells;maps.Checked=client.MapsInstalled;refreshing=false;
        detected.Text=Language(client.Locale)+"  ·  "+(client.Hd?"HD models detected":"Original models detected")+"  ·  Build 12340";
    }
    async void RefreshPlan(object sender,EventArgs args) {
        if(refreshing||busy||client==null||recoveryOnly)return;SetBusy(true);status.Text="Checking installed files…";
        try {
            bool newSpells=spells.Checked,consecration=cons.Checked,includeMaps=maps.Checked;
            plan=await Task.Run(()=>InstallPlan.Build(client,catalog,newSpells,consecration,includeMaps));
            download.Text=plan.Operations.Count==0?"Your selected release 3.0.6 is already installed.":"Download up to "+FormatSize(plan.DownloadBytes)+"  ·  "+(plan.Maps?"Upgraded maps included":"Existing maps kept");
            install.Text=plan.Operations.Count==0?"Already installed":"Install upgrade";
            status.Text=Transaction.Pending(client.Root)!=null?"An interrupted install was found. Restore it before continuing.":"Ready. A verified backup is created before any game files change.";
        }catch(Exception ex){plan=null;status.Text=ex.Message;}finally{SetBusy(false);}
    }
    async void Install(object sender,EventArgs args) {
        if(plan==null||client==null||busy)return;SetBusy(true);cancellation=new CancellationTokenSource();cancel.Visible=true;progress.Visible=true;progress.Value=0;
        try {
            Client.AssertClosed(client.Root);
            var current=plan;string state=Transaction.StateRoot(client.Root),cache=SafePaths.Under(state,"cache");
            long done=0;
            var transfer=new Progress<TransferProgress>(p=>{if(IsDisposed)return;status.Text="Downloading "+Friendly(p.Name)+"  ·  "+FormatSize(p.Received)+" / "+FormatSize(p.Total);progress.Value=Math.Max(0,Math.Min(1000,(int)(p.Overall*1000.0/Math.Max(1,current.DownloadBytes))));});
            var messages=new Progress<string>(s=>status.Text=s);
            await Task.Run(()=>{
                using(var lease=ClientLease.Acquire(current.Root)){
                if(Transaction.Pending(current.Root)!=null)throw new IOException("An interrupted install needs restoring first.");
                var files=new Dictionary<string,string>();var loader=new Downloader(cache,Path.Combine(AppDomain.CurrentDomain.BaseDirectory,"payload"),p=>{p.Overall=done+p.Received;((IProgress<TransferProgress>)transfer).Report(p);});
                foreach(var id in current.Operations.Where(o=>o.AssetId!=null).Select(o=>o.AssetId).Distinct()) {
                    cancellation.Token.ThrowIfCancellationRequested();
                    files[id]=loader.Fetch(catalog.Get(id),cancellation.Token);done+=catalog.Get(id).Bytes;
                }
                var transaction=new Transaction(catalog,s=>((IProgress<string>)messages).Report(s),null);transaction.InstallWithLease(current,files,cancellation.Token,lease);
                }
            });
            client=await Task.Run(()=>Client.Inspect(client.Root,catalog));UpdateClientDisplay();
            progress.Value=1000;status.Text="Installed and verified. Start WoW, run /pyversion, and test your chosen effects.\nYou can restore the previous install here at any time.";
            plan=null;download.Text="Your backup is saved in the selected client’s LauSetupBackups folder.";
        }catch(OperationCanceledException){status.Text="Cancelled. Completed downloads are kept for your next attempt.";}
        catch(Exception ex){status.Text=ex.Message;}
        finally{cancellation.Dispose();cancellation=null;cancel.Visible=false;SetBusy(false);}
    }
    async void Restore(object sender,EventArgs args) {
        if(client==null||busy)return;
        string record;try{record=Transaction.Pending(client.Root)??Transaction.Journals(client.Root).FirstOrDefault(f=>Transaction.Status(f)=="INSTALLED");}catch(Exception ex){status.Text=ex.Message;return;}
        if(record==null){status.Text="There is no previous install to restore.";return;}
        if(MessageBox.Show(this,"Restore the game files from the most recent Lau Setup backup? Your addons and saved settings are preserved.","Restore previous install",MessageBoxButtons.YesNo,MessageBoxIcon.Question)!=DialogResult.Yes)return;
        await RestoreRecord(record);
    }
    internal async Task RestoreRecord(string record){
        SetBusy(true);status.Text="Restoring your previous install…";
        try{await Task.Run(()=>new Transaction(catalog,null,null).Restore(record));client=await Task.Run(()=>Client.Inspect(client.Root,catalog));recoveryOnly=false;UpdateClientDisplay();status.Text="Previous install restored and verified.";plan=null;}
        catch(Exception ex){status.Text=ex.Message;}finally{SetBusy(false);}
    }
    void SetBusy(bool value) { busy=value;browse.Enabled=!value;cons.Enabled=!value&&!recoveryOnly;spells.Enabled=!value&&!recoveryOnly&&client!=null&&client.Hd;maps.Enabled=!value&&!recoveryOnly&&client!=null&&!client.MapsInstalled;install.Enabled=!value&&plan!=null&&plan.Operations.Count>0;restore.Enabled=false;if(!value&&client!=null)try{restore.Enabled=Transaction.Journals(client.Root).Any(f=>new[]{"STAGING","COMMITTING","RESTORING","RECOVERY_REQUIRED","INSTALLED"}.Contains(Transaction.Status(f)));if(Transaction.Pending(client.Root)!=null)install.Enabled=false;}catch(Exception ex){install.Enabled=false;status.Text=ex.Message;} }
    internal void Preview(string output,string state="ready") {
        if(state!="initial"){
            folder.Text=@"D:\Games\World of Warcraft";detected.Text="English (US)  ·  HD models detected  ·  Build 12340";spells.Checked=true;spells.Enabled=true;
            download.Text="Download up to 472.4 MB  ·  Existing maps kept";status.Text="Ready. A verified backup is created before any game files change.";install.Enabled=true;
        }
        if(state=="busy"){SetBusy(true);cancel.Visible=true;progress.Visible=true;progress.Value=420;status.Text="Downloading spell visuals  ·  84.0 MB / 200.0 MB";}
        CreateControl();ShowInTaskbar=false;Location=new Point(-32000,-32000);Show();PerformLayout();Application.DoEvents();
        using(var bitmap=new Bitmap(Width,Height)){DrawToBitmap(bitmap,new Rectangle(0,0,Width,Height));bitmap.Save(output,System.Drawing.Imaging.ImageFormat.Png);}
        // Preview does not perform an installation and must not trip the busy-close guard.
        busy=false;Close();
    }
    public static string FormatSize(long bytes){return bytes>=1000000000?(bytes/1000000000.0).ToString("0.00")+" GB":(bytes/1000000.0).ToString("0.0")+" MB";}
    public static string Language(string locale){switch(locale){case "enUS":return "English (US)";case "deDE":return "Deutsch";case "frFR":return "Français";case "esES":return "Español (España)";case "esMX":return "Español (México)";case "koKR":return "한국어";case "ruRU":return "Русский";case "zhCN":return "简体中文";case "zhTW":return "繁體中文";default:return locale;}}
    static string Friendly(string id){return id=="Maps"?"maps and minimap":id.StartsWith("Y-")?"spell indicators":id.Contains("Q-")?"loading screens and regional artwork":id=="Executable"?"the compatible game executable":"spell visuals";}
}
public static class Program {
    [STAThread] public static int Main(string[] args) {
        try {
            if(!WineHost.Active) {
                object release=Microsoft.Win32.Registry.GetValue(@"HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\NET Framework Setup\NDP\v4\Full","Release",null);
                if(release==null||Convert.ToInt32(release)<528040) {
                    if(MessageBox.Show("Lau Setup requires .NET Framework 4.8. Open Microsoft's official runtime download page?","Install .NET Framework 4.8",MessageBoxButtons.YesNo,MessageBoxIcon.Information)==DialogResult.Yes)
                        Process.Start(new ProcessStartInfo("https://dotnet.microsoft.com/en-us/download/dotnet-framework/net48"){UseShellExecute=true});
                    return 2;
                }
            }
            Application.EnableVisualStyles();Application.SetCompatibleTextRenderingDefault(false);var catalog=Catalog.Embedded();
            using(var form=new SetupForm(catalog)) {
                if((args.Length==2||args.Length==3)&&args[0]=="--render-preview"){form.Preview(Path.GetFullPath(args[1]),args.Length==3?args[2]:"ready");return 0;}
                Application.Run(form);return 0;
            }
        }catch(Exception ex){while(ex is TypeInitializationException&&ex.InnerException!=null)ex=ex.InnerException;MessageBox.Show(ex.Message,"Lau Setup",MessageBoxButtons.OK,MessageBoxIcon.Error);return 1;}
    }
    }
}
