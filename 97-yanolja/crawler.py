import json
import time

from bs4 import BeautifulSoup
from selenium import webdriver

URL = 'https://www.yanolja.com/reviews/domestic/1000086255?sort=HOST_CHOICE'

def crawl_yanolja_reviews():
    rewiew_list = []
    options = webdriver.ChromeOptions()
    # options = webdriver.FirefoxOptions()
# required for idx.dev because no user interface is available
    options.add_argument('--headless')
    # driver = webdriver.Firefox(options=options)
    driver = webdriver.Chrome(options=options)
    driver.get(URL)
    time.sleep(3)

    scroll_count = 10
    for i in range(scroll_count):
# Suggested code may be subject to a license. Learn more: ~LicenseLog:4268613303.
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(3)

    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    review_containers = soup.select('#__next > section > div > div.css-1js0bc8 > div')
    for i in range(len(review_containers)):
        review_text = review_containers[i].find('p', class_='content-text').text
        review_star = review_containers[i].find_all('path', {'fill-rule': 'evenodd'})
        star_cnt = 5 - len(review_star)
        date = review_containers[i].find('p', class_='css-1irbwe1').text

        review_dict = {
            'review_text': review_text,
            'stars': star_cnt,
            'date': date
        }
        rewiew_list.append(review_dict)
    with open('./res/yanolja_reviews.json', 'w', encoding='utf-8') as f:
        json.dump(rewiew_list, f, ensure_ascii=False, indent=4)


if __name__ == '__main__':
    crawl_yanolja_reviews()

