from datetime import timedelta
from skyfield.api import load, Topos
import pytz
import math

import logging
import traceback

# Configure logging
logging.basicConfig(
    level=logging.DEBUG, 
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class CelestialCalculator:
    def __init__(self, latitude, longitude, elevation=0):
        """
        Initialize Celestial Calculator with geographical location
        """
        try:
            # Load timescale
            self.ts = load.timescale()
            
            # Load comprehensive SPICE kernel
            self.planets = load('de440s.bsp')
            
            # Create observer location
            self.location = Topos(
                latitude_degrees=latitude, 
                longitude_degrees=longitude, 
                elevation_m=elevation
            )
            
            # Initialize celestial bodies with direct references
            self.earth = self.planets['earth']
            
            # Comprehensive celestial bodies dictionary
            self.celestial_bodies = {
                'sun': {
                    'body': self.planets['sun'],
                    'name': 'Sun',
                    'type': 'direct'
                },
                'moon': {
                    'body': self.planets['moon'],
                    'name': 'Moon',
                    'type': 'direct'
                },
                'mercury': {
                    'body': self.planets['mercury barycenter'],
                    'name': 'Mercury',
                    'type': 'barycenter'
                },
                'venus': {
                    'body': self.planets['venus barycenter'],
                    'name': 'Venus',
                    'type': 'barycenter'
                },
                'mars': {
                    'body': self.planets['mars barycenter'],
                    'name': 'Mars',
                    'type': 'barycenter'
                },
                'jupiter': {
                    'body': self.planets['jupiter barycenter'],
                    'name': 'Jupiter',
                    'type': 'barycenter'
                },
                'saturn': {
                    'body': self.planets['saturn barycenter'],
                    'name': 'Saturn',
                    'type': 'barycenter'
                },
                'uranus': {
                    'body': self.planets['uranus barycenter'],
                    'name': 'Uranus',
                    'type': 'barycenter'
                },
                'neptune': {
                    'body': self.planets['neptune barycenter'],
                    'name': 'Neptune',
                    'type': 'barycenter'
                },
                'pluto': {
                    'body': self.planets['pluto barycenter'],
                    'name': 'Pluto',
                    'type': 'barycenter'
                }
            }
            
            logger.info(f"Celestial Calculator initialized: {latitude}°N, {longitude}°E")
        
        except Exception as e:
            logger.critical(f"Celestial Calculator initialization failed: {e}")
            logger.critical(traceback.format_exc())
            raise

    def get_celestial_objects_data(self, start_date, end_date):
        """
        Retrieve celestial object data for a given date range
        """
        # Ensure dates are timezone-aware
        start_date = self._ensure_timezone(start_date)
        end_date = self._ensure_timezone(end_date)
        
        if start_date > end_date:
            raise ValueError("Start date must be before end date")

        # Generate date range
        dates = self._generate_dates(start_date, end_date)
        
        # Prepare result data structure
        result_data = {
            'metadata': {
                'dates': {
                    'from': start_date.isoformat(),
                    'to': end_date.isoformat()
                },
                'observer': {
                    'location': {
                        'latitude': self.location.latitude.degrees,
                        'longitude': self.location.longitude.degrees,
                        'elevation': self.location.elevation.m
                    }
                }
            },
            'celestial_objects': []
        }

        # Process each celestial body
        for obj_id, obj_data in self.celestial_bodies.items():
            try:
                object_details = self._calculate_object_details(obj_id, obj_data, dates)
                result_data['celestial_objects'].append(object_details)
            except Exception as e:
                logger.error(f"Error calculating data for {obj_id}: {e}")
                logger.error(traceback.format_exc())
                result_data['celestial_objects'].append({
                    'id': obj_id,
                    'name': obj_data['name'],
                    'error': str(e)
                })

        return result_data

    def _calculate_object_details(self, obj_id, obj_data, dates):
        """
        Calculate detailed observations for a celestial object
        """
        object_details = {
            'id': obj_id,
            'name': obj_data['name'],
            'observations': []
        }

        # Determine the correct body to observe
        planet = obj_data['body']

        for date in dates:
            try:
                # Ensure date is in UTC and create Skyfield time
                t = self.ts.from_datetime(date)
                
                # Robust observation method
                try:
                    # Geocentric observation
                    geocentric = self.earth.at(t).observe(planet)
                    
                    # Calculate apparent geocentric position
                    apparent_geocentric = geocentric.apparent()
                    
                    # Calculate right ascension and declination
                    right_ascension, declination, _ = apparent_geocentric.radec()

                    # Prepare observation data
                    observation = {
                        'date': date.isoformat(),
                        'distance': {
                            'au': geocentric.distance().au,
                            'km': geocentric.distance().km
                        },
                        'position': {
                            'equatorial': {
                                'right_ascension': right_ascension.hours,  # Use .hours
                                'declination': declination.degrees  # Use .degrees
                            }
                        }
                    }

                    # Add horizontal coordinates for direct bodies
                    if obj_data['type'] == 'direct':
                        try:
                            # Topocentric observation for direct bodies
                            observer = self.earth + self.location
                            topocentric = observer.at(t).observe(planet)
                            apparent_topocentric = topocentric.apparent()
                            
                            # Calculate horizontal coordinates
                            alt, az, _ = apparent_topocentric.altaz()
                            
                            observation['position']['horizontal'] = {
                                'altitude': alt.degrees,
                                'azimuth': az.degrees
                            }
                        except Exception as topo_err:
                            logger.warning(f"Topocentric observation error for {obj_id}: {topo_err}")
                            observation['position']['horizontal_error'] = str(topo_err)

                    # Add constellation information
                    constellation = self.get_constellation(right_ascension.hours * 15, declination.degrees)
                    if constellation:
                        observation['constellation'] = constellation

                    # Add moon phase for moon
                    if obj_id == 'moon':
                        try:
                            # Calculate moon phase
                            moon_phase = self._calculate_moon_phase(t)
                            observation['moon_phase'] = moon_phase
                        except Exception as phase_err:
                            logger.warning(f"Moon phase calculation error: {phase_err}")
                            observation['moon_phase_error'] = str(phase_err)
                                        
                    object_details['observations'].append(observation)
                
                except Exception as obs_err:
                    logger.error(f"Observation error for {obj_id}: {obs_err}")
                    logger.error(traceback.format_exc())
                    object_details['observations'].append({
                        'date': date.isoformat(),
                        'error': str(obs_err)
                    })
                
            except Exception as e:
                logger.error(f"Error processing date {date.isoformat()} for {obj_id}: {e}")
                logger.error(traceback.format_exc())
                object_details['observations'].append({
                    'date': date.isoformat(),
                    'error': str(e)
                })

        return object_details

    def get_constellation(self, ra, dec):
        """
        Determine the constellation for given coordinates
        
        :param ra: Right Ascension in degrees
        :param dec: Declination in degrees
        :return: Constellation dictionary
        """
        # Normalize RA to be between 0 and 360
        ra = ra % 360

        # constellation definitions
        constellations = {
            # Northern Hemisphere
            'and': {'id': 'and', 'short': 'And', 'name': 'Andromeda', 'ra_range': (0, 40), 'dec_range': (20, 50)},
            'aur': {'id': 'aur', 'short': 'Aur', 'name': 'Auriga', 'ra_range': (70, 100), 'dec_range': (30, 50)},
            'boo': {'id': 'boo', 'short': 'Boo', 'name': 'Boötes', 'ra_range': (210, 250), 'dec_range': (0, 50)},
            'cam': {'id': 'cam', 'short': 'Cam', 'name': 'Camelopardalis', 'ra_range': (60, 120), 'dec_range': (50, 80)},
            'cas': {'id': 'cas', 'short': 'Cas', 'name': 'Cassiopeia', 'ra_range': (0, 60), 'dec_range': (50, 70)},
            'cep': {'id': 'cep', 'short': 'Cep', 'name': 'Cepheus', 'ra_range': (300, 360), 'dec_range': (60, 90)},
            'cyg': {'id': 'cyg', 'short': 'Cyg', 'name': 'Cygnus', 'ra_range': (280, 340), 'dec_range': (30, 60)},
            'dra': {'id': 'dra', 'short': 'Dra', 'name': 'Draco', 'ra_range': (260, 360), 'dec_range': (50, 80)},
            'her': {'id': 'her', 'short': 'Her', 'name': 'Hercules', 'ra_range': (240, 290), 'dec_range': (20, 50)},
            'lyr': {'id': 'lyr', 'short': 'Lyr', 'name': 'Lyra', 'ra_range': (280, 300), 'dec_range': (30, 50)},
            'peg': {'id': 'peg', 'short': 'Peg', 'name': 'Pegasus', 'ra_range': (330, 360), 'dec_range': (0, 30)},
            'per': {'id': 'per', 'short': 'Per', 'name': 'Perseus', 'ra_range': (40, 80), 'dec_range': (30, 60)},
            'umi': {'id': 'umi', 'short': 'UMi', 'name': 'Ursa Minor', 'ra_range': (210, 280), 'dec_range': (70, 90)},
            'uma': {'id': 'uma', 'short': 'UMa', 'name': 'Ursa Major', 'ra_range': (150, 250), 'dec_range': (50, 70)},

            # Zodiac constellations
            'ari': {'id': 'ari', 'short': 'Ari', 'name': 'Aries', 'ra_range': (30, 50), 'dec_range': (10, 30)},
            'tau': {'id': 'tau', 'short': 'Tau', 'name': 'Taurus', 'ra_range': (50, 90), 'dec_range': (-10, 30)},
            'gem': {'id': 'gem', 'short': 'Gem', 'name': 'Gemini', 'ra_range': (90, 120), 'dec_range': (10, 30)},
            'cnc': {'id': 'cnc', 'short': 'Cnc', 'name': 'Cancer', 'ra_range': (120, 140), 'dec_range': (0, 30)},
            'leo': {'id': 'leo', 'short': 'Leo', 'name': 'Leo', 'ra_range': (140, 180), 'dec_range': (0, 30)},
            'vir': {'id': 'vir', 'short': 'Vir', 'name': 'Virgo', 'ra_range': (180, 210), 'dec_range': (-10, 10)},
            'lib': {'id': 'lib', 'short': 'Lib', 'name': 'Libra', 'ra_range': (210, 240), 'dec_range': (-30, 0)},
            'sco': {'id': 'sco', 'short': 'Sco', 'name': 'Scorpius', 'ra_range': (240, 260), 'dec_range': (-40, -10)},
            'sgr': {'id': 'sgr', 'short': 'Sgr', 'name': 'Sagittarius', 'ra_range': (260, 290), 'dec_range': (-30, -10)},
            'cap': {'id': 'cap', 'short': 'Cap', 'name': 'Capricornus', 'ra_range': (290, 320), 'dec_range': (-30, -10)},
            'aqr': {'id': 'aqr', 'short': 'Aqr', 'name': 'Aquarius', 'ra_range': (320, 360), 'dec_range': (-30, 0)},
            'psc': {'id': 'psc', 'short': 'Psc', 'name': 'Pisces', 'ra_range': (0, 30), 'dec_range': (-10, 30)},

            # Southern Hemisphere
            'car': {'id': 'car', 'short': 'Car', 'name': 'Carina', 'ra_range': (150, 210), 'dec_range': (-70, -30)},
            'cen': {'id': 'cen', 'short': 'Cen', 'name': 'Centaurus', 'ra_range': (200, 260), 'dec_range': (-60, -30)},
            'cru': {'id': 'cru', 'short': 'Cru', 'name': 'Crux', 'ra_range': (180, 200), 'dec_range': (-70, -50)},
            'erid': {'id': 'erid', 'short': 'Eri', 'name': 'Eridanus', 'ra_range': (30, 90), 'dec_range': (-60, -10)},
            'grus': {'id': 'grus', 'short': 'Gru', 'name': 'Grus', 'ra_range': (320, 360), 'dec_range': (-60, -30)},
            'ind': {'id': 'ind', 'short': 'Ind', 'name': 'Indus', 'ra_range': (300, 360), 'dec_range': (-60, -30)},
            'lup': {'id': 'lup', 'short': 'Lup', 'name': 'Lupus', 'ra_range': (200, 250), 'dec_range': (-50, -30)},
            'oct': {'id': 'oct', 'short': 'Oct', 'name': 'Octans', 'ra_range': (0, 60), 'dec_range': (-90, -60)},
            'pav': {'id': 'pav', 'short': 'Pav', 'name': 'Pavo', 'ra_range': (300, 360), 'dec_range': (-70, -40)},
            'scl': {'id': 'scl', 'short': 'Scl', 'name': 'Sculptor', 'ra_range': (20, 50), 'dec_range': (-40, -20)},
            'tel': {'id': 'tel', 'short': 'Tel', 'name': 'Telescopium', 'ra_range': (240, 270), 'dec_range': (-60, -40)},
            'tri': {'id': 'tri', 'short': 'Tri', 'name': 'Triangulum', 'ra_range': (0, 30), 'dec_range': (20, 40)}
        }

        for const_key, const_info in constellations.items():
            ra_in_range = (
                const_info['ra_range'][0] <= ra <= const_info['ra_range'][1] or
                (const_info['ra_range'][0] > const_info['ra_range'][1] and 
                (ra >= const_info['ra_range'][0] or ra <= const_info['ra_range'][1]))
            )
            
            dec_in_range = (
                const_info['dec_range'][0] <= dec <= const_info['dec_range'][1]
            )
            
            if ra_in_range and dec_in_range:
                return {
                    "id": const_key,
                    "short": const_info['short'],
                    "name": const_info['name']
                }
        
        return None
    def _calculate_moon_phase(self, t):
        """
        Calculate the moon phase for a given time
        """
        try:
            # Calculate the angular separation between moon and sun
            moon = self.planets['moon']
            sun = self.planets['sun']
            
            # Get geocentric positions
            e = self.earth.at(t)
            moon_geo = e.observe(moon)
            sun_geo = e.observe(sun)
            
            # Calculate phase angle
            phase_angle = moon_geo.separation_from(sun_geo).degrees
            
            # Determine phase name
            if phase_angle < 22.5:
                phase = "New Moon"
            elif phase_angle < 67.5:
                phase = "Waxing Crescent"
            elif phase_angle < 112.5:
                phase = "First Quarter"
            elif phase_angle < 157.5:
                phase = "Waxing Gibbous"
            elif phase_angle < 202.5:
                phase = "Full Moon"
            elif phase_angle < 247.5:
                phase = "Waning Gibbous"
            elif phase_angle < 292.5:
                phase = "Last Quarter"
            else:
                phase = "Waning Crescent"
            
            # Convert to phase percentage
            # 0% = New Moon, 100% = Full Moon
            phase_percentage = abs(math.cos(math.radians(phase_angle))) * 100
            
            return {
                "moon_phase": {
                    "phase": phase,
                    "angle": phase_angle,
                    "percentage": phase_percentage
                }
            }
        except Exception as e:
            logger.error(f"Moon phase calculation error: {e}")
            return {
                "moon_phase": {
                    "error": str(e)
                }
            }
    def _ensure_timezone(self, date):
        """
        Ensure the date is timezone-aware
        """
        if date.tzinfo is None:
            return date.replace(tzinfo=pytz.UTC)
        return date

    def _generate_dates(self, start_date, end_date):
        """
        Generate a list of dates from start to end
        """
        current = start_date
        dates = []
        while current <= end_date:
            dates.append(current)
            current += timedelta(days=1)
        return dates
