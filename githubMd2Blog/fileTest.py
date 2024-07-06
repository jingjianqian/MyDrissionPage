from githubMd2Blog import MyFileUtil

if __name__ == '__main__':
    file_name = '01.初识Python.md'
    filename = file_name.replace('.', '-')
    print(filename)
    MyFileUtil.MyFileUtil('./projectTempInfo/' + 'test').create_folder()