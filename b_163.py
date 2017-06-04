from fanc import *
from reg_163 import *
command()
uaList=[]
dr = start_chromedr()
accounts = account_load('Accounts\\Mail_Acounts.txt')
i = 0
for account in accounts:
    if i%4 == 0:
        #ipchange()
        check_163(dr)
    i += 1
    mail_name = account[0]
    psw = account[1]
    if bili_reg(dr,mail_name) == 0 :
        account_del('Accounts\Mail_Acounts.txt')
        account_save(mail_name,psw,'','','Accounts\\Mail_Acounts_mis.txt')
        continue
    cookies,name,psw_bili = bili_act(dr,mail_name,psw)
    if cookies == '':
        account_del('Accounts\Mail_Acounts.txt')
        account_save(mail_name,psw,'','','Accounts\\Mail_Acounts_mis.txt')
        continue
    if cookies == 'Mail_Acounts_mis_again':
        account_del('Accounts\Mail_Acounts.txt')
        account_save(mail_name,psw,'','','Accounts\\Mail_Acounts_mis_again.txt')
        continue
    bili_sav(dr,mail_name,psw,name,psw_bili,cookies)
