from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from youtube_transcript_api import YouTubeTranscriptApi
from bs4 import BeautifulSoup
from dotenv import load_dotenv, dotenv_values
from youtube_transcript_api import YouTubeTranscriptApi
import google.generativeai as genai
import requests
import os
import time
import json

class Scraper:
    soup = ""
    page_title = ""
    links = []
    video_dict = {}
    
    
    def write_file(self,destination, contents):
        try:
            with open(destination, 'w', encoding='utf-8') as f:
               f.write(contents)
        except Exception as e:
            raise e
    
    def search_youtube(self, query):
        try:
            driver = webdriver.Edge()
            driver.get('https://www.youtube.com')
            search_box = driver.find_element(By.NAME, 'search_query')
            search_box.send_keys(query)
            search_box.send_keys(Keys.RETURN)
            # driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(5)
            html = driver.page_source
            driver.quit()
            self.soup = BeautifulSoup(html, 'html5lib')

            # file write
            self.write_file("html5parsed.html", str(self.soup))
        except Exception as e:
            raise e
    
    def get_videos(self, search_query):
        try:
            self.search_youtube(search_query)
            self.video_dict = {}
            for vid in self.soup.find_all("span", id="video-title"):
                title = str(vid.string).strip()
                tag = vid.parent.parent
                if 'href' in tag.attrs:
                    self.video_dict[title] = tag['href']
    
            # file write
            video_json = json.dumps(self.video_dict)
            self.write_file('vidlist.json', video_json)
        except Exception as e:
            raise e
        
    def get_video_summary(self, vid_link):
        try:
            video_id = vid_link.split("v=")[1]
            transcript = YouTubeTranscriptApi.get_transcript(video_id)
            transcript_text = ""
            for line in transcript:
                transcript_text = transcript_text + " " + line['text']
            load_dotenv()
            genai.configure(api_key=os.environ['GEMINI_KEY'])
            model = genai.GenerativeModel('gemini-pro')
            response = model.generate_content(f'Based on the transcript, give me the summary of the youtube video. Here is the transcript: {transcript_text}')
            resp_json = json.dumps(response.text)

            # file write
            self.write_file("vid_summary.json", resp_json)

            return response.text
        except Exception as e:
            return "Either video transcript is disabled or too long to be under token limit for the AI model"
        
        