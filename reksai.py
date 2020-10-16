#!/usr/bin/python
# -*- coding: utf-8 -*-

from script import Bander,ToolsConfig,ToolsScan
import time
import subprocess
import threading
import readline
import os

seeting = ToolsConfig.Config()
seeting.gopath()
seeting.tools()

def get_domain():
    print (domain.UseOneforall())

def get_dir():
    print(domain.UseDirmap())

def get_port():
    print(domain.GetPort(url))

def get_other():
    print(domain.GetC(url),
          domain.GetCPort())


while True:
    if __name__ == '__main__':
        while True:
            try:
                if os.path.isfile(os.getcwd() + '/url.txt') == True:
                    with open('url.txt', 'r+') as f:
                        s = 0
                        data = f.readlines()
                        while s < len(data):
                            url = data[s].replace('\n','')
                            re1 = subprocess.getoutput('curl --connect-timeout 3 -o /dev/null -s -w "%%{http_code}\n" http://%s' % url)
                            re2 = subprocess.getoutput('curl --connect-timeout 3 -o /dev/null -s -w "%%{http_code}\n" https://%s' % url)
                            if  re1 == '200' or re2 == '200' :
                                domain = ToolsScan.GetIG(url)
                                print('\033[32m[DOMAIN IP]\033[0m The current domain  was resolved successfully IPADD：%s' % domain.GetAddr()[1])
                                print(domain.CheckFile())
                                print('\n\033[34m[SCAN]\033[0m 开始多线程扫描 %s/%s\n' % (s + 1, len(data)))
                                threading_list = [get_dir, get_domain, get_port, get_other]
                                threading_join = []
                                for i in threading_list:
                                    t = threading.Thread(target=i)
                                    threading_join.append(t)
                                for t in threading_join:
                                    t.start()
                                for t in threading_join:
                                    t.join()

                                print(domain.Result())
                                s += 1
                            else:
                                s += 1
                                print('域名失活，下一个')
                                continue
                        else:
                            title = "所有任务扫描结束！你还在等什么？"
                            content = "你在服务器上批量的扫描任务已经完成啦！快去看看结果吧！"
                            seeting.servertool(title, content)
                            sys.exit()

                        f.close()

                else:
                    url = input('\033[32m[INPUT]\033[0m Input Domain：')
                    start_time = time.time()
                    domain = ToolsScan.GetIG(url)
                    print('\033[32m[DOMAIN IP]\033[0m The current domain  was resolved successfully IPADD：%s' % domain.GetAddr()[1])
                    print(domain.CheckFile())
                    print('\n\033[34m[SCAN]\033[0m 开始多线程扫描\n')
                    threading_list = [get_dir, get_domain, get_port, get_other]
                    threading_join = []
                    for i in threading_list:
                        t = threading.Thread(target=i)
                        threading_join.append(t)
                    for t in threading_join:
                        t.start()
                    for t in threading_join:
                        t.join()

                    print(domain.Result())
                    end_time = time.time()
                    print('\n\033[34m[SCAN]\033[0m 总耗时%s S' % (end_time - start_time))

            except Exception as information:
                title = "出现未知异常！"
                content = "出现了未知异常，请将你的错误信息提交到github上哦！"
                seeting.servertool(title, content)
                sys.exit()