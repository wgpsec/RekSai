import subprocess
import sys
import os

class Config(object):
    def __init__(self):
        self.Tools = ['masscan','OneForAll','nmap','dirmap']
        self.path = os.getcwd() + '/tools'

    def tools(self):
        print('\033[33m[WARN]\033[0m Downloading Toolkit...')
        if len(subprocess.getoutput('find %s -name dirmap' % self.path)) == 0:
            DownLoad = subprocess.getoutput('git clone https://gitee.com/abaokris/tools.git;'
                                            'yum -y install unzip whois;'
                                            'apt-get -y install unzip whois;'
                                            'python3 -m pip install --upgrade pip -i https://pypi.tuna.tsinghua.edu.cn/simple;'
                                            'python3 -m pip install request bs4  -i https://pypi.tuna.tsinghua.edu.cn/simple')

            for Tool in self.Tools:
                FinTool = subprocess.getoutput('find %s -name %s' % (self.path,Tool))
                if str(FinTool).find(Tool) != -1 :
                    rm_zip = subprocess.getoutput('cd tools;'
                                                  'rm -rf %s.zip' % Tool)
                    print('\033[32m[SUCC]\033[0m %s Already Exists' % Tool)
                else:
                    if Tool == 'masscan':
                        unzip = subprocess.getoutput('yum  -y install git gcc make libpcap*;'
                                                     'apt-get -y install git gcc make libpcap*;'
                                                     'cd tools;'
                                                     'unzip masscan.zip')
                        make = subprocess.getoutput('cd tools/masscan;'
                                                    'make')


                    elif Tool == 'dirmap':
                        unzip = subprocess.getoutput('cd tools;'
                                                    'unzip dirmap.zip;')

                        make = subprocess.getoutput('cd tools/dirmap;'
                                                    'python3 -m pip install -r requirement.txt -i https://pypi.tuna.tsinghua.edu.cn/simple')

                    elif Tool == 'OneForAll':
                        make = subprocess.getoutput('cd tools;'
                                                    'git clone https://gitee.com/shmilylty/OneForAll.git;'
                                                    'cd OneForAll/;'
                                                    'python -m pip install -U pip setuptools wheel -i https://mirrors.aliyun.com/pypi/simple/;'
                                                    'pip3 install -r requirements.txt -i https://mirrors.aliyun.com/pypi/simple/')

                    elif Tool == 'nmap':
                        make = subprocess.getoutput('yum -y install nmap')
                    else:
                        unzip = subprocess.getoutput('cd tools;'
                                                     'unzip %s.zip' % Tool)

                    print('\033[32m[SUCC]\033[0m %s Dowland Success!' % Tool)
            print('\033[34m[OUT] \033[0m 工具检测完成！\n')

        else:
            print('\033[34m[OUT] \033[0m 工具检测完成！\n')



    def gopath(self):
        print('\033[33m[WARR]\033[0m golang environmental testing...')
        goinstall = subprocess.getoutput('go')
        if len(goinstall) < 50 :
            install = subprocess.getoutput('wget https://studygolang.com/dl/golang/go1.12.linux-amd64.tar.gz;'
                                           'tar -C /usr/local -xzf go1.12.linux-amd64.tar.gz;'
                                           'rm -rf go1.12.linux-amd64.tar.gz;'
                                           'echo "export GOROOT=/usr/local/go\n'
                                           'export GOPATH=/usr/local/var/www/go\n'
                                           'export GOBIN=\$GOPATH/bin \n'
                                           'export PATH=\$PATH:\$GOBIN:\$GOROOT/bin" >> /etc/profile;')
            return '\033[34m[OUT] \033[0m 语言环境检测完成！\n'
        else:
            print('\033[34m[OUT] \033[0m 语言环境检测完成！\n')
