// Author, Creator, Last Modified By: Neil Mitchell
using System;
using System.IO;
using System.Linq;
using System.Collections.Generic;
using System.Diagnostics;
using System.Threading;

namespace LauSetup {
// Deliberately limited to classic MPQ hash tables. No extraction, native code,
// decompression, archive writes or inference from generic shared DBC filenames.
public static class MpqScan {
    static readonly uint[] crypt=CryptTable();
    static uint[] CryptTable(){var t=new uint[1280];uint s=0x100001;for(int i=0;i<256;i++)for(int j=0;j<5;j++){s=(s*125+3)%0x2AAAAB;uint a=(s&65535)<<16;s=(s*125+3)%0x2AAAAB;t[i+j*256]=a|(s&65535);}return t;}
    internal static uint NameHash(string name,int kind){unchecked{uint a=0x7FED7FED,b=0xEEEEEEEE;foreach(char c in name.ToUpperInvariant()){if(c>127)throw new InvalidDataException("Non-ASCII probe");a=crypt[kind*256+c]^(a+b);b=c+a+b+(b<<5)+3;}return a;}}
    internal static byte[] Decode(byte[] bytes){unchecked{uint a=NameHash("(hash table)",3),b=0xEEEEEEEE;for(int i=0;i<bytes.Length;i+=4){b+=crypt[1024+(a&255)];uint value=BitConverter.ToUInt32(bytes,i)^(a+b);Buffer.BlockCopy(BitConverter.GetBytes(value),0,bytes,i,4);a=((~a<<21)+0x11111111)|(a>>11);b=value+b+(b<<5)+3;}return bytes;}}
    static void Budget(Stopwatch watch,CancellationToken token){token.ThrowIfCancellationRequested();if(watch.ElapsedMilliseconds>60000)throw new IOException("Patch conflict scan exceeded one minute. No game files changed; check the selected drive and retry.");}
    internal static bool HasMarkers(string path,Stopwatch watch,CancellationToken token){
        SafePaths.Plain(path);
        using(var stream=new FileStream(path,FileMode.Open,FileAccess.Read,FileShare.Read))using(var reader=new BinaryReader(stream)){
            long start=-1;
            for(long at=0;at+32<=stream.Length&&at<=1024*1024;at+=512){Budget(watch,token);stream.Position=at;if(reader.ReadUInt32()==0x1A51504D){start=at;break;}}
            if(start<0)throw new InvalidDataException("No supported MPQ header.");
            stream.Position=start+4;uint header=reader.ReadUInt32();reader.ReadUInt32();ushort version=reader.ReadUInt16();reader.ReadUInt16();uint table=reader.ReadUInt32();reader.ReadUInt32();uint count=reader.ReadUInt32(),blocks=reader.ReadUInt32();
            if(version>1||header<(version==0?32:44)||header>4096||count==0||count>262144||(count&(count-1))!=0)throw new InvalidDataException("Unsupported MPQ table layout.");
            ulong position=table;
            if(version==1){if(start+44>stream.Length)throw new InvalidDataException("Truncated MPQ header.");stream.Position=start+40;position|=(ulong)reader.ReadUInt16()<<32;}
            long length=(long)count*16;
            if(position<(ulong)header||position>(ulong)stream.Length||start+(long)position>stream.Length-length)throw new InvalidDataException("Invalid MPQ hash table bounds.");
            stream.Position=start+(long)position;byte[] data=reader.ReadBytes((int)length);if(data.Length!=length)throw new InvalidDataException("Truncated MPQ hash table.");Decode(data);
            var entries=new HashSet<ulong>();
            for(int i=0;i<data.Length;i+=16){if((i&16383)==0)Budget(watch,token);uint block=BitConverter.ToUInt32(data,i+12);if(block>=0xFFFFFFFE)continue;if(block>=blocks)throw new InvalidDataException("Invalid MPQ member index.");entries.Add(((ulong)BitConverter.ToUInt32(data,i)<<32)|BitConverter.ToUInt32(data,i+4));}
            Func<string,bool> has=n=>entries.Contains(((ulong)NameHash(n,1)<<32)|NameHash(n,2));
            bool addon=has(@"Interface\AddOns\!PYAndre\!PYAndre.toc");
            int models=new[]{@"Spells\PW_HalionMeteor_Ground.m2",@"Spells\PW_Coldflame_Ground.m2",@"Spells\PW_Rotface_SlimeSpray_Fan25_Room.m2"}.Count(has);
            return addon||models>=2;
        }
    }
    public static void Check(string root,string locale,Catalog catalog,CancellationToken token){
        root=SafePaths.Root(root);var watch=Stopwatch.StartNew();int count=0;
        var expected=new HashSet<string>(StringComparer.OrdinalIgnoreCase);
        foreach(char c in "qmsy"){expected.Add(@"Data\patch-"+c+".mpq");expected.Add(@"Data\"+locale+@"\patch-"+locale+"-"+c+".mpq");}
        var known=catalog.Assets.Values.Where(a=>a.Id!="Executable").GroupBy(a=>a.Bytes).ToDictionary(g=>g.Key,g=>new HashSet<string>(g.Select(a=>a.Sha256),StringComparer.OrdinalIgnoreCase));
        foreach(string relativeDir in new[]{"Data",@"Data\"+locale}){
            string dir=SafePaths.Under(root,relativeDir);SafePaths.Plain(dir);if(!Directory.Exists(dir))continue;
            foreach(string path in Directory.EnumerateFiles(dir)){
                Budget(watch,token);if(!Path.GetExtension(path).Equals(".mpq",StringComparison.OrdinalIgnoreCase))continue;
                string relative=relativeDir+"\\"+Path.GetFileName(path);if(expected.Contains(relative))continue;
                if(++count>2048)throw new IOException("Too many MPQ files to scan safely. No game files changed.");
                try{
                    SafePaths.Plain(path);
                    HashSet<string> matches;
                    if(known.TryGetValue(new FileInfo(path).Length,out matches)&&matches.Contains(TimedHash(path,watch,token)))throw new ConflictException();
                    if(HasMarkers(path,watch,token))throw new ConflictException();
                }catch(ConflictException){throw new IOException("Possible renamed upgrade patch: "+relative+". Keep a backup and move this copy outside Data before retrying. Setup will not delete it.");}
                catch(OperationCanceledException){throw;}
                catch(Exception ex){if(!(ex is IOException)&&!(ex is InvalidDataException)&&!(ex is UnauthorizedAccessException))throw;throw new IOException("Cannot safely check patch: "+relative+". No game files changed. Check this archive before retrying. "+ex.Message,ex);}
            }
        }
    }
    sealed class ConflictException:Exception{}
    static string TimedHash(string path,Stopwatch watch,CancellationToken token){using(var f=new FileStream(path,FileMode.Open,FileAccess.Read,FileShare.Read))using(var sha=System.Security.Cryptography.SHA256.Create()){byte[] b=new byte[1024*1024];int n;while((n=f.Read(b,0,b.Length))>0){Budget(watch,token);sha.TransformBlock(b,0,n,b,0);}sha.TransformFinalBlock(b,0,0);return BitConverter.ToString(sha.Hash).Replace("-","").ToLowerInvariant();}}
}
}
