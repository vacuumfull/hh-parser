class HH:
	"""html pathes config"""

	vacancies_path = "//div[@class='bloko-column bloko-column_l-13 bloko-column_m-9']\
					//div[@class='bloko-gap bloko-gap_top']//div//div[@class='vacancy-serp']\
					//div[@class='vacancy-serp-item ']"
	
	link_path = "div[@class='vacancy-serp-item__row']\
				/div[@class='vacancy-serp-item__info']//div[@class='vacancy-serp-item__title']\
				/a/@href"

	date_path = "div[@class='vacancy-serp-item__row vacancy-serp-item__row_controls']\
				/span[@class='vacancy-serp-item__controls-item vacancy-serp-item__controls-item_last']\
				/span[@class='vacancy-serp-item__publication-date']" 
	
	title_path = "div[@class='vacancy-serp-item__row']\
				/div[@class='vacancy-serp-item__info']/div[@class='vacancy-serp-item__title']/a"

	last_pager = "//div[@class='bloko-gap bloko-gap_top']/div/a[@class='bloko-button HH-Pager-Control']"

	content_path = "//div[@class='vacancy-description']//div[@class='vacancy-section']"
	employer_name = "//p[@class='vacancy-company-name-wrapper']//a"
	vacancy_salary = "//p[@class='vacancy-salary']"

	experience_path = "//div[@class='vacancy-description']/div[@class='bloko-gap bloko-gap_bottom']/p[1]/span"
	address_path = "//div[@class='vacancy-address-text HH-Maps-ShowAddress-Address']//span"

	