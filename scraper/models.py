from django.db import models

class PollenForecast(models.Model):
	text=models.TextField()

class AirQualityReport(models.Model):
	text=models.TextField()
