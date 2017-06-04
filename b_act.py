from fanc import *

def nameinput():
    name = random_nam_ch()
    drwait(3,0.3,"//*[@name='uname']")
    xfind("//*[@name='uname']").send_keys(name)
    drwait(3,0.3,"//*[@value='创建账号']")
    xfind("//*[@value='创建账号']").click()
    drwait(0.3,3,"//*[@value='创建账号']")
    xfind("//*[@value='创建账号']").click()
    time.sleep(2)
    cookies2 = dr.get_cookies()
    return name,cookies2
def vecodeinput():
    drwait(0.3,3,"//*[@id='vdCodeTxt']")
    input('ces')
    xfind("//*[@id='vdCodeTxt']").click()
    input('ces')
    vdcode = captcha_sc("//*[@id='captchaImg']",'ruokuai.blilbili_register()','0')
    xfind("//*[@id='vdCodeTxt']").send_keys(vdcode)
    drwait(0.3,3,"//*[@value='发送验证邮件']")
    xfind("//*[@value='发送验证邮件']").click()
def bili_reg(mail_name):
    url = 'https://passport.bilibili.com/register/mail'
    dr.get(url)
    drwait(0.3,3,"//*[@value='填写常用邮箱']")
    xfind("//*[@value='填写常用邮箱']").send_keys(mail_name)
    xfind("//*[@id='agree']").click()
    vecodeinput()
    while 1:
        try:
            time.sleep(1)
            drwait(0.3,3,"//*[@id='vdCodeTxt']")
        except:
            print('激活模块成功完成')
            return
        input('ces')
        xfind("//*[@id='vdCodeTxt']").clear()
        input('ces')
        xfind("//*[@id='captchaImg']").click()
        vecodeinput()
def bili_act():
    cookies,name=[None,None]
    url = 'https://outlook.live.com/owa/'
    dr.get(url)
    attempt = 0
    
    while 1:
        if attempt < 4:
            try:
                drwait(0.5,10,"//span[contains(text() ,'【哔哩哔哩】会员邮件验证通知 请确认并完成绑定')]")
                xfind("//span[contains(text() ,'【哔哩哔哩】会员邮件验证通知 请确认并完成绑定')]").click()
                drwait(0.5,10,"//a[contains(text(),'https://passport.bilibili.com/register/')]")
                url_mail = xfind("//a[contains(text(),'https://passport.bilibili.com/register/')]").text
                break
            except:
                attempt += 1
                dr.refresh()
        else:
            print('未收到邮件')
            return cookies,name
    
    dr.delete_all_cookies()  
    dr.get(url_mail)
    drwait(0.3,5,"//*[@id='userpwd']")
    xfind("//*[@id='userpwd']").send_keys(psw)
    cookies1 = dr.get_cookies()
    name,cookies2= nameinput()
    while cookies1  == cookies2:
        xfind("//*[@name='uname']").clear()
        name,cookies2 = nameinput()
    dr.delete_cookie('CNZZDATA2724999')
    cookies = dr.get_cookies()
    return cookies,name
#记录cookies和账户
def bili_sav(mail_name,cookies,name):
    x='DedeUserID'
    if x not in str(cookies):
        print('发生错误，无效的cookies')
        print(mail_name,psw)
    else:
        account_save(mail_name,psw,name)
        cookies_save(mail_name,cookies)
        print('{} 注册成功'.format(mail_name))
    dr.delete_all_cookies()
    return
