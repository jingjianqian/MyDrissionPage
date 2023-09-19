"""
github 项目内部 markdown 转 博客以及
"""
import pathlib

import DrissionPage
from DataRecorder import Recorder
import csv


class GithubProject:

    def __init__(self):
        self.page = None

    def __int__(self, project_name, project_url, markdown_2_blog_site):
        self._project_url = project_url  # 项目地址
        self._project_name = project_name  # 项目名称
        self._markdown_2_blog_site = markdown_2_blog_site  # markdown 转 blog文章网站

    def parse_project_md_files(self, md_file_lists=None):
        self.page = DrissionPage.ChromiumPage()
        print(self._project_url)
        main_tab_id = self.page.get(self._project_url)
        mypath = pathlib.Path('./projectTempInfo/')
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
            xpath_str = "xpath://ul/li[@id='" + text + "-item']//ul//li"
            recorder.add_data((link, text, xpath_str))
        recorder.record()

    def mardkdown_url_to_files(self):
        file_path = './projectTempInfo/' + self._project_name + '.csv'
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
        for els in seconds_files:
            print(els.inner_html)

    def markdown_to_blog(self, markdown, blog):
        print(self._project_url)
        return blog

    def handle_images(self, blog):
        pass


if __name__ == '__main__':
    githubMd2Blog = GithubProject()
    githubMd2Blog.__int__('100天Python入门到放弃', 'https://github.com/jackfrued/Python-100-Days',
                          'https://doocs.gitee.io/md/')
    githubMd2Blog.parse_project_md_files()
    githubMd2Blog.mardkdown_url_to_files()
