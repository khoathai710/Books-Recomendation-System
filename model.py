import pandas as pd
import numpy as np

import pandas as pd
from scipy.sparse import csr_matrix
from sklearn.neighbors import NearestNeighbors

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel
        
        
class ContentBasedRecomendation():
    def __init__(self, books,top_n=10):
        self.books = books
        self.linear_kernel_function()
        self.top_n = top_n
    
    def linear_kernel_function(self):
    
        tfidf = TfidfVectorizer(stop_words='english')
        try: 
            matrix = tfidf.fit_transform(self.books['bag_of_words'])
            self.linear_kernel = linear_kernel(matrix, matrix)
        except KeyError:
            raise KeyError("Column 'bag_of_words' not found in DataFrame")

    
    def search(self, title):
        index = self.books[self.books['title'] == title].index[0]
        
        list = []
        for i in range(self.linear_kernel.shape[0]):
            if self.linear_kernel[index][i] > 0:
                list.append((i, self.linear_kernel[index][i]))
        sorted_list = sorted(list, key=lambda x: x[1], reverse=True)
        
        return sorted_list
    def recommend(self, title):
        books = []
        scores = []
        list = self.search(title)
        for j,i in enumerate(list[:self.top_n]):
           
            books.append((self.books.iloc[i[0]]['title'],self.books.iloc[i[0]]['Image-URL-M']))
            scores.append((list[j][1].item(),self.books.iloc[i[0]]['isbn']))
        
        
        return books,scores 

class Collaborative_Fitering:
    def __init__(self, books):
        self.books = books
        self.data = pd.read_csv('normalize_data.csv')
        self.user_item = self.data.pivot_table(columns='user_id',index='isbn',values='rating')
        self.user_item_sparse = csr_matrix(self.user_item)
        self.model = NearestNeighbors(algorithm='brute')
        self.model.fit(self.user_item_sparse)


    def recommend(self, title):
        
        isbn = self.books[self.books['title'] == title]['isbn'].values[0]
        
        
        obs = self.user_item.loc[isbn].values.reshape(1, -1)
        dist, suggestions = self.model.kneighbors(obs, n_neighbors=10)
        suggestions = suggestions.flatten()
        lst = []
        recommendations = []
        for stt,ind in enumerate(suggestions):
            book_isbn = self.user_item.iloc[ind].name
            book_title = self.books.loc[self.books['isbn'] == book_isbn, 'title']
            
            if not book_title.empty:
                recommendations.append((book_title.values[0],self.books.loc[self.books['isbn'] == book_isbn, 'Image-URL-S']))
                lst.append((dist.flatten()[stt].item(),book_isbn))
        
        return recommendations,lst


class HybridRecommendation():
    def __init__(self,books):
        self.books = books
        self.collab = Collaborative_Fitering(self.books)
        self.content = ContentBasedRecomendation(self.books)
    
    def normalize_result(self,lst):  
        scores = np.array([i[0] for i in lst])  
        min_val, max_val = np.min(scores), np.max(scores)  
        normalized_scores = (scores - min_val) / (max_val - min_val)  

        return {isbn: norm_score.item() for norm_score, (_, isbn) in zip(normalized_scores, lst)}
    def merge_dicts(self, dict1, dict2, weight1=0.4, weight2=0.6):
        merged = {}
        all_keys = set(dict1.keys()).union(set(dict2.keys()))
        
        for key in all_keys:
            value1 = dict1.get(key, 0) * weight1
            value2 = dict2.get(key, 0) * weight2
            merged[key] = value1 + value2
            
        return merged


    
    def recomend(self,title):
        
        _,list = self.collab.recommend(title)
        
        _,content = self.content.recommend(title)
        
        content = self.normalize_result(content)
        list = self.normalize_result(list)
        
        dict = self.merge_dicts(list,content)
        
        sorted_dict = sorted(dict.items(), key=lambda x: x[1], reverse=True)
        
        count = 0
        
        recommend = []
        for key,_ in sorted_dict:
            recommend.append((self.books[self.books['isbn'] == key]['title'].item(),self.books[self.books['isbn'] == key]['Image-URL-M'].item()))
            
            count = count + 1
            if count == 6:
                break
        return recommend