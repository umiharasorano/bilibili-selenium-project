from ans_fanc_new import *
import b_login
from threading import Thread
def dr_captcha(dr,ans_lib,ans_zx_lib,pos_lib,thread,s):
    drwait(dr, 3, 0.3, "//div[@class ='click-box']")
    xfind(dr, "//div[@class ='click-box']").click()
    moveto(thread,dr)
    result = movecheck(thread,dr)
    while result:
        dr.refresh()
        drwait(dr,3,0.3, "//div[@class ='click-box']")
        xfind(dr, "//div[@class ='click-box']").click()
        moveto(thread,dr)
        result = movecheck(thread,dr)
    xfind(dr,"//span[@id ='proansSubmit']").click()
    time.sleep(5)
    try:
        drwait(dr,8,0.3,"//span[contains(text() ,'颁奖词')]")
    except Exception as e:
        raise Exception("未知错误")
    dr.delete_all_cookies()
    dr.quit()
    return
def dr_start_check(account,ans_lib,ans_zx_lib,pos_lib,thread):
    dr,uaList = strat_isml(thread)
    mail_name,psw,psw_bili = [account[0],account[1],account[3]]
    login_result = b_login.main(dr,mail_name,psw_bili,thread)
    if login_result[0] in ['登录出错','封禁账号']:
        dr.quit()
        return login_result
    else:
        timestr = login_result[1]
    ranj = random_ques()
    s = ans_cookies_read(dr)
    try:
        ans_base(dr,ans_lib,pos_lib,s,uaList,thread)
        ans_zx(dr,ans_zx_lib,ranj,pos_lib,s,uaList,thread)
        xfind(dr, "//span[contains(text() ,'提交答案')]").click()
        dr_captcha(dr,ans_lib,ans_zx_lib,pos_lib,thread,s)
        print('{}答题成功'.format(mail_name))
        return  '答题成功',timestr
    except Exception as e:
        try:
            ans_zx(dr,ans_zx_lib,ranj,pos_lib,s,uaList,thread)
            xfind(dr, "//span[contains(text() ,'提交答案')]").click()
            dr_captcha(dr,ans_lib,ans_zx_lib,pos_lib,thread,s)
            print('{}答题成功'.format(mail_name))
            return  '答题成功',timestr
        except Exception as e:
            try:
                dr_captcha(dr,ans_lib,ans_zx_lib,pos_lib,thread,s)
                print('{}答题成功'.format(mail_name))
                return '答题成功',timestr
            except Exception as e:
                print('{}答题出错'.format(mail_name))
                #dr.save_screenshot('screenshot.png')
                dr.quit()
                return '答题出错',timestr
class MyThread(Thread):
    def __init__(self, *args):
        Thread.__init__(self)
        self.args =args
    def run(self):
        self.result = dr_start_check(*(self.args))
    def get_result(self):
        return self.result
    
if __name__== '__main__':
    try:
        #pass
        command()
    except Exception as e:
        print('请检查网络连接')
        time.sleep(2)
    else:
        accounts = account_load('Accounts\\Bili_Accounts.txt')
        ans_lib,ans_zx_lib,pos_lib = ans_dic_read()
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
                t = MyThread(accounts[counts*i+j],ans_lib,ans_zx_lib,pos_lib,str(j))
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
                if thread_mis[h][0] == '答题出错':
                    try:
                        str_list[5] = thread_mis[h][1]
                        str_list[6] = '待答题'
                    except:
                        str_list.append(thread_mis[h][1])
                        str_list.append('待答题')
                    account_save(str_list,'Accounts\\Bili_Accounts_mis.txt')
                elif thread_mis[h][0] == '答题成功':
                    try:
                        str_list[5] = thread_mis[h][1]
                        str_list[6] = '待绑定'
                    except:
                        str_list.append(thread_mis[h][1])
                        str_list.append('待绑定')
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
