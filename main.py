#!/usr/bin/python
# -*- coding: utf-8 -*-

from script import Bander,ToolsConfig,ToolsScan
import time
import threading
import readline

seeting = ToolsConfig.Config()
seeting.gopath()
seeting.tools()

def get_domain():
    print (domain.GetDomain())

def get_dir():
    print(domain.UseDirmap())

def get_port():
    print(domain.GetPort(url))

def get_other():
    print(domain.GetC(url),
          domain.GetCPort())

while True:
    if __name__ == '__main__':
        try:
            start_time = time.time()
            url = input('\033[32m[INPUT]\033[0m Input Domain：')
            domain = ToolsScan.GetIG(url)
            print('\033[32m[DOMAIN IP]\033[0m The current domain  was resolved successfully IPADD：%s' % domain.GetAddr(url)[1])
            print(domain.CheckFile())
            print('\n\033[34m[SCAN]\033[0m 开始多线程扫描\n')
            threading_list = [get_dir,get_domain,get_port,get_other]
            threading_join = []
            for i in  threading_list:
                t = threading.Thread(target=i)
                threading_join.append(t)
            for t in threading_join:
                t.start()
            for t in threading_join:
                t.join()

            print(domain.Result())
            end_time = time.time()
            print('\n\033[34m[SCAN]\033[0m 总耗时%s S' %(end_time - start_time))
        except:
            pass
