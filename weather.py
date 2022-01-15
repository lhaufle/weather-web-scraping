import requests
from bs4 import BeautifulSoup
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

values = requests.get('value not included in example')

html = values.text

soup = BeautifulSoup(html)


#pull the low and high for each day of the 10-day forcast
highest = soup.find_all('div', class_='weather-10-day__temperature-high')
days = soup.find_all(
    'span', class_='weather-10-day__day weather-10-day__day_visible_true')
lowest = soup.find_all('div', class_='weather-10-day__temperature-low')

weekdays = []
high_temps = []
low_temps = []


#loop through each value and check for empty strings
for line in highest:
    if line.text != '':
        high_temps.append(int(line.text))

for day in days:
    if day.text != '':
        weekdays.append(day.text)

for low in lowest:
    if low.text != '':
        low_temps.append(int(low.text))

#create dataframe
df1 = pd.DataFrame({'Days': weekdays, 'Highs': high_temps, 'Lows': low_temps})

#pass data for bar chart
df1.plot(x="Days", y=["Highs", "Lows"], kind="bar")

#show barchart
plt.show()
