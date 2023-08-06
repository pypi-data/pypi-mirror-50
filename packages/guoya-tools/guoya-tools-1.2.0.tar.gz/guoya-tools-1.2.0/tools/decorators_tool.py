
"""
常用装饰器
"""
import allure
from tools import log_tool
from tools import string_tool



# 日志装饰器
def logs(func):
    def _func(*args, **kwargs):
        r= func(*args, **kwargs)
        request = "---------------请求-----------------" \
                  "\n{0}\n{1}\n{2}".format(r.url,string_tool.dic_to_str(r.request.headers),r.request.body)
        log_tool.info(request)
        response = "---------------响应----------------" \
                   "\n{0}\n{1}\n{2}".format(r.status_code,string_tool.dic_to_str(r.headers),r.text)
        log_tool.info(response)
        allure.attach(request,'请求',allure.attachment_type.TEXT)
        allure.attach(response, '响应', allure.attachment_type.TEXT)
        return r

    return _func