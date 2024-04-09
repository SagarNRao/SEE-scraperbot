import time
from selenium import webdriver
# from selenium.chrome.service import service
from selenium.webdriver.common.by import By

url = 'https://www.youtube.com/@JohnWatsonRooney/videos'

driver = webdriver.Chrome()
driver.get(url)

videos = driver.find_element(By.CLASS_NAME, "style-scope ytd-rich-grid-row")

for video in videos:
    titles = video.find_element(By.XPATH, ".//a[@id='video-title']")
    for title in titles:
        print(title.text)

time.sleep(10)
