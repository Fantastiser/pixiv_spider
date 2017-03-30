# coding:UTF-8
import re
import requests
import time
import os
s=requests.session()
class Pixiv:
    def __init__(self):
        self.baseUrl = "https://accounts.pixiv.net/login?lang=zh&source=pc&view_type=page&ref=wwwtop_accounts_index"
        self.LoginUrl = "https://accounts.pixiv.net/api/login?lang=zh"
        self.firstPageUrl = 'http://www.pixiv.net/ranking.php?mode=daily'
        self.loginHeader = {
            'Host': "accounts.pixiv.net",
            'User-Agent': "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.75 Safari/537.36",
            'Referer': "https://accounts.pixiv.net/login?lang=zh&source=pc&view_type=page&ref=wwwtop_accounts_index",
            'Content-Type': "application/x-www-form-urlencoded; charset=UTF-8",
            'Connection': "keep-alive"
        }
        self.return_to = "http://www.pixiv.net/"
        self.pixiv_id = '',
        self.password = ''
        self.postKey = []
        self.dailyurl = 'http://www.pixiv.net/ranking.php?mode=daily'
        self.picurl = 'http://www.pixiv.net/ranking.php?mode=daily&content=illust'
        self.name = ''
        f = open('cookies.txt', 'r')
        self.cookies = eval(f.read())

    # 获取此次session的post_key
    def Login(self):
        loginHtml = s.get(self.baseUrl)
        pattern = re.compile('<input type="hidden".*?value="(.*?)">', re.S)
        result = re.search(pattern, loginHtml.text)
        self.postKey = result.group(1)
        loginData = {"pixiv_id": self.pixiv_id, "password": self.password, 'post_key': self.postKey,
                     'return_to': self.return_to}
        a = s.post(self.LoginUrl, data=loginData, headers=self.loginHeader)
        cookies_dict = requests.utils.dict_from_cookiejar(a.cookies)
        if len(cookies_dict) == 2:
            print u'登录成功'
            f = open('cookies.txt', 'w')
            f.write(str(cookies_dict))
            f.close()
        else:
            print u'登录失败'
    def getImg(self, pageUrl,k):
        pattern = re.compile('<div class="_illust_modal.*?<img alt="(.*?)".*?data-src="(.*?)".*?</div>', re.S)
        pageHtml = s.get(pageUrl,cookies=self.cookies).text
        result = re.search(pattern, pageHtml)  # 如果这个页面只有一张图片，那就返回那张图片的url和名字，如果是多张图片 那就找不到返回none
        if (result):
            imgName = result.group(1)
            imgSourceUrl = result.group(2)
            print u'名字: ' ,
            print result.group(1)
            print u'地址：' + result.group(2)
            header = {
                'Referer': pageUrl,
                'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.75 Safari/537.36'
            }
            imgExist = os.path.exists(self.name+'//'+str(k)+'.'+imgName + '.jpg')
            if (imgExist):
                print u'该图片已经存在，跳过！'
            else:
                img = s.get(imgSourceUrl, headers=header,cookies=self.cookies)
                f = open(self.name+'//'+str(k)+'.'+imgName + '.jpg', 'wb')
                f.write(img.content)
                f.close()
                print u'下载完成!'
                print '--------------------------------------------------------------------------------------------------------'

    def download(self,url):
        html = requests.get(url,cookies=self.cookies)
        result_url = re.findall(
            'class="_icon sprites-info open-info ui-modal-trigger"></i></div><div class="ranking-image-item"><a href="(.*?)" class="work  _work " target="_blank"><div class="_layout-thumbnail">',
            html.text, re.S)
        k = 1
        for i in result_url:
            if "class" in i:
                continue
            else:
                p_url0 = "http://www.pixiv.net/" + i.split("&amp;uarea=daily")[0]
                p_url1 = p_url0.split("amp;")
                p_url = p_url1[0] + p_url1[1]
                self.getImg(p_url,k)
                k =k + 1


def first():
    print (u'1.下载每日综合排行榜榜单')
    print (u'2.下载每日插画排行榜榜单')
    p_choice = raw_input()
    return p_choice

if __name__ == "__main__":
    p=Pixiv()
    p_choice = first()
    if p_choice=="1":
        print u"      ————————————综合区每日排行榜——————————————"
        path = os.getcwd()
        title = time.strftime("%Y-%m-%d")
        p.name=str(title)+'-all'
        new_path = os.path.join(path, p.name)
        if not os.path.isdir(new_path):
            os.makedirs(new_path)
        p.download(p.dailyurl)
    elif p_choice=="2":
        print u"      ————————————插画区每日排行榜——————————————"
        path = os.getcwd()
        title = time.strftime("%Y-%m-%d")
        p.name = str(title) + '-illust'
        new_path = os.path.join(path, p.name)
        if not os.path.isdir(new_path):
            os.makedirs(new_path)
        p.download(p.picurl)
    else:
        first()