# -*- coding:utf-8 -*-
# Author : 小吴老师
# Data ：2019/7/18 18:29
from tools import os_tool
from tools import excel_tool


############################
# 初始化工程目录
############################
def init_dirs():
    # 工程根目录
    root_path = os_tool.get_root_path()

    # 配置文件夹
    os_tool.mkdir(root_path + 'config')

    # 测试用例文件夹
    test_case = root_path + 'test_case'
    os_tool.mkdir(test_case)
    os_tool.mkdir((test_case + '/demo'))

    # 测试数据文件夹
    os_tool.mkdir(root_path + 'data')

    # allure报告文件夹
    reports = root_path + 'reports'
    os_tool.mkdir(reports + '/xml')
    os_tool.mkdir(reports + '/html')

    # 日志文件夹
    os_tool.mkdir(root_path + 'logs')


#####################
# 初始化config包
#####################
def init_config():
    config = os_tool.get_root_path() + 'config'
    os_tool.mkdir(config)
    conf = "GY_API_URL = 'http://dev.guoyasoft.com:8080'\n\n" \
           "GY_DB_URL = {                               \n" \
           "    'host': 'qa.guoyasoft.com',             \n" \
           "    'port': 3306,                           \n" \
           "    'db': 'guoya_virtual_mall_1811',        \n" \
           "    'user': 'root',                         \n" \
           "    'passwd': 'Guoya006',                   \n" \
           "    'charset': 'utf8'                       \n" \
           "}											\n"
    with open(config + '/conf.py', 'w', encoding='utf-8') as f:
        f.write(conf)


###################
# 新建run.py脚本
###################
def ini_run():
    root_path = os_tool.get_root_path()
    run = "# -*- coding:utf-8 -*-																		\n" \
          "# Author : 小吴老师                                                                        \n" \
          "# Data ：2019/7/12 7:41                                                                    \n" \
          "from tools import log_tool                                                                 \n" \
          "from tools import shell_tool                                                               \n" \
          "from tools import log_tool                                                                 \n" \
          "import pytest                                                                              \n" \
          "                                                                                           \n" \
          "if __name__ == '__main__':                                                                 \n" \
          "    # 修改成要执行的测试用例                                                               \n" \
          "    test_case = './test_case/demo/test_hello.py'                                         \n" \
          "                                                                                           \n" \
          "    xml_report_path = './reports/xml/'                                                     \n" \
          "    html_report_path = './reports/html/'                                                   \n" \
          "                                                                                           \n" \
          "    pytest.main(['-s', '-q', '--alluredir',                                                \n" \
          "                 xml_report_path, test_case])                                              \n" \
          "    cmd1 = 'allure generate %s -o %s --clean' % (xml_report_path, html_report_path)        \n" \
          "    cmd2 = 'allure serve %s' % (xml_report_path)                                           \n" \
          "                                                                                           \n" \
          "    shell_tool.invoke(cmd1)                                                                \n" \
          "    shell_tool.invoke(cmd2)                                                              \n"

    if not os_tool.exists(root_path + '/run.py'):
        with open(root_path + '/run.py', 'w', encoding='utf-8') as f:
            f.write(run)


#############################
# xml配置category和
#############################
def ini_allure():
    reports_xml = os_tool.get_root_path() + 'reports/xml'
    os_tool.mkdir(reports_xml)
    category = '[{                                                    \n' \
               '        "name": "Ignored tests",                      \n' \
               '        "matchedStatuses": ["skipped"]                \n' \
               '    },                                                \n' \
               '    {                                                 \n' \
               '        "name": "Infrastructure problems",            \n' \
               '        "matchedStatuses": ["broken", "failed"],      \n' \
               '        "messageRegex": ".*bye-bye.*"                 \n' \
               '    },                                                \n' \
               '    {                                                 \n' \
               '        "name": "Outdated tests",                     \n' \
               '        "matchedStatuses": ["broken"],                \n' \
               '        "traceRegex": ".*FileNotFoundException.*"     \n' \
               '    },                                                \n' \
               '    {                                                 \n' \
               '        "name": "Product defects",                    \n' \
               '        "matchedStatuses": ["failed"]                 \n' \
               '    },                                                \n' \
               '    {                                                 \n' \
               '        "name": "Test defects",                       \n' \
               '        "matchedStatuses": ["broken"]                 \n' \
               '    }                                                 \n' \
               ']                                                     \n'

    if not os_tool.exists(reports_xml + '/categories.json'):
        with open(reports_xml + '/categories.json', 'w', encoding='utf-8') as f:
            f.write(category)

    environment = 'Browser=Chrome         \n' \
                  'Browser.Version=63.0   \n' \
                  'Stand=Production       \n'

    if not os_tool.exists(reports_xml + '/environment.properties'):
        with open(reports_xml + '/environment.properties', 'w', encoding='utf-8') as f:
            f.write(environment)


#############################
# test_hello.py
#############################
def init_test_demo():
    test_case = os_tool.get_root_path() + 'test_case'
    os_tool.mkdir(test_case)
    test_hello = "# -*- coding:utf-8 -*-                                                                                        \n" \
                 "# Author : 小吴老师                                                                                           \n" \
                 "# Data ：2019/7/18 19:23                                                                                      \n" \
                 "import allure                                                                                                 \n" \
                 "import json                                                                                                   \n" \
                 "                                                                                                              \n" \
                 "                                                                                                              \n" \
                 "@allure.epic('一级归类')                                                                                      \n" \
                 "@allure.feature('二级归类')                                                                                   \n" \
                 "@allure.story('三级归类')                                                                                     \n" \
                 "def test_hello_world():                                                                                       \n" \
                 "    print('hello world !')                                                                                    \n" \
                 "    request = {                                                                                               \n" \
                 "        'pwd': 'a123456',                                                                                     \n" \
                 "        'userName': '13s32'                                                                                   \n" \
                 "    }                                                                                                         \n" \
                 "    allure.attach(json.dumps(request,ensure_ascii=False,indent=4), '请求', allure.attachment_type.TEXT)       \n" \
                 "                                                                                                              \n" \
                 "    response = {                                                                                              \n" \
                 "        'code': 2000,                                                                                         \n" \
                 "        'message': '登录成功',                                                                                \n" \
                 "        'data': {                                                                                             \n" \
                 "            'token': 'eyJ0aW1lT3V0IjoxNTYzNDUxMjg4MjY3LCJ1c2VySWQiOjQwMywidXNlck5hbWUiOiIxM3MzMiJ9',          \n" \
                 "            'userName': '13s32'                                                                               \n" \
                 "        }                                                                                                     \n" \
                 "    }                                                                                                         \n" \
                 "    allure.attach(json.dumps(response,ensure_ascii=False,indent=4), '响应', allure.attachment_type.TEXT)      \n"

    os_tool.mkdir('__init__.py')
    demo = test_case + '/demo'
    os_tool.mkdir(demo)
    if not os_tool.exists(demo + '/test_hello.py'):
        with open(demo + '/test_hello.py', 'w', encoding='utf-8') as f:
            f.write(test_hello)


#######################################
# 全局文件conftest.py
######################################
def init_conftest():
    conftest = "import pytest                                               \n" \
               "                                                            \n" \
               "                                                            \n" \
               "@pytest.fixture(scope='session')                            \n" \
               "def pub_dic():                                              \n" \
               "    data = {'token':'asdfasdfjsldkfjlsxllkj'}               \n" \
               "    return data                                             \n" \
               "                                                            \n" \
               "                                                            \n" \
               "@pytest.fixture(scope='session')                            \n" \
               "def pub_list():                                             \n" \
               "    data = ['张三','zhangsan',30,'男','aaa123']             \n" \
               "    return data                                             \n" \
               "                                                            \n" \
               "                                                            \n" \
               "@pytest.fixture(scope='session')                            \n" \
               "def pub_var():                                              \n" \
               "    token = 'xxxxsdfsdfjkllwklewe'                          \n" \
               "    return token                                            \n"
    file_path = os_tool.get_root_path() + 'test_case'
    if not os_tool.exists(file_path + '/conftest.py'):
        with open(file_path + '/conftest.py', 'w', encoding='utf-8') as f:
            f.write(conftest)


#######################################
# 初始化测试数据
#######################################
def init_data():
    file_path = os_tool.get_root_path() + 'data/demo'
    os_tool.mkdir(file_path)
    file_name = file_path + '/excel_demo.xlsx'

    data_title = ['test_case', 'i_user_name', 'i_pwd', 'o_code', 'o_token']
    data_list = [['登陆成功', 'guoya2019', 'aaa123', 2000, None], ['用户名不存在', 'guoya2016', 'aaa123', 9999, None],
                 ['密码错误', 'guoya2019', 'aaa000', 9999, None]]
    excel_tool.write_excel(file_name, data_title=data_title, data_list=data_list)


#######################################
# 初始化.gitignore
######################################
def init_git():
    root_path = os_tool.get_root_path()
    gitignore = '# pycharm                                                                                     \n' \
                '.idea/                                                                                        \n' \
                '# Byte-compiled / optimized / DLL files                                                       \n' \
                '__pycache__/                                                                                  \n' \
                '*.py[cod]                                                                                     \n' \
                '*$py.class                                                                                    \n' \
                '                                                                                              \n' \
                '# C extensions                                                                                \n' \
                '*.so                                                                                          \n' \
                '                                                                                              \n' \
                '# Distribution / packaging                                                                    \n' \
                '.Python                                                                                       \n' \
                'build/                                                                                        \n' \
                'develop-eggs/                                                                                 \n' \
                'dist/                                                                                         \n' \
                'downloads/                                                                                    \n' \
                'eggs/                                                                                         \n' \
                '.eggs/                                                                                        \n' \
                'lib/                                                                                          \n' \
                'lib64/                                                                                        \n' \
                'parts/                                                                                        \n' \
                'sdist/                                                                                        \n' \
                'var/                                                                                          \n' \
                'wheels/                                                                                       \n' \
                '*.egg-info/                                                                                   \n' \
                '.installed.cfg                                                                                \n' \
                '*.egg                                                                                         \n' \
                'MANIFEST                                                                                      \n' \
                '                                                                                              \n' \
                '# PyInstaller                                                                                 \n' \
                '#  Usually these files are written by a python script from a template                         \n' \
                '#  before PyInstaller builds the exe, so as to inject date/other infos into it.               \n' \
                '*.manifest                                                                                    \n' \
                '*.spec                                                                                        \n' \
                '                                                                                              \n' \
                '# Installer logs                                                                              \n' \
                'pip-log.txt                                                                                   \n' \
                'pip-delete-this-directory.txt                                                                 \n' \
                '                                                                                              \n' \
                '# Unit test / coverage reports                                                                \n' \
                'htmlcov/                                                                                      \n' \
                '.tox/                                                                                         \n' \
                '.coverage                                                                                     \n' \
                '.coverage.*                                                                                   \n' \
                '.cache                                                                                        \n' \
                'nosetests.xml                                                                                 \n' \
                'coverage.xml                                                                                  \n' \
                '*.cover                                                                                       \n' \
                '.hypothesis/                                                                                  \n' \
                '.pytest_cache/                                                                                \n' \
                '                                                                                              \n' \
                '# Translations                                                                                \n' \
                '*.mo                                                                                          \n' \
                '*.pot                                                                                         \n' \
                '                                                                                              \n' \
                '# Django stuff:                                                                               \n' \
                '*.log                                                                                         \n' \
                'local_settings.py                                                                             \n' \
                'db.sqlite3                                                                                    \n' \
                '                                                                                              \n' \
                '# Flask stuff:                                                                                \n' \
                'instance/                                                                                     \n' \
                '.webassets-cache                                                                              \n' \
                '                                                                                              \n' \
                '# Scrapy stuff:                                                                               \n' \
                '.scrapy                                                                                       \n' \
                '                                                                                              \n' \
                '# Sphinx documentation                                                                        \n' \
                'docs/_build/                                                                                  \n' \
                '                                                                                              \n' \
                '# PyBuilder                                                                                   \n' \
                'target/                                                                                       \n' \
                '                                                                                              \n' \
                '# Jupyter Notebook                                                                            \n' \
                '.ipynb_checkpoints                                                                            \n' \
                '                                                                                              \n' \
                '# pyenv                                                                                       \n' \
                '.python-version                                                                               \n' \
                '                                                                                              \n' \
                '# celery beat schedule file                                                                   \n' \
                'celerybeat-schedule                                                                           \n' \
                '                                                                                              \n' \
                '# SageMath parsed files                                                                       \n' \
                '*.sage.py                                                                                     \n' \
                '                                                                                              \n' \
                '# Environments                                                                                \n' \
                '.env                                                                                          \n' \
                '.venv                                                                                         \n' \
                'env/                                                                                          \n' \
                'venv/                                                                                         \n' \
                'ENV/                                                                                          \n' \
                'env.bak/                                                                                      \n' \
                'venv.bak/                                                                                     \n' \
                '                                                                                              \n' \
                '# Spyder project settings                                                                     \n' \
                '.spyderproject                                                                                \n' \
                '.spyproject                                                                                   \n' \
                '                                                                                              \n' \
                '# Rope project settings                                                                       \n' \
                '.ropeproject                                                                                  \n' \
                '                                                                                              \n' \
                '# mkdocs documentation                                                                        \n' \
                '/site                                                                                         \n' \
                '                                                                                              \n' \
                '# mypy                                                                                        \n' \
                '.mypy_cache/                                                                                  \n'

    if not os_tool.exists(root_path + '/.gitignore'):
        with open(root_path + '/.gitignore', 'w', encoding='utf-8') as f:
            f.write(gitignore)


def init_project():
    #########################################
    # 初始化工程：目录+配置+脚本
    #########################################
    # 初始化工程目录
    init_dirs()
    # 　初始化配置文件
    init_config()
    # 初始化allure
    ini_allure()
    # 初始化演示demo
    init_test_demo()
    # 初始化excel模板
    init_data()
    # 初始化conftest
    init_conftest()
    # 初始化run.py
    ini_run()
    # 初始化git
    init_git()
