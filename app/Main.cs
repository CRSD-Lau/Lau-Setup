// Author, Creator, Last Modified By: Neil Mitchell
using System;
using System.IO;
using System.Linq;
using System.Collections.Generic;
using System.Drawing;
using System.Drawing.Drawing2D;
using System.Windows.Forms;
using System.Threading;
using System.Threading.Tasks;
using System.Diagnostics;

namespace LauSetup {
// Windows' default disabled text can turn nearly black on a dark control.
// Keep real Enabled semantics and paint only the disabled appearance ourselves.
public class RoundedPanel:Panel {
    public Color BorderColor=Color.FromArgb(48,70,87);
    public RoundedPanel(){DoubleBuffered=true;}
    protected override void OnPaintBackground(PaintEventArgs e){e.Graphics.Clear(Parent==null?BackColor:Parent.BackColor);e.Graphics.SmoothingMode=SmoothingMode.AntiAlias;using(var path=Shape(new Rectangle(0,0,Width-1,Height-1),10))using(var fill=new SolidBrush(BackColor))e.Graphics.FillPath(fill,path);}
    protected override void OnPaint(PaintEventArgs e){base.OnPaint(e);e.Graphics.SmoothingMode=SmoothingMode.AntiAlias;using(var path=Shape(new Rectangle(0,0,Width-1,Height-1),10))using(var pen=new Pen(BorderColor))e.Graphics.DrawPath(pen,path);}
    internal static GraphicsPath Shape(Rectangle r,int radius){var p=new GraphicsPath();int d=radius*2;p.AddArc(r.Left,r.Top,d,d,180,90);p.AddArc(r.Right-d,r.Top,d,d,270,90);p.AddArc(r.Right-d,r.Bottom-d,d,d,0,90);p.AddArc(r.Left,r.Bottom-d,d,d,90,90);p.CloseFigure();return p;}
}
public sealed class WizardStep:Label {
    public int Number,Current;
    protected override void OnPaint(PaintEventArgs e){
        e.Graphics.Clear(BackColor);e.Graphics.SmoothingMode=SmoothingMode.AntiAlias;
        int diameter=32,y=(Height-diameter)/2;
        var color=Number==Current?Color.FromArgb(223,181,104):Number<Current?Color.FromArgb(97,148,132):Color.FromArgb(36,55,70);
        using(var b=new SolidBrush(color))e.Graphics.FillEllipse(b,0,y,diameter,diameter);
        using(var bold=new Font(Font,FontStyle.Bold))TextRenderer.DrawText(e.Graphics,Number.ToString(),bold,new Rectangle(0,y,diameter,diameter),Number<=Current?BackColor:ForeColor,TextFormatFlags.HorizontalCenter|TextFormatFlags.VerticalCenter|TextFormatFlags.NoPadding|TextFormatFlags.SingleLine);
        int rule=Number<4?Math.Min(60,Width/5):0;
        using(var face=new Font(Font,Number==Current?FontStyle.Bold:FontStyle.Regular))TextRenderer.DrawText(e.Graphics,Text,face,new Rectangle(42,0,Math.Max(1,Width-50-rule),Height),ForeColor,TextFormatFlags.Left|TextFormatFlags.VerticalCenter|TextFormatFlags.WordBreak);
        if(rule>0)using(var pen=new Pen(Color.FromArgb(48,70,87),2))e.Graphics.DrawLine(pen,Width-rule,Height/2,Width-8,Height/2);
    }
}
public sealed class ReadableButton:Button {
    protected override void OnPaint(PaintEventArgs e) {
        e.Graphics.Clear(Parent==null?BackColor:Parent.BackColor);e.Graphics.SmoothingMode=SmoothingMode.AntiAlias;
        Color background=Enabled?BackColor:Color.FromArgb(35,47,64),text=Enabled?ForeColor:Color.FromArgb(196,207,223);
        using(var path=RoundedPanel.Shape(new Rectangle(0,0,Width-1,Height-1),9))using(var fill=new SolidBrush(background))e.Graphics.FillPath(fill,path);
        TextRenderer.DrawText(e.Graphics,Text,Font,ClientRectangle,text,TextFormatFlags.HorizontalCenter|TextFormatFlags.VerticalCenter|TextFormatFlags.EndEllipsis);
        if(Focused&&ShowFocusCues)ControlPaint.DrawFocusRectangle(e.Graphics,new Rectangle(5,5,Width-10,Height-10),text,background);
    }
}
public sealed class ReadableCheckBox:CheckBox {
    protected override void OnPaint(PaintEventArgs e) {

        Color background=Parent==null?BackColor:Parent.BackColor,text=Enabled?ForeColor:Color.FromArgb(196,207,223);
        using(var fill=new SolidBrush(background))e.Graphics.FillRectangle(fill,ClientRectangle);
        int size=Math.Max(24,Font.Height-1),left=2,top=(Height-size)/2;
        using(var fill=new SolidBrush(Checked?Color.FromArgb(223,181,104):Color.FromArgb(11,20,32)))e.Graphics.FillRectangle(fill,left,top,size,size);
        using(var pen=new Pen(Color.FromArgb(154,173,197)))e.Graphics.DrawRectangle(pen,left,top,size,size);
        if(Checked)using(var pen=new Pen(Color.FromArgb(11,20,32),3F))e.Graphics.DrawLines(pen,new[]{new Point(left+3,top+size/2),new Point(left+size/2,top+size-4),new Point(left+size-3,top+3)});
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
    readonly ToolTip folderTip=new ToolTip();
    Label folderPlaceholder;
    readonly Color ink=Color.FromArgb(237,243,247),muted=Color.FromArgb(169,189,204),surface=Color.FromArgb(20,35,50),gold=Color.FromArgb(223,181,104);
    TextBox folder;Label detected,download,status,baseDescription;CheckBox cons,spells,maps,basePatch,executable;Button browse,install,restore,cancel;ProgressBar progress;ComboBox language;
    FlowLayoutPanel[] pages;Label[] stepLabels;Label reviewFolder,reviewChoices,reviewIncluded,reviewWarning;Button back,next;int step;bool navigationBlocked,previewing;
    protected override bool ShowWithoutActivation { get { return previewing; } }
    ClientInfo client;InstallPlan plan;CancellationTokenSource cancellation;bool busy,refreshing,recoveryOnly,choicesDirty;
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
        Ui.Select(choice,persist);SuspendLayout();RefreshUiFont(this,UiFont);TranslateControls(this);UpdateReview();language.Refresh();folder.AccessibleName=Ui.T("Game folder");folderTip.SetToolTip(folder,Ui.T("Choose the folder containing WoW.exe. Do not choose the Data folder."));folderTip.SetToolTip(folderPlaceholder,Ui.T("Choose the folder containing WoW.exe. Do not choose the Data folder."));ResumeLayout(true);
        if(!String.IsNullOrEmpty(Ui.LastPreferenceError))SetText(status,"This language is active for this session, but the preference could not be saved.");
    }
    public SetupForm(Catalog catalog) {
        this.catalog=catalog;Text="Lau Setup";Font=new Font(UiFont,10F);ForeColor=ink;BackColor=Color.FromArgb(11,20,32);MinimumSize=new Size(900,650);ClientSize=new Size(Math.Min(1100,Screen.PrimaryScreen.WorkingArea.Width-40),Math.Min(790,Screen.PrimaryScreen.WorkingArea.Height-80));StartPosition=FormStartPosition.CenterScreen;AutoScaleMode=AutoScaleMode.Dpi;
        using(var icon=typeof(SetupForm).Assembly.GetManifestResourceStream("LauSetup.Icon.ico"))if(icon!=null)Icon=new Icon(icon);
        var grid=new TableLayoutPanel{Dock=DockStyle.Fill,Padding=new Padding(48,22,48,14),ColumnCount=1,RowCount=9};Controls.Add(grid);grid.Paint+=(sender,e)=>{using(var brush=new SolidBrush(gold))e.Graphics.FillRectangle(brush,0,0,grid.Width,5);};
        foreach(int h in new[]{48,32,12,62,1,44,20,80,0})grid.RowStyles.Add(new RowStyle(h==1?SizeType.Percent:SizeType.Absolute,h==1?100:h));
        var header=new TableLayoutPanel{Dock=DockStyle.Fill,ColumnCount=2};header.ColumnStyles.Add(new ColumnStyle(SizeType.Percent,60));header.ColumnStyles.Add(new ColumnStyle(SizeType.Percent,40));header.Controls.Add(Label("LAU SETUP",20,FontStyle.Bold,ink),0,0);grid.Controls.Add(header,0,0);grid.SetRowSpan(header,2);
        header.RowCount=2;header.RowStyles.Add(new RowStyle(SizeType.Percent,65));header.RowStyles.Add(new RowStyle(SizeType.Percent,35));header.Controls.Add(Label("Your existing game. Your choice of visuals.",11,FontStyle.Regular,muted),0,1);
        var languageRow=new TableLayoutPanel{Dock=DockStyle.Fill,ColumnCount=2,Margin=new Padding(0,0,0,8)};
        languageRow.ColumnStyles.Add(new ColumnStyle(SizeType.AutoSize));languageRow.ColumnStyles.Add(new ColumnStyle(SizeType.Percent,100));
        var languageLabel=Label("Interface language",10,FontStyle.Regular,muted);languageLabel.AutoSize=true;languageLabel.Dock=DockStyle.None;languageLabel.Anchor=AnchorStyles.Left;languageLabel.Margin=new Padding(0,0,16,0);languageRow.Controls.Add(languageLabel);
        language=new ComboBox{Name="interfaceLanguage",DropDownStyle=ComboBoxStyle.DropDownList,Anchor=AnchorStyles.Left|AnchorStyles.Right,BackColor=surface,ForeColor=ink,DisplayMember="Name",ValueMember="Code",AccessibleName=Ui.T("Interface language")};
        foreach(var option in Ui.Languages)language.Items.Add(option);
        language.SelectedIndex=Array.FindIndex(Ui.Languages,x=>x.Code==Ui.Choice);if(language.SelectedIndex<0)language.SelectedIndex=0;
        language.SelectedIndexChanged+=(s,e)=>{if(language.SelectedItem!=null){ChangeLanguage(((LanguageOption)language.SelectedItem).Code,true);language.AccessibleName=Ui.T("Interface language");}};
        languageRow.Controls.Add(language);header.Controls.Add(languageRow,1,0);header.SetRowSpan(languageRow,2);languageRow.Padding=new Padding(0);languageRow.RowStyles.Add(new RowStyle(SizeType.Percent,100));
        var steps=new TableLayoutPanel{Dock=DockStyle.Fill,ColumnCount=4,Margin=new Padding(0,0,0,8)};
        stepLabels=new Label[4];var stepNames=new[]{"Game folder","Your visuals","Review","Finished"};for(int n=0;n<4;n++){stepLabels[n]=new WizardStep{Number=n+1,Dock=DockStyle.Fill,Font=new Font(UiFont,11),BackColor=BackColor,ForeColor=muted};SetText(stepLabels[n],stepNames[n]);}
        foreach(var label in stepLabels){steps.ColumnStyles.Add(new ColumnStyle(SizeType.Percent,25));label.Padding=new Padding(9,0,2,0);steps.Controls.Add(label);}grid.Controls.Add(steps,0,3);
        var host=new Panel{Dock=DockStyle.Fill,Margin=new Padding(0)};grid.Controls.Add(host,0,4);
        pages=new FlowLayoutPanel[4];
        for(int i=0;i<pages.Length;i++){
            var page=new FlowLayoutPanel{Dock=DockStyle.Fill,AutoScroll=true,FlowDirection=FlowDirection.TopDown,WrapContents=false,Margin=new Padding(0)};
            page.Resize+=(s,e)=>{foreach(Control c in page.Controls)c.Width=Math.Max(200,page.ClientSize.Width-SystemInformation.VerticalScrollBarWidth-6);};pages[i]=page;host.Controls.Add(page);
        }
        AddPage(0,Label("First, choose your World of Warcraft folder.",23,FontStyle.Bold,ink),60);
        AddPage(0,Label("Setup will check your game and choose the right files for it.",14,FontStyle.Regular,muted),48);
        var row=new TableLayoutPanel{ColumnCount=2,Dock=DockStyle.Fill,Margin=new Padding(0),BackColor=surface};row.ColumnStyles.Add(new ColumnStyle(SizeType.Percent,100));row.ColumnStyles.Add(new ColumnStyle(SizeType.Absolute,216));row.RowCount=1;row.RowStyles.Add(new RowStyle(SizeType.Percent,100));
        var field=new RoundedPanel{Dock=DockStyle.Fill,BackColor=BackColor,Margin=new Padding(0,0,18,0),Padding=new Padding(18,1,18,1)};
        folder=new TextBox{ReadOnly=true,BackColor=BackColor,ForeColor=ink,BorderStyle=BorderStyle.None,Font=new Font(UiFont,14),AccessibleName=Ui.T("Game folder")};
        var placeholder=folderPlaceholder=Label("Choose your game folder to get started",14,FontStyle.Regular,muted);placeholder.Dock=DockStyle.Fill;placeholder.Margin=new Padding(0);field.Controls.Add(folder);field.Controls.Add(placeholder);
        field.Resize+=(sender,e)=>{folder.SetBounds(18,(field.Height-folder.PreferredHeight)/2,Math.Max(1,field.Width-36),folder.PreferredHeight);};
        folder.TextChanged+=(sender,e)=>{placeholder.Visible=String.IsNullOrEmpty(folder.Text);folder.Visible=!placeholder.Visible;};folder.Visible=false;
        folderTip.SetToolTip(placeholder,Ui.T("Choose the folder containing WoW.exe. Do not choose the Data folder."));folderTip.SetToolTip(folder,Ui.T("Choose the folder containing WoW.exe. Do not choose the Data folder."));
        row.Controls.Add(field,0,0);
        browse=Button("Browse...",false);browse.AutoSize=false;browse.Dock=DockStyle.Fill;browse.Margin=new Padding(0);browse.Font=new Font(UiFont,14,FontStyle.Bold);browse.BackColor=Color.FromArgb(36,55,70);browse.Click+=Choose;row.Controls.Add(browse,1,0);
        var folderCard=new RoundedPanel{BackColor=surface,Padding=new Padding(24,20,24,28)};
        var picker=new TableLayoutPanel{Dock=DockStyle.Fill,ColumnCount=1,RowCount=2,Margin=new Padding(0)};picker.RowStyles.Add(new RowStyle(SizeType.Absolute,42));picker.RowStyles.Add(new RowStyle(SizeType.Percent,100));picker.Controls.Add(Label("Where is your game installed?",15,FontStyle.Bold,ink),0,0);picker.Controls.Add(row,0,1);folderCard.Controls.Add(picker);AddPage(0,folderCard,166);
        var help=Label("Not sure which folder?",16,FontStyle.Bold,ink);help.Padding=new Padding(0,22,0,0);AddPage(0,help,64);
        AddPage(0,Label("Choose the folder containing WoW.exe. Do not choose the Data folder.\nClose World of Warcraft before continuing.",14,FontStyle.Regular,muted),64);
        detected=Label("",11,FontStyle.Regular,muted);detected.TextChanged+=(sender,e)=>detected.Visible=!String.IsNullOrEmpty(detected.Text);AddPage(0,detected,44);detected.Visible=false;
        AddPage(1,Label("Choose the look you want.",23,FontStyle.Bold,ink),60);
        basePatch=Check("Patch-Y Non-HD",true);basePatch.Enabled=false;baseDescription=Label("Selected for your detected client. A full HD model pack is not included.",10,FontStyle.Regular,muted);AddOption(basePatch,baseDescription);
        executable=Check("Compatible WoW.exe + loading screens",false);AddOption(executable,Label("Installs the compatible WoW.exe and Lau's loading screens together. Off keeps both unchanged.",10,FontStyle.Regular,muted));
        cons=Check("Enhanced Consecration",false);AddOption(cons,Label("Uses Lau's custom ground effect for Consecration. Turn off for the original appearance.",10,FontStyle.Regular,muted));
        spells=Check("New spell visuals  ·  available with HD models",false);spells.Enabled=false;AddOption(spells,Label("Adds upgraded spell effects. Requires an existing HD model client.",10,FontStyle.Regular,muted));
        maps=Check("Upgrade maps and minimap  ·  optional extra download",false);AddOption(maps,Label("Lau's maps and minimaps plus Trimitor's dungeon, raid and cave maps. Includes WDM support addons. Loading screens are separate.",10,FontStyle.Regular,muted));
        AddPage(2,Label("Review your choices before installing.",23,FontStyle.Bold,ink),70);
        var reviewCard=new RoundedPanel{BackColor=surface,Padding=new Padding(24,12,24,12)};
        var reviewRows=new TableLayoutPanel{Dock=DockStyle.Fill,ColumnCount=1,RowCount=3};foreach(int h in new[]{40,86,100})reviewRows.RowStyles.Add(new RowStyle(SizeType.Absolute,h));reviewCard.Controls.Add(reviewRows);
        reviewFolder=Label("",12,FontStyle.Regular,ink);reviewRows.Controls.Add(reviewFolder);
        reviewChoices=Label("",12,FontStyle.Bold,ink);reviewRows.Controls.Add(reviewChoices);
        reviewIncluded=Label("",11,FontStyle.Regular,muted);reviewRows.Controls.Add(reviewIncluded);AddPage(2,reviewCard,250);
        reviewWarning=Label("",10,FontStyle.Regular,gold);AddPage(2,reviewWarning,90);
        download=Label("Select your folder to see the download size.",12,FontStyle.Bold,gold);AddPage(2,download,45);
        var backupCard=new RoundedPanel{BackColor=Color.FromArgb(26,46,51),Padding=new Padding(24,12,24,12)};
        backupCard.Controls.Add(Label("Setup preserves existing files before replacing or moving them. Keep LauSetupBackups to restore the originals.",12,FontStyle.Regular,muted));AddPage(2,backupCard,100);
        AddPage(3,Label("Your game is ready.",18,FontStyle.Bold,gold),65);
        AddPage(3,Label("Installed and verified. Start WoW, run /pyversion, and test your chosen effects.\nYou can restore the previous install here at any time.",12,FontStyle.Regular,ink),125);
        AddPage(3,Label("Your backup is saved in the selected client’s LauSetupBackups folder.",11,FontStyle.Regular,muted),90);
        status=Label("",10,FontStyle.Regular,ink);status.Padding=new Padding(0,6,0,0);status.AutoSize=true;var statusScroll=new Panel{Dock=DockStyle.Fill,AutoScroll=true,Margin=new Padding(0,6,0,0)};statusScroll.Controls.Add(status);status.Dock=DockStyle.Top;statusScroll.Resize+=(s,e)=>{status.MaximumSize=new Size(Math.Max(100,statusScroll.ClientSize.Width-SystemInformation.VerticalScrollBarWidth),0);};grid.Controls.Add(statusScroll,0,5);
        progress=new ProgressBar{Dock=DockStyle.Fill,Maximum=1000,Visible=false,Margin=new Padding(0,5,0,5)};grid.Controls.Add(progress,0,6);
        var actions=new FlowLayoutPanel{Dock=DockStyle.Fill,FlowDirection=FlowDirection.LeftToRight,WrapContents=false,AutoScroll=false,Margin=new Padding(0,8,0,4)};
        back=Button("Back",false);back.Click+=(s,e)=>{if(!busy&&step>0)ShowStep(step-1);};actions.Controls.Add(back);
        next=Button("Next",true);next.Click+=(s,e)=>Advance();actions.Controls.Add(next);
        install=Button("Install upgrade",true);install.Enabled=false;install.Click+=Install;actions.Controls.Add(install);
        cancel=Button("Cancel",false);cancel.Visible=false;cancel.Click+=(s,e)=>{if(cancellation!=null)cancellation.Cancel();};actions.Controls.Add(cancel);
        restore=Button("Restore previous install",false);restore.Enabled=false;restore.Click+=Restore;actions.Controls.Add(restore);actions.FlowDirection=FlowDirection.RightToLeft;actions.Controls.SetChildIndex(next,0);actions.Controls.SetChildIndex(install,1);actions.Controls.SetChildIndex(back,2);actions.Controls.SetChildIndex(cancel,3);actions.Controls.SetChildIndex(restore,4);var footer=new TableLayoutPanel{Dock=DockStyle.Fill,ColumnCount=2,Margin=new Padding(0),Padding=new Padding(0,12,0,0)};footer.RowCount=1;footer.RowStyles.Add(new RowStyle(SizeType.Percent,100));footer.ColumnStyles.Add(new ColumnStyle(SizeType.Percent,100));footer.ColumnStyles.Add(new ColumnStyle(SizeType.AutoSize));actions.AutoSize=true;footer.Controls.Add(actions,1,0);actions.Margin=new Padding(0);actions.Padding=new Padding(0,8,0,0);footer.Paint+=(sender,e)=>{using(var pen=new Pen(Color.FromArgb(48,70,87)))e.Graphics.DrawLine(pen,0,0,footer.Width,0);};grid.Controls.Add(footer,0,7);
        var release=Label("",9,FontStyle.Regular,muted);SetText(release,"Setup {2}  •  Game {0} Lau  •  {1}  •  Build 12340",catalog.Version,WineHost.Active?"Wine 11 on Linux":"Windows 10 / 11",catalog.InstallerVersion);footer.Controls.Add(release,0,0);footer.Resize+=(sender,e)=>{bool compact=footer.Width<950;foreach(Button action in new[]{back,next,install,cancel,restore}){action.MinimumSize=new Size(action==next||action==install?(compact?180:210):(compact?100:130),52);if(action.Font.Size!=(compact?10F:11F)){var previous=action.Font;action.Font=new Font(UiFont,compact?10F:11F,FontStyle.Bold);previous.Dispose();}}};
        cons.CheckedChanged+=ChoicesChanged;spells.CheckedChanged+=ChoicesChanged;maps.CheckedChanged+=ChoicesChanged;executable.CheckedChanged+=ChoicesChanged;
        FormClosed+=(s,e)=>folderTip.Dispose();
        FormClosing+=(s,e)=>{if(busy){e.Cancel=true;SetText(status,"Please wait for this operation to finish, or use Cancel.");}};
        var stripe=new Panel{Dock=DockStyle.Top,Height=5,BackColor=gold};Controls.Add(stripe);stripe.BringToFront();
        ShowStep(0);
    }
    void AddPage(int index,Control control,int height){control.Dock=DockStyle.None;control.Height=height;control.Width=900;control.Margin=new Padding(0,0,0,6);pages[index].Controls.Add(control);}
    void AddOption(CheckBox check,Label note){
        var card=new RoundedPanel{BackColor=surface,Padding=new Padding(22,6,16,7)};check.Dock=DockStyle.Top;check.Height=40;check.Font=new Font(UiFont,13,FontStyle.Bold);
        note.Font=new Font(UiFont,11);note.Dock=DockStyle.Fill;note.Padding=new Padding(34,0,0,0);card.Controls.Add(note);card.Controls.Add(check);check.CheckedChanged+=(s,e)=>{card.BorderColor=check.Checked?gold:Color.FromArgb(48,70,87);card.Invalidate();};card.BorderColor=check.Checked?gold:Color.FromArgb(48,70,87);AddPage(1,card,88);
        Action fit=()=>{int width=Math.Max(160,card.ClientSize.Width-card.Padding.Horizontal);int titleHeight=Math.Max(40,TextRenderer.MeasureText(check.Text,check.Font,new Size(width-40,0),TextFormatFlags.WordBreak).Height+8);int noteHeight=TextRenderer.MeasureText(note.Text,note.Font,new Size(width-34,0),TextFormatFlags.WordBreak).Height+8;check.Height=titleHeight;int height=Math.Max(88,card.Padding.Vertical+titleHeight+noteHeight);if(card.Height!=height)card.Height=height;};card.Resize+=(sender,e)=>fit();check.TextChanged+=(sender,e)=>fit();note.TextChanged+=(sender,e)=>fit();fit();
    }
    void UpdateReview(){
        SetText(reviewFolder,"Folder: {0}",folder.Text);
        SetText(reviewIncluded,"Patch-Y and matching language patches: {0}\nWoW.exe: {1}\nLoading screens and artwork (Patch-Q): {2}",client==null?Language("enUS"):Language(client.Locale),Phrase(executable.Checked?"Install":"Keep existing"),Phrase(executable.Checked?"Install":"Keep existing"));
        reviewWarning.Visible=plan!=null&&plan.Warnings.Count>0;if(reviewWarning.Visible)SetText(reviewWarning,"Unrecognized Patch-V kept in Data. Compatibility could not be verified. You can continue installing; this file will not be changed.");
        var choices=new List<string>{Ui.T("Patch-Y (Lau’s version)")};if(cons.Checked)choices.Add(Ui.T("Enhanced Consecration"));if(spells.Checked)choices.Add(Ui.T("New Spells"));if(maps.Checked)choices.Add(Ui.T("Map Upgrade"));if(executable.Checked)choices.Add(Ui.T("Compatible WoW.exe + loading screens"));SetText(reviewChoices,"Your choices: {0}",String.Join(" + ",choices));
    }
    void ShowStep(int value){
        step=value;for(int i=0;i<pages.Length;i++){pages[i].Visible=i==step;((WizardStep)stepLabels[i]).Current=step+1;stepLabels[i].ForeColor=i==step?ink:muted;stepLabels[i].Invalidate();}pages[step].BringToFront();UpdateReview();UpdateNavigation();
    }
    void ChoicesChanged(object sender,EventArgs args){if(refreshing||busy)return;choicesDirty=true;UpdateReview();}
    async void Advance(){
        if(busy)return;
        if(step==3||(step==2&&plan!=null&&plan.Operations.Count==0)){Close();return;}
        if(client==null||recoveryOnly||navigationBlocked||plan==null)return;
        if(step==1&&choicesDirty){await PreparePlan();if(plan==null)return;}
        if(step<2)ShowStep(step+1);
    }
    void UpdateNavigation(){
        if(pages==null||next==null)return;
        back.Visible=step==1||step==2;back.Enabled=!busy;
        next.Visible=!busy&&(step<2||step==3||(step==2&&plan!=null&&plan.Operations.Count==0));
        next.Enabled=!busy&&(step==3||(client!=null&&!recoveryOnly&&!navigationBlocked&&plan!=null));SetText(next,step>=2?"Finish":"Next");
        install.Visible=step==2&&!busy&&(plan==null||plan.Operations.Count>0);
        install.Enabled=!busy&&step==2&&!recoveryOnly&&!navigationBlocked&&plan!=null&&plan.Operations.Count>0;
        AcceptButton=install.Visible&&install.Enabled?install:next.Visible&&next.Enabled?next:null;
    }
    Label Label(string text,float size,FontStyle style,Color color) { var label=new Label{Font=new Font(UiFont,size,style),ForeColor=color,Dock=DockStyle.Fill,AutoEllipsis=false,Margin=new Padding(0),TextAlign=ContentAlignment.MiddleLeft};SetText(label,text);return label; }
    Button Button(string text,bool primary) { var b=new ReadableButton{Height=52,AutoSize=true,AutoSizeMode=AutoSizeMode.GrowAndShrink,MinimumSize=new Size(primary?210:130,52),Padding=new Padding(12,0,12,0),FlatStyle=FlatStyle.Flat,BackColor=primary?gold:surface,ForeColor=primary?Color.FromArgb(12,20,33):ink,Cursor=Cursors.Hand,Margin=new Padding(0,0,10,0),Font=new Font(UiFont,11,FontStyle.Bold)};b.FlatAppearance.BorderColor=primary?gold:Color.FromArgb(114,133,157);SetText(b,text);return b; }
    CheckBox Check(string text,bool check) { var box=new ReadableCheckBox{Checked=check,Dock=DockStyle.Fill,AutoSize=false,Margin=new Padding(0),Padding=new Padding(0,2,0,2),ForeColor=ink};SetText(box,text);return box; }
    async void Choose(object sender,EventArgs args) {
        using(var dialog=new FolderBrowserDialog{Description=Ui.T("Setup will check your game and choose the right files for it."),ShowNewFolderButton=false,SelectedPath=client==null?"":client.Root}) {
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
        client=await Task.Run(()=>Client.Inspect(root,catalog));UpdateClientDisplay();refreshing=true;cons.Checked=false;spells.Checked=false;refreshing=false;
        SetText(status,"Ready. A verified backup is created before any game files change.");
    }
    void UpdateClientDisplay(){
        SetText(baseDescription,client.Hd?"Your client has HD models active. The appropriate Patch-Y HD version will be installed.":"Your client does not have HD models active. The appropriate Patch-Y Non-HD version will be installed.");
        folder.Text=client.Root;SetText(basePatch,client.Hd?"Patch-Y HD":"Patch-Y Non-HD");SetText(maps,client.MapsInstalled?"Map Upgrade — already installed, kept":"Upgrade maps and minimap  ·  optional extra download");refreshing=true;spells.Checked=false;maps.Checked=client.MapsInstalled;refreshing=false;
        SetText(detected,"{0}  ·  {1}  ·  Build 12340",Language(client.Locale),client.Hd?Phrase("HD models detected"):Phrase("Original models detected"));
    }
    void UpdatePlanDisplay(){SetText(install,"Install upgrade");if(plan.Operations.Count==0)SetText(download,"Your selected release {0} is already installed.",catalog.Version);else SetText(download,"Download up to {0}  ·  {1}",FormatSize(plan.DownloadBytes),plan.Maps?Phrase("Upgraded maps included"):Phrase("Existing maps kept"));}
    async void RefreshPlan(object sender,EventArgs args) {await PreparePlan();}
    async Task PreparePlan() {
        if(refreshing||busy||client==null||recoveryOnly)return;SetBusy(true);progress.Visible=true;progress.Style=ProgressBarStyle.Marquee;SetText(status,"Checking installed files…");
        try {
            bool newSpells=spells.Checked,consecration=cons.Checked,includeMaps=maps.Checked,includeExecutable=executable.Checked,includeArtwork=executable.Checked;
            plan=await Task.Run(()=>InstallPlan.Build(client,catalog,newSpells,consecration,includeMaps,default(CancellationToken),includeExecutable,includeArtwork));
            choicesDirty=false;UpdatePlanDisplay();
            SetText(status,Transaction.Pending(client.Root)!=null?"An interrupted install was found. Restore it before continuing.":(!newSpells?"Patch-S becomes .mpq.disabled. Any older disabled copy is preserved separately. Restore previous install reverses the change.":"Ready. A verified backup is created before any game files change."));
            if(Transaction.Pending(client.Root)==null&&plan.Operations.Any(o=>o.ExtraPatch))SetText(status,"{0} extra upgrade patches will be backed up automatically in LauSetupBackups. Click Install upgrade to continue.",plan.Operations.Count(o=>o.ExtraPatch));
        }catch(Exception ex){plan=null;SetMessage(status,ex.Message);}finally{progress.Style=ProgressBarStyle.Continuous;progress.Visible=false;SetBusy(false);}
    }
    async void Install(object sender,EventArgs args) {
        if(plan==null||client==null||busy||step!=2)return;SetBusy(true);cancellation=new CancellationTokenSource();cancel.Visible=true;progress.Visible=true;progress.Value=0;
        try {
            Client.AssertClosed(client.Root);
            var current=plan;string state=Transaction.StateRoot(client.Root),cache=SafePaths.Under(state,"cache");
            long done=0;var lastTransfer=System.Diagnostics.Stopwatch.StartNew();
            var transfer=new Progress<TransferProgress>(p=>{if(IsDisposed)return;SetText(status,"Downloading {0}  ·  {1} / {2}",Phrase(Friendly(p.Name)),FormatSize(p.Received),FormatSize(p.Total));progress.Value=Math.Max(progress.Value,Math.Min(700,(int)(p.Overall*700.0/Math.Max(1,current.DownloadBytes))));});
            var messages=new Progress<string>(s=>SetMessage(status,s));
            var installation=new Progress<int>(n=>{if(!IsDisposed)progress.Value=Math.Max(progress.Value,700+Math.Max(0,Math.Min(299,n*299/100)));});
            await Task.Run(()=>{
                using(var lease=ClientLease.Acquire(current.Root)){
                if(Transaction.Pending(current.Root)!=null)throw new IOException("An interrupted install needs restoring first.");
                MpqScan.ValidatePlan(current,catalog,cancellation.Token);
                var files=new Dictionary<string,string>();var loader=new Downloader(cache,Path.Combine(AppDomain.CurrentDomain.BaseDirectory,"payload"),p=>{p.Overall=done+p.Received;if(lastTransfer.ElapsedMilliseconds>=100||p.Received==p.Total){lastTransfer.Restart();((IProgress<TransferProgress>)transfer).Report(p);}});
                foreach(var id in current.Operations.Where(o=>o.AssetId!=null&&o.SourceRelative==null).Select(o=>o.AssetId).Distinct()) {
                    cancellation.Token.ThrowIfCancellationRequested();
                    files[id]=loader.Fetch(catalog.Get(id),cancellation.Token);done+=catalog.Get(id).Bytes;
                }
                ((IProgress<string>)messages).Report(Ui.T("Checking installed files…"));
                var transaction=new Transaction(catalog,s=>((IProgress<string>)messages).Report(s),null);transaction.Progress=n=>((IProgress<int>)installation).Report(n);transaction.InstallWithLease(current,files,cancellation.Token,lease);
                }
            });
            client=await Task.Run(()=>Client.Inspect(client.Root,catalog));UpdateClientDisplay();
            progress.Value=1000;SetText(status,"Installed and verified. Start WoW, run /pyversion, and test your chosen effects.\nYou can restore the previous install here at any time.");
            plan=null;SetText(download,"Your backup is saved in the selected client’s LauSetupBackups folder.");ShowStep(3);
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
        SetBusy(true);plan=null;SetText(status,"Restoring your previous install…");
        try{await Task.Run(()=>new Transaction(catalog,null,null).Restore(record));client=await Task.Run(()=>Client.Inspect(client.Root,catalog));recoveryOnly=false;UpdateClientDisplay();ShowStep(0);SetText(status,"Previous install restored and verified.");bool newSpells=spells.Checked,consecration=cons.Checked,includeMaps=maps.Checked,includeExecutable=executable.Checked,includeArtwork=executable.Checked;plan=await Task.Run(()=>InstallPlan.Build(client,catalog,newSpells,consecration,includeMaps,default(CancellationToken),includeExecutable,includeArtwork));UpdatePlanDisplay();ShowStep(0);}
        catch(Exception ex){SetMessage(status,ex.Message);}finally{SetBusy(false);}
    }
    void SetBusy(bool value) {
        busy=value;executable.Enabled=!value&&!recoveryOnly;language.Enabled=true;browse.Enabled=!value;cons.Enabled=!value&&!recoveryOnly;spells.Enabled=!value&&!recoveryOnly&&client!=null&&client.Hd;maps.Enabled=!value&&!recoveryOnly&&client!=null&&!client.MapsInstalled;restore.Enabled=false;navigationBlocked=false;
        if(!value&&client!=null)try{restore.Enabled=Transaction.Journals(client.Root).Any(f=>new[]{"STAGING","COMMITTING","RESTORING","RECOVERY_REQUIRED","INSTALLED"}.Contains(Transaction.Status(f)));navigationBlocked=Transaction.Pending(client.Root)!=null;}catch(Exception ex){navigationBlocked=true;SetMessage(status,ex.Message);}
        UpdateReview();UpdateNavigation();
    }
    internal void Preview(string output,string state="ready") {
        previewing=true;
        if(state.StartsWith("small-",StringComparison.Ordinal)){Size=MinimumSize;state=state.Substring(6);}
        if(state!="initial"){
            SetText(basePatch,"Patch-Y HD");SetText(baseDescription,"Your client has HD models active. The appropriate Patch-Y HD version will be installed.");folder.Text=@"D:\Games\World of Warcraft";SetText(detected,"{0}  ·  {1}  ·  Build 12340",Language("enUS"),Phrase("HD models detected"));spells.Checked=state!="options";spells.Enabled=true;
            SetText(download,"Download up to {0}  ·  {1}","472.4 MB",Phrase("Existing maps kept"));SetText(status,"Ready. A verified backup is created before any game files change.");install.Enabled=true;
        }
        if(state=="busy"){SetBusy(true);cancel.Visible=true;progress.Visible=true;progress.Value=420;SetText(status,"Downloading {0}  ·  {1} / {2}",Phrase("spell visuals"),"84.0 MB","200.0 MB");}
        if(state=="recovery"){SetText(detected,"{0}  ·  Interrupted installation found",Language("enUS"));SetText(status,"Click Restore previous install to recover your game files.");install.Enabled=false;restore.Enabled=true;}
        if(state=="error")SetMessage(status,@"Cannot safely check patch: Data\patch-test.mpq. No game files changed. Check this archive before retrying. Unsupported MPQ table layout.");
        if(state=="conflicts")SetText(status,"{0} extra upgrade patches will be backed up automatically in LauSetupBackups. Click Install upgrade to continue.",3);
        if(state=="patch-v")plan=new InstallPlan{Warnings=new List<string>{@"Data\patch-v.mpq"}};
        ShowStep(state=="initial"||state=="recovery"||state=="error"?0:state=="options"?1:state=="finished"?3:2);
        if(state!="initial"){next.Enabled=state!="busy"&&state!="recovery";install.Enabled=step==2&&state!="busy";restore.Enabled=state=="recovery"||state=="finished";}
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
    static void CollectPreview(Control parent,List<object> controls){foreach(Control c in parent.Controls){if(c.Visible&&(c is Label||c is Button||c is CheckBox||c is ComboBox||c is TextBox)){var measured=TextRenderer.MeasureText(c.Text,c.Font,new Size(Math.Max(1,c.ClientSize.Width-c.Padding.Horizontal),Int32.MaxValue),TextFormatFlags.WordBreak|TextFormatFlags.NoPrefix);controls.Add(new{Type=c.GetType().Name,c.Text,c.Width,c.Height,c.Top,c.Left,ParentHeight=c.Parent.ClientSize.Height,ParentWidth=c.Parent.ClientSize.Width,TextHeight=measured.Height,Scrollable=c.Parent is Panel&&((Panel)c.Parent).AutoScroll});}CollectPreview(c,controls);}}
    public static string FormatSize(long bytes){return bytes>=1000000000?(bytes/1000000000.0).ToString("0.00")+" GB":(bytes/1000000.0).ToString("0.0")+" MB";}
    public static string Language(string locale){switch(locale){case "enUS":return "English (US)";case "deDE":return "Deutsch";case "frFR":return "Français";case "esES":return "Español (España)";case "esMX":return "Español (México)";case "koKR":return "한국어";case "ruRU":return "Русский";case "zhCN":return "简体中文";case "zhTW":return "繁體中文";default:return locale;}}
    static string Friendly(string id){return id=="Maps"||id.StartsWith("MapDetails-")||id.StartsWith("MapAddon-")?"maps and minimap":id.StartsWith("Y-")?"spell indicators":id.Contains("Q-")?"loading screens and regional artwork":id=="Executable"?"the compatible game executable":"spell visuals";}
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
