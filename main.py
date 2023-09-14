# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
from DrissionPage import ChromiumPage
from pathlib import Path
import ddddocr

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


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi('PyCharm')

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
