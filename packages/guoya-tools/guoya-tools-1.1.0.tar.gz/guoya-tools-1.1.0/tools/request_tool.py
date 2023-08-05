"""
封装request
"""

import requests
from tools import log_tool
from tools.decorators_tool import logs
import time

@logs
def get_request(url, params=None, headers=None, cookies=None):
    """
    Get请求
    :param url:
    :param data:
    :param header:
    :return:
    """

    if not (url.startswith('http://') or url.startswith('https://')):
        url = '%s%s' % ('http://', url)
        print(url)
    try:

        response = requests.get(url=url, params=params, headers=headers, cookies=cookies)

    except requests.RequestException as e:
        log_tool.error('%s%s' % ('Exception url: ', url))
        log_tool.error(e)
        return ()

    except Exception as e:
        log_tool.error('%s%s' % ('Exception url: ', url))
        return ()

    time_consuming = response.elapsed.microseconds / 1000
    log_tool.info('----请求用时: %s 秒数' % time_consuming)

    return response


@logs
def post_request(url, data=None,files=None, params=None, headers=None, json=None, cookies=None):
    """
    Post请求
    :param url:
    :param data:
    :param header:
    :return:
    """
    if not (url.startswith('http://') or url.startswith('https://')):
        url = '%s%s' % ('http://', url)
        print(url)
    try:
        response = requests.post(url, data=data,files=files, params=params, headers=headers, json=json, cookies=cookies)

    except requests.RequestException as e:
        log_tool.error('%s%s' % ('RequestException url: ', url))
        log_tool.error(e)
        return ()

    except Exception as e:
        log_tool.error('%s%s' % ('Exception url: ', url))
        log_tool.error(e)
        return ()

    # time_consuming为响应时间，单位为毫秒
    time_consuming = response.elapsed.microseconds / 1000
    log_tool.info('----请求用时: %s 秒数' % time_consuming)

    return response


@logs
def post_request_multipart(url, files=None, headers=None, cookies=None):
    """
    提交Multipart/form-data 格式的Post请求
    :param url:
    :param data:
    :param header:
    :param file_parm:
    :param file:
    :param type:
    :return:
    """
    if not (url.startswith('http://') or url.startswith('https://')):
        url = '%s%s' % ('http://', url)
        print(url)
    response = requests.post(url=url, files=files, headers=headers, cookies=cookies)
    # time_consuming为响应时间，单位为毫秒
    time_consuming = response.elapsed.microseconds / 1000
    log_tool.info('----请求用时: %s 秒数' % time_consuming)

    return response


@logs
def put_request(url, data, header=None, cookies=None):
    """
    Put请求
    :param url:
    :param data:
    :param header:
    :return:
    """
    if not (url.startswith('http://') or url.startswith('https://')):
        url = '%s%s' % ('http://', url)
        log_tool.debug(url)

    try:
        if data is None:
            response = requests.put(url=url, headers=header, cookies=cookies)
        else:
            response = requests.put(url=url, params=data, headers=header, cookies=cookies)

    except requests.RequestException as e:
        log_tool.error('%s%s' % ('RequestException url: ', url))
        log_tool.error(e)
        return ()

    except Exception as e:
        print('%s%s' % ('Exception url: ', url))
        print(e)
        return ()

    time_consuming = response.elapsed.microseconds / 1000
    log_tool.info('----请求用时: %s 秒数' % time_consuming)

    return response

def down_big_file(srcUrl, localFile):
    print('%s\n --->>>\n  %s' % (srcUrl, localFile))
    startTime = time.time()
    with requests.get(srcUrl, stream=True) as r:
        contentLength = int(r.headers['content-length'])
        line = 'content-length: %dB/ %.2fKB/ %.2fMB'
        line = line % (contentLength, contentLength / 1024, contentLength / 1024 / 1024)
        print(line)
        print('正在下载中..............')
        downSize = 0
        with open(localFile, 'wb') as f:
            for chunk in r.iter_content(8192):
                if chunk:
                    f.write(chunk)
                downSize += len(chunk)
                line = '%d KB/s - %.2f MB， 共 %.2f MB'
                line = line % (
                downSize / 1024 / (time.time() - startTime), downSize / 1024 / 1024, contentLength / 1024 / 1024)
                print(line, end='\r')
                if downSize >= contentLength:
                    break
        timeCost = time.time() - startTime
        line = '共耗时: %.2f s, 平均速度: %.2f KB/s'
        line = line % (timeCost, downSize / 1024 / timeCost)
        print(line)

def copy_github_file(url,save_name):
    resp = get_request(url)
    body = resp.text
    with open(save_name, 'w', encoding='utf-8') as file:
        file.write(body)