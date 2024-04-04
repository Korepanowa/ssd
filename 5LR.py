import os
import zipfile
import string

import pymorphy2

import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
nltk.download('stopwords')

from sklearn.decomposition import NMF, LatentDirichletAllocation
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer

import matplotlib.pyplot as plt


# Получим список стоп-слов для русского языка.
stop_words = set(stopwords.words('russian'))

# Создадим объект для нормализации слов.
norm = pymorphy2.MorphAnalyzer()

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

# Создадим векторные представления для каждого текста с помощью CountVectorizer и TfidfVectorizer.
countV = CountVectorizer(max_features=1000)                                        
X_countV = countV.fit_transform(text_corpus)

tfidfV = TfidfVectorizer(max_features=1000)                                        
X_tfidfV = tfidfV.fit_transform(text_corpus)


# Зададим количество тем и топ слов.
topics = 10                                                                               
top_words = 20 

models = []
nmf_countV = NMF(n_components=topics, random_state=42)                                      
nmf_countV.fit(X_countV)
models.append(nmf_countV)

nmf_tfidfV = NMF(n_components=topics, random_state=42)                                      
nmf_tfidfV.fit(X_tfidfV)
models.append(nmf_tfidfV)

lda_countV = LatentDirichletAllocation(n_components=topics, random_state=42)                
lda_countV.fit(X_countV)
models.append(lda_countV)

lda_tfidfV = LatentDirichletAllocation(n_components=topics, random_state=42)                
lda_tfidfV.fit(X_tfidfV)
models.append(lda_tfidfV)

# Получим список признаков.
list_of_signs = tfidfV.get_feature_names_out() 

titles = ["NMF с помощью CountVectorizer","NMF с помощью TfidfVectorizer","LDA с помощью CountVectorizer","LDA с помощью TfidfVectorizer"]

# Визуализируем топ слов для каждой модели.
for model, title in zip(models, titles):
	fig, axes = plt.subplots(2, 5, figsize=(30, 15), sharex=True)
	axes = axes.flatten()

	for idx, topic in enumerate(model.components_):
		idx_features = topic.argsort()[:-top_words -1:-1]
		top_features = [list_of_signs[i] for i in idx_features]
		weights = topic[idx_features]

		ax = axes[idx]
		ax.barh(top_features, weights, height=0.7)
		ax.set_title(f'Topic {idx +1}', fontdict={'fontsize': 30})
		ax.invert_yaxis()
		ax.tick_params(axis='both', which='major', labelsize=20)
		
		for i in 'top right left'.split():
			ax.spines[i].set_visible(False)
		fig.suptitle(title, fontsize=40)

	plt.subplots_adjust(top=0.90, bottom=0.05, wspace=0.90, hspace=0.3)
	plt.show()