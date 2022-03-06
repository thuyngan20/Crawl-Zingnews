from linecache import _SourceLoader
from urllib.error import ContentTooShortError
from selenium import webdriver
from bs4 import BeautifulSoup
from dataaccess import DataAccess
import yaml


config = yaml.load(open("./config.yaml","r",encoding= "utf8"), Loader= yaml.FullLoader)
data_access = DataAccess(MONGO_URI = config["MONGO_URI"], MONGO_DB = config["MONGO_DB"])
options = webdriver.ChromeOptions()
options.add_argument("--headless")
driver = webdriver.Chrome(executable_path="./chromedriver",options=options)
driver.get("https://zingnews.vn/")
#sleep(3)

source = BeautifulSoup(driver.page_source)
p_tag = source.find_all('p',class_ ="article-title")
for p in p_tag:
    content = p.find('a').getText()
    link = p.find('a').get('href')

link = data_access.get_item(content = "Hành trình di tản khỏi Ukraine của nhóm người Việt")








    
