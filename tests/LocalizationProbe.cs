// Author, Creator, Last Modified By: Neil Mitchell
using System;
using System.IO;
using System.Windows.Forms;

public static class LocalizationProbe {
    [STAThread] public static int Main(string[] args) {
        Application.EnableVisualStyles();Application.SetCompatibleTextRenderingDefault(false);
        string work=args.Length==1?Path.GetFullPath(args[0]):Path.Combine(Path.GetTempPath(),"lau-localization-"+Guid.NewGuid().ToString("N"));
        Directory.CreateDirectory(work);
        try { LocalizationTests.Run(work);Console.WriteLine("LOCALIZATION_PASS "+work);return 0; }
        catch(Exception ex){Console.Error.WriteLine(ex);return 1;}
    }
}
