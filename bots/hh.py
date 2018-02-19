import json
import time
import datetime
import copy
from bots.config import HH
from grab import Grab
from bs4 import BeautifulSoup
from grab.spider import Task, Spider


class HHSpider(Spider):

	base_url = 'https://spb.hh.ru'
	keyword = 'python'
	page = 0
	request_uri = '/search/vacancy?clusters=true&area=2\
								&enable_snippets=true&text='+ keyword + '&page=' + str(page)
	initial_urls = [base_url + request_uri]

	monthes = [	{'Янв': '01'}, {'Фев': '02'}, {'Мар': '03'}, {'Апр': '04'},{'Мая': '05'},
				{'Май': '05'}, {'Июн': '06'}, {'Июл': '07'}, {'Авг': '08'},
				{'Сент': '09'}, {'Окт': '10'}, {'Нояб': '11'}, {'Дек': '12'}]


	def task_initial(self, grab, task):
		print('Loaded main page')
		print(grab.doc.select(HH.last_pager).text())

		for elem in grab.doc.select(HH.vacancies_path):	
			info = {}
			link = elem.select(HH.link_path).text()
			info['title'] = elem.select(HH.title_path).text()
			info['date'] = elem.select(HH.date_path).text()
			info['link'] = link
			print(info)
			yield Task('open_page', url=link, info=copy.deepcopy(info))


	def task_open_page(self, grab, task, **kwargs):
		time.sleep(2)
		info_card = self.load_content(task.info)


	def task_load_info(self, grab, task, **kwargs):
		print(task.url)


	def load_content(self, info):
		"""Load content from url"""
		grabber = Grab()
		grabber.go(info.get('link'))
		print(grabber.doc.select(HH.experience_path).text())
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