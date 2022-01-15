import requests
from bs4 import BeautifulSoup
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import xlsxwriter


# grab the data from website
values = requests.get('https://www.wqad.com/weather')
html = values.text
soup = BeautifulSoup(html)

'''
crawl through the local webservice to get the 7 day forecast
then clean the data to be used later for a barchart
'''
# pull the low and high for each day of the 10-day forcast
highest = soup.find_all('div', class_='weather-10-day__temperature-high')
days = soup.find_all(
    'span', class_='weather-10-day__day weather-10-day__day_visible_true')
lowest = soup.find_all('div', class_='weather-10-day__temperature-low')

weekdays = []
high_temps = []
low_temps = []

# loop through each value and check for empty strings
for line in highest:
    if line.text != '':
        high_temps.append(int(line.text))

for day in days:
    if day.text != '':
        weekdays.append(day.text)

for low in lowest:
    if low.text != '':
        low_temps.append(int(low.text))


'''
Crawl through the nation weather service page for local summary 
for the next seven days then insert in the worksheet below the
bar chart. 
'''

nat_weather_values = requests.get(
    'https://forecast.weather.gov/MapClick.php?x=196&y=121&site=dvn&zmx=&zmy=&map_x=196&map_y=121#.YeIfl_7MLIU')
nhtml = nat_weather_values.text
nsoup = BeautifulSoup(nhtml)

desc_day = nsoup.find_all('div', class_='col-sm-2 forecast-label')
describe = nsoup.find_all('div', class_='col-sm-10 forecast-text')

ndays = []
ndescribe = []

# grab each of the days
for i in desc_day:
    ndays.append(i.findChild().text)

for j in describe:
    ndescribe.append(j.text)

# create dataframe
df1 = pd.DataFrame({'Days': weekdays, 'Highs': high_temps, 'Lows': low_temps})

# pass data for bar chart
df1.plot(x="Days", y=["Highs", "Lows"], kind="bar")

# save the chart
plt.savefig('weather.png', dpi=400)

# open workbook and create worksheet for chart
workbook = xlsxwriter.Workbook('weather.xlsx')
worksheet = workbook.add_worksheet()

worksheet.insert_image('B2', 'weather.png')

# To hold values to write to cells
iteration = 26

# write values below image B & C
for val in range(len(ndays)):
    worksheet.write('B' + str(iteration), ndays[val])
    worksheet.write('C' + str(iteration), ndescribe[val])
    iteration += 1

workbook.close()

# show barchart
# plt.show()
