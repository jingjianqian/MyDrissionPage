import DrissionPage
from DrissionPage._configs.chromium_options import ChromiumOptions

if __name__ == '__main__':
    do1 = ChromiumOptions()
    do1.set_local_port(port=1234)
    do1.set_load_mode()
    pag = DrissionPage.ChromiumPage(do1)

