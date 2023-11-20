import logging
import re

import DrissionPage
from DrissionPage.commons.constants import NoneElement
from DrissionPage.errors import ElementNotFoundError
import pyperclip

from githubMd2Blog.MyFileUtil import MyFileUtil


class Blog:
    # 配置日志记录器
    logging.basicConfig(level=logging.DEBUG, filename='blog.log', filemode='w',
                        format='%(asctime)s - %(levelname)s - %(message)s')

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
            is_login = self._chrome.ele('xpath://input[@id="username"]')
            if is_login is not NoneElement:
                is_login.input(self._blog_user_name)
                self._chrome.ele('xpath://input[@id="password"]').input(self._blog_pwd)
                self._chrome.ele('xpath://button').click()
            return True
        except ElementNotFoundError:
            logging.error('element not found,maybe is login status!')
            return False

    def upload_images(self, filepath):
        # 判断文件是否存在
        my_file_util = MyFileUtil(filepath)
        self.close_notice()
        if my_file_util.file_if_exists(filepath):
            self._chrome.ele('xpath://div//section//aside//div//ul/li[@title="图片管理"]').click()
            self._chrome.set.upload_files(filepath)
            self._chrome.eles('xpath://button[@type="button"]')[1].click()
            self._chrome.wait.upload_paths_inputted()
            logging.info('clicked the upload button!')
            clipboard_content = pyperclip.paste()
            print('get file_md_path:' + clipboard_content)
            """
                返回图片
            """
            # return self._chrome.ele('//div//section//aside//div//ul/li[@title="上传图片"]').click()
            filepath = filepath.replace("\\", "/")
            # file_name = 'xixi'
            if filepath.rfind('/') != -1:
                file_name = filepath[filepath.rfind('/') + 1:]
            else:
                return False
            url_re = r"!\[.*?\]\((.*" + file_name + ".*?)\)"
            if len(re.findall(url_re, clipboard_content, flags=0)) > 0:
                return clipboard_content
            else:
                logging.error('maybe have same name_picture!')
                new_file_path = my_file_util.change_file_name(filepath)
                if new_file_path is not False:
                    self.upload_images(new_file_path)
                else:
                    return False
        else:
            logging.error('file not exists!!')
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

    def close_notice(self):
        try:
            version_notice = self._chrome.ele('xpath://a[@class="ant-notification-notice-close"]')
            if version_notice is not NoneElement:
                version_notice.click()
                logging.info('Closed version update notice!!')
        except ElementNotFoundError:
            logging.info('Element not found when try to close version update notice!')


if __name__ == '__main__':
    blog = Blog()
    blog.__int__('https://jingjianqian.top/admin', 'joker', 'Jing.jianqian2334')
    blog.login()
    image_upload_result = blog.upload_images('D:\\data\\code\\back\\python\\MyDrissionPage\\githubMd2Blog\\projectTempInfo\\Python-100-Days\\Day01-15\\res\\python-idle.png')
