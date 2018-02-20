import time
import numpy as np
import datetime
import copy
from bots.config import HH
from grab import Grab
from grab.spider import Task, Spider
from bots.tasks import check_with_cache, parse_next_page


class HHSpider(Spider):

	base_url = 'https://spb.hh.ru'
	keyword = 'python'
	max_on_page = 0
	page = 0
	limit = 10


	request_uri = '/search/vacancy?clusters=true&area=2\
								&enable_snippets=true&text='+ keyword + '&page='
	initial_urls = [base_url + request_uri + '0']

	monthes = [	{'Янв': '01'}, {'Фев': '02'}, {'Мар': '03'}, {'Апр': '04'},{'Мая': '05'},
				{'Май': '05'}, {'Июн': '06'}, {'Июл': '07'}, {'Авг': '08'},
				{'Сент': '09'}, {'Окт': '10'}, {'Нояб': '11'}, {'Дек': '12'}]


	def create_urls(self, limit):
		urls = []
		rang = np.arange(self.page, limit, 1)
		for i in rang: urls.append(self.base_url + self.request_uri + str(i))
		return urls


	def task_initial(self, grab, task):
		counter = 0
		print('Loaded main page')
		last_page = grab.doc.select(HH.last_pager).text()
		self.max_on_page = len(grab.xpath_list(HH.vacancies_path))
		for elem in grab.doc.select(HH.vacancies_path):	
			counter+=1
			info = {}
			link = elem.select(HH.link_path).text()
			info['counter'] = counter
			info['title'] = elem.select(HH.title_path).text()
			info['date'] = elem.select(HH.date_path).text()
			info['link'] = link
			yield Task('open_page', url=link, info=copy.deepcopy(info))
	


	def task_open_page(self, grab, task, **kwargs):
		time.sleep(2)
		counter = task.info.get('counter')
		info_card = self.load_content(task.info)
		check_with_cache.delay(info_card)	

		if counter == self.max_on_page:
			time.sleep(6)
			parse_next_page.delay(self.page, self.limit)	


	def reset_default(self, page):
		self.page = page
		self.request_uri = self.request_uri[:-1] + str(self.page)
		self.initial_urls = [self.base_url + self.request_uri]


	def load_content(self, info):
		"""Load content from url"""
		grabber = Grab()
		grabber.go(info.get('link'))
		info.pop('counter', None)
		info['content'] = grabber.doc.select(HH.content_path).html()
		info['date'] = self.format_date(info.get('date'))
		info['employer'] = grabber.doc.select(HH.employer_name).text()
		info['salary'] = grabber.doc.select(HH.vacancy_salary).text()
		if grabber.doc.select(HH.address_path).exists():
			info['address'] = grabber.doc.select(HH.address_path).text()
		else:
			info['address'] = ""
		info['experience'] = grabber.doc.select(HH.experience_path).text()
		print(info)
		return info


	def format_date(self, datestring):
		year = '2018'
		splited = datestring.split(' ')
		day = str(splited[0]) if int(splited[0]) > 9 else '0' + str(splited[0])
		month = ""
		for mon in self.monthes:
			for item in mon.keys():
				if splited[1].find(item.lower()) > -1:
					month = mon[item]
		date = str(day) + str(month) + str(year)
		return datetime.datetime.strptime(date, '%d%m%Y').date().isoformat()


if __name__ == 'main':
	bot = HHSpider()
	bot.run()