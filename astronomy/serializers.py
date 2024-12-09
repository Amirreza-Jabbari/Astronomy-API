from rest_framework import serializers
from .models import CelestialBody, Observation, Constellation

class ObservationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Observation
        fields = ['date', 'distance_au', 'distance_km', 'altitude_degrees', 'azimuth_degrees', 'right_ascension_hours', 'declination_degrees', 'magnitude', 'elongation']

class CelestialBodySerializer(serializers.ModelSerializer):
    observations = ObservationSerializer(many=True)

    class Meta:
        model = CelestialBody
        fields = ['id', 'name', 'observations']

class ConstellationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Constellation
        fields = ['id', 'name', 'short']