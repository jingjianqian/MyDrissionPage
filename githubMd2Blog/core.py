"""
github 项目内部 markdown 转 博客以及
"""
import DrissionPage
from DrissionPage import *


class GithubProject:
    def __int__(self, project_url, markdown_2_blog_site):
        self._project_url = project_url  # 项目名称
        self._markdown_2_blog_site = markdown_2_blog_site  # markdown 转 blog文章网站

    def parse_project_md_files(self, md_file_lists=None):
        page = DrissionPage.ChromiumPage()
        page.get(self._project_url)
        project_src = page.eles("xpath://div[@class='js-details-container Details']//div[@role='rowheader']//a")
        # project_src[0].click()
        for ele in project_src:
            print(ele)
            ele.click()
        md_file_list = ['']
        return md_file_lists

    def markdown_to_blog(self, markdown, blog):
        print(self._projectname)
        return blog

    def handle_images(self, blog):
        pass


if __name__ == '__main__':
    githubMd2Blog = GithubProject()
    githubMd2Blog.__int__('https://github.com/jackfrued/Python-100-Days/tree/master', 'https://doocs.gitee.io/md/')
    githubMd2Blog.parse_project_md_files()
