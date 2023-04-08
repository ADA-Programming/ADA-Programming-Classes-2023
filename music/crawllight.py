"""Web scraping and crawling.
BeautifulSoup documentation: https://www.crummy.com/software/BeautifulSoup/bs4/doc/
"""

#%%
# Setup / Data

# import requests
from bs4 import BeautifulSoup
from selenium import webdriver
import pandas as pd

from util import utility
from settings import *

#%%
# Getting started

# The Website to work with, i.e. to scrape info from and crawl over it - Ultimate Classic Rock.
# The starting URL refers to articles about George Harrison.
start_url = 'https://ultimateclassicrock.com/search/?s=George%20Harrison'


#%%
def get_soup_selenium(url: str) -> BeautifulSoup:
    """Returns BeautifulSoup object from the corresponding URL, passed as a string.
    Makes an HTTP GET request, using driver = webdriver.Chrome() from the selenium package and its driver.get(url).
    Then uses the page_source field of the driver object and the 'html.parser' to create and return the BeautifulSoup o.
    """

    # Before running the line driver = webdriver.Chrome(),
    # make sure to download and unzip chromedriver and put chromedriver.exe
    # in the Scripts subfolder of your Python installation folder,
    # e.g. C:\Users\Vladan\AppData\Local\Programs\Python\Python310\Scripts.
    # The driver should be downloaded from https://chromedriver.chromium.org/downloads.
    # Then you need not provide the path of the driver, just run: driver = webdriver.Chrome().
    # (Adapted from https://stackoverflow.com/a/60062969/1899061.)

    driver = webdriver.Chrome()
    driver.get(url)
    return BeautifulSoup(driver.page_source, 'html.parser')


#%%
# Test get_soup_selenium(url)
soup = get_soup_selenium(start_url)
print(soup)


#%%
def get_specific_page(start_url: str, page=1):
    """Returns a specific page from a Website where long lists of items are split in multiple pages.
    """

    if page > 1:
        return start_url.split('&searchpage=')[0] + '&searchpage=' + str(page)
    return start_url.split('&searchpage=')[0]


#%%
# Test get_specific_page(start_url, page)
print(get_specific_page(start_url, 3))


#%%
def get_next_soup_selenium(start_url: str, page=1):
    """Returns the BeautifulSoup object corresponding to a specific page
    in case there are multiple pages that list objects of interest, using selenium instead of requests.
    Parameters:
    - start_url: the starting page/url of a multi-page list of objects
    - page: the page number of a specific page of a multi-page list of objects
    Essentially, get_next_soup() just returns get_soup_selenium(get_specific_page(start_url, page)),
    i.e. converts the result of the call to get_specific_page(start_url, page), which is a string,
    into a BeautifulSoup object.
    """

    return get_soup_selenium(get_specific_page(start_url, page))


#%%
# Test get_next_soup_selenium(start_url: str, page=1)
soup = get_next_soup_selenium(start_url, 3)
print(soup)


#%%
def crawl(url: str, max_pages=1):
    """Web crawler that collects info about specific articles from Ultimate Classic Rock,
    implemented as a Python generator that yields BeautifulSoup objects (get_next_soup() or get_next_soup_selenium())
    from multi-page movie lists.
    Parameters: the url of the starting page and the max number of pages to crawl in case of multi-page lists.
    """

    for page in range(max_pages):
        yield get_next_soup_selenium(url, page + 1)
        page += 1


#%%
# Test crawl(url: str, max_pages=1)
gen = crawl(start_url, 3)
count = 1
while True:
    try:
        soup = next(gen)
        print('Done', count)
        count += 1
    except StopIteration:
        break
print('OK, that\'s it :)')

#%%
# Save BeautifulSoup object to an HTML file,
# using <Path-file-object>.write_text(str(<BeautifulSoup object>), encoding='utf-8', errors='replace').
file = DATA_DIR / 'soup.html'
file.write_text(str(soup), encoding='utf-8', errors='replace')

#%%
# Demonstrate <BeautifulSoup object>.find('<tag>'); e.g., find the first 'article' tag.
article = soup.find('article')
print(article)

#%%
# Demonstrate <BeautifulSoup object>.find('<tag>').find('<nested tag>'); e.g., find the 'a' tag in an 'article' tag.
print(soup.find('article').find('a'))
print(soup.find('article').find('a').text)

#%%
# Demonstrate getting a dictionary of all attributes of a tag (e.g., for an 'a' tag nested in an 'article' tag),
# using <tag>.attrs.
print(article.find('a').attrs)

#%%
# Demonstrate getting a tag with specific attributes
# using <BeautifulSoup object>.find('<tag>', {'<attribute>': '<value>'});
# e.g., find a 'div' tag with the 'article-image-wrapper' attribute, and then another 'div' tag with the 'content' att.
print(soup.find('div', {'class': 'article-image-wrapper'}))
print()
print(soup.find('div', {'class': 'content'}))

#%%
# Demonstrate getting values of tag attributes,
# e.g. <BeautifulSoup object>.find('<tag>').text for a 'div' tag, for an 'article' tag, and for an 'a' tag.
print(soup.find('div', {'class': 'article-image-wrapper'}).text)
print()
print(soup.find('article').text)
print()
print(soup.find('article').find('a').text)
print()
print(soup.find('span', {'class': 'visually-hidden'}).text)

#%%
# Demonstrate <BeautifulSoup object>.find_all(<tag>), e.g. for the 'article' tag; returns a ResultSet object.
articles = soup.find_all('article')
print(type(articles))

#%%
# Demonstrate occasional anomalies in the ResultSet returned by <BeautifulSoup object>.find_all(<tag>);
# note that they may be appearing only in the selenium version, not in the requests version.

# The following lines show that there are 11 articles on the page, not 10.
# The 11th one is something else, not visible on the page at the first glance and should be eliminated from
# further processing.
print(len(articles))

#%%
# The following line shows an anomaly in the articles ResultSet.
print(articles[10])

#%%
# Compare it to any of the other results from the Result set returned by ResultSet
# returned by <BeautifulSoup object>.find_all(<tag>).
print(articles[0])
print(articles[1])
# ...

#%%
# Demonstrate <tag>.find_next_siblings() (returns all <tag>'s siblings) and
# <tag>.find_next_sibling() (returns just the first one); e.g., use the 'div' tag, class='rowline clearfix'.
# IMPORTANT: <tag> MUST be a Tag object (e.g., a 'span' tag) encompassed by ANOTHER tag (e.g., a 'div' tag) AND
# having same-level siblings (e.g., multiple 'span' tags at the same level), not a ResultSet object!!!
all_articles_encompassing_div_tag = soup.find('div', {'class': 'rowline clearfix'})
first_span_tag = all_articles_encompassing_div_tag.find('span')
print(first_span_tag)
print()
print(first_span_tag.find_next_sibling())
print()
print()
print()

for sibling in first_span_tag.find_next_siblings():
    print(sibling, '\n')

#%%
# Each bs4.element.ResultSet, bs4.element.Tag,... can be used to create another BeautifulSoup object,
# using BeautifulSoup(str(<bs4.element object>), features='html.parser').
sibling_soup = BeautifulSoup(str(sibling), 'html.parser')
print(sibling_soup)

#%%
# Get/Return all text from a bs4.element.Tag object, using <bs4.element.Tag object>.text, e.g. for an 'article' tag.
print(article.text)

#%%
# Get/Return and remove a specific item from a bs4.element.ResultSet using <result set>.pop(<index>) (default: last).
print(len(articles))
articles.pop()
print(len(articles))


#%%
def get_article_info_list(start_url: str, max_pages=1):
    """
    Returns structured information about articles related to George Harrison from a multi-page article list.
    :param start_url: the url of the starting page of a multi-page article list
    :param max_pages: the max number of pages to crawl
    :return: a list of tuples of info-items about the articles from a multi-page article list
    Creates and uses the following data:
    - article_title
    - article_date
    - article_author
    - featured_image_url
    """

    gen = crawl(start_url, max_pages)
    article_info_list = []
    while True:
        try:
            soup = next(gen)
            articles = soup.find_all('article')[:-1]
            for article in articles:
                figure = article.find('div', {'class': 'article-image-wrapper'})
                content = article.find('div', {'class': 'content'})
                article_date = content.find('time').text
                article_title = content.a.text
                article_author = content.em.text.split('by')[1].lstrip()
                featured_image_url = figure.find('a').attrs['data-image']
                article_info_list.append((article_title, article_author, article_date, featured_image_url))
        except StopIteration:
            break
    return article_info_list


#%%
# print(article.find('a').attrs)
# print()
# print(article.find('a').attrs['data-image'])

# figure = article.find('div', {'class': 'article-image-wrapper'})
# featured_image_url = figure.find('a').attrs['data-image']
# print(featured_image_url)

# content = article.find('div', {'class': 'content'})
# article_date = content.find('time').text
# print(article_date)

# content = article.find('div', {'class': 'content'})
# article_title = content.a.text
# print(article_title)

# content = article.find('div', {'class': 'content'})
# article_author = content.em.text.split('by')[1].lstrip()
# print(article_author)

#%%
# Test get_article_info_list(start_url: str, max_pages=1)
article_info_list = get_article_info_list(start_url, 3)
print(article_info_list)

#%%
# Put everything in a csv file

# # Alternatuve 2, using Pandas
# csv_file = DATA_DIR / 'articles.csv'
# df = pd.DataFrame(article_info_list, columns=['Title', 'Author', 'Date', 'Featured image'])
# # df
# df.to_csv(csv_file)

csv_file = DATA_DIR / 'articles.csv'
df = pd.DataFrame(article_info_list, columns=['Title', 'Author', 'Date', 'Image'])
df.to_csv(csv_file)
print('Done.')

#%%
df = pd.read_csv(csv_file)
df
