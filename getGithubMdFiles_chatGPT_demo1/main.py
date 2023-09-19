import DrissionPage
from bs4 import BeautifulSoup
import requests
import re
import os


def save_file(url, save_path):
    response = requests.get(url)
    with open(save_path, 'wb') as file:
        file.write(response.content)


def process_images(md_content, md_path):
    soup = BeautifulSoup(md_content, 'html.parser')
    img_tags = soup.find_all('img')
    for img_tag in img_tags:
        img_url = img_tag.get('src')
        if img_url.startswith('http'):
            response = requests.get(img_url)
            img_filename = os.path.basename(img_url)
            img_save_path = os.path.join(os.path.dirname(md_path), img_filename)
            with open(img_save_path, 'wb') as img_file:
                img_file.write(response.content)
            img_tag['src'] = img_filename
    return str(soup)


def save_md_files_from_github(owner, repo, save_dir):
    url = f"https://github.com/{owner}/{repo}"

    response = requests.get(url)
    page_content = response.text

    md_file_urls = re.findall(r'href="(.*\.md)"', page_content)

    for md_file_url in md_file_urls:

        md_response = requests.get(md_file_url)
        md_content = md_response.text

        md_filename = os.path.basename(md_file_url)
        md_save_path = os.path.join(save_dir, md_filename)

        processed_md_content = process_images(md_content, md_save_path)

        with open(md_save_path, 'w', encoding='utf-8') as md_file:
            md_file.write(processed_md_content)


if __name__ == '__main__':
    owner = "jingjianqian"
    repo = "https://github.com/jackfrued/Python-100-Days"
    save_dir = "./projects"

    save_md_files_from_github(owner, repo, save_dir)
