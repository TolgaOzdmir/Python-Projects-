import nltk
import string
import re

global child_num
child_num = 29


class TrieNode:

    # Trie node class
    def __init__(self, catnum=14, docnum=6893):
        self.children = [None] * child_num

        # isEndOfWord is True if node represent the end of the word
        self.isEndOfWord = False
        self.doc = 0
        self.count = 0
        self.lastdoc = -1
        self.doc_list = []
        self.doc_count = {}
        self.cat_list = [0] * catnum


class Trie:

    # Trie data structure class
    def __init__(self):
        self.root = self.getNode()

    def getNode(self):

        # Returns new trie node (initialized to NULLs)
        return TrieNode()

    def _charToIndex(self, ch):

        # private helper function
        # Converts key current character into index
        # use only 'a' through 'z' and lower case

        return ord(ch) - ord('A')

    def insert(self, key, document_id):

        # If not present, inserts key into trie
        # If the key is prefix of trie node,
        # just marks leaf node
        pCrawl = self.root
        length = len(key)
        for level in range(length):
            index = self._charToIndex(key[level])

            # if current character is not present
            if not pCrawl.children[index]:
                pCrawl.children[index] = self.getNode()
            pCrawl = pCrawl.children[index]

        pCrawl.count += 1
        if document_id in pCrawl.doc_count.keys():
            pCrawl.doc_count[document_id] += 1
        else:
            pCrawl.doc_count.update({document_id: 1})
        if document_id != pCrawl.lastdoc:
            pCrawl.doc += 1
            pCrawl.lastdoc = document_id
            pCrawl.doc_list.append(document_id)
        # mark last node as leaf
        pCrawl.isEndOfWord = True

    def insert_cat(self, key, document_id, cat_id):

        # If not present, inserts key into trie
        # If the key is prefix of trie node,
        # just marks leaf node
        pCrawl = self.root
        length = len(key)
        for level in range(length):
            index = self._charToIndex(key[level])

            # if current character is not present
            if not pCrawl.children[index]:
                pCrawl.children[index] = self.getNode()
            pCrawl = pCrawl.children[index]

        pCrawl.count += 1
        if document_id != pCrawl.lastdoc:
            pCrawl.doc += 1
            pCrawl.lastdoc = document_id
            pCrawl.doc_list.append(document_id)
        # mark last node as leaf
        pCrawl.cat_list[cat_id] += 1
        pCrawl.isEndOfWord = True

    def search(self, key):

        # Search key in the trie
        # Returns true if key presents
        # in trie, else false
        pCrawl = self.root
        length = len(key)
        for level in range(length):
            index = self._charToIndex(key[level])
            if not pCrawl.children[index]:
                return False
            pCrawl = pCrawl.children[index]

        return pCrawl is not None and pCrawl.isEndOfWord

    def display(self, node: TrieNode, fptr, text=""):
        if node.isEndOfWord:
            # print(text, node.doc, node.count, sep="\t")
            a = text + "\t" + str(node.doc) + "\t" + str(node.count) + "\n"
            fptr.write(a)
        for i in range(child_num):
            if node.children[i] is not None:
                self.display(node.children[i], fptr, str(text + chr(i + ord("A"))))

    def display_postinglist(self, node: TrieNode, fptr, text=""):
        if node.isEndOfWord:
            # print(text, node.doc, node.count, sep="\t")
            # a = text + " "
            a = ""
            for i in node.doc_list:
                a += str(i) + ","
                a = a.rstrip()

            fptr.write(a[:-1] + "\n")
        for i in range(child_num):
            if node.children[i] is not None:
                self.display_postinglist(node.children[i], fptr, str(text + chr(i + ord("A"))))

    def display_doc(self, node: TrieNode, fptr, text=""):
        if node.isEndOfWord:
            # print(text, node.doc, node.count, sep="\t")
            # a = text + " "
            a = text + "\t"
            for i, dc in enumerate(node.doc_list):
                if i == len(node.doc_list) - 1:
                    a += str(dc) + "\t" + str(node.doc_count[dc])
                else:
                    a += str(dc) + "\t" + str(node.doc_count[dc]) + "\t"

            fptr.write(a + "\n")
        for i in range(child_num):
            if node.children[i] is not None:
                self.display_doc(node.children[i], fptr, str(text + chr(i + ord("A"))))

    def display_cat(self, node: TrieNode, fptr, text=""):
        if node.isEndOfWord:
            # print(text, node.doc, node.count, sep="\t")
            # a = text + "\t" + str(node.doc) + "\t" + str(node.count) + "\t"
            a = text + "\t"
            for i in range(len(node.cat_list)):
                if i == len(node.cat_list) - 1:
                    a += str(node.cat_list[i]) + "\n"
                else:
                    a += str(node.cat_list[i]) + "\t"
            fptr.write(a)
        for i in range(child_num):
            if node.children[i] is not None:
                self.display_cat(node.children[i], fptr, str(text + chr(i + ord("A"))))


def pre_proc(source, dest):
    file = open(source, "r")
    nfile = open(dest, "w")
    corp = ["<CA", "<CO", "<IN", "<SO", "</I", "</C"]

    for line in file:
        if line[:3] in corp:
            nfile.write(line)
        else:
            line = line.translate(str.maketrans("ğĞıİöÖüÜşŞçÇðýþÐÝÞ", "gGiIoOuUsScCgisGIS",
                                                string.punctuation))  # turk to eng & delete punc.
            line = line.encode("ascii", "ignore").decode("utf-8")  # deleting non-ascii
            if len(line) > 0:
                line = line.upper()
                line = re.sub(' +', ' ', line)
                nfile.write(line)

    file.close()
    nfile.close()


def lexicon(source, dest):
    trie = Trie()
    file = open(source, "r")
    corp = ["<CA", "<CO", "<IN", "<SO", "</I", "</C"]
    doc_id = 1
    for line in file:
        if line[:3] not in corp:
            tokens = nltk.tokenize.word_tokenize(line)
            for word in tokens:
                trie.insert(word, doc_id)
        if line[:3] == "</I":
            doc_id += 1
    fptr = open(dest, "w")
    # trie.display(trie.root, fptr, "")
    trie.display_doc(trie.root, fptr, "")
    file.close()
    fptr.close()


def lexicon_cat(source, dest, cat_list: list):
    trie = Trie()
    file = open(source, "r")
    corp = ["<CA", "<CO", "<IN", "<SO", "</I", "</C"]
    doc_id = 1
    category_id = -1
    for line in file:
        if line[:3] == "<CA":
            category = str(line[10:-2])
            category_id = cat_list.index(category)
        if line[:3] not in corp:
            tokens = nltk.tokenize.word_tokenize(line)
            for word in tokens:
                trie.insert_cat(word, doc_id, category_id)
        if line[:3] == "</I":
            doc_id += 1
    fptr = open(dest, "w")
    trie.display_cat(trie.root, fptr, "")
    file.close()
    fptr.close()


def docs(source, dest):
    file = open(source, "r")
    fptr = open(dest, "w")
    docid_line = [1, 0]
    # fptr.write("id\tinstance\tcategory\tfirst line\n")
    for line in file:
        docid_line[1] += 1
        if line[:3] == "<IN":
            fptr.write(str(docid_line[0]) + "\t" + str(line[10:-2]) + "\t")
        if line[:3] == "<CA":
            fptr.write(str(line[10:-2]) + "\t" + str(docid_line[1] + 1) + "\n")
        if line[:3] == "</I":
            docid_line[0] += 1
    file.close()
    fptr.close()


def inverted_index(source, dest):
    file = open(source, "r")
    fptr = open(dest, "w")
    trie = Trie()
    corp = ["<CA", "<CO", "<IN", "<SO", "</I", "</C"]
    doc_id = 1
    for line in file:
        if line[:3] not in corp:
            tokens = nltk.tokenize.word_tokenize(line)
            for word in tokens:
                trie.insert(word, doc_id)
        if line[:3] == "</I":
            doc_id += 1
    trie.display_postinglist(trie.root, fptr, "")
    file.close()
    fptr.close()


if __name__ == '__main__':
    # pre_proc()
    lexicon("radikal.preprocess.corpus", "radikal.doc_sorted.terms")
    # docs()
    # inverted_index("radikal.preprocess.corpus", "radikal.doc_sorted.terms")
