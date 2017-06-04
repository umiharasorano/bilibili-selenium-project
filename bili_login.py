from fanc import *
import b_login
from selenium.webdriver.support.select import Select
from threading import Thread
class MyThread(Thread):
    def __init__(self, *args):
        Thread.__init__(self)
        self.args =args
    def run(self):
        self.result = main(*(self.args))
    def get_result(self):
        return self.result
def main(account,thread):
    dr,uaList = strat_isml(thread)
    dr.set_page_load_timeout(15)
    dr.set_script_timeout(15)
    mail_name,psw,psw_bili = [account[0],account[1],account[3]]
    login_result = b_login.main(dr,mail_name,psw_bili,thread)
    if login_result[0] in ['登录出错','封禁账号']:
        dr.quit()
        return login_result
    else:
        timestr = login_result[1]
    dr.quit()
    return '登录成功',timestr
if __name__== '__main__':
    try:
        #pass
        command()
    except Exception as e:
        print('请检查网络连接')
        time.sleep(2)
    else:
        accounts = account_load('Accounts\\Bili_Accounts.txt')
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
                t = MyThread(accounts[counts*i+j],str(j))
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
                if thread_mis[h][0] == '登录成功':
                    try:
                        str_list[5] = thread_mis[h][1]
                    except:
                        str_list.append(thread_mis[h][1])
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
            #break
            account_del('Accounts\\Bili_Accounts.txt',counts)
