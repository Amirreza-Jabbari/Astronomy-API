
---

# Astronomy API Documentation

## Table of Contents
1. [Overview](#overview)
2. [Installation](#installation)
3. [API Endpoints](#api-endpoints)  
   - [GET /api/astronomy/](#get-apiastronomy)  
   - [POST /api/astronomy/](#post-apiastronomy)  
4. [Serializers](#serializers)
5. [Views](#views)
6. [Calculations](#calculations)
7. [Example of Use](#example-of-use)
8. [License](#license)
9. [Get Location](#get-location)
---

## Overview
The Astronomy API provides endpoints to retrieve data about celestial objects based on user-defined locations and date ranges. It leverages the Skyfield library for astronomical calculations.

---

## Installation
To install the required packages, run:

```bash
pip install -r requirements.txt
```

---

## API Endpoints

### GET `/api/astronomy/`
Retrieve celestial object data based on query parameters.

**Query Parameters:**
- `latitude` (float): Latitude of the observation point (default: 38.775867).
- `longitude` (float): Longitude of the observation point (default: -84.39733).
- `elevation` (float): Elevation in meters (default: 0).
- `start_date` (ISO 8601): Start date for calculations (optional).
- `end_date` (ISO 8601): End date for calculations (optional).

---

### POST `/api/astronomy/`
Retrieve celestial object data based on JSON payload.

**Request Body:**
```json
{
  "location": {
    "latitude": 38.775867,
    "longitude": -84.39733,
    "elevation": 0
  },
  "date_range": {
    "start_date": "2020-12-20T09:00:00-05:00",
    "end_date": "2020-12-23T09:00:00-05:00"
  }
}
```

---

## Serializers
The serializers handle the validation and transformation of request and response data.

### CelestialBodySerializer
```python
class CelestialBodySerializer(serializers.ModelSerializer):
    observations = ObservationSerializer(many=True)

    class Meta:
        model = CelestialBody
        fields = ['id', 'name', 'observations']
```

### ObservationSerializer
```python
class ObservationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Observation
        fields = ['date', 'distance_au', 'distance_km', 'altitude_degrees', 'azimuth_degrees', 'right_ascension_hours', 'declination_degrees', 'magnitude', 'elongation']
```

### ConstellationSerializer
```python
class ConstellationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Constellation
        fields = ['id', 'name', 'short']
```

---

## Views
The views handle incoming requests and return responses.

```python
class AstronomyDataView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        # Handle GET request
        pass

    def post(self, request):
        # Handle POST request
        pass
```

---

## Calculations
The calculations module uses Skyfield to compute celestial data.

```python
class CelestialCalculator:
    def __init__(self, latitude, longitude, elevation=0):
        """
        Initialize Celestial Calculator with geographical location
        """
        pass

    def get_celestial_objects_data(self, start_date, end_date):
        """
        Retrieve celestial object data for a given date range
        """
        pass

    def _calculate_object_details(self, obj_id, obj_data, dates):
        """
        Calculate detailed observations for a celestial object
        """
        pass

    def get_constellation(self, ra, dec):
        """
        Determine the constellation for given coordinates
        
        :param ra: Right Ascension in degrees
        :param dec: Declination in degrees
        :return: Constellation dictionary
        """
        pass

    def _calculate_moon_phase(self, t):
        """
        Calculate the moon phase for a given time
        """
        pass

    def _ensure_timezone(self, date):
        """
        Ensure the date is timezone-aware
        """
        pass

    def _generate_dates(self, start_date, end_date):
        """
        Generate a list of dates from start to end
        """
        pass
```

---

## Example of Use

### Example Request
```bash
curl -X POST http://127.0.0.1:8000/api/astronomy/ \
-H "Content-Type: application/json" \
-d '{
    "location": {
        "latitude": 35.6824,
        "longitude": 51.4158,
        "elevation": 1156
    },
    "date_range": {
        "start_date": "2024-12-09",
        "end_date": "2024-12-09"
    }
}
```

### Example Response
```json
{
    "metadata": {
        "dates": {
            "from": "2024-12-09T00:00:00+00:00",
            "to": "2024-12-09T00:00:00+00:00"
        },
        "observer": {
            "location": {
                "latitude": 35.6824,
                "longitude": 51.4158,
                "elevation": 1156.0
            }
        }
    },
    "celestial_objects": [
        {
            "id": "sun",
            "name": "Sun",
            "observations": [
                {
                    "date": "2024-12-09T00:00:00+00:00",
                    "distance": {
                        "au": 0.9849299530333308,
                        "km": 147343423.76243728
                    },
                    "position": {
                        "equatorial": {
                            "right_ascension": 17.062160011274038,
                            "declination": -22.806012396742435
                        },
                        "horizontal": {
                            "altitude": -42.331561819639916,
                            "azimuth": 89.56092204488478
                        }
                    },
                    "constellation": {
                        "id": "sco",
                        "short": "Sco",
                        "name": "Scorpius"
                    }
                }
            ]
        },
        {
            "id": "moon",
            "name": "Moon",
            "observations": [
                {
                    "date": "2024-12-09T00:00:00+00:00",
                    "distance": {
                        "au": 0.0024823007514765427,
                        "km": 371346.9068579006
                    },
                    "position": {
                        "equatorial": {
                            "right_ascension": 23.51645870095422,
                            "declination": -4.233145426825709
                        },
                        "horizontal": {
                            "altitude": -39.812473857261594,
                            "azimuth": 298.0038835352312
                        }
                    },
                    "constellation": {
                        "id": "aqr",
                        "short": "Aqr",
                        "name": "Aquarius"
                    },
                    "moon_phase": {
                        "moon_phase": {
                            "phase": "First Quarter",
                            "angle": 94.60931385482792,
                            "percentage": 8.036095708407135
                        }
                    }
                }
            ]
        },
        {
            "id": "mercury",
            "name": "Mercury",
            "observations": [
                {
                    "date": "2024-12-09T00:00:00+00:00",
                    "distance": {
                        "au": 0.6930993705301217,
                        "km": 103686190.01481654
                    },
                    "position": {
                        "equatorial": {
                            "right_ascension": 16.59945872902403,
                            "declination": -19.827801372608217
                        }
                    },
                    "constellation": {
                        "id": "sco",
                        "short": "Sco",
                        "name": "Scorpius"
                    }
                }
            ]
        },
        {
            "id": "venus",
            "name": "Venus",
            "observations": [
                {
                    "date": "2024-12-09T00:00:00+00:00",
                    "distance": {
                        "au": 0.9178243142371275,
                        "km": 137304563.08656195
                    },
                    "position": {
                        "equatorial": {
                            "right_ascension": 20.298309566164523,
                            "declination": -22.102228101020504
                        }
                    },
                    "constellation": {
                        "id": "cap",
                        "short": "Cap",
                        "name": "Capricornus"
                    }
                }
            ]
        },
        {
            "id": "mars",
            "name": "Mars",
            "observations": [
                {
                    "date": "2024-12-09T00:00:00+00:00",
                    "distance": {
                        "au": 0.7565068605161593,
                        "km": 113171815.50315933
                    },
                    "position": {
                        "equatorial": {
                            "right_ascension": 8.595719041799386,
                            "declination": 21.644016435122452
                        }
                    },
                    "constellation": {
                        "id": "cnc",
                        "short": "Cnc",
                        "name": "Cancer"
                    }
                }
            ]
        },
        {
            "id": "jupiter",
            "name": "Jupiter",
            "observations": [
                {
                    "date": "2024-12-09T00:00:00+00:00",
                    "distance": {
                        "au": 4.090419171635449,
                        "km": 611917998.3471209
                    },
                    "position": {
                        "equatorial": {
                            "right_ascension": 4.9739276965380546,
                            "declination": 22.0109297809184
                        }
                    },
                    "constellation": {
                        "id": "tau",
                        "short": "Tau",
                        "name": "Taurus"
                    }
                }
            ]
        },
        {
            "id": "saturn",
            "name": "Saturn",
            "observations": [
                {
                    "date": "2024-12-09T00:00:00+00:00",
                    "distance": {
                        "au": 9.659854141176211,
                        "km": 1445093610.7925384
                    },
                    "position": {
                        "equatorial": {
                            "right_ascension": 22.997041813567634,
                            "declination": -8.62474072674412
                        }
                    },
                    "constellation": {
                        "id": "aqr",
                        "short": "Aqr",
                        "name": "Aquarius"
                    }
                }
            ]
        },
        {
            "id": "uranus",
            "name": "Uranus",
            "observations": [
                {
                    "date": "2024-12-09T00:00:00+00:00",
                    "distance": {
                        "au": 18.64708314086849,
                        "km": 2789563932.639794
                    },
                    "position": {
                        "equatorial": {
                            "right_ascension": 3.4470254554384665,
                            "declination": 18.52131616078166
                        }
                    },
                    "constellation": {
                        "id": "tau",
                        "short": "Tau",
                        "name": "Taurus"
                    }
                }
            ]
        },
        {
            "id": "neptune",
            "name": "Neptune",
            "observations": [
                {
                    "date": "2024-12-09T00:00:00+00:00",
                    "distance": {
                        "au": 29.7128088481803,
                        "km": 4444972936.203892
                    },
                    "position": {
                        "equatorial": {
                            "right_ascension": 23.83766552241007,
                            "declination": -2.4717175903446402
                        }
                    },
                    "constellation": {
                        "id": "aqr",
                        "short": "Aqr",
                        "name": "Aquarius"
                    }
                }
            ]
        },
        {
            "id": "pluto",
            "name": "Pluto",
            "observations": [
                {
                    "date": "2024-12-09T00:00:00+00:00",
                    "distance": {
                        "au": 35.867929168949665,
                        "km": 5365765830.09329
                    },
                    "position": {
                        "equatorial": {
                            "right_ascension": 20.200341071055174,
                            "declination": -23.3188836195693
                        }
                    },
                    "constellation": {
                        "id": "cap",
                        "short": "Cap",
                        "name": "Capricornus"
                    }
                }
            ]
        }
    ]
}
```
## License
```markdown
MIT License

Copyright (c) 2024 Amirreza Jabbari

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```
## Get Location
You can get your  location information by using get_location.py in location folder.
```bash
pip install -r location/requirements.txt
python location/get_location.py
```
---