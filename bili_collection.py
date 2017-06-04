from fanc import *
import b_login
from selenium.webdriver.support.select import Select
from threading import Thread
def face_change(dr,face_lib):
    dr.get('https://account.bilibili.com/site/face.html')
    drwait(dr,5,0.3,"//a[@id = 'face-g-change']")
    xfind(dr,"//a[@id = 'face-g-change']").click()
    drwait(dr,5,0.3,"//a[@id = 'ord-pic']")
    xfind(dr,"//a[@id = 'ord-pic']").click()
    elem = xfind(dr,"//input[@name = 'face']")
    
    elem.send_keys('C:\\Users\\administrator\\Desktop\\4319头像包\\{}'.format(random.choice(face_lib)))
    time.sleep(2)
    drwait(dr,5,0.3,"//input[@class = 'sure']")
    xfind(dr,"//input[@class = 'sure']").click()
    time.sleep(2)
def pre():
    rootdir = 'C:\\Users\\administrator\\Desktop\\4319头像包'
    face_lib = os.listdir(rootdir)
    with open('Base_Data\姓.txt') as f:
        name_first = eval(f.read())
    with open('Base_Data\名.txt') as f:
        name_last = eval(f.read())
    return name_first,name_last,face_lib
def name_ran(name_first,name_last):
    name_ran = random.choice(name_first)+random.choice(name_last)
    return name_ran
def safe_change(dr,name_first,name_last):
    dr.get('https://passport.bilibili.com/site/site.html')
    name = '密保已设置'
    while 1:
        try:
            drwait(dr,3,0.3,"//span[contains(text(),'已设置密保问题')]")
            print('密保已设置')
            break
        except:
            drwait(dr,5,0.3,"//a[contains(text(), '设置密保')]")
            xfind(dr,"//a[contains(text(), '设置密保')]").click()
            elem = xfind(dr,"//select[@id = 'oldsafequestion']")
            Select(elem).select_by_value(str(random.choice(range(4,7))))
            name = name_ran(name_first,name_last)
            xfind(dr,"//input[@id = 'oldsafeanswer']").send_keys(name)
            drwait(dr,5,0.3,"//div[@class = 'safequbtn sure']")
            xfind(dr,"//div[@class = 'safequbtn sure']").click()
            drwait(dr,5,0.3,"//input[@class = 'd-button d-state-highlight']")
            xfind(dr,"//input[@class = 'd-button d-state-highlight']").click()
    return name

class MyThread(Thread):
    def __init__(self, *args):
        Thread.__init__(self)
        self.args =args
    def run(self):
        self.result = main(*(self.args))
    def get_result(self):
        return self.result
def main(account,name_first,name_last,face_lib,thread):
    dr,uaList = strat_isml(thread)
    mail_name,psw,psw_bili = [account[0],account[1],account[3]]
    login_result = b_login.main(dr,mail_name,psw_bili,thread)
    if login_result[0] in ['登录出错','封禁账号']:
        dr.quit()
        return login_result
    else:
        timestr = login_result[1]
    try:
        name = safe_change(dr,name_first,name_last) 
        print('{}密保设置成功'.format(mail_name))
    except Exception as e:
        print('{}设置密保出错'.format(mail_name))
        dr.quit()
        return '设置出错',timestr
    try:
        face_change(dr,face_lib)
        print('{}头像设置成功'.format(mail_name))
    except Exception as e:
        print('{}设置头像出错'.format(mail_name))
        dr.quit()
        return '设置出错',timestr
    dr.quit()
    return '设置成功',timestr,name
if __name__== '__main__':
    try:
        #pass
        command()
    except Exception as e:
        print('请检查网络连接')
        time.sleep(2)
    else:
        accounts = account_load('Accounts\\Bili_Accounts.txt')
        name_first,name_last,face_lib = pre()
        while 1:
            input_str = input('请输入多开数量(num 1-4):')
            if input_str in [str(x) for x in range(1,5)]:
                break
            else:
                pass
        counts = int(input_str)
        if len(accounts) < counts:
            print('请放入足够的账户到Bili_Accounts')
            time.sleep(2)
        for i in range(len(accounts)//counts):
            ip_info = ipchange()
            #ip_info = '122'
            thread_mis = []
            threads_list =[]
            for j in range(counts):
                t = MyThread(accounts[counts*i+j],name_first,name_last,face_lib,str(j))
                threads_list.append(t)
            for t in threads_list:
                t.setDaemon(True)
                t.start()
            for t in threads_list:
                t.join()
            for t in threads_list:
                thread_mis.append(t.get_result())
            for h in range(counts):
                str_list = accounts[counts*i+h][:]
                try:
                    str_list[4] = ip_info
                except:
                    str_list.append(ip_info)
                if thread_mis[h][0] == '设置出错':
                    try:
                        str_list[5] = thread_mis[h][1]
                        str_list[6] = '待设置'
                    except:
                        str_list.append(thread_mis[h][1])
                        str_list.append('待设置')
                    account_save(str_list,'Accounts\\Bili_Accounts_mis.txt')
                elif thread_mis[h][0] == '设置成功':
                    try:
                        str_list[5] = thread_mis[h][1]
                        str_list[6] = '待绑定'
                    except:
                        str_list.append(thread_mis[h][1])
                        str_list.append('待绑定')
                    if thread_mis[h][2] == '密保已设置':
                        pass
                    else:
                        str_list.append(thread_mis[h][2])
                    account_save(str_list,'Accounts\\Bili_Accounts_ansok.txt')
                elif thread_mis[h][0] == '登录出错':
                    try:
                        str_list[5] = thread_mis[h][1]
                    except:
                        str_list.append(thread_mis[h][1])
                    account_save(str_list,'Accounts\\Bili_Login_mis.txt')
                elif thread_mis[h][0] == '封禁账号':
                    text = '----'.join(accounts[counts*i+h]) + '\n' + thread_mis[h][2] +' '+thread_mis[h][1] + '\n'
                    fo = open('Accounts\\Bili_Login_black.txt','a+')
                    fo.write(text)
                    fo.flush()
                    fo.close()
            account_del('Accounts\\Bili_Accounts.txt',counts)
