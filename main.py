# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
from DrissionPage import ChromiumPage
from pathlib import Path
import ddddocr
from DrissionPage.errors import ElementNotFoundError


class Primeton:
    main_url = 'https://ame.primeton.com/'
    emai_address = 'https://mail.primeton.com/'
    in_common_emails = ['C205-JSRH@primeton.com', 'huln@primeton.com']

    def print_hi(name):
        # Use a breakpoint in the code line below to debug your script.
        print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.
        page = ChromiumPage()
        page.get('')
        page.ele('#username').input('')
        page.ele('#password').input('')
        image_base64 = page.ele("xpath://div[@id='verifyCode_container']/img").get_src()
        with open("./images/code.jpg", 'wb') as f:
            f.write(image_base64)
        with open('./images/code.jpg', 'rb') as f:
            image_read = f.read()
        ocr = ddddocr.DdddOcr()
        result = ocr.classification(image_read)
        print(result)
        page.ele("xpath://input[@name='verifyCode']").input(result)
        page.ele('#login_btn').click()

        # print()
        # page.ele('#login_btn').click()

    # 个人周报
    def personal_week_report(self):
        page = ChromiumPage()
        try:

            """
                登录
            """
            page.get(self.emai_address)
            page.ele('xpath://div//input[@id="qquin"]').input('jingjq')
            page.ele('xpath://div//div//input[@id="pptext"]').input('')
            page.ele('xpath://div//div//input[@type="submit"]').click()
            """
                写信
            """
            page.ele("//div//div//ul/li//a[@id='composebtn']").input(self.emai_address[0])

            """
              抄送人
            """
            page.ele("").input(self.emai_address[1])

            """
              新建内容
            """
            content = """
            <div>
                <font>各位领导、同事：</font>
            </div>
            <div>
                <font>&nbsp;大家好，本人双周滚动计划如下：</font>
            </div>
            一、售前
             无
            二、客户/项目支持
             1、广西路桥集团
                  1)  确认部门业务规则
                  2）确认业务规则版本
                  3) 根据业务规则调整系统数据
             
            三、组织工作
            无
            四、下周工作
             1、广西路桥集团
                  1)  处理部分反馈的BUG
                  2）沟通协调数据问题核对方案
                  3）现阶段数据问题整理对比
                  4）沟通后续系统升级优化
            """
        except ElementNotFoundError:
            print('找不到元素')


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    primeton = Primeton()
    primeton.personal_week_report()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
