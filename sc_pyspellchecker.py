import os
from nltk.tokenize import word_tokenize
from Levenshtein import distance
from itertools import product
from string import ascii_lowercase
from collections import defaultdict
import datrie
import re
import nltk
import tkinter as tk
from tkinter import filedialog, Text, messagebox, scrolledtext
from spellchecker import SpellChecker


def download_if_needed(package_name):
    try:
        nltk.data.find(package_name)
        print(f'{package_name} package is already downloaded')
    except LookupError:
        nltk.download(package_name)
        print(f'{package_name} package has been downloaded')

download_if_needed('punkt')


trie = datrie.Trie('abcdefghijklmnopqrstuvwxyz')


def read_in_chunks(file_object, block_size=1024 * 1024):
    while True:
        data = file_object.read(block_size)
        if not data:
            break
        yield data

def add_words_to_database(filename):
    with open(filename, 'r', encoding='utf-8') as file:
        for piece in read_in_chunks(file):
            text = piece
            text = re.sub(r'\W+', ' ', text)
            words = word_tokenize(text)
            words = [word.lower() for word in words if word.isalpha()]
            for word in words:
                if word not in trie:
                    trie[word] = 1

def build_database(directory):
    for filename in os.listdir(directory):
        if filename.endswith('.txt'):
            add_words_to_database(os.path.join(directory, filename))


build_database(r'D:\BYLW\enwiki-20230401-pages-articles-multistream-index.txt')

trie.save(r'D:\BYLW\word_trie2.2change.dat')

trie = datrie.Trie.load(r'D:\BYLW\word_trie2.2change.dat')

# Write to plain text file (specify the same path)
with open(r'D:\BYLW\my_text_file.txt', 'w', encoding='utf-8') as file:
    for word in trie.keys():
        file.write(word + '\n')





spell = SpellChecker(language=None, case_sensitive=True)
spell.word_frequency.load_text_file(r'D:\BYLW\my_text_file.txt')

def check_spelling(word):
    if word in spell:
        return ""
    else:
        suggestions = spell.candidates(word)
        # Converted to a list and sorted by edit distance from the original word
        suggestions = sorted(list(suggestions), key=lambda x: nltk.edit_distance(word, x))
        # Take only the first three recommendations
        suggestions = suggestions[:3]
        suggestion_string = f"'{word}' is not found in the dictionary. Did you mean:\n"
        for suggestion in suggestions:
            suggestion_string += f"- '{suggestion}'\n"
        return suggestion_string

def check_document_spelling(text):
    words = word_tokenize(text)
    words = [word.lower() for word in words if word.isalpha()]
    result = ""
    for word in words:
        check_result = check_spelling(word)
        if check_result is not None:
            result += check_result + "\n"
    return result


def open_file():
    filename = filedialog.askopenfilename(initialdir="/", title="Select File",
                                          filetypes=(("text files", "*.txt"), ("all files", "*.*")))
    if filename:
        with open(filename, 'r', encoding='utf-8') as file:
            text = file.read()
        result = check_document_spelling(text)
        text_scroll.delete(1.0, tk.END)  # Delete old output
        text_scroll.insert(tk.END, result)

def check_text():
    text = entry_field.get(1.0, tk.END)
    result = check_document_spelling(text)
    text_scroll.delete(1.0, tk.END)  # Delete old output
    text_scroll.insert(tk.END, result)

root = tk.Tk()
canvas = tk.Canvas(root, height=400, width=400)
canvas.pack()

openFileButton = tk.Button(root, text="Open File", padx=10, pady=5, fg="white", bg="black", command=open_file)
openFileButton.pack()

entry_field = tk.Text(root, width=50, height=10)
entry_field.pack()
checkTextButton = tk.Button(root, text="Check Text", padx=10, pady=5, fg="white", bg="black", command=check_text)
checkTextButton.pack()

text_scroll = tk.Text(root, width=50, height=10)
text_scroll.pack()

root.mainloop()



