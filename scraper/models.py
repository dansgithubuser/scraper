from django.db import models
import datetime
import re
from urllib.request import urlopen

def already_done(Model):
	if Model.objects.count()==0: return False
	if Model.objects.latest('created').created.day==datetime.datetime.utcnow().day:
		print('already done')
		return True
	return False

class PollenForecast(models.Model):
	text=models.TextField()
	created=models.DateTimeField(auto_now_add=True)

	def scrape():
		if already_done(PollenForecast): return
		try:
			response=urlopen('https://www.theweathernetwork.com/ca/forecasts/pollen/ontario/toronto').read().decode()
			match=re.search(
				'<div class="threeday_outlook clearfix">.*?'
					'<div class="column ">.*?'
						'<!--<p class="title">([^<]+)</p>-->.*?'
						'<div.*?'
							'<span class="date-level">([^<]+)</span>.*?'
						'</div>.*?'
						'<div class="level-wrapper">.*?'
							'<div class="[^"]+">([^<]+) - <span class="pollen-level">([^<]+)</span></div>.*?'
							'<div class="[^"]+">([^<]+) - <span class="pollen-level">([^<]+)</span></div>.*?'
							'<div class="[^"]+">([^<]+) - <span class="pollen-level">([^<]+)</span></div>.*?'
						'</div>.*?'
					'</div>.*?'
					'<div class="column ">.*?'
						'<!--<p class="title">([^<]+)</p>-->.*?'
						'<div.*?'
							'<span class="date-level">([^<]+)</span>.*?'
						'</div>.*?'
						'<div class="level-wrapper">.*?'
							'<div class="[^"]+">([^<]+) - <span class="pollen-level">([^<]+)</span></div>.*?'
							'<div class="[^"]+">([^<]+) - <span class="pollen-level">([^<]+)</span></div>.*?'
							'<div class="[^"]+">([^<]+) - <span class="pollen-level">([^<]+)</span></div>.*?'
						'</div>.*?'
					'</div>.*?'
					'<div class="column last">.*?'
						'<!--<p class="title">([^<]+)</p>-->.*?'
						'<div.*?'
							'<span class="date-level">([^<]+)</span>.*?'
						'</div>.*?'
						'<div class="level-wrapper">.*?'
							'<div class="[^"]+">([^<]+) - <span class="pollen-level">([^<]+)</span></div>.*?'
							'<div class="[^"]+">([^<]+) - <span class="pollen-level">([^<]+)</span></div>.*?'
							'<div class="[^"]+">([^<]+) - <span class="pollen-level">([^<]+)</span></div>.*?'
						'</div>.*?'
					'</div>',
				response,
				re.DOTALL,
			)
			assert match
			groups=match.groups()
			assert all([len(i) for i in groups])
		except Exception as e:
			print('exception raised, dumping response')
			print(response)
			raise e
		l=[]
		for i in range(0, len(groups), 8):
			date=groups[i]
			overall=groups[i+1]
			specifics=[]
			for j in range(3):
				pollen=groups[i+2+j*2+0]
				amount=groups[i+2+j*2+1]
				specifics.append([pollen, amount])
			l.append([date, overall, specifics])
		forecast=PollenForecast(text=str(l))
		forecast.save()

class AirQualityReport(models.Model):
	text=models.TextField()
	created=models.DateTimeField(auto_now_add=True)

	def scrape():
		if already_done(AirQualityReport): return
		try:
			response=urlopen('https://www.theweathernetwork.com/ca/forecasts/air-quality/ontario/toronto').read().decode()
			match=re.search(
				'<div class="column forecast ">.*?'
					'<p class="title">	([^<]+)	</p>.*?'
					'<div class=".*?'
						'<span>([^<]+)</span>.*?'
					'</div>.*?'
				'</div>.*?'
				'<div class="column forecast ">.*?'
					'<p class="title">	([^<]+)	</p>.*?'
					'<div class=".*?'
						'<span>([^<]+)</span>.*?'
					'</div>.*?'
				'</div>.*?'
				'<div class="column forecast last">.*?'
					'<p class="title">	([^<]+)	</p>.*?'
					'<div class=".*?'
						'<span>([^<]+)</span>',
				response,
				re.DOTALL,
			)
			assert match
			groups=match.groups()
			assert all([len(i) for i in groups])
		except Exception as e:
			print('exception raised, dumping response')
			print(response)
			raise e
		l=[]
		for i in range(0, len(groups), 2):
			time=groups[i]
			risk=groups[i+1]
			l.append([time, risk])
		report=AirQualityReport(text=str(l))
		report.save()
