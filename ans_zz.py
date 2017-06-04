from fanc import *
def main(dr):
    #加载位置
    left = [16,15,16,17]
    right = [68,67,68,69]
    top = [22,36,50,64]
    bottom = [34,48,62,76]
    top2 = [42,56,70,84]
    bottom2 = [54,68,82,96]
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
    ranj = list(range(1,61))
    random.shuffle(ranj)
    ranj = ranj[:random.randint(5,15)]
    #切换到答题页
    url = 'https://account.bilibili.com/answer/base'
    dr.get(url)
    #输入任意键开始答题
    dr.delete_cookie('CNZZDATA2724999')
    s = requests.session()
    for i in dr.get_cookies():
        s.cookies.set(i['name'],i['value'], path=i['path'],domain=i['domain'])
    for j in range(1,41):
        drwait(5,0.3,"//ul[@id ='examListUl']/li[{}]/div[1]".format(j))
        a = xfind("//ul[@id ='examListUl']/li[{}]/div[1]".format(j)).get_attribute('style')
        a = re.sub(r'^.*?"', "", a)
        url = re.sub(r'".*?$', "", a)
        qs_id = re.sub(r'^.*?=', "", url)
        qs_id = re.sub(r'&.*?$', "", qs_id)
        qs_id = qs_id[:5]
        url1 = 'https://account.bilibili.com'+url
        if qs_id in ['43737','43740']:
            pic = s.get(url1)
            f = open('临时.png','wb')
            f.write(pic.content)
            f.close()
            a =[]
            for i in range(4):
                im = Image.open('临时.png')
                im = im.crop((left[i], top2[i], right[i], bottom2[i]))
                h = im.histogram()
                a.append(h)
            ans_h = ans_lib[qs_id]
            ans = a.index(ans_h) + 1
            xfind("//ul[@id ='examListUl']/li[{}]/div[2]/ul/li[{}]".format(j,ans)).click()
            time.sleep(random.randint(2,3))
        else:
            pic = s.get(url1)
            f = open('临时.png','wb')
            f.write(pic.content)
            f.close()
            a =[]
            for i in range(4):
                im = Image.open('临时.png')
                im = im.crop((left[i], top[i], right[i], bottom[i]))
                h = im.histogram()
                a.append(h)
            ans_h = ans_lib[qs_id]
            ans = a.index(ans_h) + 1
            xfind("//ul[@id ='examListUl']/li[{}]/div[2]/ul/li[{}]".format(j,ans)).click()
            time.sleep(random.randint(2,3))
    xfind("//span[@class ='enterBut enterButdefault']").click()
    drwait(5,0.3,"//span[contains(@class_id ,'28')]")
    xfind("//span[contains(@class_id ,'28')]").click()
    drwait(5,0.3,"//span[contains(@class_id ,'30')]")
    xfind("//span[contains(@class_id ,'30')]").click()
    drwait(5,0.3,"//span[contains(@class_id ,'31')]")
    xfind("//span[contains(@class_id ,'31')]").click()
    drwait(5,0.3,"//span[@class ='enterButdefault enterBut']")
    xfind("//span[@class ='enterButdefault enterBut']").click()
    time.sleep(3)
    for j in range(1,61):
        drwait(5,0.3,"//ul[@id ='examListUl']/li[{}]/div[1]".format(j))
        a = xfind("//ul[@id ='examListUl']/li[{}]/div[1]".format(j)).get_attribute('style')
        a = re.sub(r'^.*?"', "", a)
        url = re.sub(r'".*?$', "", a)
        url1 = 'https://account.bilibili.com'+url
        qs_id = re.sub(r'^.*?=', "", url)
        qs_id = re.sub(r'&.*?$', "", qs_id)
        if qs_id in ['689','1178','3136','20518','20610','25212','25241','27245','28558','28707','28990'] or j in ranj:
            ans = random.randint(1,4)
            xfind("//ul[@id ='examListUl']/li[{}]/div[2]/ul/li[{}]".format(j,ans)).click()
            time.sleep(random.randint(2,3))
            continue
        try:
            pic = s.get(url1)
            f = open('临时.png','wb')
            f.write(pic.content)
            f.close()
            a =[]
            for i in range(4):
                im = Image.open('临时.png')
                im = im.crop((left[i], top[i], right[i], bottom[i]))
                h = im.histogram()
                a.append(h)
            ans_h = ans_zx_lib[qs_id]
            ans = a.index(ans_h) + 1
            xfind("//ul[@id ='examListUl']/li[{}]/div[2]/ul/li[{}]".format(j,ans)).click()
            time.sleep(random.randint(2,3))
        except:
            ans = random.randint(1,4)
            xfind("//ul[@id ='examListUl']/li[{}]/div[2]/ul/li[{}]".format(j,ans)).click()
            time.sleep(random.randint(2,3))
        
    n = input('请选择未选题目,滑动验证码并完成答题，任意键继续下一个号,输入88退出')
    dr.delete_all_cookies()
    return n
