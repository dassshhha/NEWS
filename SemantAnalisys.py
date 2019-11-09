import numpy
from numpy import *
import nltk
from nltk.stem import SnowballStemmer
import re
import pymorphy2

morph = pymorphy2.MorphAnalyzer()


# нахождение документов, в которых есть основа слова и поиск полной формы слова, запись главных новостей
def find_words_and_doc(wrd):
    global word
    wordFind = False
    for r in range(len(docs)):
        if A[wrd][r] != 0.0:
            with open(str('data/mainNews.txt'), 'a', encoding="utf-8") as news:
                if words_per_doc[r] > 2 and printed_docs[r] == 0:
                    news.write(docs[r] + '\n')
                    printed_docs[r] = 1
            if not wordFind:
                words = re.findall(r'\w+', docs[r])
                stemmed = [stemmer.stem(w).lower() for w in words]
                for en, stem in enumerate(stemmed):
                    if c[wrd] == stem and c[wrd] == words[en].lower():  # основа совпадает с самим словом (трамп=Трамп)
                        word = words[en]
                        wordFind = True
                    elif c[wrd] == stem:
                        if words[en][0].upper() == words[en][0]:  # слово с большой буквы но совп только основы (трамп!=Трампа)
                            word = words[en]
                        else:  # слово не с большой буквы применяется pymorphy
                            word = morph.parse(words[en])[0]
                            word = word.normal_form
    return word


stemmer = SnowballStemmer('russian')
stopwords = nltk.corpus.stopwords.words('russian')
stopwords += ['дом', 'россиян', 'россияне', 'год', 'время', 'россиянин', 'слов', 'дело', 'видео']
docs = []
with open(str('data/parsedNews.txt'), 'r', encoding="utf-8") as f:
    for line in f.readlines():
        docs.append(line)
word = nltk.word_tokenize(' '.join(docs))
for_del = ['VERB', 'ADJF', 'ADJS', 'INFN', 'PRTF', 'PRTF', 'PRTS', 'GRND', 'NUMR', 'ADVB', 'COMP', 'PRED']
for dw in for_del:
    word = [w for w in word if dw not in morph.parse(w)[0].tag]  # удаление прил,глаг, и тд
word_stem = [stemmer.stem(w).lower() for w in word if len(w) > 1 and w.isalpha()]  # Стемминг всех слов с исключением символов
stopword = [stemmer.stem(w).lower() for w in stopwords]  # Стемминг стоп-слов
word_stop = [w for w in word_stem if w not in stopword]  # Исключение стоп-слов
fdist = nltk.FreqDist(word_stop)
t = [w for (w, freq) in fdist.most_common(30)]  # выборка 30 ключевых слов
d = {}
c = []
for i in range(0, len(docs)):
    word = re.findall(r'\w+', docs[i])
    word_stem = [stemmer.stem(w).lower() for w in word if len(w) > 1 and w.isalpha()]
    words = [w for w in word_stem if w in t]
    for w in words:
        if w not in c:
            c.append(w)
            d[w] = [i]
        elif w in c:
            d[w] = d[w] + [i]
# построение матрицы (слова-документы)
a = len(c)
b = len(docs)
A = numpy.zeros([a, b])
c.sort()
for i, k in enumerate(c):
    for j in d[k]:
        A[i, j] += 1
words_per_doc = sum(A, axis=0)
docs_for_del = []
# удаление документов, в которых не оказалось ключевых слов
for i, k in enumerate(words_per_doc):
    q = int(k)
    if q == 0:
        docs_for_del.append(i)
while docs_for_del:
    dfd = docs_for_del.pop()
    A = numpy.delete(A, dfd, axis=1)
    docs.pop(dfd)
words_per_doc = sum(A, axis=0)
f = open('data/mainNews.txt', 'w+')
f.seek(0)
f.close()
# запись ключевых слов и главных новостей в файлы
with open(str('data/keyWords.txt'), 'w', encoding="utf-8") as f:
    printed_docs = []
    for i in range(len(docs)):
        printed_docs.append(0)
    for i in range(len(c)):
        word = find_words_and_doc(i)
        f.write(word + '\n')
