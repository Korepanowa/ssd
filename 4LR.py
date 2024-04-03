import os
import zipfile
import numpy as np

import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
nltk.download('stopwords')

import pymorphy3
from scipy.spatial.distance import pdist, squareform
import seaborn as sns

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.cluster import SpectralClustering
from sklearn.metrics import silhouette_score

import matplotlib.pyplot as plt

# Получим список стоп-слов для русского языка.
stop_words = set(stopwords.words('russian'))

# Создадим объект для нормализации слов.
norm = pymorphy3.MorphAnalyzer()

# Обработаем тексты.
text_corpus = []

for folder in os.listdir("2021_SPORT"):
	path_to_folder = os.path.join("2021_SPORT", folder)
	if os.path.isdir(path_to_folder):                   
        
		for name in os.listdir(path_to_folder):

			if name.endswith('.txt'):
				file_path = os.path.join(path_to_folder, name)

				with open(file_path, 'r', encoding='utf-8') as file:        
					text = file.read()
					tokens = word_tokenize(text)
					tokens = [norm.parse(token)[0].normal_form for token in tokens if token.isalnum() and not token.isdigit()]
					tokens = [token for token in tokens if token not in stop_words]
					text = ' '.join(tokens)                    
					text_corpus.append(text)


# Проведём векторизацию текстов.
vectorizer = CountVectorizer(max_features=150)
X = vectorizer.fit_transform(text_corpus).toarray()

# Построим матрицу расстояний и визуализируем её в тепловой карте.
distance = squareform(pdist(X, metric='cosine'))

plt.figure(figsize = (10, 10))
plt.scatter(distance[:,0], distance[:,1], c = distance[:,1], cmap = 'plasma', marker = 'o')
plt.colorbar()
plt.title('Матрица расстояний')
plt.show()


# Проведём кластерный анализ.
sameness_matrix = np.exp(-distance ** 2 / (2. * 4.0 ** 2)) 
spectral = SpectralClustering(affinity='precomputed', random_state=0, n_clusters=3)
clusters = spectral.fit_predict(sameness_matrix)

medium_silhouette = silhouette_score(sameness_matrix, clusters)
print("Коэффициент силуэта:", medium_silhouette)

plt.figure(figsize=(10, 6))                                             
plt.scatter(X[:, 0], X[:, 1], c=clusters, cmap='viridis', alpha=0.5)
plt.title('Визуализация кластеров')
plt.colorbar(label='Кластер')
plt.show()