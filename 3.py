import collections
import heapq
import math
import csv
import matplotlib.pyplot as plt
from itertools import product
import pandas as pd

# Функция для частотного анализа
def frequency_analysis(text):
    freq = collections.Counter(text)
    total_chars = sum(freq.values())
    probabilities = {char: count / total_chars for char, count in freq.items()}
    return freq, probabilities

# Подсчет символов без пробелов
def count_chars_without_spaces(text):
    return len(text.replace(" ", ""))

# Функция построения дерева Хаффмана
def huffman_tree(freq):
    heap = [[weight, [char, ""]] for char, weight in freq.items()]
    heapq.heapify(heap)
    while len(heap) > 1:
        lo = heapq.heappop(heap)
        hi = heapq.heappop(heap)
        for pair in lo[1:]:
            pair[1] = '0' + pair[1]
        for pair in hi[1:]:
            pair[1] = '1' + pair[1]
        heapq.heappush(heap, [lo[0] + hi[0]] + lo[1:] + hi[1:])
    return dict(heap[0][1:])

# Функция расчета энтропии
def entropy(probabilities):
    return -sum(p * math.log2(p) for p in probabilities.values())

# Функция расчета избыточности алфавита
def redundancy_alphabet(entropy, alphabet_size):
    return 1 - (entropy / math.log2(alphabet_size)) if alphabet_size > 1 else 0

# Функция расчета избыточности кода
def redundancy_code(entropy, avg_length):
    return avg_length - entropy

# Функция расчета вектора Крафта
def kraft_inequality(code_dict):
    return sum(2 ** -len(code) for code in code_dict.values())

# Функция генерации блочных кодов
def block_codes(probabilities, block_size):
    alphabet = list(probabilities.keys())
    combinations = [''.join(p) for p in product(alphabet, repeat=block_size)]
    block_freq = collections.Counter(combinations)
    total_blocks = sum(block_freq.values())
    block_prob = {block: count / total_blocks for block, count in block_freq.items()}
    return block_prob

# Чтение текстов
with open("fiction_text.txt", "r", encoding="utf-8") as f:
    fiction_text = f.read()
with open("science_text.txt", "r", encoding="utf-8") as f:
    science_text = f.read()

# Анализ данных
fiction_freq, fiction_probs = frequency_analysis(fiction_text)
science_freq, science_probs = frequency_analysis(science_text)

fiction_huffman = huffman_tree(fiction_freq)
science_huffman = huffman_tree(science_freq)

# Графики
plt.figure(figsize=(10, 5))
plt.bar(fiction_probs.keys(), fiction_probs.values(), alpha=0.5, label='Художественный текст')
plt.bar(science_probs.keys(), science_probs.values(), alpha=0.5, label='Научный текст')
plt.xlabel("Символы")
plt.ylabel("Вероятность появления")
plt.title("Распределение вероятностей символов в текстах")
plt.legend()
plt.show()

# График вектора Крафта
fiction_kraft = kraft_inequality(fiction_huffman)
science_kraft = kraft_inequality(science_huffman)
plt.figure(figsize=(6, 4))
plt.bar(["Художественный", "Научный"], [fiction_kraft, science_kraft], color=['blue', 'orange'])
plt.xlabel("Тип текста")
plt.ylabel("Значение вектора Крафта")
plt.title("Сравнение значений вектора Крафта")
plt.show()

# График энтропии
fiction_entropy = entropy(fiction_probs)
science_entropy = entropy(science_probs)
plt.figure(figsize=(6, 4))
plt.bar(["Художественный", "Научный"], [fiction_entropy, science_entropy], color=['blue', 'orange'])
plt.xlabel("Тип текста")
plt.ylabel("Энтропия")
plt.title("Сравнение энтропии текстов")
plt.show()

# Подготовка таблицы кодов Хаффмана
def generate_huffman_table(freq, huffman_codes):
    table = []
    for char, count in freq.items():
        probability = count / sum(freq.values())
        code = huffman_codes[char]
        bit_columns = list(code)
        table.append([char, count, probability] + bit_columns + [code])
    return table

fiction_huffman_table = generate_huffman_table(fiction_freq, fiction_huffman)
science_huffman_table = generate_huffman_table(science_freq, science_huffman)

# Сохранение таблицы Хаффмана в CSV
huffman_filename = "huffman_codes.csv"
with open(huffman_filename, "w", newline="", encoding="utf-8") as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["Буква", "Кол-во", "Частота"] + [str(i+1) for i in range(10)] + ["Код"])
    writer.writerow(["Художественный текст"])
    for row in fiction_huffman_table:
        writer.writerow(row)
    writer.writerow([])
    writer.writerow(["Научный текст"])
    for row in science_huffman_table:
        writer.writerow(row)

print(f"Таблица кодов Хаффмана сохранена в {huffman_filename}")
