#let's try to avoid importing other libraries
import numpy as np
VECTOR_LENGTH = 2
#our data
paragraph = """apple banana orange apple orange banana banana apple orange apple apple orange orange math science history english history english math math math science history english history cat dog rabbit rabbit dog dog cat dog cat rabbit cat cat cat"""

#randomize our word_to_vec dictionary
word_to_vec = dict()
for word in paragraph.split():
    if word not in word_to_vec:
        word_to_vec[word] = [2 * (np.random.random(1)-.5)[0] for _ in range(VECTOR_LENGTH)]
    
print('randomized initial values:')
for word, vec in word_to_vec.items():
    print(f'{word} = {vec}')
print()
    
# ======================================================================================
     
    
# (1) implement the get_most_similar_word function
def get_most_similar_word(word, word_to_vec):
    min_dist = float('inf')
    closest_word = word
    word_embedding = word_to_vec[word]
    for key,value in word_to_vec.items():
        if key == word:
            continue
        # euclidean distance
        tmp_dist = np.sqrt(np.sum([(v-w)**2 for v,w in zip(value,word_embedding)]))
        
        # manhattan distance
        #tmp_dist = sum([np.abs(v+w) for v,w in zip(value,word_embedding)])
        
        if tmp_dist < min_dist:
            closest_word = key
            min_dist = tmp_dist
    if closest_word == word:
        #something went wrong
        return None    
            
    return closest_word

#this function prints out most similar word for each word
def print_most_similar_words(word_to_vec):
    print('most similar after training:')
    for w in word_to_vec:
        print(f'{w} ~ {get_most_similar_word(w, word_to_vec)}')
        print()

#print_most_similar_words(word_to_vec)

# ======================================================================================
    
#(2) write an algorithm which will update the word vectors so that:
#    - if w1, w2 are close to each other in the text (eg. "apple" and "banana"), then their vectors are close to each other
#.   - if w1, w2 are far from each other in the text (eg. "apple" and "cat") then their vectors are are far from each other

def calc_avg_vector(vec1:list,vec2:list,learning_rate:float,mult:float) -> list:
    return [(w1+w2)*learning_rate*mult/len(vec1) for w1,w2 in zip(vec1,vec2)]

def update_word_vectors(word_to_vec, paragraph,learning_rate=0.001,iterations=10000,vector_length=VECTOR_LENGTH,penalty_rate=2.,debug = True):
    # loop through paragraph, any word that is next to another is similar
    # any word that is not next to the other is different
    seen_tuples = {} # key is tuple, value is count seen
    words = paragraph.split()
    # loop through paragraph, counting occurrence of each bigram
    for i in range(len(words)-1):
        word1 = words[i]
        word2 = words[i+1]
        if word1 == word2:
            continue
        if (word1,word2) not in seen_tuples and (word2,word1) not in seen_tuples:
            seen_tuples[(word1,word2)] = 1
        else:
            if (word1,word2) not in seen_tuples:
                seen_tuples[(word2,word1)] += 1
            else:
                seen_tuples[(word1,word2)] += 1
    print(seen_tuples.values())
    # add all unseen tuples to be able to move them farther apart
    unseen_tuples = {}
    for w1 in word_to_vec.keys():
        for w2 in word_to_vec.keys():
            if w1 != w2:
                if (w1,w2) not in seen_tuples and (w2,w1) not in seen_tuples:
                    unseen_tuples[(w1,w2)] = 1
    
    value_to_add = {}
    for i in range(iterations):
        value_to_add.clear()
        for word in word_to_vec.keys():
            value_to_add[word] = [0. for _ in range(vector_length)]
        # Positive training loop, add average vector
        for seen_vec,count in seen_tuples.items():
            word1 = seen_vec[0]
            word2 = seen_vec[1]
            word1_vec = word_to_vec[word1]
            word2_vec = word_to_vec[word2]
            
            avg_vec = calc_avg_vector(word1_vec,word2_vec,learning_rate,count)
            #print(f"len avg_vec: {len(avg_vec)}")
            value_to_add[word1] = [w1 + w2 for w1,w2 in zip(word1_vec,avg_vec)]
            value_to_add[word2] = [w1 + w2 for w1,w2 in zip(word2_vec,avg_vec)]
            #print(f"len value_to_add w1: {len(value_to_add[word1])}")
            #print(value_to_add[word2])
        for tup in unseen_tuples.keys():
            word1 = tup[0]
            word2 = tup[1]
            word1_vec = word_to_vec[word1]
            word2_vec = word_to_vec[word2]
            avg_vec = calc_avg_vector(word1_vec,word2_vec,learning_rate,penalty_rate)
            value_to_add[word1] = [w1 - w2 for w1,w2 in zip(word1_vec,avg_vec)]
            value_to_add[word2] = [w1 - w2 for w1,w2 in zip(word2_vec,avg_vec)]
        
        # update step, add changed values
        for word in word_to_vec.keys():
            cur_word_vec = word_to_vec[word]
            cur_word_vec = [c+v for c,v in zip(cur_word_vec,value_to_add[word])]
            #print(f"len cur_word_vec: {len(cur_word_vec)}")
            if (i-1) % 100 == 0: # normalize the vector so they don't grow too fast
                l2 = np.sqrt(sum([w**2 for w in cur_word_vec]))
                cur_word_vec = [c / l2 for c in cur_word_vec]
            word_to_vec[word] = cur_word_vec
        if i % 100 == 0 and debug:
            print(f'values at epoch {i} of training:')
            for word, vec in word_to_vec.items():
                print(f'{word} = {vec}')
    
    return word_to_vec
        
word_to_vec = update_word_vectors(word_to_vec, paragraph,debug=False)
print('values after training:')
for word, vec in word_to_vec.items():
    print(f'{word} = {vec}')
print()
print_most_similar_words(word_to_vec)

