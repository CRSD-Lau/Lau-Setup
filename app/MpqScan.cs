// Author, Creator, Last Modified By: Neil Mitchell
using System;
using System.IO;
using System.Linq;
using System.Collections.Generic;
using System.Diagnostics;
using System.Threading;

namespace LauSetup {
public sealed class PatchConflict { public string Relative,Sha256;public long Bytes; }
// Deliberately limited to classic MPQ hash tables. No extraction, native code,
// decompression, archive writes or inference from generic shared DBC filenames.
public static class MpqScan {
    static readonly uint[] crypt=CryptTable();
    static uint[] CryptTable(){var t=new uint[1280];uint s=0x100001;for(int i=0;i<256;i++)for(int j=0;j<5;j++){s=(s*125+3)%0x2AAAAB;uint a=(s&65535)<<16;s=(s*125+3)%0x2AAAAB;t[i+j*256]=a|(s&65535);}return t;}
    internal static uint NameHash(string name,int kind){unchecked{uint a=0x7FED7FED,b=0xEEEEEEEE;foreach(char c in name.ToUpperInvariant()){if(c>127)throw new InvalidDataException("Non-ASCII probe");a=crypt[kind*256+c]^(a+b);b=c+a+b+(b<<5)+3;}return a;}}
    static void Decode(byte[] bytes,ref uint a,ref uint b){unchecked{for(int i=0;i<bytes.Length;i+=4){b+=crypt[1024+(a&255)];uint value=BitConverter.ToUInt32(bytes,i)^(a+b);bytes[i]=(byte)value;bytes[i+1]=(byte)(value>>8);bytes[i+2]=(byte)(value>>16);bytes[i+3]=(byte)(value>>24);a=((~a<<21)+0x11111111)|(a>>11);b=value+b+(b<<5)+3;}}}
    internal static byte[] Decode(byte[] bytes){uint a=NameHash("(hash table)",3),b=0xEEEEEEEE;Decode(bytes,ref a,ref b);return bytes;}
    static ulong MarkerHash(string name){return ((ulong)NameHash(name,1)<<32)|NameHash(name,2);}
    static void Budget(Stopwatch watch,CancellationToken token){token.ThrowIfCancellationRequested();if(watch.ElapsedMilliseconds>60000)throw new IOException("Patch conflict scan exceeded one minute. No game files changed; check the selected drive and retry.");}
    internal static bool HasMarkers(string path,Stopwatch watch,CancellationToken token){
        SafePaths.Plain(path);
        using(var stream=new FileStream(path,FileMode.Open,FileAccess.Read,FileShare.Read))return HasMarkers(stream,watch,token);
    }
    static bool HasMarkers(Stream stream,Stopwatch watch,CancellationToken token){
        using(var reader=new BinaryReader(stream,System.Text.Encoding.UTF8,true)){
            long start=-1;
            for(long at=0;at+32<=stream.Length&&at<=1024*1024;at+=512){Budget(watch,token);stream.Position=at;if(reader.ReadUInt32()==0x1A51504D){start=at;break;}}
            if(start<0)throw new InvalidDataException("No supported MPQ header.");
            stream.Position=start+4;uint header=reader.ReadUInt32();reader.ReadUInt32();ushort version=reader.ReadUInt16();reader.ReadUInt16();uint table=reader.ReadUInt32();reader.ReadUInt32();uint count=reader.ReadUInt32(),blocks=reader.ReadUInt32();
            if(version>1||header<(version==0?32:44)||header>4096||count==0||(count&(count-1))!=0)throw new InvalidDataException("Unsupported MPQ table layout.");
            ulong position=table;
            if(version==1){if(start+44>stream.Length)throw new InvalidDataException("Truncated MPQ header.");stream.Position=start+40;position|=(ulong)reader.ReadUInt16()<<32;}
            long length=(long)count*16;
            if(position<(ulong)header||position>(ulong)stream.Length||start+(long)position>stream.Length-length)throw new InvalidDataException("Invalid MPQ hash table bounds.");
            // Stream encrypted entries with continuous cipher state. Memory use is
            // independent of archive table size; inspect every entry even after a match.
            var probes=new[]{MarkerHash(@"Interface\AddOns\!PYAndre\!PYAndre.toc"),MarkerHash(@"Spells\PW_HalionMeteor_Ground.m2"),MarkerHash(@"Spells\PW_Coldflame_Ground.m2"),MarkerHash(@"Spells\PW_Rotface_SlimeSpray_Fan25_Room.m2")};
            var found=new bool[probes.Length];uint key=NameHash("(hash table)",3),seed=0xEEEEEEEE;
            stream.Position=start+(long)position;
            for(long remaining=length;remaining>0;){
                Budget(watch,token);int take=(int)Math.Min(65536L,remaining);byte[] data=reader.ReadBytes(take);
                if(data.Length!=take)throw new InvalidDataException("Truncated MPQ hash table.");Decode(data,ref key,ref seed);
                for(int i=0;i<data.Length;i+=16){uint block=BitConverter.ToUInt32(data,i+12);if(block>=0xFFFFFFFE)continue;if(block>=blocks)throw new InvalidDataException("Invalid MPQ member index.");ulong hash=((ulong)BitConverter.ToUInt32(data,i)<<32)|BitConverter.ToUInt32(data,i+4);for(int p=0;p<probes.Length;p++)if(hash==probes[p])found[p]=true;}
                remaining-=take;
            }
            Budget(watch,token);return found[0]||found.Skip(1).Count(value=>value)>=2;
        }
    }
    // Only an empty Patch-V is retired. Nonempty files are never classified.
    internal static bool IsRetiredPatch(string relative){return relative.Equals(@"Data\patch-v.mpq",StringComparison.OrdinalIgnoreCase);}
    public static void Check(string root,string locale,Catalog catalog,CancellationToken token){Find(root,locale,catalog,token);}
    public static List<PatchConflict> Find(string root,string locale,Catalog catalog,CancellationToken token,List<string> warnings=null){
        root=SafePaths.Root(root);token.ThrowIfCancellationRequested();
        var conflicts=new List<PatchConflict>();
        // Do not inspect or classify unrelated MPQs. Keep the explicitly requested
        // empty-V cleanup; nonempty V is preserved without parsing its contents.
        string dir=SafePaths.Under(root,"Data");SafePaths.Plain(dir);
        if(!Directory.Exists(dir))return conflicts;
        foreach(string path in Directory.EnumerateFiles(dir)){
            token.ThrowIfCancellationRequested();
            if(!Path.GetFileName(path).Equals("patch-v.mpq",StringComparison.OrdinalIgnoreCase))continue;
            string relative=@"Data\"+Path.GetFileName(path);
            SafePaths.Plain(path);
            if(new FileInfo(path).Length!=0){if(warnings!=null)warnings.Add(relative);continue;}
            using(var stream=new FileStream(path,FileMode.Open,FileAccess.Read,FileShare.Read)){
                if(stream.Length!=0)throw new IOException("Game files changed while downloading. No install was applied.");
                conflicts.Add(new PatchConflict{Relative=relative,Bytes=0,Sha256=TimedHash(stream,Stopwatch.StartNew(),token)});
            }
        }
        return conflicts;
    }
    internal static bool KnownHash(string hash,long bytes,Catalog catalog){return releasedArchiveHashes.Contains(hash)||catalog.Assets.Values.Any(a=>a.Id!="Executable"&&a.Bytes==bytes&&a.Sha256.Equals(hash,StringComparison.OrdinalIgnoreCase));}
    internal static PatchConflict Identify(string path,Catalog catalog,Stopwatch watch,CancellationToken token){
        SafePaths.Plain(path);
        using(var stream=new FileStream(path,FileMode.Open,FileAccess.Read,FileShare.Read)){
            long bytes=stream.Length;string hash=null;
            // Classification and fingerprint use this same non-write-sharing handle.
            if(catalog.Assets.Values.Any(a=>a.Id!="Executable"&&a.Bytes==bytes))hash=TimedHash(stream,watch,token);
            bool known=hash!=null&&KnownHash(hash,bytes,catalog);
            if(!known&&!HasMarkers(stream,watch,token))return null;
            if(hash==null)hash=TimedHash(stream,watch,token);
            return new PatchConflict{Sha256=hash,Bytes=bytes};
        }
    }
    internal static void VerifyOriginal(string path,string hash,long bytes,Catalog catalog,bool retired=false){
        if(!Hash.Matches(path,hash,bytes))throw new IOException("An original backup has changed: "+path);
        if(!(retired&&bytes==0)&&!KnownHash(hash,bytes,catalog)&&!HasMarkers(path,Stopwatch.StartNew(),CancellationToken.None))throw new IOException("Invalid backup entry.");
    }
    public static void ValidatePlan(InstallPlan plan,Catalog catalog,CancellationToken token){
        var actual=Find(plan.Root,plan.Locale,catalog,token);var expected=plan.Operations.Where(o=>o.ExtraPatch).ToArray();
        if(actual.Count!=expected.Length||actual.Any(a=>!expected.Any(e=>e.Relative.Equals(a.Relative,StringComparison.OrdinalIgnoreCase)&&e.Existed&&e.OldHash==a.Sha256&&e.OldBytes==a.Bytes)))throw new IOException("Game files changed while downloading. No install was applied.");
    }
    static string TimedHash(Stream f,Stopwatch watch,CancellationToken token){f.Position=0;using(var sha=System.Security.Cryptography.SHA256.Create()){byte[] b=new byte[1024*1024];int n;while((n=f.Read(b,0,b.Length))>0){Budget(watch,token);sha.TransformBlock(b,0,n,b,0);}sha.TransformFinalBlock(b,0,0);return BitConverter.ToString(sha.Hash).Replace("-","").ToLowerInvariant();}}
    // Append-only published MPQ fingerprints for recovery across catalog upgrades.
    // Game 3.0.8 / Setup 1.2.1 catalog; never replace old entries when adding a release.
    static readonly HashSet<string> releasedArchiveHashes=new HashSet<string>(StringComparer.OrdinalIgnoreCase){
        "0a7f2eef34085785b72f1d18b83108c25dac2c2deada412738182fee5e738a80",
        "0d307cabbeb874e481ecf92b3f44a3f4fa1f8eee0e6f2741ed4b871e3b6cb567",
        "177445dee261bf6bea06fd8ca8cf1398b64c231ee26878329ff8faebfb1bce17",
        "17ff68d574e559741663dcb93dcaa34ee1439135fe05f2476bab7dd4650ecf47",
        "187ae741e7c364830834cd782b32ea7153caad2b804918ff44227c9af923c237",
        "270afe55b5d517ea4f0b976437b00c663da5bee52d9fb7f9969a5042e8d3fd8e",
        "2941cbbf61bebcabd2e0ff51361268447e7b6739fafef7da175b2a31662991a3",
        "2eb1fde5691cc1e5dcfa9b45e4a2b50ed302b8afe619fe9dffd030854c6f8a8c",
        "4ae311c9eef3158f6c9f8a6840cf7ad340be9fa9279f8fcc893a599f9dcb524d",
        "4c24eca61f60ab4fe8f6df3e862bdb2c1a0f59d0cc11434ec36fd64fb50daff2",
        "508020eb056d73597d0d64fed17662018cbbe7236a401623b2088b051664d9f2",
        "5f675980f93440e3e8a333c1874ac09dad4e17a6e46a168c4151bf4b88423a4a",
        "6cc47ec31ac489149577d491aa3e2baa42d0894af6786616a40d4a5813720f4a",
        "6dd53dd139ae0f05e0eff1133819da84c683f2a280bc634ee019a288efe48ada",
        "773747e64d3c09f94b813d58d858c54e889000e2000f3f131531533e9620d7a4",
        "89c8018a293a72380a51c826f908503f7d61313c5249162f815035d551852a0d",
        "962577c0d1206222fb581a8bfe38077e2b7fdd9211ec9c810ef6560d0241360a",
        "b14e0f8f3729e19807baeb9a217990a5f2bb869c20e9a4ef6de603e0ba66659f",
        "d477b60836c37ccfabefc8186b0745484cefdcee74b3c6ba768fdcba9c59312e",
        "e841709e455f70dd3255a691b337b28ecf1761fef8e758570db4038ba7a2d062",
        "ec6f91ceea7bdbc7e5d0b51d566a9f5d59ccc8387bf00ac2ab7069be16096eb5"
    };
}
}
