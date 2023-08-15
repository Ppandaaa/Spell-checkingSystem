import os
import nltk
import tkinter as tk
from nltk.tokenize import word_tokenize
from tkinter import filedialog
from transformers import BertForMaskedLM, BertTokenizer

# Make sure have downloaded the necessary packages
nltk.download('punkt')

def download_pretrained_model():
    global model, tokenizer
    model = BertForMaskedLM.from_pretrained('bert-base-uncased')
    tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')

model = BertForMaskedLM.from_pretrained('bert-base-uncased')
tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')

def correct_word_with_bert(word):

    masked_text = '[MASK]'

    input_ids = tokenizer.encode(masked_text, return_tensors='pt')

    output = model(input_ids, labels=input_ids)
    top_k_predictions = output[0].argsort(descending=True)[:,:10]
    for pred in top_k_predictions[0]:
        predicted_word = tokenizer.decode([pred])

        if nltk.edit_distance(word, predicted_word) <= 2:
            return predicted_word
    return word

def correct_text_with_bert(text):
    words = word_tokenize(text)
    corrected_text = ""
    for word in words:
        corrected_word = correct_word_with_bert(word)
        corrected_text += corrected_word + " "
    return corrected_text.strip()

def open_file():
    filename = filedialog.askopenfilename(initialdir="/", title="Select File",
                                          filetypes=(("text files", "*.txt"), ("all files", "*.*")))
    if filename:
        with open(filename, 'r', encoding='utf-8') as file:
            text = file.read()
        corrected_text = correct_text_with_bert(text)
        text_scroll.delete(1.0, tk.END)  # Delete old output
        text_scroll.insert(tk.END, corrected_text)

def correct_entry_text():
    text = entry_field.get(1.0, tk.END)
    corrected_text = correct_text_with_bert(text)
    text_scroll.delete(1.0, tk.END)  # Delete old output
    text_scroll.insert(tk.END, corrected_text)

root = tk.Tk()
canvas = tk.Canvas(root, height=400, width=400)
canvas.pack()

openFileButton = tk.Button(root, text="Open File", padx=10, pady=5, fg="white", bg="black", command=open_file)
openFileButton.pack()

entry_field = tk.Text(root, width=50, height=10)
entry_field.pack()

correctTextButton = tk.Button(root, text="Correct Text", padx=10, pady=5, fg="white", bg="black", command=correct_entry_text)
correctTextButton.pack()

text_scroll = tk.Text(root, width=50, height=10)
text_scroll.pack()

root.mainloop()



