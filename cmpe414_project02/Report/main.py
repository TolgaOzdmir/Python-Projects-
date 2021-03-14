import pickle
import math
from golomb import golomb_encoding
import datetime
import os


def get_terms_into_dic():  # it is for generating dictionary which holds terms as a key and an empty list for doc_ids
    file = open("./data/crawl.terms", "r")
    dictionary = {}  # to hold term_ids as {term: []}
    lines = file.readlines()
    start = datetime.datetime.now()
    for i in range(len(lines)):
        word = lines[i].split(" ")[1]  # it gets word id
        dictionary.update({int(word): []})
    end = datetime.datetime.now()
    print("Time for getting terms into dic: ", end - start)
    file.close()
    return dictionary


def make_idv_dictionary(dictionary):  # to append sorted doc_ids into {term: []} dictionary
    files = ["./data/crawl.DV.0", "./data/crawl.DV.1"]
    line_counter = 0
    start = datetime.datetime.now()
    for i in range(len(files)):  # to traverses two files in files list
        file = open(files[i], "r")
        lines = file.readlines()
        for j in range(len(lines)):
            splitted = lines[j].split(" ")
            data = [int(splitted[i]) for i in range(1, len(splitted)) if i % 2 == 1]  # for getting term_id in crawl.DV
            for word_id in data:
                dictionary[word_id].append(line_counter)
            line_counter += 1
        file.close()
    end = datetime.datetime.now()
    print("Time for creating dictionary which holds sorted doc_ids: ", end - start)


def write_dict_to_textfile(dictionary):  # to create and fill crawl.IDV file
    file = open("crawl.IDV", "w")
    start = datetime.datetime.now()
    for i in dictionary.keys():
        for length, id in enumerate(dictionary[i]):
            if length != len(dictionary[i]) - 1:
                file.write((str(id) + "\t"))
            else:
                file.write((str(id) + "\n"))
    end = datetime.datetime.now()
    print("Time for writing dict to text: ", end - start)
    file.close()


def golomb_version():  # to encode files with golomb encoding, it gets data in crawl.IDV
    file = open("crawl.IDV", "r")
    f = 0
    for line in file:  # in this part, it calculates f value which is the number of distinct (doc,id) pairs
        splitted = line.split("\t")
        f += len(splitted)
    file.close()

    file = open("./data/crawl.info", "r")
    lines = file.readlines()
    n = int(lines[1].split(" ")[1])  # the number of total distinct terms
    N = int(lines[2].split(" ")[1])  # the number of total documents
    file.close()
    b = int(0.69 * (N * n) / f)  # to calculate optimal b value
    # but I did not use this value since it is not an optimal value for our case
    # I use this part to calculate which b values is the optimal value
    """print()  
    print("-" * 50)
    for j in range(15, 21):
        b = 2 ** j
        dictionary = {}
        for i in range(N + 1):
            dictionary.update({i: golomb_encoding(i, b)})

        file = open("crawl.IDV", "r")
        fptr = open(f"golombIDV_bvalue_{b}.bin", "wb")
        start = datetime.datetime.now()
        for line in file:
            splitted = line.split("\t")
            golombed_data = [dictionary[int(i)] for i in splitted]
            pickle.dump(golombed_data, fptr)
        end = datetime.datetime.now()
        print(f"Time for golomb encoding with b: {b} : ", end - start, "\tGB: ",
              round(os.stat(f"golombIDV_bvalue_{b}.bin").st_size / 10 ** 9, 3))
        dictionary.clear()
        fptr.close()
        file.close()"""

    b = 2 ** 18  # it is the optimal b_value that I found
    dictionary = {}
    for i in range(N + 1):  # to generate dictionary, {doc_id: encoded_doc_id}
        dictionary.update({i: golomb_encoding(i, b)})

    file = open("crawl.IDV", "r")
    fptr = open("crawl.IDV.encoded.bin", "wb")
    start = datetime.datetime.now()
    for line in file:
        splitted = line.split("\t")
        golombed_data = [dictionary[int(i)] for i in splitted]  # it is the encoded version of the doc_ids
        pickle.dump(golombed_data, fptr)  # I use pickle library to write binary format
    end = datetime.datetime.now()
    print(f"Time for golomb encoding with b value, {b}: ", end - start, "\tGB: ",
          round(os.stat("crawl.IDV.encoded.bin").st_size / 10 ** 9, 3))
    fptr.close()
    file.close()


if __name__ == "__main__":
    # dictionary = get_terms_into_dic()
    # make_idv_dictionary(dictionary)
    # write_dict_to_textfile(dictionary)
    golomb_version()
