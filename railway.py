from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import csv

URL = ["https://ja.wikipedia.org/wiki/%E6%97%A5%E6%9C%AC%E3%81%AE%E9%89%84%E9%81%93%E8%B7%AF%E7%B7%9A%E4%B8%80%E8%A6%A7_%E3%81%82-%E3%81%8B%E8%A1%8C",
"https://ja.wikipedia.org/wiki/%E6%97%A5%E6%9C%AC%E3%81%AE%E9%89%84%E9%81%93%E8%B7%AF%E7%B7%9A%E4%B8%80%E8%A6%A7_%E3%81%95-%E3%81%AA%E8%A1%8C",
"https://ja.wikipedia.org/wiki/%E6%97%A5%E6%9C%AC%E3%81%AE%E9%89%84%E9%81%93%E8%B7%AF%E7%B7%9A%E4%B8%80%E8%A6%A7_%E3%81%AF-%E3%82%8F%E8%A1%8C"]
Selector = "body"

op = Options()
op.add_argument("--disable-gpu");
op.add_argument("--disable-extensions");
op.add_argument("--proxy-server='direct://'");
op.add_argument("--proxy-bypass-list=*");
op.add_argument("--start-maximized");
op.add_argument("--headless");
driver = webdriver.Chrome(options=op)

NGWords = ["通称", "愛称", "総称", "旧称"]
data = []
for i in range(3):
    driver.get(URL[i])
    WebDriverWait(driver, 30).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, Selector))
    )

    soup = BeautifulSoup(driver.page_source, features="html.parser")
    lists = soup.select("h3+ul > li")

    for li in lists:
        exist_ng = 0
        text = li.get_text()
        if "旅客鉄道" in text:
            for ng in NGWords:
                if ng in text:
                    exist_ng = 1
            if exist_ng == 1:
                continue

            el = li.select("a")
            row = []
            if len(el) == 1:
                row.append(el[0].get_text())
            else:
                row.append(el[0].get_text())
                row.extend([corp.get_text() for corp in el[1:] if ("旅客鉄道" in corp.get_text())])
            data.append(row)

with open('./railway.csv', 'w') as f:
    writer = csv.writer(f)
    for row in data:
        writer.writerow(row)
