from selenium import webdriver
from bs4 import BeautifulSoup
from dataaccess import DataAccess
import yaml

config = yaml.load(open("./config.yaml","r",encoding= "utf8"), Loader= yaml.FullLoader)
data_access = DataAccess(MONGO_URI = config["MONGO_URI"], MONGO_DB = config["MONGO_DB"])
options = webdriver.ChromeOptions()
options.add_argument("--headless")


links = data_access.get_link()
for link in links:
    try:
        driver = webdriver.Chrome(executable_path="./chromedriver",options=options)
        url = "https://zingnews.vn" + link['link']
        driver.get(url)
        soup = BeautifulSoup(driver.page_source)
        summary = soup.find('h1', class_ ="video-title")
        title = summary.find('a').getText()
        body = soup.find('p', class_ ="video-summary").getText()
        data_access.update_body(link['link'], title, body)
        driver.close()
    except:
        print(url + "lỗi")
    
    

