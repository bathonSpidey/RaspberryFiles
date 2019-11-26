
from weather import Weather
weather=Weather
class CurrentWeather:
    temp=''
    weather_conditions=''
    wind_speed=''
    city=''
    
    def __init__(self, city='dublin'):
        
        self.city=city
        lookup=weather.lookup_by_location(self.city)
        self.temp=lookup.condition.temp
        self.weather_conditions=lookup.condition.text
        self.wind_speed=lookup.wind.speed
        
    def getTemperature(self):
       return self.temp
    def getWeatherCondition(self):
        return self.weather_conditions
    
    def getWindSpeed(self):
        return self.wind_speed
    
    def getCity(self):
        return self.city
    
if __name__=='__main__':
    current_weather=CurrentWeather('dublin')
    print('{} {} {} windspeed {} km/h'.format(current_weather.getCity(), current_weather.getTemp(),current_weather.getWeatherCondition(),current_weather.getWindSpeed()))
    
    