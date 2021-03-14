import random
import math
import nltk
from sklearn.metrics import accuracy_score
import numpy as np
from sklearn.neighbors import KNeighborsClassifier
from sklearn.neighbors import NearestCentroid
from gensim import corpora, models
from proj1 import lexicon


def fill_dict(source):  # to fill dictionary such as {category: [[doc_id, text],...],...}
    file = open(source, "r")
    dictionary = {}
    category = ""
    text = ""
    corp = ["<CA", "<CO", "<IN", "<SO", "</I", "</C"]
    doc_id = 0
    for line in file:
        if line[:3] == "<CA":
            doc_id += 1
            category = str(line[10:-2])
            if category not in dictionary.keys():
                dictionary.update({category: []})
        if line[:3] not in corp:
            if line[-1] == "\n":
                text += line[:-1]
            else:
                text += line
        if line[:3] == "</I":
            dictionary[category].append([doc_id, text])
            text = ""
    file.close()
    return dictionary


def split_train_test(dictionary, N):  # takes N document in each category for training set
    train_list = []
    test_list = []

    for key in dictionary.keys():
        random.shuffle(dictionary[key])
        # train_list.update({key: []})
        # test_list.update({key: []})
        for i in range(N):
            # train_list[key].append(dictionary[key][i])
            train_list.append([[key, dictionary[key][i][0]], dictionary[key][i][1]])
        for i in range(N, len(dictionary[key])):
            # test_list[key].append(dictionary[key][i])
            test_list.append([[key, dictionary[key][i][0]], dictionary[key][i][1]])
    return train_list, test_list


def split_train_test_percentage(dictionary, percentage):
    # takes "percentage" percent documents in each category for training set
    train_list = []
    test_list = []

    for key in dictionary.keys():
        random.shuffle(dictionary[key])
        length = (len(dictionary[key]) * percentage) // 100
        for i in range(length):
            train_list.append([[key, dictionary[key][i][0]], dictionary[key][i][1]])
        for i in range(length, len(dictionary[key])):
            test_list.append([[key, dictionary[key][i][0]], dictionary[key][i][1]])
    return train_list, test_list


def generate_word_dict_doc(source):
    # generates dict that holds {term: [[word_id, {doc_id: term_freq,...}],...],...}
    file = open(source, "r")
    word_dict = {}
    word_id = 0
    for line in file:
        splitted_line = line.split("\t")
        word_dict.update({splitted_line[0]: [word_id, {}]})
        for i in range(1, len(splitted_line), 2):
            word_dict[splitted_line[0]][1].update({int(splitted_line[i]): int(splitted_line[i + 1])})
        word_id += 1
    file.close()
    return word_dict


def vectorize_doc(word_dict, cat_list, trans_list):  # vectorize a list
    total_word_count = len(word_dict)
    for i, liste in enumerate(trans_list):
        tokens = nltk.tokenize.word_tokenize(liste[1])
        vector = [0] * total_word_count
        category_id = cat_list.index(liste[0][0])
        for token in tokens:
            vector[word_dict[token][0]] = word_dict[token][1][liste[0][1]]
        vector.append(category_id)
        trans_list[i] = vector


def vectorize_single_doc(word_dict, cat_list, liste):  # vectorize a single document
    total_word_count = len(word_dict)
    tokens = nltk.tokenize.word_tokenize(liste[1])
    vector = [0] * total_word_count
    category_id = cat_list.index(liste[0][0])
    # print(train_list[0])
    # print(word_dict)
    # print(tokens)
    for token in tokens:
        vector[word_dict[token][0]] = word_dict[token][1][liste[0][1]]
    return vector


def KNN(train, test, word_dict, k, cat_list):
    # vectorize(word_dict, train)
    prediction = predict(train, test, word_dict, k, cat_list)
    print("My KNN algo:", accuracy_score([test[i][0][0] for i in range(len(test))], prediction))


def most_freq(lst, k, cat_list, num=14):  # calculates the most frequent term in a list
    cat = [0] * 14
    val = k
    for i, out in enumerate(lst):
        cat[cat_list.index(out)] += val
        val -= 0.5
    return cat_list[np.argmax(cat)]


def predict(train, test, word_dict, k, cat_list):
    predictions = []
    for i in range(len(test)):  # traverses all of the test
        distances = []
        vector = vectorize_single_doc(word_dict, cat_list, test[i])  # vectorize single test folder
        for j in range(len(train)):
            # calculates the all distances bw train set and single test
            distances.append(math.dist(train[j][:-1], vector))
        zips = zip(distances, train)
        zips = sorted(zips)  # sort distances ascending order
        train = [point[1] for point in zips]
        predictions.append(
            most_freq([cat_list[train[x][-1]] for x in range(k)], k, cat_list))
    return predictions


def LDA(dictionary):
    texts = []
    for key in dictionary.keys():
        for liste in dictionary[key]:
            texts.append(nltk.tokenize.word_tokenize(liste[1]))
    new_dict = corpora.Dictionary(texts)
    corpus = [new_dict.doc2bow(text) for text in texts]
    print(dictionary.keys())
    ldamodel = models.ldamodel.LdaModel(corpus, num_topics=14, id2word=new_dict, passes=20)
    for liste in ldamodel.print_topics(num_topics=14, num_words=10):
        splitted = liste[1].split("+")
        print(f"Topic: {liste[0]} || ", end="")
        for split in splitted:
            print(split, "-> ", end="")
        print()


def runs_KNN(dictionary, word_dict, iter_no, k, test_limit):
    for i in range(iter_no):
        train_list, test_list = split_train_test(dictionary, min_category_len)
        # train_list, test_list = split_train_test_percentage(dictionary, percentage=50)

        print("Train size:", len(train_list))
        cat_list = list(dictionary.keys())  # holds string version of the categories as list

        vectorize_doc(word_dict, cat_list, train_list)  # vectorize all the train list

        random.shuffle(test_list)  # shuffle the test_list

        KNN(train_list, test_list[:test_limit], word_dict, k, cat_list)  # my KNN algorithm

        train_list_x = [train_list[x][:-1] for x in range(len(train_list))]
        train_list_y = [cat_list[train_list[x][-1]] for x in range(len(train_list))]

        neigh = KNeighborsClassifier(n_neighbors=k)
        neigh.fit(train_list_x, train_list_y)

        a = []
        for i in range(test_limit):  # to create vectorized test list of the given number of test
            a.append(vectorize_single_doc(word_dict, cat_list, test_list[i]))

        test_list_y = [test_list[x][0][0] for x in range(test_limit)]
        print("Sklearn KNN:", accuracy_score(neigh.predict(a), test_list_y))
        print("-" * 1000)


def rocchio_classifier(dictionary, word_dict, iter_no, test_limit):
    for i in range(iter_no):
        train_list, test_list = split_train_test(dictionary, min_category_len)
        # train_list, test_list = split_train_test_percentage(dictionary, percentage=50)

        print("Train size:", len(train_list))
        cat_list = list(dictionary.keys())  # holds string version of the categories as list

        vectorize_doc(word_dict, cat_list, train_list)  # vectorize all the train list

        random.shuffle(test_list)  # shuffle the test_list

        a = []
        for i in range(test_limit):  # to create vectorized test list of the given number of test
            a.append(vectorize_single_doc(word_dict, cat_list, test_list[i]))

        train_list_x = [train_list[x][:-1] for x in range(len(train_list))]
        train_list_y = [cat_list[train_list[x][-1]] for x in range(len(train_list))]
        test_list_y = [test_list[x][0][0] for x in range(test_limit)]

        clf = NearestCentroid()
        clf.fit(train_list_x, train_list_y)
        print("Sklearn Rocchio:", accuracy_score(clf.predict(a), test_list_y))
        print("-" * 1000)


if __name__ == '__main__':
    # pre_proc("radikal.corpus", "radikal.preprocess.corpus")  # to preprocess the corpus
    # lexicon("radikal.preprocess.corpus", "radikal.doc_sorted.terms") # to create radikal.doc_sorted.terms

    # this creates the dictionary such as {category: [[doc_id, text],...],...}
    dictionary = fill_dict("radikal.preprocess.corpus")
    min_category_len = len(dictionary[min(dictionary.items(), key=lambda x: len(x[1]))[0]])
    min_category_len //= 2

    # generates word_dict that holds {term: [[word_id, {doc_id: term_freq,...}],...],...}
    word_dict = generate_word_dict_doc("radikal.doc_sorted.terms")

    runs_KNN(dictionary, word_dict, iter_no=10, k=3, test_limit=250)  # runs my KNN and sklearn KNN algorithms
    rocchio_classifier(dictionary, word_dict, iter_no=10, test_limit=250)  # runs my rocchio classifier
    LDA(dictionary)  # runs LDA model
