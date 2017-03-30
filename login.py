# coding:UTF-8
import spider_pixiv
print u'请输入你的pixiv id:',
pixiv_id = raw_input()
print u'请输入你的pixiv密码:',
password = raw_input()
p = spider_pixiv.Pixiv()
p.pixiv_id =pixiv_id
p.password = password
p.Login()