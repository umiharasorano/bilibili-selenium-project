from fanc import *
def main(dr,mail_name,psw_bili,thread):
    dr.get('https://passport.bilibili.com/login')
    try:
        cookies_load(dr,mail_name,psw_bili)
    except Exception as e:
        print('{}未找到有效cookies，开始登陆账户'.format(mail_name))
        try:
            cookies,timestr = login_check(dr,mail_name,psw_bili,thread)
        except Exception as e:
            print('{}登录出错'.format(mail_name))
            return '登录出错','网络错误'
        else:
            try:
                int(timestr[:4])
            except Exception as e:
                return '登录出错',timestr
            else:
                cookies_save(mail_name,psw_bili,cookies)
    else:
        timestr = str(datetime.today())[:-7]
    dr.get('https://message.bilibili.com/#system')
    try:
        drwait(dr,3,0.3,"//div[contains(text() ,'账号违规处理通知')]")
    except Exception as e:
        pass
    else:
        a = xfind(dr,"//div[contains(text() ,'账号违规处理通知')]/span").get_attribute('innerText')
        b = xfind(dr,"//div[contains(text() ,'抱歉，由于你的账号涉嫌违规操作')]").get_attribute('innerText')
        print('{}封禁账号'.format(mail_name))
        return '封禁账号',a,b
    return '登录成功',timestr
def login_check(dr,mail_name,psw_bili,thread):
    dr.get('https://passport.bilibili.com/login')
    cookies = login(dr,mail_name,psw_bili,thread)
    while 1:
        if 'DedeUserID' in str(cookies):
            timestr = str(datetime.today())[:-7]
            dr.delete_cookie('CNZZDATA2724999')
            dr.delete_cookie('JSESSIONID')
            cookies = dr.get_cookies()
            break
        else:
            a = xfind(dr,"//li[@class = 'item vdcode']/div/p").get_attribute('innerText')
            b = xfind(dr,"//li[@class = 'item username']/div/p").get_attribute('innerText')
            if '验证码错误' in a:
                print('验证码错误')
                time.sleep(2)
                cookies = login_captcha(dr,mail_name,psw_bili,thread)
            elif '用户名或密码错误' in b:
                timestr = '用户名或密码错误'
                print('用户名或密码错误')
                break
    return cookies,timestr
def login(dr,mail_name,psw_bili,thread):
    drwait(dr,5,0.3,"//input[@id='login-username']")
    xfind(dr,"//input[@id='login-username']").send_keys(mail_name)
    drwait(dr,5,0.3,"//input[@id='login-passwd']")
    xfind(dr,"//input[@id='login-passwd']").send_keys(psw_bili)
    drwait(dr,5,0.3,"//a[@class='btn btn-login']")
    drwait(dr,8,0.3,"//li[@class='item vdcode']/input")
    cookies = login_captcha(dr,mail_name,psw_bili,thread)
    return cookies
def login_captcha(dr,mail_name,psw_bili,thread):
    xfind(dr,"//li[@class='item vdcode']/input").click()
    time.sleep(3)
    drwait(dr,5,0.3,"//li[@class='item vdcode']/img")
    vdcode = captcha_sc(dr,"//li[@class='item vdcode']/img",'ruokuai.blilbili_login()','0',thread)
    drwait(dr,5,0.3,"//li[@class='item vdcode']/input")
    xfind(dr,"//li[@class='item vdcode']/input").send_keys(vdcode)
    xfind(dr,"//a[@class='btn btn-login']").click()
    time.sleep(1)
    cookies = dr.get_cookies()
    return cookies
