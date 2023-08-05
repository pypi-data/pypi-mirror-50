"""
封装request
"""

import requests
from tools import log_tool
from tools.decorators_tool import logs

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

