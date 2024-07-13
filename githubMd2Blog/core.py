"""
github 项目内部 markdown 转 博客以及
"""
import csv
import logging
import re
import time

import DrissionPage
from DrissionPage._configs.chromium_options import ChromiumOptions
from DrissionPage.errors import *

from githubMd2Blog import MyFileUtil
from githubMd2Blog.LskyApi import LskyApi


def change_markdown_file_image(markdown_file, target_file_name, new_image_url):
    img_pattern = re.compile(r'(!\[[^\]]*\]\([^)]*' + re.escape(target_file_name) + r'[^)]*\))')
    with open(markdown_file, 'r', encoding='utf-8') as file:
        markdown_file_text = file.read()
        file.close()
    updated_markdown = img_pattern.sub(new_image_url, markdown_file_text, )
    with open(markdown_file, 'w', encoding='utf-8') as file:
        file.write(updated_markdown)
        file.close()


def replace_markdown_image_urls(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()
        reg = r"!\[([^\]]*)\]\(([^)]+)\)"
        new_content = re.sub(reg, r'![\1](www.baidu.com)', content)
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(new_content)


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
    =========初始化基础数据===============
    ======@project_name: 项目名称
    ======@project_url:项目地址(注意是项目文件夹结构地址)
    ======@markdown_2_blog_site:博客地址
    ==========================================
    """

    def __int__(self, project_name: str, project_url: str, markdown_2_blog_site: object):
        self._project_url = project_url  # 项目地址
        self._project_name = project_name  # 项目名称
        self._markdown_2_blog_site = markdown_2_blog_site  # markdown 转 blog文章网站


    """
    =========第一步、获取项目第一层文件夹清单===============
    ======
    ======@return_tree_array:第一层文件夹列表清单
    ======
    ==========================================
    """

    def parse_project__files(self):
        print('=======================================第一步============================================')
        logging.info('=======================================第一步============================================')
        logging.info('开始爬取:' + self._project_name + '项目的Markdown文件')
        print('开始爬取:' + self._project_name + '项目的Markdown文件')
        logging.info('开始爬取:' + self._project_name + '项目的Markdown文件')
        """打开浏览器"""
        self.page = DrissionPage.ChromiumPage()
        """设置下载路径"""
        self.page.set.download_path('./projectTempInfo/')
        print('访问项目地址中：' + str(self._project_url))
        logging.info('访问项目地址中：' + str(self._project_url))
        """访问项目地址"""
        self.page.get(str(self._project_url))
        """寻找第一层文件夹"""
        first_levels = self.page.eles("xpath:/html/body//ul//li[@class='PRIVATE_TreeView-item' and @aria-level='1']")
        print('找到第一层文件情况数量：' + str(len(first_levels)))
        logging.info('找到第一层文件情况数量：' + str(len(first_levels)))
        """
            获取每一个文件夹的访问路径，放到数据返回
        """
        return_tree_array = []
        for first_levels_name in first_levels:
            tree_name = first_levels_name.attr("id")
            return_tree_array.append(self._API_TREE_URL + '/' + tree_name.replace('-item', ''))
        print('结束爬取:' + self._project_name + '项目的Markdown文件,一共爬取文件夹数量：' + str(len(return_tree_array)) + '个')
        logging.info('结束爬取:' + self._project_name + '项目的Markdown文件,一共爬取文件夹数量：' + str(len(return_tree_array)) + '个')
        print('=======================================第一步============================================')
        logging.info('=======================================第一步============================================')
        return return_tree_array

    """
    =========第二步、获取第一步每个文件夹下的markdown_list文件清单===============
    ======
    ======@return_tree_array:第一层文件夹列表清单
    ======
    ==========================================
    """

    def parse_folder_md_files(self, _tree_array):
        print('=======================================第二步============================================')
        logging.info('=======================================第二步============================================')
        print('开始循环：' + str(len(_tree_array) + 1) + '文件夹')
        logging.info('开始循环：' + str(len(_tree_array) + 1) + '文件夹')
        current = 1
        _markdown_list = dict()
        for tree_url in _tree_array:
            print('开始获取第' + str(current) + '个文件夹路径下的markdown文件列表,路径地址为：' + str(tree_url))
            logging.info('开始获取第' + str(current) + '个文件夹路径下的markdown文件列表,路径地址为：' + str(tree_url))
            current = current + 1
            self.page.get(tree_url)
            time.sleep(1)
            try:
                md_files = self.page.eles("xpath:/html//tbody//tr//td[@colspan='1']//div["
                                      "@class='react-directory-filename-column']//a")
            except ElementNotFoundError:
                continue
            markdown_files_count = 0
            for file_name in md_files:
                temp_tile = file_name.attr('title')
                temp_href = file_name.attr('href')
                if temp_href.endswith(".md"):
                    _markdown_list[temp_tile] = temp_href
                    markdown_files_count = markdown_files_count + 1
                else:
                    pass
        print(_markdown_list)
        print('=======================================第二步============================================')
        logging.info('=======================================第二步============================================')
        return _markdown_list
    """
    =========第四步，解析markdown文件===============
    ======
    ======
    ======
    ==========================================
    """
    def parse_md_link_to_md_file(self, md_files_array):
        print('=======================================第三步============================================')
        logging.info('=======================================第三步============================================')
        print(len(md_files_array))
        for file_name in md_files_array:
            md_link = md_files_array[file_name]
            print('访问：' + md_link + ' 文件地址')
            self.page.get(md_link)
            time.sleep(1)
            self.page.set.download_path('./projectTempInfo/' + self._project_name)
            self.page.set.when_download_file_exists('overwrite')
            self.page.set.download_file_name(file_name)  # 设置文件名
            try:
                self.page.ele("xpath://button[@aria-label='Download raw content']").click()
            except ElementNotFoundError:
                continue

            time.sleep(1)
            self.page.wait.download_begin()  # 等待下载开始
            print(file_name + '下载中')
            logging.info(file_name + '下载中')
            time.sleep(1)
            mission = self.page.wait.all_downloads_done()  # 等待所有任务结束
            if mission is not True:
                continue
            target_file = './projectTempInfo/' + self._project_name + '/' + file_name
            print(file_name + '下载完成')
            logging.info(file_name + '下载完成')
            time.sleep(1)
            """开始处理文章内的图片"""
            try:
                image_urls = self.page.eles("xpath:/html//article//a[@rel='noopener noreferrer']")
            except ElementNotFoundError:
                continue
            print(image_urls)
            do1 = ChromiumOptions().set_paths(local_port=9111).set_load_mode('none')
            for image in image_urls:
                img_urm = image.attr('href')
                # print(img_urm)
                page2 = DrissionPage.ChromiumPage(do1)
                base_path = './projectTempInfo/' + self._project_name + '/images/'
                MyFileUtil.MyFileUtil(base_path).create_folder()
                temp_path = base_path + file_name.replace('.', '-')
                MyFileUtil.MyFileUtil(temp_path).create_folder()
                page2.set.download_path(temp_path)
                page2.set.when_download_file_exists('overwrite')
                page2.get(img_urm)
                try:
                    page2.ele("xpath://button[@aria-label='Download raw content']").click()
                except ElementNotFoundError:
                    continue
                page2.wait.download_begin()  # 等待下载开始
                last_slash_index = img_urm.rfind('/')
                # 提取斜杠后面的部分作为文件名
                image_file_name = img_urm[last_slash_index + 1:]

                lsky_api = LskyApi()
                lsky_api.tokens('18697998680@163.com', '')
                try:
                    res_json = lsky_api.upload(temp_path + '/' + image_file_name)
                except TypeError:
                    res_json = None
                if res_json is not None:
                    new_image_url = res_json['data']['links']['markdown']
                else:
                    new_image_url = ''
                print(file_name + '下载中')
                logging.info(file_name + '下载中')
                time.sleep(1)
                sec_mission = page2.wait.all_downloads_done()  # 等待所有任务结束
                if sec_mission is not True:
                    continue
                print(file_name + '下载完成')
                logging.info(file_name + '下载完成')
                """
                    markdown中的图片地址替换成模板地址
                """
                print("要修改的文件：")
                print(target_file)
                print("图片关键字:")
                print(image_file_name)
                print("目标路径:")
                print(new_image_url)
                change_markdown_file_image(target_file, image_file_name, new_image_url)
                # change_markdown_file_image(markdown_file_path, target_file_name, new_image_url):
                time.sleep(1)
                page2.close()

    """
    将文件中的Markdown图片地址替换为固定的www.baidu.com。

    参数:
    file_path (str): 要处理的文件路径。
    """

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
        file_path = './projectTempInfo/' + str(self._project_name) + '.csv'
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
    githubMd2Blog.__int__('Python-100天从新手到大师', 'https://github.com/jackfrued/Python-100-Days/tree/master/Day01-15/',
                          'https://doocs.gitee.io/md/')
    # 解析项目第一层文件夹并返回路径
    tree_array = githubMd2Blog.parse_project__files()
    # 解析第一层文件夹下，并且返回第一层下的所有markdown文件列表
    markdown_list = githubMd2Blog.parse_folder_md_files(tree_array)
    githubMd2Blog.parse_md_link_to_md_file(markdown_list)
    # githubMd2Blog.markdown_url_to_files()
