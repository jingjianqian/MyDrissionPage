import logging

import DrissionPage
from DrissionPage.errors import ElementNotFoundError


class Imageshack:
    def __int__(self,url,username,pwd):
        self._url = url
        self._username = username
        self._pwd = pwd

    def upload_image(self):
        try:
            chrome = DrissionPage.ChromiumPage()
            chrome.get(self._blog_admin_url)
            chrome.ele('').input(self._blog_user_name)
            chrome.ele('').input(self._blog_pwd)
            chrome.ele('').click()

        except ElementNotFoundError:
            logging.error('元素没有找到')
            return False
