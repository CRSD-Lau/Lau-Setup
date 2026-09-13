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
    static readonly Dictionary<string,string> uiFonts=new Dictionary<string,string>(StringComparer.OrdinalIgnoreCase);
    static string UiFont { get { return ChooseFont(Ui.Locale); } }
    static string ChooseFont(string locale) {
        string value;if(uiFonts.TryGetValue(locale,out value))return value;
        using(var fonts=new System.Drawing.Text.InstalledFontCollection())value=SelectFont(locale,fonts.Families.Select(f=>f.Name),WineHost.Active);
        uiFonts[locale]=value;return value;
    }
    internal static string SelectFont(string locale,IEnumerable<string> names,bool wine) {
        var candidates=new List<string>();
        if(wine) {
            if(locale=="zh-CN")candidates.Add("Noto Sans CJK SC");
            else if(locale=="zh-TW")candidates.Add("Noto Sans CJK TC");
            else if(locale=="ko-KR")candidates.Add("Noto Sans CJK KR");
            foreach(string candidate in new[]{"Noto Sans CJK SC","Noto Sans CJK TC","Noto Sans CJK KR","Liberation Sans","DejaVu Sans","Tahoma","Arial"})if(!candidates.Contains(candidate))candidates.Add(candidate);
        } else candidates.AddRange(new[]{"Segoe UI","Tahoma","Liberation Sans","DejaVu Sans","Arial"});
        foreach(string candidate in candidates)if(names.Contains(candidate,StringComparer.OrdinalIgnoreCase))return candidate;
        throw new InvalidOperationException("No supported interface font was found. Install Liberation Sans fonts in your Wine environment, then reopen Lau Setup.");
    }
    readonly Catalog catalog;
    readonly Color ink=Color.FromArgb(241,245,251),muted=Color.FromArgb(190,204,224),surface=Color.FromArgb(23,33,49),gold=Color.FromArgb(224,179,98);
    TextBox folder;Label detected,download,status;CheckBox cons,spells,maps;Button browse,install,restore,cancel;ProgressBar progress;ComboBox language;
    ClientInfo client;InstallPlan plan;CancellationTokenSource cancellation;bool busy,refreshing,recoveryOnly;
    sealed class PhraseValue { readonly string key;public PhraseValue(string key){this.key=key;}public override string ToString(){return Ui.T(key);} }
    sealed class TextBinding {
        public string Key;public object[] Arguments;public bool Message;
        public string Render(){return Message?Ui.Message(Key):Ui.F(Key,Arguments.Select(a=>a is PhraseValue?a.ToString():a).ToArray());}
    }
    static object Phrase(string key){return new PhraseValue(key);}
    static void SetText(Control control,string key,params object[] arguments){var binding=new TextBinding{Key=key,Arguments=arguments};control.Tag=binding;control.Text=binding.Render();}
    static void SetMessage(Control control,string message){var binding=new TextBinding{Key=message,Arguments=new object[0],Message=true};control.Tag=binding;control.Text=binding.Render();}
    void TranslateControls(Control parent){foreach(Control control in parent.Controls){var binding=control.Tag as TextBinding;if(binding!=null)control.Text=binding.Render();TranslateControls(control);}}
    static void RefreshUiFont(Control control,string family){
        if(!control.Font.FontFamily.Name.Equals(family,StringComparison.OrdinalIgnoreCase))control.Font=new Font(family,control.Font.Size,control.Font.Style);
        foreach(Control child in control.Controls)RefreshUiFont(child,family);
    }
    internal void ChangeLanguage(string choice,bool persist){
        Ui.Select(choice,persist);SuspendLayout();RefreshUiFont(this,UiFont);TranslateControls(this);language.Refresh();ResumeLayout(true);
        if(!String.IsNullOrEmpty(Ui.LastPreferenceError))SetText(status,"This language is active for this session, but the preference could not be saved.");
    }
    public SetupForm(Catalog catalog) {
        this.catalog=catalog;Text="Lau Setup";Font=new Font(UiFont,10F);ForeColor=ink;BackColor=Color.FromArgb(12,20,33);ClientSize=new Size(920,760);MinimumSize=new Size(840,700);StartPosition=FormStartPosition.CenterScreen;AutoScaleMode=AutoScaleMode.Dpi;
        using(var icon=typeof(SetupForm).Assembly.GetManifestResourceStream("LauSetup.Icon.ico"))if(icon!=null)Icon=new Icon(icon);
        var grid=new TableLayoutPanel{Dock=DockStyle.Fill,Padding=new Padding(34,25,34,24),ColumnCount=1,RowCount=11};Controls.Add(grid);
        foreach(int h in new[]{42,36,44,30,46,52,36,44,44,46,1})grid.RowStyles.Add(new RowStyle(h==1?SizeType.Percent:SizeType.Absolute,h==1?100:h));
        grid.Controls.Add(Label("LAU  /  WRATH VISUAL UPGRADE",18,FontStyle.Bold,ink));
        grid.Controls.Add(Label("Your client. Your language. One simple install.",11,FontStyle.Regular,muted));
        var languageRow=new TableLayoutPanel{Dock=DockStyle.Fill,ColumnCount=2,Margin=new Padding(0,0,0,8)};
        languageRow.ColumnStyles.Add(new ColumnStyle(SizeType.AutoSize));languageRow.ColumnStyles.Add(new ColumnStyle(SizeType.Percent,100));
        var languageLabel=Label("Interface language",10,FontStyle.Regular,muted);languageLabel.AutoSize=true;languageLabel.Margin=new Padding(0,0,16,0);languageRow.Controls.Add(languageLabel);
        language=new ComboBox{Name="interfaceLanguage",DropDownStyle=ComboBoxStyle.DropDownList,Dock=DockStyle.Fill,BackColor=surface,ForeColor=ink,DisplayMember="Name",ValueMember="Code",AccessibleName=Ui.T("Interface language")};
        foreach(var option in Ui.Languages)language.Items.Add(option);
        language.SelectedIndex=Array.FindIndex(Ui.Languages,x=>x.Code==Ui.Choice);if(language.SelectedIndex<0)language.SelectedIndex=0;
        language.SelectedIndexChanged+=(s,e)=>{if(language.SelectedItem!=null){ChangeLanguage(((LanguageOption)language.SelectedItem).Code,true);language.AccessibleName=Ui.T("Interface language");}};
        languageRow.Controls.Add(language);grid.Controls.Add(languageRow);
        grid.Controls.Add(Label("1   Choose your existing WoW 3.3.5a folder",10,FontStyle.Bold,ink));
        var row=new TableLayoutPanel{Dock=DockStyle.Fill,ColumnCount=2,Margin=new Padding(0)};row.ColumnStyles.Add(new ColumnStyle(SizeType.Percent,100));row.ColumnStyles.Add(new ColumnStyle(SizeType.AutoSize));
        folder=new TextBox{ReadOnly=true,Dock=DockStyle.Fill,BackColor=surface,ForeColor=ink,BorderStyle=BorderStyle.FixedSingle,Margin=new Padding(0,5,12,3)};row.Controls.Add(folder);
        browse=Button("Choose folder…",false);browse.Dock=DockStyle.Fill;browse.Click+=Choose;row.Controls.Add(browse);grid.Controls.Add(row);
        detected=Label("Language and model setup will be detected automatically.",10,FontStyle.Regular,muted);detected.Padding=new Padding(0,11,0,0);grid.Controls.Add(detected);
        cons=Check("Enhanced Consecration",true);grid.Controls.Add(cons);
        spells=Check("New spell visuals  ·  available with HD models",false);spells.Enabled=false;grid.Controls.Add(spells);
        maps=Check("Upgrade maps and minimap  ·  optional extra download",false);grid.Controls.Add(maps);
        download=Label("Select your folder to see the download size.",10,FontStyle.Regular,muted);download.Padding=new Padding(0,10,0,0);grid.Controls.Add(download);
        var bottom=new TableLayoutPanel{Dock=DockStyle.Fill,ColumnCount=1,RowCount=5,Margin=new Padding(0,8,0,0)};
        bottom.RowStyles.Add(new RowStyle(SizeType.Absolute,48));bottom.RowStyles.Add(new RowStyle(SizeType.Absolute,28));bottom.RowStyles.Add(new RowStyle(SizeType.Percent,100));bottom.RowStyles.Add(new RowStyle(SizeType.Absolute,32));bottom.RowStyles.Add(new RowStyle(SizeType.Absolute,32));
        var actions=new FlowLayoutPanel{Dock=DockStyle.Fill,FlowDirection=FlowDirection.LeftToRight,WrapContents=false,Margin=new Padding(0)};
        install=Button("Install upgrade",true);install.Width=182;install.Enabled=false;install.Click+=Install;actions.Controls.Add(install);
        cancel=Button("Cancel",false);cancel.Width=164;cancel.Visible=false;cancel.Click+=(s,e)=>{if(cancellation!=null)cancellation.Cancel();};actions.Controls.Add(cancel);
        restore=Button("Restore previous install",false);restore.Width=205;restore.Enabled=false;restore.Click+=Restore;actions.Controls.Add(restore);bottom.Controls.Add(actions);
        progress=new ProgressBar{Dock=DockStyle.Fill,Maximum=1000,Visible=false,Margin=new Padding(0,8,0,8)};bottom.Controls.Add(progress);
        status=Label("",10,FontStyle.Regular,ink);status.Padding=new Padding(0,6,0,0);status.AutoSize=true;var statusScroll=new Panel{Dock=DockStyle.Fill,AutoScroll=true,Margin=new Padding(0)};statusScroll.Controls.Add(status);status.Dock=DockStyle.Top;statusScroll.Resize+=(s,e)=>{status.MaximumSize=new Size(Math.Max(100,statusScroll.ClientSize.Width-SystemInformation.VerticalScrollBarWidth),0);};bottom.Controls.Add(statusScroll);
        bottom.Controls.Add(Label("Automatic backups. Existing addons and personal settings are preserved.",10,FontStyle.Regular,muted));
        var release=Label("",10,FontStyle.Regular,muted);SetText(release,"Release {0} Lau  •  {1}  •  Existing build 12340 required",catalog.Version,WineHost.Active?"Wine 11 on Linux":"Windows 10 / 11");bottom.Controls.Add(release);grid.Controls.Add(bottom);
        cons.CheckedChanged+=RefreshPlan;spells.CheckedChanged+=RefreshPlan;maps.CheckedChanged+=RefreshPlan;
        FormClosing+=(s,e)=>{if(busy){e.Cancel=true;SetText(status,"Please wait for this operation to finish, or use Cancel.");}};
        AcceptButton=install;
    }
    Label Label(string text,float size,FontStyle style,Color color) { var label=new Label{Font=new Font(UiFont,size,style),ForeColor=color,Dock=DockStyle.Fill,AutoEllipsis=false,Margin=new Padding(0),TextAlign=ContentAlignment.MiddleLeft};SetText(label,text);return label; }
    Button Button(string text,bool primary) { var b=new ReadableButton{Height=40,AutoSize=true,AutoSizeMode=AutoSizeMode.GrowAndShrink,MinimumSize=new Size(140,40),Padding=new Padding(12,0,12,0),FlatStyle=FlatStyle.Flat,BackColor=primary?gold:surface,ForeColor=primary?Color.FromArgb(12,20,33):ink,Cursor=Cursors.Hand,Margin=new Padding(0,0,10,0),Font=new Font(UiFont,10,primary?FontStyle.Bold:FontStyle.Regular)};b.FlatAppearance.BorderColor=primary?gold:Color.FromArgb(114,133,157);SetText(b,text);return b; }
    CheckBox Check(string text,bool check) { var box=new ReadableCheckBox{Checked=check,Dock=DockStyle.Fill,AutoSize=false,Margin=new Padding(0),Padding=new Padding(0,2,0,2),ForeColor=ink};SetText(box,text);return box; }
    async void Choose(object sender,EventArgs args) {
        using(var dialog=new FolderBrowserDialog{Description=Ui.T("Select your World of Warcraft folder (the folder containing WoW.exe)."),ShowNewFolderButton=false,SelectedPath=client==null?"":client.Root}) {
            if(dialog.ShowDialog(this)!=DialogResult.OK)return;
            SetBusy(true);SetText(status,"Checking your client…");
            try {
                await SelectRoot(dialog.SelectedPath);
            }catch(Exception ex){client=null;plan=null;SetText(detected,"Client could not be prepared.");SetMessage(status,ex.Message);}
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
            SetText(detected,"{0}  ·  Interrupted installation found",Language(client.Locale));
            SetText(download,"Restore is available even if the game executable is missing.");
            SetText(status,"Click Restore previous install to recover your game files.");return;
        }
        client=await Task.Run(()=>Client.Inspect(root,catalog));UpdateClientDisplay();
        SetText(status,"Ready. A verified backup is created before any game files change.");
    }
    void UpdateClientDisplay(){
        folder.Text=client.Root;refreshing=true;spells.Checked=client.NewSpells;maps.Checked=client.MapsInstalled;refreshing=false;
        SetText(detected,"{0}  ·  {1}  ·  Build 12340",Language(client.Locale),client.Hd?Phrase("HD models detected"):Phrase("Original models detected"));
    }
    async void RefreshPlan(object sender,EventArgs args) {
        if(refreshing||busy||client==null||recoveryOnly)return;SetBusy(true);SetText(status,"Checking installed files…");
        try {
            bool newSpells=spells.Checked,consecration=cons.Checked,includeMaps=maps.Checked;
            plan=await Task.Run(()=>InstallPlan.Build(client,catalog,newSpells,consecration,includeMaps));
            if(plan.Operations.Count==0)SetText(download,"Your selected release {0} is already installed.",catalog.Version);else SetText(download,"Download up to {0}  ·  {1}",FormatSize(plan.DownloadBytes),plan.Maps?Phrase("Upgraded maps included"):Phrase("Existing maps kept"));
            SetText(install,plan.Operations.Count==0?"Already installed":"Install upgrade");
            SetText(status,Transaction.Pending(client.Root)!=null?"An interrupted install was found. Restore it before continuing.":(!newSpells?"Patch-S becomes .mpq.disabled. Any older disabled copy is preserved separately. Restore previous install reverses the change.":"Ready. A verified backup is created before any game files change."));
            if(Transaction.Pending(client.Root)==null&&plan.Operations.Any(o=>o.ExtraPatch))SetText(status,"{0} extra upgrade patches will be backed up automatically in LauSetupBackups. Click Install upgrade to continue.",plan.Operations.Count(o=>o.ExtraPatch));
        }catch(Exception ex){plan=null;SetMessage(status,ex.Message);}finally{SetBusy(false);}
    }
    async void Install(object sender,EventArgs args) {
        if(plan==null||client==null||busy)return;SetBusy(true);cancellation=new CancellationTokenSource();cancel.Visible=true;progress.Visible=true;progress.Value=0;
        try {
            Client.AssertClosed(client.Root);
            var current=plan;string state=Transaction.StateRoot(client.Root),cache=SafePaths.Under(state,"cache");
            long done=0;
            var transfer=new Progress<TransferProgress>(p=>{if(IsDisposed)return;SetText(status,"Downloading {0}  ·  {1} / {2}",Phrase(Friendly(p.Name)),FormatSize(p.Received),FormatSize(p.Total));progress.Value=Math.Max(0,Math.Min(1000,(int)(p.Overall*1000.0/Math.Max(1,current.DownloadBytes))));});
            var messages=new Progress<string>(s=>SetMessage(status,s));
            await Task.Run(()=>{
                using(var lease=ClientLease.Acquire(current.Root)){
                if(Transaction.Pending(current.Root)!=null)throw new IOException("An interrupted install needs restoring first.");
                MpqScan.ValidatePlan(current,catalog,cancellation.Token);
                var files=new Dictionary<string,string>();var loader=new Downloader(cache,Path.Combine(AppDomain.CurrentDomain.BaseDirectory,"payload"),p=>{p.Overall=done+p.Received;((IProgress<TransferProgress>)transfer).Report(p);});
                foreach(var id in current.Operations.Where(o=>o.AssetId!=null&&o.SourceRelative==null).Select(o=>o.AssetId).Distinct()) {
                    cancellation.Token.ThrowIfCancellationRequested();
                    files[id]=loader.Fetch(catalog.Get(id),cancellation.Token);done+=catalog.Get(id).Bytes;
                }
                var transaction=new Transaction(catalog,s=>((IProgress<string>)messages).Report(s),null);transaction.InstallWithLease(current,files,cancellation.Token,lease);
                }
            });
            client=await Task.Run(()=>Client.Inspect(client.Root,catalog));UpdateClientDisplay();
            progress.Value=1000;SetText(status,"Installed and verified. Start WoW, run /pyversion, and test your chosen effects.\nYou can restore the previous install here at any time.");
            plan=null;SetText(download,"Your backup is saved in the selected client’s LauSetupBackups folder.");
        }catch(OperationCanceledException){SetText(status,"Cancelled. Completed downloads are kept for your next attempt.");}
        catch(Exception ex){SetMessage(status,ex.Message);}
        finally{cancellation.Dispose();cancellation=null;cancel.Visible=false;SetBusy(false);}
    }
    async void Restore(object sender,EventArgs args) {
        if(client==null||busy)return;
        string record;try{record=Transaction.Pending(client.Root)??Transaction.Journals(client.Root).FirstOrDefault(f=>Transaction.Status(f)=="INSTALLED");}catch(Exception ex){SetMessage(status,ex.Message);return;}
        if(record==null){SetText(status,"There is no previous install to restore.");return;}
        if(MessageBox.Show(this,Ui.T("Restore the game files from the most recent Lau Setup backup? Your addons and saved settings are preserved."),Ui.T("Restore previous install"),MessageBoxButtons.YesNo,MessageBoxIcon.Question)!=DialogResult.Yes)return;
        await RestoreRecord(record);
    }
    internal async Task RestoreRecord(string record){
        SetBusy(true);SetText(status,"Restoring your previous install…");
        try{await Task.Run(()=>new Transaction(catalog,null,null).Restore(record));client=await Task.Run(()=>Client.Inspect(client.Root,catalog));recoveryOnly=false;UpdateClientDisplay();SetText(status,"Previous install restored and verified.");plan=null;}
        catch(Exception ex){SetMessage(status,ex.Message);}finally{SetBusy(false);}
    }
    void SetBusy(bool value) { if(value)busy=true;language.Enabled=!value;browse.Enabled=!value;cons.Enabled=!value&&!recoveryOnly;spells.Enabled=!value&&!recoveryOnly&&client!=null&&client.Hd;maps.Enabled=!value&&!recoveryOnly&&client!=null&&!client.MapsInstalled;install.Enabled=!value&&plan!=null&&plan.Operations.Count>0;restore.Enabled=false;if(!value&&client!=null)try{restore.Enabled=Transaction.Journals(client.Root).Any(f=>new[]{"STAGING","COMMITTING","RESTORING","RECOVERY_REQUIRED","INSTALLED"}.Contains(Transaction.Status(f)));if(Transaction.Pending(client.Root)!=null)install.Enabled=false;}catch(Exception ex){install.Enabled=false;SetMessage(status,ex.Message);} busy=value; }
    internal void Preview(string output,string state="ready") {
        if(state!="initial"){
            folder.Text=@"D:\Games\World of Warcraft";SetText(detected,"{0}  ·  {1}  ·  Build 12340",Language("enUS"),Phrase("HD models detected"));spells.Checked=true;spells.Enabled=true;
            SetText(download,"Download up to {0}  ·  {1}","472.4 MB",Phrase("Existing maps kept"));SetText(status,"Ready. A verified backup is created before any game files change.");install.Enabled=true;
        }
        if(state=="busy"){SetBusy(true);cancel.Visible=true;progress.Visible=true;progress.Value=420;SetText(status,"Downloading {0}  ·  {1} / {2}",Phrase("spell visuals"),"84.0 MB","200.0 MB");}
        if(state=="recovery"){SetText(detected,"{0}  ·  Interrupted installation found",Language("enUS"));SetText(status,"Click Restore previous install to recover your game files.");install.Enabled=false;restore.Enabled=true;}
        if(state=="error")SetMessage(status,@"Cannot safely check patch: Data\patch-test.mpq. No game files changed. Check this archive before retrying. Unsupported MPQ table layout.");
        if(state=="conflicts")SetText(status,"{0} extra upgrade patches will be backed up automatically in LauSetupBackups. Click Install upgrade to continue.",3);
        CreateControl();ShowInTaskbar=false;StartPosition=FormStartPosition.Manual;Location=WineHost.Active?Point.Empty:new Point(-32000,-32000);Show();PerformLayout();Refresh();Application.DoEvents();
        // Mono's DrawToBitmap omits custom controls. Capture the real Wine window
        // on the isolated test display so visual evidence includes every control.
        using(var bitmap=new Bitmap(Width,Height)){
            if(WineHost.Active)using(var graphics=Graphics.FromImage(bitmap))graphics.CopyFromScreen(Location,Point.Empty,Size);
            else DrawToBitmap(bitmap,new Rectangle(0,0,Width,Height));
            bitmap.Save(output,System.Drawing.Imaging.ImageFormat.Png);
        }
        var controls=new List<object>();CollectPreview(this,controls);
        File.WriteAllText(output+".json",Json.Text(new{Author="Neil Mitchell",Creator="Neil Mitchell",LastModifiedBy="Neil Mitchell",Locale=Ui.Locale,Choice=Ui.Choice,State=state,Capture=WineHost.Active?"screen":"DrawToBitmap",Font=Font.Name,Controls=controls}));
        // Preview does not perform an installation and must not trip the busy-close guard.
        busy=false;Close();
    }
    static void CollectPreview(Control parent,List<object> controls){foreach(Control c in parent.Controls){if(c.Visible&&(c is Label||c is Button||c is CheckBox||c is ComboBox)){var measured=TextRenderer.MeasureText(c.Text,c.Font,new Size(Math.Max(1,c.ClientSize.Width-c.Padding.Horizontal),Int32.MaxValue),TextFormatFlags.WordBreak|TextFormatFlags.NoPrefix);controls.Add(new{Type=c.GetType().Name,c.Text,c.Width,c.Height,TextHeight=measured.Height,Scrollable=c.Parent is Panel&&((Panel)c.Parent).AutoScroll});}CollectPreview(c,controls);}}
    public static string FormatSize(long bytes){return bytes>=1000000000?(bytes/1000000000.0).ToString("0.00")+" GB":(bytes/1000000.0).ToString("0.0")+" MB";}
    public static string Language(string locale){switch(locale){case "enUS":return "English (US)";case "deDE":return "Deutsch";case "frFR":return "Français";case "esES":return "Español (España)";case "esMX":return "Español (México)";case "koKR":return "한국어";case "ruRU":return "Русский";case "zhCN":return "简体中文";case "zhTW":return "繁體中文";default:return locale;}}
    static string Friendly(string id){return id=="Maps"?"maps and minimap":id.StartsWith("Y-")?"spell indicators":id.Contains("Q-")?"loading screens and regional artwork":id=="Executable"?"the compatible game executable":"spell visuals";}
}
public static class Program {
    [STAThread] public static int Main(string[] args) {
        try {
            string requested=null;var remaining=new List<string>();
            for(int i=0;i<args.Length;i++){
                if(args[i]=="--language"){
                    if(requested!=null||i+1==args.Length)throw new ArgumentException("Use --language followed by one language code or auto.");
                    requested=args[++i];
                }else remaining.Add(args[i]);
            }
            bool preview=remaining.Count>=2&&remaining[0]=="--render-preview";
            Ui.Initialize(requested,!preview);
            if(remaining.Count!=0&&(!preview||remaining.Count>3))throw new ArgumentException("Unknown setup option.");
            if(!WineHost.Active) {
                object release=Microsoft.Win32.Registry.GetValue(@"HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\NET Framework Setup\NDP\v4\Full","Release",null);
                if(release==null||Convert.ToInt32(release)<528040) {
                    if(MessageBox.Show(Ui.T("Lau Setup requires .NET Framework 4.8. Open Microsoft's official runtime download page?"),Ui.T("Install .NET Framework 4.8"),MessageBoxButtons.YesNo,MessageBoxIcon.Information)==DialogResult.Yes)
                        Process.Start(new ProcessStartInfo("https://dotnet.microsoft.com/en-us/download/dotnet-framework/net48"){UseShellExecute=true});
                    return 2;
                }
            }
            Application.EnableVisualStyles();Application.SetCompatibleTextRenderingDefault(false);var catalog=Catalog.Embedded();
            using(var form=new SetupForm(catalog)) {
                if(preview){form.Preview(Path.GetFullPath(remaining[1]),remaining.Count==3?remaining[2]:"ready");return 0;}
                Application.Run(form);return 0;
            }
        }catch(Exception ex){while(ex is TypeInitializationException&&ex.InnerException!=null)ex=ex.InnerException;MessageBox.Show(Ui.Message(ex.Message),"Lau Setup",MessageBoxButtons.OK,MessageBoxIcon.Error);return 1;}
    }
    }
}
