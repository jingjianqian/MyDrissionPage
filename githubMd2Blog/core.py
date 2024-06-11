"""
github 项目内部 markdown 转 博客以及
"""
import asyncio
import pathlib
import re
import time

from DrissionPage._functions.tools import ElementsList

import MyFileUtil
import logging
import DrissionPage
import csv


class GithubProject:
    _API_TREE_URL = 'https://github.com/jackfrued/Python-100-Days/tree/master'  # 项目文件结构基路径
    """
    =========默认构造函数===============
    ======@base_host: github地址
    ======@default_master:默认分支
    ======@workDirectory:记录当前的工作路径（相对项目的）
    ==========================================
    """

    def __init__(self):
        self.page = None
        self.base_host = 'https://github.com'  # 默认主页
        self.base_host_file_host = 'https://raw.githubusercontent.com'  # 默认.md文件浏览地址
        self.default_master = "master"  # 默认分支
        self.workDirectory = ''
        # 配置日志记录器
        logging.basicConfig(level=logging.INFO, filename='app.log', filemode='w',
                            format='%(asctime)s - %(levelname)s - %(message)s')

    """
    =========第一步、初始化基础数据===============
    ======@project_name: 项目名称
    ======@project_url:项目地址(注意是项目文件夹结构地址)
    ======@markdown_2_blog_site:博客地址
    ==========================================
    """

    def __int__(self, project_name: object, project_url: object, markdown_2_blog_site: object) -> object:
        self._project_url = project_url  # 项目地址
        self._project_name = project_name  # 项目名称
        self._markdown_2_blog_site = markdown_2_blog_site  # markdown 转 blog文章网站

    """
    =========第二步、获取项目第一层文件夹清单===============
    ======
    ======@return_tree_array:第一层文件夹列表清单
    ======
    ==========================================
    """

    def parse_project__files(self):
        print('开始爬取:' + str(self._project_name) + '项目的Markdown文件')
        self.page = DrissionPage.ChromiumPage()
        print('访问项目地址中：' + str(self._project_url))
        self.page.get(str(self._project_url))
        first_levels = self.page.eles("xpath:/html/body//ul//li[@class='PRIVATE_TreeView-item' and @aria-level='1']")
        print('找到第一层文件情况数量：' + str(len(first_levels)))
        return_tree_array = []
        for first_levels_name in first_levels:
            tree_name = first_levels_name.attr("id")
            # print("路径：" + self._API_TREE_URL + '/' + tree_name.replace('-item', ''))
            return_tree_array.append(self._API_TREE_URL + '/' + tree_name.replace('-item', ''))
        # print(return_tree_array)
        return return_tree_array

    """
    =========第三步、获取第二步每个文件夹下的markdown_list文件清单===============
    ======
    ======@return_tree_array:第一层文件夹列表清单
    ======
    ==========================================
    """

    def parse_folder_md_files(self, _tree_array):
        current = 1
        markdown_list = []
        for tree_url in _tree_array:
            print('开始获取：' + str(tree_url) + '路径下的markdown文件列表' + str(current))
            current = current + 1
            self.page.get(tree_url)
            # temp_tab.get(tree_url)
            # temp_tab.set.activate()
            # temp_tab.wait.load_start()
            time.sleep(3)
            md_files = self.page.eles("xpath:/html/body//div[@class='react-directory-filename-column']//a")
            for file_name in md_files:
                print(str(file_name))
            # self.page.close_tabs(temp_tab)
            # tab = tree_url.click.for_new_tab()
            # markdown_list = self.parse_folder_md_files_detail(self.page.get_tab(tab))
            # temp_tab = self.page.new_tab()
            # temp_tab.get(tree_url)
            # self.page.get_tab(temp_tab).wait.load_start()
            # # tab.set.activate()
            # markdown_list = self.parse_folder_md_files_detail(self.page.get_tab(temp_tab))
            # print(markdown_list)
            # time.sleep(1)
            # # print(self.page.get_tabs())
            # # self.page.to_tab(self.page.get_tab(0))
            # self.page.close_tabs(temp_tab)
        return markdown_list

    """
    =========第三步的辅助子方法===============
    ======
    ======@md_list:获取文件夹下面的markdown 文件清单
    ======
    ==========================================
    """

    def parse_folder_md_files_detail(self, temp_tab):
        temp_tab.set.activate()
        md_list = self.page.eles("xpath:/html/body//div[@class='react-directory-filename-column']//a")
        return_markdown_files_array = []
        for markdown_files_obj in md_list:
            return_markdown_files_array.append(markdown_files_obj)
        return return_markdown_files_array

    def project_first_list(drssion_page_, xpath):
        pass
        # list = drssion_page_.eles("xpath:/html/body//ul//li[@class='PRIVATE_TreeView-item']")
        # print(list)
        # /html/body//ul//li[@class='PRIVATE_TreeView-item']

    #
    # def parse_project_md_files(self, md_file_lists=None):
    #     logging.info('开始爬取:' + self._project_name + '项目的Markdown文件')
    #     self.page = DrissionPage.ChromiumPage()
    #     logging.info('访问项目地址中：' + self._project_url)
    #     # main_tab_id =
    #     self.page.get(self._project_url)
    #
    # mypath = pathlib.Path('./projectTempInfo/') logging.info('存储项目基本信息：' + str(mypath.absolute())) mypath.mkdir(
    # parents=True, exist_ok=True)  # 创建文件夹 file = str(mypath) + '/' + self._project_name + '.csv' pathlib.Path(
    # file).touch(mode=438, exist_ok=True) # with './projectTempInfo/'+self._project_name+'.csv'.open recorder =
    # Recorder('./projectTempInfo/' + self._project_name + '.csv') recorder.clear() project_src = self.page.eles(
    # "xpath://div[@class='js-details-container Details']//div[@role='rowheader']//a") with open('./projectTempInfo/'
    # + self._project_name + '.csv', 'r+') as f: f.truncate(0) for ele in project_src: text = ele.text link =
    # ele.link xpath_str = "xpath://ul/li[@id='" + text + "-item']//ul//li/div//div//span[
    # @class='PRIVATE_TreeView-item-content-text']//span" recorder.add_data((link, text, xpath_str)) logging.info(
    # '文件内容：' + recorder.data.__str__()) recorder.record()

    def markdown_url_to_files(self):
        file_path = './projectTempInfo/' + self._project_name + '.csv'
        logging.info('开始获取markdown文件内容：' + file_path)
        # 打开CSV文件
        with open(file_path, 'r', newline='', encoding='utf-8') as csvfile:
            # 创建CSV读取器
            reader = csv.reader(csvfile)
            # 逐行读取CSV文件内容
            for row in reader:
                # 打印每一行数据
                self.parse_second_file(row)

    def parse_second_file(self, row):
        self.page.get(row[0])
        seconds_files = self.page.eles(row[1])
        self.workDirectory = str(row[2])
        my_file_utile = MyFileUtil.MyFileUtil('./projectTempInfo/' + self._project_name + '/')
        my_file_utile.create_folder()
        for els in seconds_files:

            my_file_utile = MyFileUtil.MyFileUtil('./projectTempInfo/' + self._project_name + '/' + els.text)
            my_file_utile.create_folder()
            if str(els.text).endswith('.md'):
                print('开始处理：' + els.text + ' 文件')
                xpath = 'xpath://div//li[@class="PRIVATE_TreeView-item"]//span[@class="PRIVATE_TreeView-item-content-text"]//span[contains(text(), "' + els.text + '")]'
                self.page.ele(xpath).click()
                # https://raw.githubusercontent.com/jackfrued/Python-100-Days/master/Day01-15/01.%E5%88%9D%E8%AF%86Python.md
                md_download_url = 'https://raw.githubusercontent.com/jackfrued/Python-100-Days/master/' + row[
                    1] + '/' + els.text
                md_file_path = './projectTempInfo\\' + self._project_name + '' + '\\' + els.text
                logging.info('开始下载文件：' + md_file_path)
                self.page.download_set.by_DownloadKit()
                self.page.wait.download_begin()
                download_result = self.page.download(
                    md_download_url,
                    md_file_path,
                    None,
                    'overwrite',
                    show_msg=True
                )
                if download_result[0] == 'success':
                    self.handle_images(download_result[1])
            else:
                pass

    def markdown_to_blog(self, markdown, blog):
        print(self._project_url)
        return blog

    # md文件中的图片地址转为本地
    def handle_images(self, md_path):
        print('当前处理的文件夹：' + self.workDirectory)
        #  1 读取文件
        print(self._project_url)
        url_re = r"!\[.*?\]\((.*?)\)"
        # 读取markdown文件并获取图片数组
        with open(md_path, 'r', newline='', encoding='utf-8') as md_file:
            md_text = md_file.read()
        image_urls = re.findall(url_re, md_text)
        # 解析图片地址
        if len(image_urls) > 0:
            for img in image_urls:
                if img.startswith('http'):  # 处理网络图片
                    print('TODO handle this!')
                    pass
                elif img.startswith('./') or img.startswith('/') or img.startswith('\\'):  # 处理相相对路径的本地图片
                    folders = img.split('/')
                    if folders[0] == '.':
                        # for folder in folders:
                        #     print(folder)
                        for index in range(len(folders)):
                            if index == 0:
                                pass
                            elif index == len(folders) - 1:
                                pass
                            else:
                                print(self.workDirectory)
                                print(folders[index])
                else:
                    print('未知路径')
        else:
            logging.info('没有找到图片信息')

    def http_image_to_my_blog(self, image_url):
        print(self._project_url)
        pass


"""
=====================
===
===入口
===
=========================
"""
if __name__ == '__main__':
    githubMd2Blog = GithubProject()
    # 初始化项目信息
    githubMd2Blog.__int__('100天Python入门到放弃', 'https://github.com/jackfrued/Python-100-Days/tree/master/Day01-15',
                          'https://doocs.gitee.io/md/')
    # 解析项目第一层文件夹并返回路径
    tree_array = githubMd2Blog.parse_project__files()
    # 解析第一层文件夹下，并且返回第一层下的所有markdown文件列表
    githubMd2Blog.parse_folder_md_files(tree_array)
    # githubMd2Blog.markdown_url_to_files()
