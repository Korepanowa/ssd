import yaml                                                    
from typing import List, Tuple                                                              
from dataclasses import dataclass

import matplotlib.pyplot as plt


# Создадим структуру данных для точки.
@dataclass                                                     
class DataPoint:
	date: str                                                
	value: float
  

# Создадим структуру данных для представления временного ряда.
@dataclass                                                     
class TimeSeries:
	name: str                                                  
	data: List[DataPoint]

# Загрузим файл и получим из него список временных рядов.
file = r"weather.yaml" 

with open(file, 'r') as f:
	data = yaml.safe_load(f) 

time_series = []
for time_data in data:                                            
	name = time_data['name']                                           
	data = [DataPoint(date=point['date'], value=point['value']) for point in time_data['data']]    
	time_series.append(TimeSeries(name=name, data=data))

for time in time_series:
	dates = [point.date for point in time.data]                       
	values = [point.value for point in time.data]                     

	plt.plot(dates, values, color = 'green')                                                  
	plt.xlabel('Дата')                                                       
	plt.ylabel('Температура')             
	plt.title(f'Среднее значение температуры днём за месяц {time.name}')                                              
	plt.show()  