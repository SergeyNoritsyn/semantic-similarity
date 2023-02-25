'''
Sergey Noritsyn, Marko Samardzija
ESC180 - Prof. Guerzhoy
December 3rd, 2021
Project 3
'''

import math
import timeit
time = timeit.default_timer()


def norm(vec):
    '''Return the norm of a vector stored as a dictionary,
    as described in the handout for Project 3.
    '''

    sum_of_squares = 0.0
    for x in vec:
        sum_of_squares += vec[x] * vec[x]

    return math.sqrt(sum_of_squares)


def cosine_similarity(vec1, vec2):
    if not vec1 or not vec2:
        return -1

    dot_prod = 0
    for word in vec1.keys():
        if word in vec2.keys():
            dot_prod += vec1[word] * vec2[word]
    vec1_norm = norm(vec1)
    vec2_norm = norm(vec2)
    return dot_prod / (vec1_norm * vec2_norm)


def build_semantic_descriptors(sentences):
    dict = {}
    for sentence in sentences:
        sentence = set(sentence)
        for word in sentence:
            if word.isspace() or word.isempty():
                continue
            if word not in dict:
                dict[word] = {}
            for w in sentence:
                if w not in dict:
                    dict[w] = {}
                if w != word:
                    if w not in dict[word]:
                        dict[word][w] = 1
                    else:
                        dict[word][w] += 1
    return dict

def build_semantic_descriptors_from_files(filenames):
    text = ""
    for file in filenames:
        f = open(file, "r", encoding = "latin1")
        text += f.read().lower()

    sentences = []
    text = text.replace("\n", " ").replace("!", "\n").replace("?", "\n").replace(".", "\n").replace(";", "").replace(",", "").replace("--", " ").replace(":", "").replace("-", " ").split("\n")

    for s in text:
        sentences.append(s.strip().split())

    return build_semantic_descriptors(sentences)



def most_similar_word(word, choices, semantic_descriptors, similarity_fn):
    max_sim = -2
    max_sim_word = ""
    for w in choices:
        if w in semantic_descriptors:
            cur_sim = cosine_similarity(semantic_descriptors[word], semantic_descriptors[w])
            if cur_sim > max_sim:
                max_sim_word = w
                max_sim = cur_sim

    if max_sim == -2:
        return choices[0]
    return max_sim_word


def run_similarity_test(filename, semantic_descriptors, similarity_fn):
    f = open(filename, "r", encoding = "latin1")
    text = f.read().lower().strip().split("\n")
    correct_counter = 0
    total_tests = 0
    for s in text:
        t = s.split()
        semantic_guess = most_similar_word(t[0], t[2:], semantic_descriptors, similarity_fn)
        if semantic_guess == t[1]:
            correct_counter += 1
        print(t[1])
        print(semantic_guess)
        total_tests += 1
    return correct_counter / total_tests * 100
