# -*- coding:utf-8 -*-

from urllib2 import Request, urlopen
def fetchurl(url):
    req = Request(url)
    req.add_header("User-Agent","Mozilla/5.0 (Linux;U;Android 2.3;en-us;Nexus One Build/FRF91)AppleWebKit/999+(KHTML, like Gecko)Version/4.0 Mobile Safari/999.9")
    f = urlopen(req)
    return f.read()

if __name__ == "__main__":
    url = "https://www.iesdouyin.com/share/video/6686379726505774349/?region=CN&mid=6686395143635077901&u_code=hldm8blf&titleType=title"
    print fetchurl(url)
