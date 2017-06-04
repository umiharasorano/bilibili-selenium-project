import random,string,ruokuai,os,time,sys,requests,re,queue,urllib3
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from PIL import Image
from selenium import webdriver
from lxml import etree
from datetime import datetime
def start_foxdr(thread):
    uaList = [line[:-1] for line in open('Base_Data\\ualist.txt')]
    open('Base_Data\\ualist.txt').close()
    i = random.choice(uaList)
    profile = webdriver.FirefoxProfile('c:\\Users\\'+thread)
    profile.set_preference('permissions.default.image', 2)
    profile.set_preference("general.useragent.override", i)
    path1 = 'C:\\Program Files (x86)\\Mozilla Firefox\\geckodriver.exe'
    path2 = 'C:\\Program Files\\Mozilla Firefox\\geckodriver.exe'
    try:
        dr= webdriver.Firefox(executable_path = path1,firefox_profile = profile )
    except:
        dr= webdriver.Firefox(executable_path = path2,firefox_profile = profile )
    return dr,uaList
def start_PhantomJS():
    uaList = []
    for line in open('Base_Data\\Ualist.txt'):
        uaList.append(line[:-1])
    open('Base_Data\\Ualist.txt').close()
    i = random.choice(uaList)
    headers = {
        'Accept':'*/*',
        'Accept-Language':'zh-CN,zh;q=1',
        'User-Agent': i,
        'Connection': 'keep-alive'
    }
    service_args = [
        #'--proxy=127.0.0.1:9999',
        #'--proxy-type=http',
        '--ignore-ssl-errors=true',
        ]
    for key,value in headers.items():
        webdriver.DesiredCapabilities.PHANTOMJS['phantomjs.page.customHeaders.{}'.format(key)] = value
    webdriver.DesiredCapabilities.PHANTOMJS['phantomjs.page.settings.userAgent'] = i
    dr = webdriver.PhantomJS(executable_path=r'C:\\Users\\sorano\\Desktop\\服务器配置文件\\Asuna Sword\\bin\\phantomjs.exe',service_args=service_args)
    return dr,uaList
def strat_isml(thread):
    uaList = []
    for line in open('Base_Data\\ualist.txt'):
        uaList.append(line[:-1])
    open('Base_Data\\ualist.txt').close()
    i = random.choice(uaList)
    option = webdriver.ChromeOptions()
    option.add_argument('--user-agent={}'.format(i))
    option.add_argument('--profile-directory=Default')
    option.add_argument('--user-data-dir=c:\\Users\\{}'.format(thread))
    with open("Base_Data\\ChromeOptions.txt") as a:
        for line in a:
            option.add_argument(line)
    path1 = 'C:\\Program Files (x86)\\Google\\Chrome\\Application\\chromedriver.exe'
    path2 = 'C:\\Program Files\\Google\\Chrome\\Application\\chromedriver.exe'
    try:
        dr = webdriver.Chrome(path1,chrome_options=option)
    except:
        dr = webdriver.Chrome(path2,chrome_options=option)
    return dr,uaList
def random_psw(length):
    a = list('ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz')
    random.shuffle(a)
    return ''.join(a[:length])
def random_nam_ch():
    with open('Base_Data\\Name_CN.txt','r') as a:
        a = eval(a.read())
        name_ch = a[random.randint(0,len(a)-1)] + a[random.randint(0,len(a)-1)]
        name_ch = name_ch + random_psw(random.randint(2,4))
    return name_ch
def random_nam_en():
    with open('Base_Data\\Name_US.txt','r') as a:
        a = eval(a.read())
        name_en = a[random.randint(0,len(a)-1)]
        name_en = name_en + random_psw(random.randint(1,2))
    return name_en
def xfind(dr,xpath):
    return dr.find_element_by_xpath(xpath)
def drwait(dr,outtime,t,xpath):
    l = (By.XPATH,xpath)
    WebDriverWait(dr,outtime,t).until(expected_conditions.element_to_be_clickable(l))
def captcha_sc(dr,xpath,chaptcha_mod,else_str,thread):
    time.sleep(3)
    elem = xfind(dr,xpath)
    size = elem.size
    location = elem.location     
    name,typeid = eval(chaptcha_mod)
    name = thread + name
    dr.save_screenshot('Captchas\\'+name)
    im = Image.open('Captchas\\'+name)
    left = elem.location['x']
    right = left + elem.size['width']
    top = elem.location['y'] +eval(else_str)
    bottom = top + elem.size['height']
    im = im.crop((left, top, right, bottom))
    im.save('Captchas\\'+name)      
    vdcode = ruokuai.main(name,typeid)
    return vdcode
def cookies_save(mail_name,psw_bili,cookies):
    file_name = 'Cookies\\' + mail_name +'----'+psw_bili+ ".txt"
    with open(file_name,'w') as f:
        f.write(str(cookies))
        f.flush()
    return
def cookies_load(dr,mail_name,psw_bili):
    file_name = 'Cookies\\' + mail_name +'----'+psw_bili + ".txt"
    with open(file_name,'r') as f:
        cookies = eval(f.read())
    if 'DedeUserID' not in str(cookies):
        raise Exception('错误的cookies')  
    for cookie in cookies:
        if cookie['name'] == 'DedeUserID':
            cookie_time = int(cookie['expiry'])
            if cookie_time < int(time.time()):
                print('cookies过期')
                raise Exception('cookies过期')
    for cookie in cookies:
        try:
            cookie['expiry']=int(cookie['expiry'])
        except:
            pass
        try:
            pass
            #del cookie['expires']
        except:
            pass
        dr.add_cookie(cookie)
    return

def cookies_add_s(dr):
    s = requests.session()
    for i in dr.get_cookies():
        s.cookies.set(i['name'],i['value'], path=i['path'],domain=i['domain'])
    return s
def account_save(str_list,path):
    text = '----'.join(str_list) + '\n'
    fo = open(path,'a+')
    fo.write(text)
    fo.flush()
    fo.close()
    return
def account_load(path):
    accounts=[]
    for line in open(path):
        accounts.append(line[:-1].split('----'))
    open(path).close()
    return accounts
def account_del(path,lenth = 1):
    fo = open(path,'r+')
    a = fo.readlines()
    b=''.join(a[lenth:])
    fo.close
    fo = open(path,'w')
    fo.write(b)
    fo.close()
def command():
    url='http://asuna520.applinzi.com'
    s = requests.get(url).text
    k = input('Asuna:')
    while k != s:
        k = input('Asuna:')
    return
def adsl():
    try:
        with open('C:\\Users\\Administrator\\Desktop\\宽带账号.txt','r') as f:
            account = f.read().split('----')
            account.insert(0,"宽带连接")
    except:
        with open('Base_Data\\ADSL.txt','r') as f:
            account = eval(f.read())
    cmd_str = "rasdial 宽带连接 /disconnect"
    os.system(cmd_str)
    time.sleep(8)
    cmd_str = "rasdial %s %s %s" % (account[0], account[1], account[2])
    os.system(cmd_str)
    time.sleep(8)
def ipcheck():
    s = requests.session()
    r = s.get('http://1212.ip138.com/ic.asp')
    r.encoding = 'gb2312'
    html = r.text
    lst = etree.HTML(html).xpath('//center')
    ip_str = lst[0].xpath('string(.)')
    ip_list = ip_str.split('] 来自：')
    ip = ip_list[0][7:]
    ip_loc = ip_list[1]
    ip_info = ip+''+ip_loc
    return ip_info
def ipchange():
    print('检查ip中')
    with open('Base_Data\\IPlist.txt') as f:
        a = f.read()
    with open('Base_Data\\IPBlacklist.txt') as f:
        b = f.read()
    ipblasklist = b
    iplist = a.split('\n')[:-1]
    ip_info = ipcheck()
    ip_black = '.'.join(ip_info.split('.')[:2])
    while ip_info in iplist or ip_black in ipblasklist:
        #print(ip_info,'重复ip，重新拨号')
        adsl()
        try:
            ip_info = ipcheck()
        except:
            print('网络错误,重新拨号')
            adsl()
    print(ip_info)
    fo = open("Base_Data\\IPlist.txt",'a+')
    fo.write(str(ip_info)+'\n')
    fo.flush()
    fo.close()
    return ip_info
def ipchange_siml():
    print('检查ip中')
    with open('Base_Data\\IPlist.txt') as f:
        iplist = f.read()
    ip_info = ipcheck()
    print(ip_info)
    ip_abc = '.'.join(ip_info.split('.')[:3])
    ip_ab = '.'.join(ip_info.split('.')[:2])
    with open('Base_Data\\IPBlacklist.txt') as f:
        ipblasklist = f.read()
    while ip_abc in iplist or ip_ab in ipblasklist:
        #print(ip_info,'重复ip，重新拨号')
        adsl()
        try:
            ip_info = ipcheck()
            print(ip_info)
            ip_abc = '.'.join(ip_info.split('.')[:3])
            ip_ab = '.'.join(ip_info.split('.')[:2])
        except:
            print('网络错误,重新拨号')
            adsl()
    fo = open("Base_Data\\IPlist.txt",'a+')
    fo.write(str(ip_info)+'\n')
    fo.flush()
    fo.close()
    fo = open('Base_Data\\IPBlacklist.txt','a+')
    if iplist.count(ip_ab) >= 8:
        fo.write(ip_ab+'\n')
        fo.flush()
    fo.close()
    return ip_info
def Vget(dr,url):
    try:
        dr.get(url)
    except:
        dr.execute_script('window.stop()')
    return
