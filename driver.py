from auxiliary import Scraper

obj = Scraper()
search = input
obj.search_youtube('python tutorials')
obj.get_title()
obj.get_videos()