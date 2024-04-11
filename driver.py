from auxiliary import Scraper

obj = Scraper()
obj.search_youtube('python tutorials')
obj.get_soup()
obj.get_title()
obj.get_videos()