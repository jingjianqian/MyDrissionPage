"""
github 项目内部 markdown 转 博客以及
"""
import pathlib
import re

import MyFileUtil
import logging
import DrissionPage
from DataRecorder import Recorder
import csv


class GithubProject:

    def __init__(self):
        self.page = None
        self.base_host = 'https://github.com'  # 默认主页
        self.base_host_file_host = 'https://raw.githubusercontent.com'  # 默认.md文件浏览地址
        self.default_master = "master"  # 默认分支
        self.workDirectory = ''
        # 配置日志记录器
        logging.basicConfig(level=logging.DEBUG, filename='app.log', filemode='w',
                            format='%(asctime)s - %(levelname)s - %(message)s')

    def __int__(self, project_name, project_url, markdown_2_blog_site):
        self._project_url = project_url  # 项目地址
        self._project_name = project_name  # 项目名称
        self._markdown_2_blog_site = markdown_2_blog_site  # markdown 转 blog文章网站

    def parse_project_md_files(self, md_file_lists=None):
        logging.info('开始爬取:' + self._project_name + '项目的Markdown文件')
        self.page = DrissionPage.ChromiumPage()
        logging.info('访问项目地址中：' + self._project_url)
        # main_tab_id =
        self.page.get(self._project_url)

        mypath = pathlib.Path('./projectTempInfo/')
        logging.info('存储项目基本信息：' + str(mypath.absolute()))
        mypath.mkdir(parents=True, exist_ok=True)  # 创建文件夹
        file = str(mypath) + '/' + self._project_name + '.csv'
        pathlib.Path(file).touch(mode=438, exist_ok=True)
        # with './projectTempInfo/'+self._project_name+'.csv'.open
        recorder = Recorder('./projectTempInfo/' + self._project_name + '.csv')
        recorder.clear()
        project_src = self.page.eles("xpath://div[@class='js-details-container Details']//div[@role='rowheader']//a")
        with open('./projectTempInfo/' + self._project_name + '.csv', 'r+') as f:
            f.truncate(0)
        for ele in project_src:
            text = ele.text
            link = ele.link
            xpath_str = "xpath://ul/li[@id='" + text + "-item']//ul//li/div//div//span[@class='PRIVATE_TreeView-item-content-text']//span"
            recorder.add_data((link, text, xpath_str))
            logging.info('文件内容：' + recorder.data.__str__())
        recorder.record()

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


if __name__ == '__main__':
    githubMd2Blog = GithubProject()
    githubMd2Blog.__int__('100天Python入门到放弃', 'https://github.com/jackfrued/Python-100-Days',
                          'https://doocs.gitee.io/md/')
    githubMd2Blog.parse_project_md_files()
    githubMd2Blog.markdown_url_to_files()
