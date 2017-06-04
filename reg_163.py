from fanc import *
def check_163(dr):
    url = 'https://www.baidu.com/s?wd=163&rsv_spt=1&rsv_iqid=0xb80d9de20005d8f5&issp=1&f=8&rsv_bp=1&rsv_idx=2&ie=utf-8&rqlang=cn&tn=baiduhome_pg&rsv_enter=1&inputT=503&rsv_t=120bl0XlmRxmiiPJ5L8QbZWYHhEw7%2BJ4ZcIqNFnaFi1Lgnwg4Ys7NrEvAZcM27HAzfFw&oq=python%2520%25E9%259A%258F%25E6%259C%25BA%25E5%25AD%2597%25E7%25AC%25A6%25E4%25B8%25B2&rsv_pq=a58d0bb40006325e&rsv_sug3=30&rsv_sug1=24&rsv_sug7=100&rsv_sug2=0&rsv_sug4=503'
    dr.get(url)
    mail_check = 'misaka_100861'
    psw_check = 'qwerasdfzxcv'
    drwait(3,0.3,"//*[@id='op_email3_username']")
    xfind("//*[@id='op_email3_username']").send_keys(mail_check)
    drwait(3,0.3,"//*[@class='op_email3_password']")
    xfind("//*[@class='op_email3_password']").send_keys(psw_check)
    drwait(3,0.3,"//*[@class='c-btn c-btn-large c-btn-primary c-gap-right op_email3_submit OP_LOG_BTN']")
    xfind("//*[@class='c-btn c-btn-large c-btn-primary c-gap-right op_email3_submit OP_LOG_BTN']").click()
    time.sleep(1)
    dr.close()
    handles = dr.window_handles
    dr.switch_to.window(handles[0])
    time.sleep(2)
    dr.refresh()
    while 1:
        try:
            drwait(3,0.3,"//*[@id='login_link']")
            xfind("//*[@id='login_link']").click()
            print('可用ip')
            break
        except:
            print('不可用ip')
            ipchange()
    return
def nameinput(dr):
    name = random_nam_ch()
    drwait(3,0.3,"//*[@name='uname']")
    xfind("//*[@name='uname']").send_keys(name)
    drwait(3,0.3,"//*[@value='创建账号']")
    xfind("//*[@value='创建账号']").click()
    time.sleep(2)
    cookies2 = dr.get_cookies()
    return name,cookies2
def vecodeinput(dr):
    drwait(3,0.3,"//*[@id='vdCodeTxt']")
    xfind("//*[@id='vdCodeTxt']").click()
    vdcode = captcha_sc("//*[@id='captchaImg']",'ruokuai.blilbili_register()','0')
    xfind("//*[@id='vdCodeTxt']").send_keys(vdcode)
    drwait(3,0.3,"//*[@value='发送验证邮件']")
    xfind("//*[@value='发送验证邮件']").click()
def bili_reg(dr,mail_name):
    result = 1
    url = 'https://passport.bilibili.com/register/mail'
    dr.get(url)
    drwait(3,0.3,"//*[@value='填写常用邮箱']")
    xfind("//*[@value='填写常用邮箱']").send_keys(mail_name)
    xfind("//*[@id='agree']").click()
    vecodeinput(dr)
    time.sleep(4)
    url1 = dr.current_url
    while url == url1:
        try:
            xfind("//*[@id='captchaImg']").click()
        except:
            result = 0
            print('邮箱已注册,进行至下一个账户')
            return result
        xfind("//*[@id='vdCodeTxt']").clear()
        vecodeinput(dr)
    return result
def bili_act(dr,mail_name,psw):
    cookies,name,psw_bili = ['','','']
    url = 'https://www.baidu.com/s?wd=163&rsv_spt=1&rsv_iqid=0xb80d9de20005d8f5&issp=1&f=8&rsv_bp=1&rsv_idx=2&ie=utf-8&rqlang=cn&tn=baiduhome_pg&rsv_enter=1&inputT=503&rsv_t=120bl0XlmRxmiiPJ5L8QbZWYHhEw7%2BJ4ZcIqNFnaFi1Lgnwg4Ys7NrEvAZcM27HAzfFw&oq=python%2520%25E9%259A%258F%25E6%259C%25BA%25E5%25AD%2597%25E7%25AC%25A6%25E4%25B8%25B2&rsv_pq=a58d0bb40006325e&rsv_sug3=30&rsv_sug1=24&rsv_sug7=100&rsv_sug2=0&rsv_sug4=503'
    dr.get(url)
    drwait(3,0.3,"//*[@id='op_email3_username']")
    xfind("//*[@id='op_email3_username']").send_keys(mail_name[:-8])
    drwait(3,0.3,"//*[@class='op_email3_password']")
    xfind("//*[@class='op_email3_password']").send_keys(psw)
    drwait(3,0.3,"//*[@class='c-btn c-btn-large c-btn-primary c-gap-right op_email3_submit OP_LOG_BTN']")
    xfind("//*[@class='c-btn c-btn-large c-btn-primary c-gap-right op_email3_submit OP_LOG_BTN']").click()
    time.sleep(1)
    dr.close()
    handles = dr.window_handles
    dr.switch_to.window(handles[0])
    time.sleep(2)
    dr.refresh()
    attempts = 0
    while 1:
        try:
            drwait(5,0.3,"//*[@class='gWel-mailInfo-ico']")
            xfind("//*[@class='gWel-mailInfo-ico']").click()
            break
        except:
            if attempts > 4:
                print('邮箱密码怎么样都打不对只好先跳过了')
                break
            if attempts in range(1,4):
                try:
                    dr.switch_to_alert().accept()
                    dr.refresh()
                    vdcode = captcha_sc("//*[@id='w-lc-hint-checkpic']",'ruokuai.mail_163()','0')
                    xfind("//*[@id='w-lc-hint-input']").send_keys(vdcode)
                    xfind("//*[@class='w-lc-hint-btn-sure']").click()
                    attempts += 1
                except:
                    print('邮箱密码错误了，将返回错误信息并进行到下一个账号，2s后自动跳转1')
                    return cookies,name,psw_bili
            else:
                try:
                    dr.refresh()
                    vdcode = captcha_sc("//*[@id='w-lc-hint-checkpic']",'ruokuai.mail_163()','0')
                    xfind("//*[@id='w-lc-hint-input']").send_keys(vdcode)
                    xfind("//*[@class='w-lc-hint-btn-sure']").click()
                    attempts += 1
                except:
                    print('邮箱密码错误了，将返回错误信息并进行到下一个账号，2s后自动跳转2')
                    return cookies,name,psw_bili
    #邮箱内点击处理
    time.sleep(1)
    attempts = 0
    while attempts <30:
        try:
            drwait(10,0.3,"//span[contains(text(),'哔哩哔哩')]")
            break
        except:
            dr.refresh()
            attempts += 1
    try:
        xfind("//span[contains(text(),'哔哩哔哩')]").click()
        time.sleep(3)
        dr.switch_to.frame(xfind("//iframe[contains(@class,'oD0')]"))
        drwait(10,0.3,"//a[contains(text(),'https')]")
        dr.delete_all_cookies()
        url = xfind("//a[contains(text(),'https')]").text
        time.sleep(2)
    except:
        print('未接受到邮件，账户传入至mail_again.txt')
        cookies = 'Mail_Acounts_mis_again'
        return  cookies,name,psw_bili
    dr.get(url)
    drwait(4,0.3,"//*[@id='userpwd']")
    psw_bili = random_psw(8)
    xfind("//*[@id='userpwd']").send_keys(psw_bili)
    cookies1 = dr.get_cookies()
    name,cookies2= nameinput(dr)
    while cookies1  == cookies2:
        xfind("//*[@name='uname']").clear()
        name,cookies2 = nameinput(dr)
    dr.delete_cookie('CNZZDATA2724999')
    cookies = dr.get_cookies()
    return cookies,name,psw_bili
#记录cookies和账户
def bili_sav(dr,mail_name,psw,name,psw_bili,cookies):
    account_save(mail_name,psw,name,psw_bili,'Accounts\Bili_Accounts.txt')
    cookies_save(mail_name,psw_bili,cookies)
    account_del('Accounts\Mail_Acounts.txt')
    print('{} 注册成功'.format(mail_name))
    dr.delete_all_cookies()
    return
