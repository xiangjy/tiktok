# -*- coding:utf-8 -*-
import requests


def fetchurl(url):
    header = {
            "User-Agent": "Mozilla/5.0 (Linux;U;Android 2.3;en-us;Nexus One Build/FRF91)AppleWebKit/999+(KHTML, like Gecko)Version/4.0 Mobile Safari/999.9"
    }
    response = requests.get(url=url, headers=header)
    return response.text

if __name__ == "__main__":
    url = 'https://www.douyin.com/share/user/76055758243'
    print fetchurl(url)
