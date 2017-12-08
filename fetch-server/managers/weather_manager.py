try:
  from ..models.weather import Weather
except ValueError:
  from models.weather import Weather

class WeatherManager():
  def __init__(self, db):
    self.db = db
    self.q = Weather.query
  
  def select(self, args):
    return self.q.filter_by(**args).all()
  
  def insert(self, temperature, sunny, cloudy, rainy):
    weather = Weather(temperature=temperature,
                      sunny=sunny,
                      cloudy=cloudy,
                      rainy=rainy)
    self.db.session.add(weather)
    self.db.session.commit()
    return weather

  def update(self, id, args):
    weather = self.q.get(id)
    if 'temperature' in args:
      weather.temperature = args['temperature']
    if 'sunny' in args:
      weather.sunny = args['sunny']
    if 'cloudy' in args:
      weather.cloudy = args['cloudy']
    if 'rainy' in args:
      weather.rainy = args['rainy']
    self.db.session.commit()