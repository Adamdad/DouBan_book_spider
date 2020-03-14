import pandas as pd
import numpy as np
from wordcloud import WordCloud, STOPWORDS
import matplotlib.pyplot as plt
import json

def word_count(data):
    word = []
    for book_tag in data.tags:
        tags = [kw[1:-1] for kw in book_tag[1:-1].split(', ')]
        word += tags
    wordset = list(set(word))
    wordnum = np.zeros(len(wordset))
    for k in word:
        ind = wordset.index(k)
        wordnum[ind] += 1
    sorted_index = np.argsort(wordnum)[::-1]
    wordnum = wordnum[sorted_index]
    wordset = np.array(wordset)[sorted_index]
    data = {'word':wordset,'wordnum':wordnum }
    data = pd.DataFrame.from_dict(data)
    data.to_csv('word_count.csv')
    return data

def draw_word_cloud(data):
    word = []
    stopwords = set(STOPWORDS)
    for book_tag in data.tags:
        tags = [kw[1:-1].strip() for kw in book_tag[1:-1].split(', ')]
        word += tags
    text = ' '.join(word)

    wordcloud = WordCloud(width=600, height=600,
                          background_color='white',stopwords=stopwords,
                          min_font_size=10,font_path ='simfang.ttf').generate(text)
    print('wordmap generated')

    # plot the WordCloud image
    plt.figure(figsize=(8, 8), facecolor=None)
    plt.imshow(wordcloud)
    plt.axis("off")
    plt.tight_layout(pad=0)
    plt.savefig('wordcloud.png')
    plt.show()

def word_count_with_time(data):
    for y in range(1950,2020):
        year_data = data[data.year.str.contains(str(y))]
        year_result = word_count(year_data)
        if len(year_result['word']) > 0:
            year_result = pd.DataFrame.from_dict(year_result)
            year_result.to_csv('year_data/{}_count.csv'.format(y))


if __name__ == '__main__':
    data = pd.read_csv('result.csv')
    # word_count(data)
    # draw_word_cloud(data)
    word_count_with_time(data)