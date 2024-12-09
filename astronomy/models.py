from django.db import models

class Constellation(models.Model):
    id = models.CharField(max_length=50, primary_key=True)
    name = models.CharField(max_length=100)
    short = models.CharField(max_length=10)

    def __str__(self):
        return self.name

class CelestialBody(models.Model):
    id = models.CharField(max_length=50, primary_key=True)
    name = models.CharField(max_length=100)
    constellation = models.ForeignKey(Constellation, related_name='celestial_bodies', on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class Observation(models.Model):
    body = models.ForeignKey(CelestialBody, related_name='observations', on_delete=models.CASCADE)
    date = models.DateTimeField()
    distance_au = models.FloatField()
    distance_km = models.FloatField()
    altitude_degrees = models.FloatField()
    azimuth_degrees = models.FloatField()
    right_ascension_hours = models.FloatField()
    declination_degrees = models.FloatField()
    magnitude = models.FloatField()
    elongation = models.FloatField(null=True, blank=True)

    def __str__(self):
        return f"{self.body.name} on {self.date}"