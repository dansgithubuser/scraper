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
			if 'Pollen station out of season' in response: return
			match=re.search(
				'<div class="threeday_outlook clearfix">[^<]*'
					'<div class="column ">[^<]*'
						'<!--<p class="title">([^<]+)</p>-->[^<]*'
						'<div[^<]*<[^<]*<[^<]*'
							'<span class="date-level">([^<]+)</span>[^<]*'
						'</div>[^<]*'
						'<div class="level-wrapper">[^<]*'
							'(?:<div class="[^"]+">([^<]+) - <span class="pollen-level">([^<]+)</span></div>[^<]*)?'
							'(?:<div class="[^"]+">([^<]+) - <span class="pollen-level">([^<]+)</span></div>[^<]*)?'
							'(?:<div class="[^"]+">([^<]+) - <span class="pollen-level">([^<]+)</span></div>[^<]*)?'
						'</div>[^<]*'
					'</div>[^<]*'
					'<div class="column ">[^<]*'
						'<!--<p class="title">([^<]+)</p>-->[^<]*'
						'<div[^<]*<[^<]*<[^<]*'
							'<span class="date-level">([^<]+)</span>[^<]*'
						'</div>[^<]*'
						'<div class="level-wrapper">[^<]*'
							'(?:<div class="[^"]+">([^<]+) - <span class="pollen-level">([^<]+)</span></div>[^<]*)?'
							'(?:<div class="[^"]+">([^<]+) - <span class="pollen-level">([^<]+)</span></div>[^<]*)?'
							'(?:<div class="[^"]+">([^<]+) - <span class="pollen-level">([^<]+)</span></div>[^<]*)?'
						'</div>[^<]*'
					'</div>[^<]*'
					'<div class="column last">[^<]*'
						'<!--<p class="title">([^<]+)</p>-->[^<]*'
						'<div[^<]*<[^<]*<[^<]*'
							'<span class="date-level">([^<]+)</span>[^<]*'
						'</div>[^<]*'
						'<div class="level-wrapper">[^<]*'
							'(?:<div class="[^"]+">([^<]+) - <span class="pollen-level">([^<]+)</span></div>[^<]*)?'
							'(?:<div class="[^"]+">([^<]+) - <span class="pollen-level">([^<]+)</span></div>[^<]*)?'
							'(?:<div class="[^"]+">([^<]+) - <span class="pollen-level">([^<]+)</span></div>[^<]*)?'
						'</div>[^<]*'
					'</div>',
				response,
			)
			assert match
			groups=match.groups()
			print('got {}'.format(groups))
		except Exception as e:
			e.scraper_extra={'response': response}
			raise
		l=[]
		for i in range(0, len(groups), 8):
			date=groups[i]
			overall=groups[i+1]
			specifics=[]
			for j in range(3):
				pollen=groups[i+2+j*2+0]
				if not pollen: break
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
			if 'Forecasts are not available at this time.' in response: return
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
				'(?:<div class="column forecast last">.*?'
					'<p class="title">	([^<]+)	</p>.*?'
					'<div class=".*?'
						'<span>([^<]+)</span>)?',
				response,
				re.DOTALL,
			)
			assert match
			groups=match.groups()
			print('got {}'.format(groups))
			assert all([len(i) for i in groups[:-2]])
		except Exception as e:
			e.scraper_extra={'response': response}
			raise
		l=[]
		for i in range(0, len(groups), 2):
			time=groups[i]
			if time is None: break
			risk=groups[i+1]
			l.append([time, risk])
		report=AirQualityReport(text=str(l))
		report.save()
