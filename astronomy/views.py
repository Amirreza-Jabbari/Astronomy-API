from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .celestial_calculator import CelestialCalculator
from datetime import datetime
import pytz

class AstronomyDataView(APIView):
    def post(self, request):
        location = request.data.get('location')
        date_range = request.data.get('date_range')

        if not location or not date_range:
            return Response({"error": "Location and date range are required."}, status=status.HTTP_400_BAD_REQUEST)

        start_date = date_range.get('start_date')
        end_date = date_range.get('end_date')

        if not start_date or not end_date:
            return Response({"error": "Start date and end date are required."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            start_date = self._parse_date(start_date)
            end_date = self._parse_date(end_date)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        try:
            latitude = location.get('latitude')
            longitude = location.get('longitude')
            elevation = location.get('elevation', 0)

            calculator = CelestialCalculator(latitude, longitude, elevation)
            celestial_data = calculator.get_celestial_objects_data(start_date, end_date)

            return Response(celestial_data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def _parse_date(self, date_str):
        try:
            date = datetime.fromisoformat(date_str)
            return date if date.tzinfo else date.replace(tzinfo=pytz.UTC)
        except ValueError:
            raise ValueError("Invalid date format. Please use ISO 8601 format.")