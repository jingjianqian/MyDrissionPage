import time

import DrissionPage
from DrissionPage._configs.chromium_options import ChromiumOptions

if __name__ == '__main__':
    md_file_dict = {'01.初识Python.md': 'https://github.com/jackfrued/Python-100-Days/blob/master/Day01-15/01.%E5%88%9D%E8%AF%86Python.md'
                    , '02.语言元素.md': 'https://github.com/jackfrued/Python-100-Days/blob/master/Day01-15/02.%E8%AF%AD%E8%A8%80%E5%85%83%E7%B4%A0.md'}
    for key in md_file_dict:
        md_link = md_file_dict[key]
        page = DrissionPage.ChromiumPage()
        page.get(md_link)
        page.set.download_path('./projectTempInfo/')
        page.set.when_download_file_exists('overwrite')
        page.set.download_file_name(key)  # 设置文件名
        # page.wait.download_begin()  # 等待下载开始
        page.ele("xpath://button[@aria-label='Download raw content']").click()
        page.wait.download_begin()  # 等待下载开始
        print("下载中。。。。")
        page.wait.all_downloads_done()  # 等待所有任务结束
        print("下载完成。。。。")
        """开始处理文章内的图片"""
        image_urls = page.eles("xpath:/html//article//a[@rel='noopener noreferrer']")
        print(image_urls)
        do1 = ChromiumOptions().set_paths(local_port=9111)
        for image in image_urls:
            img_urm = image.attr('href')
            print(img_urm)
            page2 = DrissionPage.ChromiumPage(do1)
            page2.set.download_path('./projectTempInfo/')
            page2.set.when_download_file_exists('overwrite')
            page2.get(img_urm)
            page2.ele("xpath://button[@aria-label='Download raw content']").click()
            time.sleep(5)
            page2.close()
            # print("下载完成。。。。")
            # time.sleep(3)
            # page.ele("xpath://button[@aria-label='Download raw content']").click()
            # page.wait.download_begin()  # 等待下载开始
            # print("下载中。。。。")
            # page.wait.all_downloads_done()  # 等待所有任务结束
            # print("下载完成。。。。")
            # if image+''.startWith('http'):
            #     print("直接下载即可")
            # elif image.startWith('/'):
            #     print("相路径，处理即可")
            #     res = page.download(image)
            #     print(res)
            # else:
            #     print("不知道的，需要特别处理")

