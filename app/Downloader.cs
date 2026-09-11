// Author, Creator, Last Modified By: Neil Mitchell
using System;
using System.IO;
using System.Net;
using System.Linq;
using System.Collections.Generic;
using System.Text.RegularExpressions;
using System.Threading;

namespace LauSetup {
public sealed class TransferProgress { public string Name;public long Received,Total,Overall; }
public sealed class Downloader {
    readonly string cache,offline;readonly Action<TransferProgress> progress;
    internal Func<Part,Uri> TestUrl { get; set; }
    public Downloader(string cache,string offline,Action<TransferProgress> progress) {
        this.cache=cache;this.offline=offline;this.progress=progress??(p=>{});SafePaths.Plain(cache);Directory.CreateDirectory(cache);
        ServicePointManager.SecurityProtocol=SecurityProtocolType.Tls12;
    }
    public string Fetch(Asset asset,CancellationToken token) {
        string target=SafePaths.Under(cache,asset.Sha256+".asset");
        if(Hash.Matches(target,asset.Sha256,asset.Bytes)){progress(new TransferProgress{Name=asset.Id,Received=asset.Bytes,Total=asset.Bytes});return target;}
        if(File.Exists(target))File.Delete(target);
        if(new DriveInfo(Path.GetPathRoot(cache)).AvailableFreeSpace<asset.Bytes*2+128L*1024*1024)throw new IOException("Not enough free space for this download and verification.");
        long previous=0;var files=new List<string>();
        foreach(var part in asset.Parts) {
            token.ThrowIfCancellationRequested();long prefix=previous;
            files.Add(FetchPart(part,token,n=>progress(new TransferProgress{Name=asset.Id,Received=prefix+n,Total=asset.Bytes})));previous+=part.Bytes;
        }
        string assembling=SafePaths.Under(cache,asset.Sha256+"."+Guid.NewGuid().ToString("N")+".assembling");
        try {
            using(var dest=new FileStream(assembling,FileMode.CreateNew,FileAccess.Write,FileShare.None)) {
                byte[] buffer=new byte[1024*1024];
                foreach(var file in files)using(var src=File.OpenRead(file)) { int read;while((read=src.Read(buffer,0,buffer.Length))>0){token.ThrowIfCancellationRequested();dest.Write(buffer,0,read);} }dest.Flush(true);
            }
            if(!Hash.Matches(assembling,asset.Sha256,asset.Bytes))throw new IOException("The downloaded upgrade failed its final verification. Please retry.");
            File.Move(assembling,target);
            // Segments are owned verified cache files; the assembled asset replaces them.
            foreach(var file in files.Distinct())if(File.Exists(file))File.Delete(file);
            return target;
        } catch { if(File.Exists(assembling))File.Delete(assembling);throw; }
    }
    internal string FetchPart(Part part,CancellationToken token,Action<long> report) {
        if(!Hash.Valid(part.Sha256)||part.FileName!=part.Sha256+".bin"||part.Bytes<=0)throw new InvalidDataException("Invalid download segment.");
        string final=SafePaths.Under(cache,part.FileName),partial=SafePaths.Under(cache,part.Sha256+".partial");
        if(Hash.Matches(final,part.Sha256,part.Bytes)){report(part.Bytes);return final;}
        if(File.Exists(final))File.Delete(final);
        if(!String.IsNullOrEmpty(offline)) {
            var local=SafePaths.Under(offline,part.FileName);
            if(File.Exists(local)) {
                if(!Hash.Matches(local,part.Sha256,part.Bytes))throw new IOException("The offline download files are damaged. Download a fresh copy.");
                File.Copy(local,final);if(!Hash.Matches(final,part.Sha256,part.Bytes))throw new IOException("Offline copy verification failed.");report(part.Bytes);return final;
            }
        }
        if(TestUrl==null&&!Catalog.ValidDownloadUrl(part))throw new IOException("This preview does not have verified public downloads configured.");
        if(File.Exists(partial)&&new FileInfo(partial).Length>part.Bytes)File.Delete(partial);
        long offset=File.Exists(partial)?new FileInfo(partial).Length:0;
        if(offset==part.Bytes) {
            if(Hash.Matches(partial,part.Sha256,part.Bytes)){File.Move(partial,final);report(part.Bytes);return final;}File.Delete(partial);offset=0;
        }
        Uri url=TestUrl==null?new Uri(part.Url):TestUrl(part);
        var cookies=new CookieContainer();
        for(int step=0;step<9;step++) {
            token.ThrowIfCancellationRequested();CheckHost(url);
            var request=(HttpWebRequest)WebRequest.Create(url);request.Method="GET";request.UserAgent="LauSetup/1.0";request.AllowAutoRedirect=false;request.CookieContainer=cookies;request.Timeout=30000;request.ReadWriteTimeout=30000;
            if(offset>0)request.AddRange(offset);
            try {
                using(token.Register(()=>request.Abort()))using(var response=(HttpWebResponse)request.GetResponse()) {
                    CheckHost(response.ResponseUri);
                    int status=(int)response.StatusCode;
                    if(status==301||status==302||status==303||status==307||status==308) {
                        string location=response.Headers["Location"];
                        if(String.IsNullOrWhiteSpace(location))throw new IOException("Download redirect is missing its destination.");
                        var next=new Uri(url,location);CheckHost(next);url=next;continue;
                    }
                    if(response.ContentType.StartsWith("text/html",StringComparison.OrdinalIgnoreCase))throw new IOException("The download host returned a page instead of the file. Your client is unchanged. Try again later; completed downloads are kept.");
                    if(response.StatusCode==HttpStatusCode.OK&&offset>0)offset=0;
                    if(response.StatusCode==HttpStatusCode.PartialContent) {
                        var range=Regex.Match(response.Headers["Content-Range"]??"",@"^bytes (\d+)-(\d+)/(\d+)$");
                        if(!range.Success||long.Parse(range.Groups[1].Value)!=offset||long.Parse(range.Groups[2].Value)!=part.Bytes-1||long.Parse(range.Groups[3].Value)!=part.Bytes)throw new IOException("Download server returned an incorrect resume range.");
                    }else if(response.StatusCode!=HttpStatusCode.OK)throw new IOException("Unexpected download response.");
                    long remaining=part.Bytes-offset;
                    if(response.ContentLength>=0&&response.ContentLength!=remaining)throw new IOException("Download size does not match the release.");
                    using(var source=response.GetResponseStream())using(var output=new FileStream(partial,FileMode.OpenOrCreate,FileAccess.Write,FileShare.None)) {
                        SafePaths.SingleLink(output);
                        if(offset==0)output.SetLength(0);else if(output.Length!=offset)throw new IOException("The partial download changed. Please retry.");
                        output.Position=offset;
                        byte[] buffer=new byte[128*1024];int read;long written=offset;
                        while((read=source.Read(buffer,0,buffer.Length))>0) {
                            token.ThrowIfCancellationRequested();if(written+read>part.Bytes)throw new IOException("Download exceeded the release size.");output.Write(buffer,0,read);written+=read;report(written);
                        }output.Flush(true);if(written!=part.Bytes)throw new IOException("Download was interrupted. Click Install to resume.");
                    }
                    if(!Hash.Matches(partial,part.Sha256,part.Bytes)){File.Delete(partial);throw new IOException("Download verification failed. Your client is unchanged. Please retry.");}
                    File.Move(partial,final);return final;
                }
            } catch(WebException ex) {
                token.ThrowIfCancellationRequested();throw new IOException("The download could not finish. Check your connection or try later. Verified downloads are kept for retry.",ex);
            }
        }
        throw new IOException("The download host redirected too many times. Please try later.");
    }
    void CheckHost(Uri uri) {
        if(TestUrl!=null&&uri.IsLoopback&&uri.Scheme=="http")return;
        var host=uri.DnsSafeHost.ToLowerInvariant();
        if(uri.Scheme!="https"||!uri.IsDefaultPort||!String.IsNullOrEmpty(uri.UserInfo)||!(host=="github.com"||host=="release-assets.githubusercontent.com"||host=="objects.githubusercontent.com"))throw new IOException("Unexpected download destination.");
        if(host=="github.com"&&!uri.AbsolutePath.StartsWith("/CRSD-Lau/Lau-Setup/releases/download/payload-3.0.4/",StringComparison.Ordinal))throw new IOException("Unexpected download destination.");
    }
}
}
