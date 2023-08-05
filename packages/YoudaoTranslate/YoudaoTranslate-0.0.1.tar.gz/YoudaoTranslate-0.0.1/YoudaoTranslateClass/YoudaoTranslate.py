#! /usr/bin/env python3
#coding=utf-8

import urllib.request
import urllib.parse
import json
import time, random
import hashlib

"""
通过查找，能找到js代码中的操作代码
1.这是计算salt的公式，在fanyi.min.js文件中找到的，
t = "" + ((new Date).getTime() + parseInt(10 * Math.random(), 10));
2.sign: n.md5("fanyideskweb" + e + t + "sr_3(QOHT)L2dx#uuGR@r")
md5一共需要四个参数，第一个和第四个都是固定的字符串，第三个是所谓的salt。第二个就是输入的要查找的单词
"""

class YoudaoTranslate:

    def getSalt(self):
        """
        这是计算salt的公式  "" + ((new Date).getTime() + parseInt(10 * Math.random(), 10));
        把它翻译成Python代码
        :return:
        """
        # (new Date).getTime()生成的时间戳与time.time()的单位不一致，所以需要乘1000
        self.salt = int(time.time() * 1000) + random.randint(0, 10)

        return  self.salt

    def getMd5(self, v):
        self.md5 = hashlib.md5()

        # 需要一个bytes格式的参数
        self.md5.update(v.encode("utf-8"))
        self.sign = self.md5.hexdigest()

        return self.sign

    def getSign(self, key, salt):
        self.sign = "fanyideskweb" + key + str(salt) + "sr_3(QOHT)L2dx#uuGR@r"
        self.sign = self.getMd5(self.sign)
        return self.sign

    def youdaoTranslate(self, content):
        self.url = "http://fanyi.youdao.com/translate?smartresult=dict&smartresult=rule"
        self.data = {
            "i": content, "from": "AUTO", "to": "AUTO",
            "smartresult": "dict", "client": "fanyideskweb", "salt": "15644691638724",
            "sign": "21dce70acabf8efc5de2926cfa2d6b19", "ts": "1564469163872", "bv": "6cf12640614e68ba598ee58ceccb0605",
            "doctype": "json", "version": "2.1", "keyfrom": "fanyi.web", "action": "FY_BY_CLICKBUTTION"
        }
        self.data = urllib.parse.urlencode(self.data).encode("utf-8")
        self.response = urllib.request.urlopen(self.url, data=self.data)
        self.html = self.response.read().decode("utf-8")
        return json.loads(self.html).get('translateResult')[0][0].get('tgt')

    # 无效了，有道词典升级了反爬虫机制，请使用youdaoTranslate
    def youdaoTranslate_new(self, content):
        self.url = "http://fanyi.youdao.com/translate_o?smartresult=dict&smartresult=rule"
        self.salt = self.getSalt()
        self.data = {
            "i": content, "from": "AUTO", "to": "AUTO",
            "smartresult": "dict", "client": "fanyideskweb", "salt": str(self.salt),
            "sign": self.getSign(content, self.salt), "ts": "1564469163872", "bv": "6cf12640614e68ba598ee58ceccb0605",
            "doctype": "json", "version": "2.1", "keyfrom": "fanyi.web", "action": "FY_BY_CLICKBUTTION"
        }
        self.data = urllib.parse.urlencode(self.data).encode("utf-8")
        self.response = urllib.request.urlopen(self.url, data=self.data)
        print(self.response.read().decode("utf-8"))
        self.html = self.response.read().decode("utf-8")
        return json.loads(self.html).get('translateResult')[0][0].get('tgt')

if __name__ == "__main__":
    youdao = YoudaoTranslate()
    content = input("请输入翻译语句：")
    result = youdao.youdaoTranslate(content)
    print(result)
