import csv                                                                    
import json                                                       
import xml.etree.ElementTree as ET

import sys
from bs4 import BeautifulSoup  

test_file = sys.argv[1]
file_to_save = sys.argv[2]

with open(test_file, 'r', encoding='utf-8') as file:
	f = file.read()

print("Выбор преобразования:")
print("1: csv в json")
print("2: csv в xml")
print("3: html в json")
print("4: html в xml")
print("5: json в csv")
print("6: xml в csv")

choice = input("Введите цифру:")

if choice == "1":

	lines = [line.split(',') for line in f.split('\n')]                    
	header = lines[0]                                                             
	json_data = []       

	for line in lines[1:]:
		json_data.append({header[i]: value for i, value in enumerate(line)})

	print("csv в json:")
	result1 = json.dumps(json_data, indent=4)

	with open(file_to_save, 'w', encoding='utf-8') as f1:
		f1.write(result1)
	print(result1)

if choice == "2":

	lines = [line.split(',') for line in f.split('\n')]                    
	root_element = ET.Element('root') 

	for line in lines:                                                             
		initial = ET.SubElement(root_element, line[0])                                     
		for value in line[1:]:                                                    
			secondary = ET.SubElement(initial, 'item')                                
			secondary.text = value

	print("csv в xml:")
	result2 = ET.tostring(root_element, encoding='unicode')   

	with open(file_to_save, 'w', encoding='utf-8') as f1:
		f1.write(result2)
	print(result2)

if choice == "3":

	soup = BeautifulSoup(f, 'html.parser')     

	print("html в jsonl:")                        
	result3 = json.dumps(soup.prettify(), indent=4)  

	with open(file_to_save, 'w', encoding='utf-8') as f1:
		f1.write(result3)
	print(result3)

if choice == "4":

	soup = BeautifulSoup(f, 'html.parser') 

	print("html в xml:")                           
	result4 = soup.prettify() 

	with open(file_to_save, 'w', encoding='utf-8') as f1:
		f1.write(result4)
	print(result4)


if choice == "5":

	js = json.loads(f)                                          
	header = list(js[0].keys())                                           
	lines = [header] 

	for item in js:
		lines.append([str(item.get(key, '')) for key in header])

	print("json в csv:")
	result5 = '\n'.join([','.join(line) for line in lines])

	with open(file_to_save, 'w', encoding='utf-8') as f1:
		f1.write(result5)
	print(result5)
  
if choice == "6":

	root_element = ET.fromstring(f)                                             
	csv_data = []

	for secondary in root_element:                                                           
		line = [secondary.tag] + [element.text for element in secondary]                       
		csv_data.append(line)

	print("xml в csv:")
	result6 = '\n'.join([','.join(line) for line in csv_data])   

	with open(file_to_save, 'w', encoding='utf-8') as f1:
		f1.write(result6)
	print(result6)
else:
	print("Ошибка ввода")




