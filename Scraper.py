from bs4 import BeautifulSoup
import requests
import json

import re
from re import sub
from decimal import Decimal
import io
from datetime import datetime
import pandas as pd


class ScraperWuxiaworld:
    linksLOM = []
    spam = [
        "Пропущена глава или т.п. - сообщи в Комментариях. Улучшить Текст можно РЕДАКТОРом!",
        "Автор: Cuttlefish That Loves Diving, 爱潜水的乌贼",
        "«Прочитайте последние главы на Wuxiaworld.site",
        "Читать дальше главу о vipnovel.com",
        "Читать дальше на vipnovel.com",
        "Прочитайте больше глав на vipnovel.com"
    ]

    def InitLinksLOM(self):
        with open('links.json') as f:
            self.linksLOM = json.load(f)

    def LordOfMysteries(self, numPage):
        url = self.linksLOM[numPage-1]
        html_text = requests.get(url).text
        soup = BeautifulSoup(html_text, 'lxml')

        text = soup.find("div", class_ = "entry-content").find_all("p")
        text = [row.text for row in text[2:len(text)-1] ]

        for spam in self.spam:
            if spam in text:
                text.pop(text.index(spam))

        return text


# s = ScraperWuxiaworld()
# s.InitLinksLOM()
# f = s.LordOfMysteries(1059)
# print(f)