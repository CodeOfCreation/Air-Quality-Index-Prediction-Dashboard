from django.db import models

from django.db import models

class PredictionHistory(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    pm25 = models.FloatField()
    pm10 = models.FloatField()
    no2 = models.FloatField()
    so2 = models.FloatField()
    co = models.FloatField()
    o3 = models.FloatField()
    temperature = models.FloatField()
    humidity = models.FloatField()
    lr_prediction = models.FloatField()
    dt_prediction = models.FloatField()

    class Meta:
        ordering = ['-timestamp']

    def __str__(self):
        return f"AQI Prediction - {self.timestamp.strftime('%Y-%m-%d %H:%M:%S')}"