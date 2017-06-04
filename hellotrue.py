import requests,random,re,time
ItemId = '4532'
notPrefix='170|177'
PhoneType = str(random.randint(1,3))
uName = 'a7122680'
pWord = '3191171'
s = requests.session()

def login():
    url = 'http://api.tianma168.com/tm/Login?uName={}&pWord={}'.format(uName,pWord)
    rs = s.get(url).text
    rs_lib = rs.split('&')
    print('账户余额',rs_lib[1])
    token = rs_lib[0]
    return token
token = login()
def pn_get():
    nr_str = 'ItemId={}&token={}&PhoneType={}&notPrefix={}'.format(ItemId,token,PhoneType,notPrefix)
    url = 'http://api.tianma168.com/tm/getPhone?'+nr_str
    pn = s.get(url).text[:-1]
    return pn
def mes_get(pn):
    success = 0
    t = 1
    time1 = 0
    url = 'http://api.tianma168.com/tm/getMessage?token={}&itemId={}&phone={}'.format(token,ItemId,pn)
    mes = ''
    #每秒检查一次短信，20秒超时
    while not success:
        rs = s.get(url).text
        if time1 < 20:
            if 'MSG' in rs:
                mes = re.sub("\D", "", rs)
                p_blicklistadd(pn)
                success = 1
            else:
                time.sleep(t)
                time1 += t
        else:
            print('未在规定时间内接收到短信,此号码加入黑名单')
            p_blicklistadd(pn)
            success = 1
    return mes
def pn_out(pn):
    url = 'http://api.tianma168.com/tm/releasePhone?token={}&phoneList={}-{}'.format(token,ItemId,pn)
    rs = s.get(url).text
    return
def p_blicklistadd(pn):
    url = 'http://api.tianma168.com/tm/addBlack?token={}&phoneList={}-{}'.format(token,ItemId,pn)
    s.get(url).text
    return
    
