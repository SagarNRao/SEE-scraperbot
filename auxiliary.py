from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import time
import json

class Scraper:
    soup = ""
    page_title = ""
    links = []
    video_list = []
    
    
    def write_file(self,destination, contents):
        with open(destination, 'w', encoding='utf-8') as f:
            f.write(contents)
    
    def search_youtube(self, query):
        driver = webdriver.Edge()
        driver.get('https://www.youtube.com')
        search_box = driver.find_element(By.NAME, 'search_query')
        search_box.send_keys(query)
        search_box.send_keys(Keys.RETURN)
        time.sleep(5)
        html = driver.page_source
        driver.quit()
        self.write_file("search_output.html",html)
    
    def get_soup(self):
        with open('search_output.html', 'r', encoding='utf-8') as f:
            file_content = f.read()
            self.soup = BeautifulSoup(file_content, 'html5lib')
            self.write_file("html5test.html", str(self.soup))
            
    def get_title(self):
        self.page_title = self.soup.title.string
    
    def get_videos(self):
        for vid in self.soup.find_all("span", id="video-title"):
            self.video_list.append(str(vid.string).strip())
        self.video_list = [' '.join(word for word in item.split() if not word.startswith('#')) for item in self.video_list]
        video_json = json.dumps(self.video_list)
        self.write_file('vidlist.json', video_json)
        print("\n\n", video_json)