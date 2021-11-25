from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import json

opt = webdriver.ChromeOptions()
#opt.add_argument('headless') 

driver = webdriver.Chrome(".\chromedriver", options=opt)

driver.get("https://wuxiaworld.ru/povelitel-tajn-lord-of-the-mysteries/povelitel-tajn-glava-517-gorod-shhedrosti-ranobe-chitat-onlajn/")

# content = driver.find_elements(By.CLASS_NAME,"ex1")

# print(f"\nKEK: {len(content)}\n")

# for i in range(len(content)):
#     content[i].click()

time.sleep(30)

content = driver.find_elements(By.CSS_SELECTOR,".nested.active li a")
print(f"\nKEK: {len(content)}\n")
links = [elem.get_attribute("href") for elem in content]

with open('data.json', 'w') as f:
    json.dump(links, f)

time.sleep(30)