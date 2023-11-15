import re
import time
from random import Random

import DrissionPage
import requests
from DrissionPage.errors import NoResourceError, ContextLossError, ElementLossError, ElementNotFoundError
import logging

from requests import ReadTimeout

from githubMd2Blog import MyFileUtil

"""
说明：获取某个仓库里根目录文件或文件夹数组
url:https://api.github.com/repos//{用户名}/{仓库名}/contents
method:get
参数：path路径-用户名 和 仓库名
结果：返回一个首层文件或文件夹数组

说明：获取某个仓库里子目录文件或文件夹数组
url:https://api.github.com/repos//{用户名}/{仓库名}/contents/{文件名或文件夹名}
method:get
参数：path路径-用户名 和 仓库名和文件名或文件夹名
结果：返回一个文件数组

说明：获取某文件的原始内容（Raw）
1. 通过上面的文件信息中提取download_url这条链接，就能获取它的原始内容了。
2. 或者直接访问：https://raw.githubusercontent.com/{用户名}/{仓库名}/{分支名}/{文件路径}
url:           https://raw.githubusercontent.com/{用户名}/{仓库名}/{分支名}/{文件路径}
method:get
参数：path路径： 用户名 和 仓库名和文件l路径
结果：返回一个文件内容的字符串
"""


class GithubProjects:
    """
    初始化构造函数
    @project_url:项目地址
    @master:主分支，默认为None
    @page:浏览器工具：默认DrissionPage.ChromiumPage()
    @workDirectory：当前处理的文件夹（目前只支持到第二层文件夹）
    @readMe :是否解析readMe文件
    @default_level:默认从第一层文件夹开始处理
    """
    # 配置日志记录器
    logging.basicConfig(level=logging.DEBUG, filename='app.log', filemode='w',
                        format='%(asctime)s - %(levelname)s - %(message)s')
    _API_PROJECT_FILES_LEVEL1 = 'https://api.github.com/repos/{}/{}/contents'  # 第一层文件目录接口
    _API_PROJECT_FILES_LEVEL2 = 'https://api.github.com/repos/{}/{}/contents/{}'  # 第二层文件目录接口（支持多层）
    _API_PROJECT_FILE_RAW = 'https://raw.githubusercontent.com/{}/{}/{}/{}'  # 文件原文内容

    def __init__(self):
        self._project_name = None
        self._project_owner_name = None
        self._workDirectory = None

    def __int__(self, project_url, name, master, page):
        self._project_url = project_url
        self._name = name
        if master is not None:
            self._branch = master
        else:
            self._branch = "main"
        self._tree_url = self._project_url + '/tree/' + self._branch
        self._page = page
        self._readMe = False
        self._default_level = 1

    """
        解析文件
        
    """

    def parse_project_files(self):
        if self._project_owner_name is not None and self._project_name is not None:
            try:
                project_level1_files_url = self._API_PROJECT_FILES_LEVEL1.format(self._project_owner_name,
                                                                                 self._project_name)
                # time.sleep(10)  # 请求频率不能太高
                result = requests.get(project_level1_files_url)
                if result.status_code == 200:
                    project_level_file = result.json()
                    for file in project_level_file:
                        if self._readMe and file.get('type') == 'file' and file.get('path') == 'READE.md':
                            self.save_markdown_file(file.get('url'), file.get('path'))
                        elif file.get('type') == 'dir':
                            #  ：https://raw.githubusercontent.com/{用户名}/{仓库名}/{分支名}/{文件路径}
                            project_level2_file_url = self._API_PROJECT_FILES_LEVEL2.format(self._project_owner_name,
                                                                                            self._project_name,
                                                                                            self._branch,
                                                                                            file.get('path'))

                            result2 = requests.get(file.get('url'))
                            if result2.status_code == 200:
                                project_level2_files = result2.json()
                                for second_file in project_level2_files:
                                    if second_file.get('type') == 'file':
                                        self.save_markdown_file(second_file.get('url'),second_file.get('path'))

                                        # break
                                        """
                                        {'name': '01.初识Python.md', 
                                         'path': 'Day01-15/01.初识Python.md', 
                                        'sha': 'e1868952473270f648cddf4e2bfe00929067453f', 
                                        'size': 12325, 
                                        'url': 'https://api.github.com/repos/jackfrued/Python-100-Days/contents/Day01-15/01.%E5%88%9D%E8%AF%86Python.md?ref=master',
                                         'html_url': 'https://github.com/jackfrued/Python-100-Days/blob/master/Day01-15/01.%E5%88%9D%E8%AF%86Python.md', 
                                         'git_url': 'https://api.github.com/repos/jackfrued/Python-100-Days/git/blobs/e1868952473270f648cddf4e2bfe00929067453f', 
                                         'download_url': 'https://raw.githubusercontent.com/jackfrued/Python-100-Days/master/Day01-15/01.%E5%88%9D%E8%AF%86Python.md', 
                                         'type': 'file', '_links': {'self': 'https://api.github.com/repos/jackfrued/Python-100-Days/contents/Day01-15/01.%E5%88%9D%E8%AF%86Python.md?ref=master', 
                                         'git': 'https://api.github.com/repos/jackfrued/Python-100-Days/git/blobs/e1868952473270f648cddf4e2bfe00929067453f', 
                                         'html': 'https://github.com/jackfrued/Python-100-Days/blob/master/Day01-15/01.%E5%88%9D%E8%AF%86Python.md'}
                                         }
                                        """
                        # break
                else:
                    logging.error('请求【' + project_level1_files_url + '】失败！')
            except KeyError:
                logging.info('初始化接口地址失败')
            except ReadTimeout:
                logging.info('请求【】超时')
            except ConnectionError:
                for i in range(1, 10):
                    logging.info(11 - i)
                    print('倒计时' + str(11 - i))
                    time.sleep(1)
                self.parse_project_files()
        else:
            logging.info('请初始化项目url地址')

        # try:
        #     logging.info('开始爬取:' + self._name + '项目的Markdown文件')
        #     self._page.get(self._project_url)
        #     logging.info('处理LEVEL1层文件夹:' + self._name + '项目的Markdown文件')
        #     level1_files = self._page.eles(
        #         "xpath://div[@class='js-details-container Details']//div[@role='rowheader']//a")
        #     if len(level1_files) > 0:
        #         logging.info('找到【' + self._name + '】项目' + str(len(level1_files)) + '个文件')
        #     else:
        #         logging.info('没有找到【' + self._name + '】项目文件信息，Game Over！')
        # except NoResourceError:
        #     logging.info('获取' + self._name + '项目元素失效，暂停10秒后继续。。。。')
        #     for i in range(1, 10):
        #         logging.info(11 - i)
        #         time.sleep(1)
        #     self.parse_project_files()
        # except ContextLossError:
        #     logging.info('页面好像被刷新了，重新来。。')
        #     self.parse_project_files()
        # except ElementLossError:
        #     logging.info('页面好像被刷新了，重新来。。')
        #     self.parse_project_files()
        # except ElementNotFoundError:
        #     logging.info('获取【' + self._name + '】LEVEL1层文件夹失效，可能页面已经调整')


    """
        解析项目地址，获取文件夹信息
    """

    def parse_project_files_with_drissionpage(self):
        try:
            chrome = DrissionPage.ChromiumPage()
            chrome.get(self._project_url)
            # 找到第一级文件夹路径
            els = chrome.eles('xpath://')
            for ele in els:
                ele.click()
        except ElementNotFoundError:
            logging.error("找不到元素")

    def parse_project_url(self):
        items = self._project_url.split('/')
        if len(items) <= 2:
            logging.info('【' + self._project_url + '】地址疑似不是正确的项目地址，请检查。。')
        else:
            items.reverse()
            self._project_name = items[0]
            self._project_owner_name = items[1]

    def save_markdown_file(self, markdown_file_url, path):
        print(self._project_name)
        temp_response = requests.get(markdown_file_url)
        if temp_response.status_code == 200:
            result = temp_response.json()
            if result.get('download_url') is not None and result.get('download_url') != '':
                # time.sleep(10)  # 慢慢来，不要急
                req = requests.get(result.get('download_url'))
                try:
                    my_file_utile = MyFileUtil.MyFileUtil(
                        './projectTempInfo/' + self._project_name + '/' + path.split('/')[0])
                    create_folder_result = my_file_utile.create_folder()
                    if create_folder_result is True:
                        with open(r"./projectTempInfo/" + self._project_name + '/' + path, "wb") as f:
                            url_re = r"!\[.*?\]\((.*?)\)"
                            image_urls = re.findall(url_re, req.text)
                            file_relative_path = str(path)
                            file_relative_folder = file_relative_path[:file_relative_path.rfind('/')]
                            print(file_relative_folder)
                            self.handle_markdown_url(image_urls)
                            f.write(req.content)
                    else:
                        my_file_utile = MyFileUtil.MyFileUtil('./projectTempInfo/')
                        my_file_utile.create_folder()
                        with open(r"./projectTempInfo/" + path, "wb") as f:
                            f.write(req.content)
                except FileNotFoundError:
                    logging.error("文件夹不存在")
        else:
            logging.info('下载【' + markdown_file_url + '文件失败，请检查')
        pass

    def parse_markdown_file(self, markdown_file_path):
        path = './projectTempInfo' + self._project_name
        with open(markdown_file_path, 'r') as content:
            file_content = content.read()
            print(file_content)
    """
        处理不通类型的图片地址
    """

    def handle_markdown_url(self, image_urls):
        print(self._project_name)
        if len(image_urls) > 0:
            for url in image_urls:
                if url.startswith('http'):  # 处理网络图片
                    print('TODO handle this!')
                    pass
                elif url.startswith('./') or url.startswith('/') or url.startswith('\\'):  # 处理相相对路径的本地图片
                    folders = url.split('/')

    """
        下载网络图片
    """
    def download_http_image(self, url):
        print(self._project_name)
        image_b = requests.get(url)
        with open('./projectTempInfo/downloads/', 'r') as content:
            content.write(image_b.text)

    """
        下载相对路径图片（github项目地址）
    """
    def handl_relative_path(self, relative_path):
        print(self._project_name)
        if relative_path.startswith('./') or relative_path.startswith('/') or relative_path.startswith('\\'):
            pass
        else:
            print("你的地址貌似不是相对地址，请核对！")


if __name__ == '__main__':
    githubProject = GithubProjects()
    githubProject.__int__('https://github.com/jackfrued/Python-100-Days', 'Python100天入门到精通', None,
                          DrissionPage.ChromiumPage())
    githubProject.parse_project_url()  # 解析url
    githubProject.parse_project_files()  # 解析项目文件
