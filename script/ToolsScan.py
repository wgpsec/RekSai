import requests
from bs4 import BeautifulSoup
import subprocess
import os
import sys
import re


class GetIG(object):
    def __init__(self,domain):
        self.path = os.getcwd() # 获取路径
        self.domain_list = [] # ip反查域名列表
        self.ip = [] # 保存输入ip反查的信息
        self.origin = [] #  保存域名查询的信息
        self.save_list = ['/domain.json','/port.json','/c.json']
        self.agreement = ['http://','https://']
        if domain.find('www') != -1:
            url = re.findall(r'\w{3}\..*\..{3,9}', domain)[0]
            for agreement in self.agreement:
                if subprocess.getoutput('curl --connect-timeout 3 -o /dev/null -s -w "%%{http_code}\n" %s%s' % (agreement,url)) == '200':
                    self.domain = agreement + url
                    self.result =  self.path + '/result/' + url
                else:
                    pass
        else:
            url =  re.findall(r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}',domain)[0]
            for agreement in self.agreement:
                if subprocess.getoutput('curl --connect-timeout 3 -o /dev/null -s -w "%%{http_code}\n" %s%s' % (agreement,url)) == '200':
                    self.domain = agreement + url
                    self.result =  self.path + '/result/' + url
                else:
                    pass


    def GetAddr(self):
        if 'gov' in self.domain:
            print('\033[31m[ERROR]\033[0m 请不要触碰法律！')
            sys.exit(0)
        else:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36'
            }
            if len(re.findall(r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}',self.domain)) > 0:
                print('\033[31m[WARR]\033[0m 反查IP中')
                url = 'https://webscan.cc/ip_' + re.findall(r'\d{1,3}.\d{1,3}.\d{1,3}.\d{1,3}',self.domain)[0]
                data = requests.get(url, headers=headers,verify=False).text
                soup = BeautifulSoup(data, 'html.parser')
                for word in soup.find_all('li', class_='J_link'):
                    self.domain_list.append(word)
                self.ip.append(re.findall(r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}',self.domain)[0])
                self.origin.append('纯IP不判断CDN')
                return ['纯IP不判断CDN',re.findall(r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}',self.domain)[0]]
            else:
                url = 'http://seo.chinaz.com/' + re.findall(r'\w{3}.\w{1,50}.\w{2,3}',self.domain)[0]
                data = requests.get(url, headers=headers).text
                soup = BeautifulSoup(data, 'html.parser')
                for word in soup.find_all('span'):
                    if 'IP：' in word:
                        ip = re.findall(r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}', word.text)[0]
                        porint = word.text.find('[')
                        origin = word.text[porint + 1:-1]
                        self.ip.append(ip)
                        self.origin.append(origin)
                return [origin,ip]

    def CheckFile(self):
        print('\n\033[33m[FILE]\033[0m 生成工作目录')
        if os.path.exists(self.result) == True:
            return '\033[32m[NICE]\033[0m 目录存在，覆盖扫描中'
        else:
            os.makedirs(self.result)
            make = open('%s/summary.txt' % self.result, 'w')
        return '\033[32m[NICE]\033[0m 工作目录创建成功'

    def UseOneforall(self):
        if self.domain.find('www') != -1:
            print('\033[31m[WARR]\033[0m 子域名扫描线程启动')
            scan = subprocess.getoutput("cd tools/OneForAll;"
                                        "python3 oneforall.py  --format json  --path=%s/domain.json --target %s run" % (
                                        self.result,re.findall(r'\w{3}.*.{3,9}',self.domain)))
            return '\033[32m[NICE]\033[0m 子域名扫描结束'
        else:
            return '\033[31m[WARR]\033[0m 纯IP不判断子域，进行下一步扫描'

    def UseJsfinder(self):
        pass

    def GetPort(self, domain):
        print('\033[31m[WARR]\033[0m 端口扫描线程启动')
        IP_ADDR = self.ip[0]
        scan = subprocess.getoutput('cd %s/tools/masscan/bin;'
                                    './masscan %s -p 0-65535 --rate 2500 -oJ %s/port.json' % (self.path,IP_ADDR, self.result))
        return '\n\033[32m[NICE]\033[0m 端口扫描结束'
    
    def CheckCDN(self, domain):
        print('\033[31m[WARR]\033[0m 判断CDN中...')
        print('\033[32m[NICE]\033[0m 来源为：%s' % self.origin[0])
        if len(re.findall(r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}',domain)) < 0:
            CDN_list = ['美国 CloudFlare节点','Stackpath','北京市 金山云bgp数据中心','北京市 阿里云bgp数据中心']
            for cnd in CDN_list:
                if self.origin[0].find(cnd) != -1:
                    return False
        else:
            return True

    def UseDirmap(self):
        print('\033[31m[WARR]\033[0m 敏感目录扫描线程启动： %s ' % self.domain)
        scan = subprocess.getoutput('cd tools/dirmap;'
                         'python3 dirmap.py -i %s -lcf\n' % self.domain)

        return '\033[32m[NICE]\033[0m 敏感路径扫描结束 '

    def GetC(self, domain):
        if self.CheckCDN(domain):
            print('\033[32m[NICE]\033[0m 当前网站不存在CDN！<--(佛系判断，建议看来源自己判断...)\n'
                      '\033[31m[WARR]\033[0m C段线程扫描启动')
            ip = self.ip[0]
            point_site = ip.rfind('.')
            c_ip = ip[0:point_site] + '.0/24'

            scan = subprocess.getoutput(
                'cd %s/tools/masscan/bin;'
                './masscan %s -p 80 --rate 2500 -oJ %s/c.json'
                % (self.path,c_ip, self.result))
            return  '\033[32m[NICE]\033[0m C段扫描结束\n'
        else:
            return '\033[31m[WARR]\033[0m 当前网站存在CDN，不建议继续收集,退出当前Domain扫描'

    def GetCPort(self):
        ip_list = []
        save = '/c.json'
        try:
            with open('%s%s'  % (self.result, save), 'r', encoding="utf-8") as f:
                date = eval(f.read())
                i = 0
                while i < len(date):
                    ip = date[i]['ip']
                    ip_list.append(ip)
                    i += 1
            f.close()
        except:
            pass
        if len(ip_list) < 10:
            print('\033[32m[NICE]\033[0m C段IP为：%s\n       开始扫描C段IP开放的端口！\n' % ip_list)
            for ip in ip_list:
                make = subprocess.getoutput('mkdir %s/c_port' % self.result)
                scan = subprocess.getoutput('cd %s/tools/masscan/bin;'
                                            './masscan %s -p 0-65535 --rate 2500 -oJ %s/c_port/%s.json' % (self.path,ip,self.result,ip))
        else:
            print('\033[33m[WARR]\033[0m C段数量超过10个，不建议扫描，可以在保存结果中查看C段IP！')

        return '\033[32m[NICE]\033[0m C段IP所有端口扫描结束'

    def Result(self):
        ip_url_list = [] # IP反查URL
        subdomain_list = [] # 子域名列表
        port_list = [] # 当前网站开放端口
        c_port_list = [] # C段IP开放端口
        c_ip_list = [] # C段IP列表
        c_ip_port_list = []
        sensitive_directory = []

        print('\n\033[32m[NICE]\033[0m 整理所有数据中...')

        for domain in self.domain_list:
            print('\033[32m[DOMAIN]\033[0m IP反查域名为：%s' % domain.a.text)
            ip_url_list.append(domain.a.text)

        for save in self.save_list:
            if save == '/domain.json':
                try:
                    if self.domain.find('www') != -1:
                        with open('%s%s' % (self.result, save), 'r+', encoding='UTF-8') as f:
                            json = f.readlines()
                            if len(json) != 0:
                                print('\033[33m[Domain]\033[0m 子域测活中')
                                for i in range(0, len(json)):
                                    code_list = [302,200,301,401]
                                    url = json[i].replace('\n', '')
                                    make = subprocess.getoutput('curl --connect-timeout 3 -o /dev/null -s -w "%%{http_code}\n" %s' % url)
                                    if int(make) in code_list:
                                        print('\033[33m[Domain]\033[0m 子域存活： %s' % json[i].replace('\n', ''))
                                        subdomain_list.append(json[i].replace('\n',''))
                                f.close()

                            else:
                                print('\033[33m[CPORT]\033[0m 当前域名没有找到子域')
                                f.close()

                            print('\033[32m[NICE]\033[0m 子域处理完毕！\n')
                    else:
                        print('\033[32m[NICE]\033[0m 纯IP不整理子域\n')
                except:
                    pass
            elif save == '/port.json':
                try:
                    with open('%s%s' % (self.result,save),'r+',encoding='UTF-8') as f:
                        date = eval(f.read())
                        i = 0
                        while i < len(date):
                            port = date[i]["ports"][0]['port']
                            print('\033[33m[CPORT]\033[0m 当前域名得到端口：%s:%s' % (self.domain,port))
                            port_list.append(port)
                            i += 1
                except:
                    print('\033[33m[CPORT]\033[0m 当前网站没有端口开放')
                    sys.exit(0)
                f.close()

                print('\033[32m[NICE]\033[0m 端口处理完毕！\n')

            elif save == '/c.json':
                try:
                    with open('%s%s' % (self.result, save), 'r+', encoding='UTF-8') as f:
                        date = eval(f.read())
                        i = 0
                        while i < len(date):
                            ip = date[i]['ip']
                            c_ip_list.append(ip)
                            print('\033[32m[NICE]\033[0m 找到C段IP：%s' % ip)
                            i += 1
                            f.close()

                    print('\033[32m[NICE]\033[0m C段处理完毕！\n')
                    print('\033[33m[WARR]\033[0m C段端口处理中')
                    for ip in c_ip_list:
                        print('\n\033[33m[CPORT]\033[0m %s的端口：' % ip)
                        with open('%s/c_port/%s.json' % (self.result,ip), 'r+', encoding='UTF-8') as f:
                            date = eval(f.read())
                            i = 0
                            while i < len(date):
                                port = date[i]["ports"][0]['port']
                                print('\033[33m[CPORT]\033[0m 找到端口：%s:%s' % (ip, port))
                                c_port = str(ip) + ':' + str(port)
                                c_ip_port_list.append(c_port)
                                i += 1
                            f.close()
                except:
                    print("\033[32m[WARR]\033[0m C段端口未找到")

        print('\n\033[33m[WARR]\033[0m 开始处理敏感文件路径：\n')
        try:
            if self.domain.find('www') == -1:
                print(re.findall(r'\d{1,3}.\d{1,3}.\d{1,3}.\d{1,3}',self.domain))
                with open('%s/tools/dirmap/output/%s.txt' % (self.path,re.findall(r'\d{1,3}.\d{1,3}.\d{1,3}.\d{1,3}',self.domain)[0])) as f:
                    data = f.readlines()
                    i = 0
                    while i < len(data):
                        url = re.findall(r'[a-zA-z]+://[^\s]*', data[i])
                        print('\033[33m[DOMAIN]\033[0m 找到敏感路径：%s' % url[0])
                        sensitive_directory.append(url[0])
                        i += 1
                    f.close()
            else:
                print(re.findall(r'\w{3}.\w{1,50}.\w{2,3}',self.domain)[0])
                with open('%s/tools/dirmap/output/%s.txt' % (self.path, re.findall(r'\w{3}.\w{1,50}.\w{2,3}',self.domain)[0])) as f:
                    data = f.readlines()
                    i = 0
                    print(data[1])
                    while i < len(data):
                        url = re.findall(r'[a-zA-z]+://[^\s]*', data[i])
                        print('\033[33m[DOMAIN]\033[0m 找到敏感路径：%s' % url[0])
                        sensitive_directory.append(url[0])
                        i += 1
                    f.close()
        except:
            pass

        with open('%s/summary.txt' % self.result, 'r+') as f:
            if self.domain.find('www') != -1:
                f.write('\n当前网站whois信息\n')
                whois = subprocess.getoutput('whois %s' % re.findall(r'\w{3}.\w{1,50}.\w{2,3}',self.domain)[0].replace('www.',''))
                f.write('\t'+whois+'\n')
                f.write('\n当前网站C段地址：\n')
                for i in c_ip_list:
                    f.write('\t'+str(i)+'\n')
                f.write('\n查找到的子域名：\n')
                for i in subdomain_list:
                    f.write('\t'+i+'\n')
                f.write('\n当前C段IP开放端口：\n')
                for i in c_ip_port_list:
                    f.write('\t'+i+'\n')
                f.write('\n当前网站开放端口：\n')
                for i in port_list:
                    f.write('\t'+self.domain+':'+str(i)+'\n')
                f.write('\n扫描到的敏感路径：\n')
                for i in sensitive_directory:
                    f.write('\t'+i+'\n')
            else:
                f.write('\n当前网站C段地址：\n')
                for i in c_ip_list:
                    f.write('\t'+str(i)+'\n')
                f.write('\nIP反查的域名为：\n')
                for i in ip_url_list:
                    f.write('\t'+i+'\n')
                f.write('\n当前C段IP开放端口：\n')
                for i in c_ip_port_list:
                    f.write('\t'+i+'\n')
                f.write('\n查找到的开放端口：\n')
                for i in port_list:
                    f.write('\t'+self.domain+':'+str(i)+'\n')
                f.write('\n扫描到的敏感路径：\n')
                for i in sensitive_directory:
                    f.write('\t'+i+'\n')
            f.close()

        return '\n\033[32m[NICE]\033[0m 数据处理完毕！整理的数据存放在%s目录下的summary.txt文件中' % self.result