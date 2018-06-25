import scraper.models
from apscheduler.schedulers.blocking import BlockingScheduler
import django
import os
import smtplib

sched=BlockingScheduler()

def send_gmail(subject, text):
	gmail='dansonlinepresence@gmail.com'
	content='''\
From: {}
To: {}
Subject: {}

{}'''.format(gmail, gmail, subject, text)
	if 'GMAIL_PASSWORD' not in os.environ:
		print('no GMAIL_PASSWORD; not gmailing the following')
		print(content)
		return
	server=smtplib.SMTP_SSL('smtp.gmail.com', 465)
	server.ehlo()
	server.login(gmail, os.environ['GMAIL_PASSWORD'])
	server.sendmail(gmail, [gmail], content)
	server.close()

@sched.scheduled_job('cron', hour=8)
def scheduled_job():
	print('scraping')
	for i in dir(scraper.models):
		attr=getattr(scraper.models, i)
		if not isinstance(attr, django.db.models.base.ModelBase): continue
		print('scraping {}'.format(i))
		try: attr.scrape()
		except Exception as e:
			print(e)
			send_gmail(
				'{} scrape failed'.format(i),
				'https://dashboard.heroku.com/apps/stark-mesa-98224/logs',
			)
	print('complete')

class Command(django.core.management.base.BaseCommand):
	def handle(self, *args, **options):
		sched.start()
