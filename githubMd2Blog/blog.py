import logging

import DrissionPage
from DrissionPage.errors import ElementNotFoundError

from githubMd2Blog.MyFileUtil import MyFileUtil


class Blog:
    def __int__(self, blog_admin_url, blog_user_name, blog_pwd):
        self._blog_admin_url = blog_admin_url
        self._blog_user_name = blog_user_name
        self._blog_pwd = blog_pwd
        self._chrome = DrissionPage.ChromiumPage()
    """
        上传图片到博客
    """
    def login(self):
        try:
            self._chrome.get(self._blog_admin_url)
            self._chrome.ele('xpath://input[@id="username"]').input(self._blog_user_name)
            self._chrome.ele('xpath://input[@id="password"]').input(self._blog_pwd)
            self._chrome.ele('xpath://button').click()
            return True
        except ElementNotFoundError:
            logging.error('元素没有找到')
            return False

    def upload_images(self, filepath):
        # 判断文件是否存在
        my_file_util = MyFileUtil(filepath)
        if my_file_util.file_if_exists():
            self._chrome.ele('//div//section//aside//div//ul/li[@title="图片管理"]').click()
            self._chrome.ele('//div//section//aside//div//ul/li[@title="上传图片"]').click()
            """
                返回图片
            """
            return self._chrome.ele('//div//section//aside//div//ul/li[@title="上传图片"]').click()
        else:
            logging.error('文件不存在')
            return False
    """
        编写文章并且发布
    """
    def public_blog(self):
        self._chrome.ele('//div//section//aside//div//ul/li[@title="文章管理"]').click()
        pass
    """
        发布已保存的全部文章
    """
    def public_all_blog(self):

        pass


if __name__ == '__main__':
    blog = Blog()
    blog.__int__('https://jingjianqian.top/admin', '', '')
    blog.login()
    image_upload_result = blog.upload_images('./githubMd2Blog/projectTempInfo/Python-100-Days/Day01-15/res/python-idle.png')






