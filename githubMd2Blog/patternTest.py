import re


def change_markdown_file_image(markdown_file, target_file_name, new_image_url):
    img_pattern = re.compile(r'(!\[[^\]]*\]\([^)]*' + re.escape(target_file_name) + r'[^)]*\))')
    with open(markdown_file, 'r', encoding='utf-8') as file:
        markdown_file_text = file.read()
        file.close()
    updated_markdown = img_pattern.sub(new_image_url, markdown_file_text, )
    with open(markdown_file, 'w', encoding='utf-8') as file:
        file.write(updated_markdown)
        file.close()

if __name__ == '__main__':



    file_name = 'python-idle.png'
    img_pattern = re.compile(r'(!\[[^\]]*\]\([^)]*' + re.escape(file_name) + r'[^)]*\))')
    print(img_pattern)
    # 读取Markdown文件内容
    with open('./projectTempInfo/Python-100天从新手到大师/01.初识Python.md', 'r', encoding='utf-8') as file:
        content = file.read()
        # file.close()

    # c2 = 'hello world world world World'
    # strinfo = re.compile('world')
    # d2 = strinfo.sub('python', c2, )
    # print('2原始字符串:{}'.format(c2))
    # print('2替换字符串:{}'.format(d2))

    updated_markdown = img_pattern.sub('http://jingjianqian.top/test.jpg', content,)
    # print(updated_markdown)
    with open('./projectTempInfo/Python-100天从新手到大师/01.初识Python.md', 'w', encoding='utf-8') as file:
        file.write(updated_markdown)
        # file.close()

