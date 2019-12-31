import pickle
import requests
import time
import json
import urllib3
import random
import os
import threading
import ua
headers = {
            'user-agent': ua.get_ua(),
            'accept-language': 'zh-CN,zh;q=0.9',
            'accept': 'application/json, text/plain, */*',
            'accept-encoding': 'gzip, deflate, br'
        }




requests.packages.urllib3.disable_warnings()

''' ------------------------------ SETTINGS ------------------------------ '''

base_url = "https://www.yeezysupply.com"
yeezy = {}
proxylist = []
cmd = "/usr/sbin/system_profiler SPHardwareDataType | fgrep 'Serial' | awk '{print $NF}'"
output = os.popen(cmd).read()
keyjson = json.loads(requests.get('http://www.tdleon.com/api/bypass.json').text)
path = os.path.expanduser('~')
brpath = path + '/brickrepublic'


def ip_test(ip):
    try:
        # ip = json.loads(ip)
        resp = requests.get(base_url, proxies=ip, timeout=10)
        if resp.status_code == 200:
            proxylist.append(ip)
            return None
        else:
            print(ip['https'] + '被ban')
            return None
    except:
        print(ip['https'] + '不可使用')
        return None


def ramdom_proxy():
    session = requests.session()
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    product = None
    variant = None
    while (product == None or variant == None):
        # Grab all the products on the site
        if len(proxylist) < 1:
            products = get_products(session)
        else:
            products = get_products(session, random.choice(proxylist))
        if products == None:
            print("未找到产品！")
            return None
        product = keyword_search(products, yeezy['keywords'].split(','))
        variant = find_size(product, random.choice(yeezy['size'].split(',')))
        if (product == None or variant == None):
            print("等待" + str(yeezy['delay']) + '秒')
            time.sleep(yeezy['delay'])
    return 1



def read_ip():
    filename = os.path.expanduser('~') + '/ip.txt'
    if os.path.exists(filename):
        with open(filename, 'r') as r:
            t = r.read().split('\n')
        threads = []
        for i in t:
            ip = {
                'https': 'https://' + i
            }
            t = threading.Thread(target=ip_test, args=(ip, ))
            threads.append(t)
        for t in threads:
            t.start()
        for t in threads:
            t.join()
    else:
        return None




def get_products(session, ip=None):
    if session == "":
        session = requests.session()
    link = base_url + "/products.json"

    try:

        r = session.get(link, verify=False, proxies=ip)
        if r.status_code == 430:
            if ip != None:
                print(ip['https'] + '被ban')
                if ip in proxylist:
                    proxylist.remove(ip)
            else:
                print('本地ip被ban')
            return None
        else:
            products_json = json.loads(r.text)
            products = products_json["products"]
            return products

    except requests.exceptions.ProxyError:
        if ip in proxylist:
            proxylist.remove(ip)
        print(ip['https'] + '不可使用')
        return None


def keyword_search(products, keywords):
    for product in products:
        if not 'F&F' in product["title"]:
            keys = 0
            for keyword in keywords:
                if(keyword.upper() in product["title"].upper()):
                    keys += 1
                if(keys == len(keywords)):
                    return product

def find_size(product, size):
    print('查找产品名称:', product['title'], '产品尺码:', size, '...')
    for variant in product["variants"]:
        if(size == variant["title"]):
            variant = str(variant["id"])
            return variant
    return None

def find_v():
    session = requests.session()
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    product = None
    variant = None
    while (product == None or variant == None):
        if len(proxylist) == 0:
            products = get_products(session, None)
        else:
            products = get_products(session, random.choice(proxylist))
        if products == None:
            return None
        product = keyword_search(products, yeezy['keywords'].split(','))
        variant = find_size(product, random.choice(yeezy['size'].split(',')))
        if (product == None or variant == None):
            print("等待" + str(yeezy['delay']) + '秒')
            time.sleep(yeezy['delay'])
    return None

def random_available(products):
    random_available_id = []
    for i in products:
        if 'F&F' in i['title']:
            pass
        else:
            # print(i['title'])
            for x in i['variants']:
                if x['available']:
                    random_available_id.append(str(x['id']))
    return random.choice(random_available_id)

def find_size(product, size):
    print('查找产品名称:', product['title'], '产品尺码:', size, '...')
    for variant in product["variants"]:
        if(size == variant["title"]):
            variant = str(variant["id"])
            return variant
    return None



def add_to_cart(session, variant, ip=None):

    # Add the product to cart
    link = base_url + "/cart/add.js?quantity=1&id=" + variant

    try:
        # ip = json.loads(ip)
        # print('add_to_cart' , ip)
        response = session.get(link, verify=False, proxies=ip)
        if response.status_code == 430:
            if ip in proxylist:
                if ip != None:
                    print(ip['https'] + '被ban')
                    if ip in proxylist:
                        proxylist.remove(ip)
                else:
                    print('本地ip被ban')
            return None
    except requests.exceptions.ProxyError:
        if ip in proxylist:
            proxylist.remove(ip)
        print(ip['https'] + '不可使用')
        return None


    # Return the response
    return response


def checkouts(link, cookie, session, ip=None):


    try:
        # ip = json.loads(ip)
        # print('checkouts', ip)
        get_in_line = session.get(link, verify=False, allow_redirects=True, cookies=cookie, proxies=ip)
        if get_in_line.status_code == 430:
            if ip in proxylist:
                if ip != None:
                    print(ip['https'] + '被ban')
                    if ip in proxylist:
                        proxylist.remove(ip)
                else:
                    print('本地ip被ban')
            return None
    except requests.exceptions.ProxyError:
        if ip in proxylist:
            proxylist.remove(ip)
        print(ip['https'] + '不可使用')
        return None

    if 'queue' in get_in_line.url:
        print("进入队列")
        print(time.asctime()[11:19], '排队开始')
        while True:
            time.sleep(14)
            queue = session.get('https://yeezysupply.com/checkout/poll?js_poll=1', proxies=ip)
            print(queue.status_code)
            if queue.status_code == 200:
                print(time.asctime()[11:19], '排队结束')
                break


    try:
        # print('get_in_line' , ip)
        res = session.get(get_in_line.url, proxies=ip)
        if res.status_code == 430:
            if ip in proxylist:
                if ip != None:
                    print(ip['https'] + '被ban')
                    if ip in proxylist:
                        proxylist.remove(ip)
                else:
                    print('本地ip被ban')
            return None
    except requests.exceptions.ProxyError:
        if ip in proxylist:
            proxylist.remove(ip)
        print(ip['https'] + '不可使用')
        return None

    return res

def submit_customer_info(session, cookie_jar, ip=None):
    # Submit the customer info
    payload = {
        "utf8": u"\u2713",
        "_method": "patch",
        "authenticity_token": "",
        "previous_step": "contact_information",
        "step": "shipping_method",
        "checkout[email]": yeezy['email'],
        "checkout[buyer_accepts_marketing]": "0",
        "checkout[shipping_address][first_name]": yeezy['first_name'],
        "checkout[shipping_address][last_name]": yeezy['last_name'],
        "checkout[shipping_address][company]": "",
        "checkout[shipping_address][address1]": yeezy['address'],
        "checkout[shipping_address][address2]": yeezy['address2'],
        "checkout[shipping_address][city]": yeezy['city'],
        "checkout[shipping_address][country]": 'United States',
        "checkout[shipping_address][province]": yeezy['province'],
        "checkout[shipping_address][zip]": yeezy['postal_code'],
        "checkout[shipping_address][phone]": yeezy['phone'],
        "checkout[remember_me]": "0",
        "checkout[client_details][browser_width]": "1710",
        "checkout[client_details][browser_height]": "1289",
        "checkout[client_details][javascript_enabled]": "1",
        "button": ""
    }

    # 进入队列
    link = base_url + "//checkout.json"
    check_out = checkouts(link, cookie_jar, session, ip)

    if check_out == None:
        return (None, None)

    # Get the checkout URL
    link = check_out.url
    checkout_link = link

    # POST the data to the checkout URL

    try:
        # ip = json.loads(ip)
        # print('submit_customer_info', ip)
        response = session.post(link, cookies=cookie_jar, data=payload, verify=False, proxies=ip)
        if response.status_code == 430:
            if ip in proxylist:
                if ip != None:
                    print(ip['https'] + '被ban')
                    if ip in proxylist:
                        proxylist.remove(ip)
                else:
                    print('本地ip被ban')
            return (None, None)
    except requests.exceptions.ProxyError:
        if ip in proxylist:
            proxylist.remove(ip)
        print(ip['https'] + '不可使用')
        return (None, None)

    return (response, checkout_link)



def open_chrome(cookies, url):
    from selenium import webdriver
    option = webdriver.ChromeOptions()
    option.add_argument('disable-infobars')
    # option.add_argument("--user-data-dir=/Users/tangdongliang/Library/Application Support/Google/Chrome")
    option.add_experimental_option('excludeSwitches', ['enable-automation'])
    try:
        driver = webdriver.Chrome(options=option)
    except:
        driver = webdriver.Chrome(executable_path=os.path.expanduser('~') + '/brickrepublic/chromedriver', options=option)
    driver.get('https://yeezysupply.com/')
    for key, value in cookies.items():
        driver.add_cookie({'name': key, 'value': value})
    driver.get(url)
    time.sleep(3600)


def save_session(bypass, ip=None, session=None):
    # print('ip为', ip)
    if session == None:
        session = requests.session()
        session.headers = headers
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    if bypass:
        variant = random_available(get_products(session))
    else:
        product = None
        variant = None
        while (product == None or variant == None):
            # Grab all the products on the site
            products = get_products(session, ip)
            if products == None:
                return None
            # Grab the product defined by keywords
            product = keyword_search(products, yeezy['keywords'].split(','))
            variant = find_size(product, random.choice(yeezy['size'].split(',')))
            if (product == None or variant == None):
                print("等待"+str(yeezy['delay'])+'秒')
                time.sleep(yeezy['delay'])

    r = add_to_cart(session, variant, ip)
    # Store the cookies
    cj = r.cookies

    # Submit customer info and get the checkout url

    (r, checkout_link) = submit_customer_info(session, cj, ip)

    if r == None:
        return None
    # Get the payment gateway ID
    link = checkout_link


    try:
        # ip = json.loads(ip)
        # print('save_session', ip)
        r = session.get(link, cookies=cj, verify=False, proxies=ip)
        if r.status_code == 430:
            if ip in proxylist:
                if ip != None:
                    print(ip['https'] + '被ban')
                    if ip in proxylist:
                        proxylist.remove(ip)
                else:
                    print('本地ip被ban')
            return None
    except requests.exceptions.ProxyError:
        if ip in proxylist:
            proxylist.remove(ip)
        print(ip['https'] + '不可使用')
        return None

    if 'cart' in checkout_link:
        print("请重试链接不可用")
        time.sleep(10)
        return None
    if not 'queue' in checkout_link:
        print('结算地址：', checkout_link)
    if bypass:
        path = os.path.expanduser('~') + '/brickrepublic/bypass/'
    else:
        path = os.path.expanduser('~') + '/brickrepublic/checkout/'
    try:
        filename = path + checkout_link.split('checkouts/')[1].replace('/stock_problems', '') + '.gyb'
        with open(filename, 'wb') as f:
            pickle.dump(session, f)
    except:
        print('无效地址')
        time.sleep(10)
    return r

def br_bypass(session):
    session.get('https://yeezysupply.com/cart/clear')
    # print(json.loads(session.get('https://yeezysupply.com/cart.js').text)['token'])
    checkout = save_session(bypass=False, session=session)
    if checkout == None:
        return None
    cookies = requests.utils.dict_from_cookiejar(checkout.cookies)
    try:
        open_chrome(cookies, checkout.url)
    except:
        print("需要将下载对应的版本 https://sites.google.com/a/chromium.org/chromedriver/home 放到  "+os.path.expanduser('~') + '/brickrepublic/  目录下')
        time.sleep(10)

def use_bypass(bypass):
    if bypass:
        path = os.path.expanduser('~') + '/brickrepublic/bypass/'
    else:
        path = os.path.expanduser('~') + '/brickrepublic/checkout/'
    list = []
    for i in os.listdir(path):
        if 'gyb' in i:
            list.append(i)
    if len(list) < 1:
        print('无结算地址可用请先去排队！')
        time.sleep(10)
        return None
    for x, y in enumerate(list):
        print(x+1, ':', 'https://yeezysupply.com/17655971/checkouts/' + y.replace('.gyb', ''))
    while True:
        ifdata = True
        listnum = input("输入编号(用空格分开):")
        list1 = []
        for i in listnum.split(' '):
            if i.isdigit():
                if int(i) > 0 and int(i) <= len(list):
                    if not list[int(i) - 1] in list1:
                        list1.append(list[int(i) - 1])
                else:
                    ifdata = False
        if ifdata:
            break
        print('输入有误!请重新输入！')
    threads = []
    for x in list1:
        bpurl = 'https://yeezysupply.com/17655971/checkouts/' + x.replace('.gyb', '')
        with open(path + x, 'rb') as f:
            session = pickle.load(f)
        t = threading.Thread(target=bypass_checkout, args=(session, bpurl, bypass))
        threads.append(t)
    for t in threads:
        t.start()
    for t in threads:
        t.join()

def bypass_checkout(ss, url, bypass):#ip待添加

    if bypass:
    # print('ip为', ip)
        print("bypass结算")
        ss.get('https://yeezysupply.com/cart/clear')
        product = None
        variant = None
        while (product == None or variant == None):
            # Grab all the products on the site
            products = get_products(ss)
            if products == None:
                return None
            # Grab the product defined by keywords
            product = keyword_search(products, yeezy['keywords'].split(','))
            variant = find_size(product, random.choice(yeezy['size'].split(',')))
            if (product == None or variant == None):
                print("等待" + str(yeezy['delay']) + '秒')
                time.sleep(yeezy['delay'])
        #加车
        add_to_cart(ss, variant)
    else:
        print("直接结算")

    checkout = ss.get(url)
    # print(json.loads(session.get('https://yeezysupply.com/cart.js').text)['token'])
    cookies = requests.utils.dict_from_cookiejar(checkout.cookies)
    try:
        open_chrome(cookies, checkout.url)
    except:
        print("需要将下载对应的版本 https://sites.google.com/a/chromium.org/chromedriver/home 放到  "+os.path.expanduser('~') + '/brickrepublic/  目录下')
        time.sleep(10)

def chose():
    selection_number = input('\n\n1:制作bypass(发售前使用 默认3个)\n2:使用bypass结算\n3:排队(发售时使用 默认为proxy个数 无proxy默认3个)\n4:结算\n输入其他退出\n请输入:')
    list1 = []
    for i in selection_number.split(' '):
        if i.isdigit():
            list1.append(int(i))
    if len(list1) > 0:
        list1.append(3)
        if list1[0] == 1:
            threads = []
            for i in range(list1[1]):
                t = threading.Thread(target=save_session, args=(True,))
                threads.append(t)
            for t in threads:
                t.start()
            for t in threads:
                t.join()
            return chose()
        elif list1[0] == 2:
            find_v()
            use_bypass(True)
        elif list1[0] == 3:
            if ramdom_proxy() == None:
                return None
            rangelist = proxylist
            print(list1)
            if len(proxylist) < 1:
                rangelist = range(list1[1])
            threads = []
            print("查找产品成功 正在创建" + str(len(rangelist)) + "条队列")
            for i in rangelist:
                if type(i) == int:
                    i = None
                t = threading.Thread(target=save_session, args=(False, i))
                threads.append(t)
            for t in threads:
                t.start()
            for t in threads:
                t.join()
            chose()
        elif list1[0] == 4:
            use_bypass(False)
        else:
            return None
    return None

def config():
    if os.path.exists(os.path.expanduser('~') + '/yeezy.txt'):
        with open(os.path.expanduser('~') + '/yeezy.txt', 'r') as r:
            setting = r.read().replace(': ', ':')
            # print(setting)
            for i in setting.split('\n'):
                if not i == '':
                    yeezy[i.split(':')[0].lower()] = i.split(':')[1].upper()
        if yeezy['delay'].isdigit():
            yeezy['delay'] = int(yeezy['delay'])
        else:
            yeezy['delay'] = int(1)
        print('\n\n')
        print('关键字:', yeezy['keywords'].split(','))
        print('尺码:', yeezy['size'].split(','))
        print('延迟:', yeezy['delay'], '秒')
        print('邮箱:', yeezy['email'])
        print('名字:', yeezy['first_name'])
        print('姓名', yeezy['last_name'])
        print('地址1:', yeezy['address'])
        print('地址2:', yeezy['address2'])
        print('城市:', yeezy['city'])
        print('省份:', yeezy['province'])
        print('国家:', 'United States')
        print('邮编:', yeezy['postal_code'])
        print('电话:', yeezy['phone'])
        products = get_products('')
        if products == None:
            return None
        # Grab the product defined by keywords
        product = keyword_search(products, yeezy['keywords'].split(','))
        if product == None:
            print('\n未在发售接口找到关键字：请参考以下产品及其尺码 修改关键字 注意：F&F 亲友产品不可购买！\n\n')
            for i in products:
                print(i['title'] + '------------可以用尺码为:', end="")
                for x in i['variants']:
                    if x['available'] == True:
                        print(" " + x['title'], end="")
                print("")
            print('\n未在发售接口找到关键字：请参考以上产品及其尺码 修改关键字 注意：F&F 亲友产品不可购买！\n\n')
            time.sleep(300)
            return None
        print('\n读取proxy中...')
        read_ip()
        print('成功获取'+str(len(proxylist))+'个proxy')
        return chose()
    else:
        print('未找到配置文件!!'+'需要将yeezy.txt放进   '+os.path.expanduser('~') + '  目录下')
        time.sleep(10)
        return None

def find_v():
    session = requests.session()
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    product = None
    variant = None
    while (product == None or variant == None):
        if len(proxylist) == 0:
            products = get_products(session, None)
        else:
            products = get_products(session, random.choice(proxylist))
        if products == None:
            return None
        product = keyword_search(products, yeezy['keywords'].split(','))
        variant = find_size(product, random.choice(yeezy['size'].split(',')))
        if (product == None or variant == None):
            print("等待" + str(yeezy['delay']) + '秒')
            time.sleep(yeezy['delay'])
    return None


def main_bot():
    print('\n读取配置中...')
    config()

def inptutcode(key=None):
    word = ''
    if key == None:
        word = '\n激活码有误请联系管理员'
        print('\n\n机器码:' + output)
        key = input("请输入激活码：")
    if key in keyjson:
        print(keyjson[key])
        if keyjson[key] + '\n' == output:
            if not os.path.exists(brpath + '/bypass/'):
                os.makedirs(brpath + '/bypass/')
            if not os.path.exists(brpath + '/checkout/'):
                os.makedirs(brpath + '/checkout/')
            with open(brpath + '/key', 'w') as w:
                w.write(key)
            print('已经激活！')
            main_bot()
        else:
            print("\n激活码已被使用")
            time.sleep(10)
            return None
    else:
        print(word)
        return inptutcode(None)


def active():
    if os.path.exists(brpath + '/key'):
        with open(brpath + '/key', 'r') as r:
            key = r.read()
        return inptutcode(key)
    else:
        return inptutcode()

''' ------------------------------- MODULES ------------------------------- '''

active()