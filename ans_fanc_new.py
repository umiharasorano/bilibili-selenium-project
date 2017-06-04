from fanc import *
from selenium.webdriver.common.action_chains import ActionChains
import math
def ans_dic_read():
    #加载位置
    left = [16,15,16,17]
    right = [68,67,68,69]
    top = [22,36,50,64]
    bottom = [34,48,62,76]
    top2 = [42,56,70,84]
    bottom2 = [54,68,82,96]
    pos_lib = [left,right,top,bottom,top2,bottom2]
    #加载字典库
    with open('Base_Data\\YukiAsuna.txt') as f1:
        a = f1.read()
        a = re.sub('[A-J]+',', ',a)
        a = re.sub('[K-Za-i]+',"'",a)
        a = re.sub('[j-z]+',': ',a)
        a = '{' + a + '}'
        ans_lib = eval(a)
    with open('Base_Data\\YukiAsuna_sword.txt') as f2:
        a = f2.read()
        a = re.sub('[A-J]+',', ',a)
        a = re.sub('[K-Za-i]+',"'",a)
        a = re.sub('[j-z]+',': ',a)
        a = '{' + a + '}'
        ans_zx_lib = eval(a)
    return ans_lib,ans_zx_lib,pos_lib
def random_ques():
    ranj = list(range(1,61))
    random.shuffle(ranj)
    ranj = ranj[:random.randint(10,25)]
    return ranj
def ans_cookies_read(dr):
    #切换到答题页
    url = 'https://account.bilibili.com/answer/base'
    dr.get(url)
    #输入任意键开始答题
    dr.delete_cookie('CNZZDATA2724999')
    s = requests.session()
    for i in dr.get_cookies():
        s.cookies.set(i['name'],i['value'], path=i['path'],domain=i['domain'])
    return s
def ans_base(dr,ans_lib,pos_lib,s,uaList,thread):
    left,right,top,bottom,top2,bottom2 = pos_lib
    for j in range(1,41):
        drwait(dr,5,0.3,"//ul[@id ='examListUl']/li[{}]/div[1]".format(j))
        a = xfind(dr,"//ul[@id ='examListUl']/li[{}]/div[1]".format(j)).get_attribute('style')
        a = re.sub(r'^.*?"', "", a)
        url = re.sub(r'".*?$', "", a)
        qs_id = re.sub(r'^.*?=', "", url)
        qs_id = re.sub(r'&.*?$', "", qs_id)
        qs_id = qs_id[:5]
        url1 = 'https://account.bilibili.com'+url
        if qs_id in ['43737','43740']:
            try:
                uaList_i = random.choice(uaList)
                headers = {
                    'Accept':'*/*',
                    'Accept-Language':'zh-CN,zh;q=1',
                    'User-Agent': uaList_i,
                    'Connection': 'close'
                        }
                pic = s.get(url1,timeout=5,headers=headers)
                f = open(thread + '临时.png','wb')
                f.write(pic.content)
                f.close()
                a =[]
                for i in range(4):
                    im = Image.open(thread + '临时.png')
                    im = im.crop((left[i], top2[i], right[i], bottom2[i]))
                    h = im.histogram()
                    a.append(h)
                ans_h = ans_lib[qs_id]
                ans = a.index(ans_h) + 1
                xfind(dr,"//ul[@id ='examListUl']/li[{}]/div[2]/ul/li[{}]".format(j,ans)).click()
                time.sleep(random.randint(2,3))
            except Exception as e:
                fo = open('mislog.txt','a+')
                fo.write(str(e) +'\n')
                fo.write(url1+'\n')
                fo.flush()
                fo.close()
                return
        else:
            try:
                uaList_i = random.choice(uaList)
                headers = {
                    'Accept':'*/*',
                    'Accept-Language':'zh-CN,zh;q=1',
                    'User-Agent': uaList_i,
                    'Connection': 'close'
                        }
                pic = s.get(url1,timeout=5,headers=headers)
                f = open(thread + '临时.png','wb')
                f.write(pic.content)
                f.close()
                a =[]
                for i in range(4):
                    im = Image.open(thread + '临时.png')
                    im = im.crop((left[i], top[i], right[i], bottom[i]))
                    h = im.histogram()
                    a.append(h)
                ans_h = ans_lib[qs_id]
                ans = a.index(ans_h) + 1
                xfind(dr,"//ul[@id ='examListUl']/li[{}]/div[2]/ul/li[{}]".format(j,ans)).click()
                time.sleep(random.randint(2,3))
            except Exception as e:
                fo = open('mislog.txt','a+')
                fo.write(str(e) +'\n')
                fo.write(url1+'\n')
                fo.flush()
                fo.close()
                return
                
    xfind(dr,"//span[@class ='enterBut enterButdefault']").click()
    time.sleep(random.randint(1,3))
    drwait(dr,5,0.3,"//span[contains(@class_id ,'28')]")
    xfind(dr,"//span[contains(@class_id ,'28')]").click()
    drwait(dr,5,0.3,"//span[contains(@class_id ,'30')]")
    xfind(dr,"//span[contains(@class_id ,'30')]").click()
    drwait(dr,5,0.3,"//span[contains(@class_id ,'31')]")
    xfind(dr,"//span[contains(@class_id ,'31')]").click()
    drwait(dr,5,0.3,"//span[@class ='enterButdefault enterBut']")
    xfind(dr,"//span[@class ='enterButdefault enterBut']").click()
    time.sleep(2)
    try:
        drwait(dr, 3, 0.3, "//a[contains(text() ,'跳过，直接答题>')]")
        xfind(dr, "//a[contains(text() ,'跳过，直接答题>')]").click()
    except:
        pass
    time.sleep(3)
    return

def ans_zx(dr,ans_zx_lib,ranj,pos_lib,s,uaList,thread):
    left,right,top,bottom,top2,bottom2 = pos_lib
    for j in range(1,61):
        drwait(dr,5,0.3,"//ul[@id ='examListUl']/li[{}]/div[1]".format(j))
        a = xfind(dr,"//ul[@id ='examListUl']/li[{}]/div[1]".format(j)).get_attribute('style')
        a = re.sub(r'^.*?"', "", a)
        url = re.sub(r'".*?$', "", a)
        url1 = 'https://account.bilibili.com'+url
        qs_id = re.sub(r'^.*?=', "", url)
        qs_id = re.sub(r'&.*?$', "", qs_id)
        if qs_id in ['689','1178','3136','20518','20610','25212','25241','27245','28558','28707','28990'] or j in ranj:
            ans = random.randint(1,4)
            xfind(dr,"//ul[@id ='examListUl']/li[{}]/div[2]/ul/li[{}]".format(j,ans)).click()
            time.sleep(random.randint(2,3))
            continue
        try:
            uaList_i = random.choice(uaList)
            headers = {
                    'Accept':'*/*',
                    'Accept-Language':'zh-CN,zh;q=1',
                    'User-Agent': uaList_i,
                    'Connection': 'close'
                        }
            pic = s.get(url1,timeout=5,headers=headers)
            f = open(thread + '临时.png','wb')
            f.write(pic.content)
            f.close()
            a =[]
            for i in range(4):
                im = Image.open(thread + '临时.png')
                im = im.crop((left[i], top[i], right[i], bottom[i]))
                h = im.histogram()
                a.append(h)
            ans_h = ans_zx_lib[qs_id]
            ans = a.index(ans_h) + 1
            xfind(dr,"//ul[@id ='examListUl']/li[{}]/div[2]/ul/li[{}]".format(j,ans)).click()
            time.sleep(random.randint(2,3))
        except:
            ans = random.randint(1,4)
            xfind(dr,"//ul[@id ='examListUl']/li[{}]/div[2]/ul/li[{}]".format(j,ans)).click()
            time.sleep(random.randint(2,3))
    return
def xpos(thread):
    im = [0,0]
    pixel = [0,0]
    for i in range(2):
        im[i] = Image.open('Captchas\\'+'{}.png'.format(thread+str(i)))
        width = im[0].size[0]
        height = im[0].size[1]
        im[i] = im[i].crop((70, 0,width, height))
        width = im[0].size[0]
        height = im[0].size[1]
        
    for w in range(0, width):
        for h in range(0, height):
            pixel[0] = sum(im[0].getpixel((w, h)))
            pixel[1] = sum(im[1].getpixel((w, h)))
            cut = abs(pixel[0] - pixel[1])
            if cut > 150:
                return w,h
    else:
        print('无匹配项')
        return 0,0
def scroll(dr,length):
    js = "var q=document.body.scrollTop={}".format(length)
    dr.execute_script(js)
def captcha_get(dr,xpath,name,else_str):
    time.sleep(3)
    name = 'Captchas\\'+name
    elem = xfind(dr,xpath)
    size = elem.size
    location = elem.location     
    dr.save_screenshot(name)
    im = Image.open(name)
    left = elem.location['x']
    right = left + elem.size['width']
    top = elem.location['y'] +eval(else_str)
    bottom = top + elem.size['height']
    im = im.crop((left, top, right, bottom))
    im.save(name)      
    return
def moveto(thread,dr):
	scroll(dr,0)
	drwait(dr,5,0.3,"//div[@class ='gt_box']")
	a = xfind(dr,"//div[@class ='gt_slider_knob gt_show']")
	drwait(dr,5,0.3,"//div[@class ='gt_box']")
	captcha_get(dr,"//div[@class ='gt_box']",thread+'0.png','0')
	a.click()
	scroll(dr,0)
	time.sleep(4)
	captcha_get(dr,"//div[@class ='gt_box']",thread+'1.png','0')
	w,h = xpos(thread)
	ActionChains(dr).click_and_hold(a).perform()
	move_length = 1.14 * w + 67
	#y轴偏移随机值
	t = 0
	k_add = 0
	k = 0
	while move_length > 20:
		#y轴偏移随机值
		c = random.uniform(-0.5,0.5)
		#x轴递减值
		t += random.randint(1,2)*0.4
		#x轴移动值
		k = random.uniform(3,6)+t
		#y轴振幅值
		k_add += k
		#剩余长度
		move_length -= k
		y = math.sin(math.radians(k_add*3))*2+c
		ActionChains(dr).move_by_offset(k,y).perform()
		time_r = random.uniform(0.02,0.03)-0*t
		time.sleep(time_r)
		#print(move_length,k,y,time_r)
	t = 2
	while move_length > k:
		#y轴偏移随机值
		c = random.uniform(-0.5,0.5)
		#x轴递减值
		t += random.uniform(1,2)
		t_1 = -(t)*0.01
		#x轴移动值
		k = random.uniform(2,3) + t_1
		#y轴振幅值
		k_add += k
		#剩余长度
		move_length -= k
		y = math.sin(math.radians(k_add*3))*2+c
		ActionChains(dr).move_by_offset(k,y).perform()
		time_r =  random.uniform(0.02,0.03)-t_1*0.1
		time.sleep(time_r)
	time.sleep(random.uniform(0.01,0.03))
	ActionChains(dr).move_by_offset(move_length,math.sin(math.radians(k_add+move_length))*3+c).perform()
	time.sleep(random.uniform(0.01,0.03))
	ActionChains(dr).release().perform()


def movecheck(thread,dr):
    #检查通过
    result = 0
    attempt = 0
    while attempt < 15:
        try:
            drwait(dr,3,0.3,"//span[contains(text() ,'验证通过')]")
            break
        except:
            try:
                drwait(dr,3,0.3,"//span[contains(text() ,'出现错误')]")
                result = 1
                break
            except:
                attempt += 1
                xfind(dr,"//a[@class ='gt_refresh_button']").click()
                time.sleep(3)
                moveto(thread,dr)
    if attempt == 15:
        print("验证码怎么样也拖动不对")
        raise Exception("验证码怎么样也拖动不对")
    return result
