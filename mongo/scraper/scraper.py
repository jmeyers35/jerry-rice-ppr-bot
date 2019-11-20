import requests
import urllib.request
import time
from bs4 import BeautifulSoup

def create_week_dictionary():
	week_stats = dict()

	url = "https://www.pro-football-reference.com/players/R/RiceJe00/gamelog/"

	response = requests.get(url)

	bs = BeautifulSoup(response.text, "html.parser")

	# print(bs)

	table = bs.findAll("table")
	rows = table[0].findAll(lambda tag: tag.name == "tr")

	for row in rows:
		if not row.has_attr('class') and row.has_attr('id'):
			cells = row.findChildren('td')
			week = None
			receptions = None
			yards = None
			td = None
			date = None
			opponent = None
			for cell in cells:
				if cell['data-stat'] == 'week_num':
					week = cell.text
				if cell['data-stat'] == 'rec':
					receptions = cell.text
				if cell['data-stat'] == 'rec_yds':
					yards = cell.text
				if cell['data-stat'] == 'rec_td':
					td = cell.text
				if cell['data-stat'] == 'game_date':
					link = cell.find('a')
					date = link.text
				if cell['data-stat'] == 'opp':
					link = cell.find('a')
					opponent = link.text
			if not td == '' and not receptions == '' and not yards == '':
				print( (receptions, yards, td) )
				ppr_points = calc_ppr(receptions, yards, td)
				standard_points = calc_standard(yards, td)
				stats = None
				if week in week_stats:
					stats = week_stats[week]
				else:
					stats = list()
				stats.append( {'date' : date, 'rec' : receptions, 'rec_yds' : yards, 'rec_td' : td, 'opponent' : opponent, 'ppr_points' : ppr_points, 'standard_points': standard_points} )
				week_stats[week] = stats
	# print(week_stats)
	return week_stats

def calc_ppr(rec, yards, td):
	return str(round(int(rec) * 1.0 + int(yards) * .1 + int(td) * 6, 4))

def calc_standard(yards, td):
	return str(round(int(yards) * .1 + int(td) * 6, 4))
