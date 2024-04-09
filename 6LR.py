import os
import subprocess
import webbrowser

import speech_recognition as sr


recognizer = sr.Recognizer()  
key_words = ['поиск', 'youtube']                                            

with sr.Microphone() as source:

	print(f"Для поиска начните фразу со слова ПОИСК")
	print(f"Для просмотра видео начните фразу со слова YOUTUBE")
	print(f"Говорите чётко 7 секунд...")

	try:
		data = recognizer.record(source, duration = 7)
		file = "audio6LR.wav"  

		with open(file, "wb") as f:
			f.write(data.get_wav_data())

		print("Аудио сохранено как", file)

		if file:

			with sr.AudioFile(file) as source:
				data = recognizer.listen(source)

			try:
				text = recognizer.recognize_google(data, language="ru-RU")
				

			except sr.UnknownValueError:
				print("Не удалось распознать речь")
					
			except sr.RequestError as e:
				print(f"Ошибка сервиса распознавания речи: {e}")
			                       
			if text:
				search_query = ""
    
				for word in key_words:
					if word in text.lower():
						search_query = text.replace(word, "")
						break
    
				search_query = search_query.strip().replace(" ", "+")

			if 'youtube' in text.lower():
				search_url = f"https://www.youtube.com/results?search_query={search_query}"
				try:
					webbrowser.open(search_url)

				except Exception as e:
					print("Ошибка при открытии youtube:", e)
				
			elif 'поиск' in text.lower(): 
				search_url = f"https://yandex.ru/search/?text={search_query}"
				try:
					webbrowser.open(search_url)

				except Exception as e:
					print("Ошибка при открытии браузера:", e)

	except Exception as e:
		print("Ошибка записи:", e)