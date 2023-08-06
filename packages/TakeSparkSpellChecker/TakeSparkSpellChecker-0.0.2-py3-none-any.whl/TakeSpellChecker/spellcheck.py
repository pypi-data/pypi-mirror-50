import math
import numpy as np
from gensim.models import Word2Vec
from pyjarowinkler import distance

class SpellCheck:
    
    def __init__(self, emb_broad, verbose: bool = True, context_candidates: int = 10, window_limit: int = 4):
        self.__emb_broad = emb_broad
        self.context_candidates = context_candidates
        self.window_limit = window_limit
    
    def __calculate_limits(self, ind: int, sentence_len: int):
        left = ind - self.window_limit
        right = ind + self.window_limit
        left_limit = max(0, left)
        right_limit = min(sentence_len, right)
        return left_limit, right_limit
    
    def __find_correct_word(self, ind: int, left_limit: int, right_limit: int, sentence_lst: list):
        left_words = sentence_lst[left_limit:ind][::-1]
        right_words = sentence_lst[ind+1:right_limit]
        similar_words = self.__emb_broad.value.predict_output_word(left_words + right_words, topn = self.context_candidates)
        similar_lst = [distance.get_jaro_distance(similar_word[0], sentence_lst[ind], winkler=False, scaling=0.1) for similar_word in similar_words]
        position = np.argmax(similar_lst)
        most_similar_word = similar_words[position][0] 
        return most_similar_word, max(similar_lst), position
    
    @staticmethod
    def __calculate_confiability_score(similarity: float, correct_position: int):
        return round(math.sqrt(pow(similarity, 3) * 0.85 / math.log10(correct_position + 8)),3)
    
    def spell_check_sentence(self, sentence: str, threshold: float, ):
        sentence_lst = sentence.split()
        mask_wrong = [False if word in self.__emb_broad.value.wv.vocab else True for word in sentence_lst]
        
        if True in mask_wrong:
            sentence_len = len(sentence_lst)
            for ind, value in enumerate(mask_wrong):
                if value:
                    left_limit, right_limit = SpellCheck.__calculate_limits(ind,sentence_len)    
                    if False in mask_wrong[left_limit:right_limit]:    
                        most_similar_word, similarity_score, candidate_position = self.__find_correct_word(ind, left_limit, right_limit, sentence_lst)    
                        confiability_score = SpellCheck.__calculate_confiability_score(similarity_score, candidate_position)
                        if confiability_score > threshold:
                            sentence_lst[ind] = most_similar_word
            return ' '.join(sentence_lst)
        return sentence