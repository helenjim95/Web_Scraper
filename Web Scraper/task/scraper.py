import string
import os
import requests
from bs4 import BeautifulSoup

page = 0
page_num = int(input())
user_article_type = input()

def create_directory(page):
    directory_name_template = string.Template("Page_$N")
    directory_name = directory_name_template.substitute(N=str(page))
    print("directory_name:", directory_name)
    directory = directory_name
    parent_dir = os.getcwd()
    path = os.path.join(parent_dir + "\\" + directory)
    os.mkdir(path)
    print("path", path)
    return path


def format_title(article_title):
    article_title_formatted = ""
    for i in (string.punctuation + '—'):
        if i in article_title:
            article_title = article_title.replace(i, '')
    article_title_formatted = article_title.replace(" ", "_")
    return article_title_formatted


for i in range(page_num):
    page = i + 1
    nature_url = "https://www.nature.com/nature/articles?sort=PubDate&year=2020&page=" + str(page)
    path = create_directory(page)
    links = []
    saved_articles = []
    nature_url_content = requests.get(nature_url).content
    nature_url_soup = BeautifulSoup(nature_url_content, "html.parser")
    #  find the articles
    nature_soup_articles = nature_url_soup.find_all('article')
    for article in nature_soup_articles:
        article_type = article.find('span', "c-meta__type").text
        if article_type == user_article_type:
            html_start = "https://www.nature.com"
            links.append(html_start + article.find('a').get('href'))
    # print("links", links)

    for link in links:
        url = link
        r2 = requests.get(url, headers={'Accept-Language': 'en-US,en;q=0.5'})
        soup2 = BeautifulSoup(r2.content, "html.parser")
        article_title = soup2.find("title").text.strip()
        # print("article_title", article_title)
        # format filename
        name_formatted = format_title(article_title)
        filename_template = string.Template("$name_formatted.txt")
        filename = filename_template.substitute(name_formatted=name_formatted)
        # print("filename", filename)
        filepath = os.path.join(path + "\\" + filename)
        with open(filepath, 'w', encoding="utf-8") as file:
            page_content = soup2.find('div', {'class': "c-article-body"}).text.strip().replace("\n", "")
            # print(page_content)
            file.write(page_content)
        saved_articles.append(filename)
        # print("Content saved.")
    print(saved_articles)

