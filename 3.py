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

# Функция средней длины кода
def average_code_length(code_dict, probabilities):
    return sum(len(code_dict[char]) * prob for char, prob in probabilities.items())

# Функция расчета избыточности кода
def redundancy_code(entropy, avg_length):
    return avg_length - entropy

# Функция расчета эффективности кода
def code_efficiency(entropy, avg_length):
    return entropy / avg_length if avg_length > 0 else 0

# Функция расчета вектора Крафта
def kraft_inequality(code_dict):
    return sum(2 ** -len(code) for code in code_dict.values())

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

fiction_entropy = entropy(fiction_probs)
science_entropy = entropy(science_probs)

fiction_avg_length = average_code_length(fiction_huffman, fiction_probs)
science_avg_length = average_code_length(science_huffman, science_probs)

fiction_redundancy = redundancy_code(fiction_entropy, fiction_avg_length)
science_redundancy = redundancy_code(science_entropy, science_avg_length)

fiction_efficiency = code_efficiency(fiction_entropy, fiction_avg_length)
science_efficiency = code_efficiency(science_entropy, science_avg_length)

fiction_kraft = kraft_inequality(fiction_huffman)
science_kraft = kraft_inequality(science_huffman)

fiction_chars_no_spaces = count_chars_without_spaces(fiction_text)
science_chars_no_spaces = count_chars_without_spaces(science_text)

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
plt.figure(figsize=(6, 4))
plt.bar(["Художественный", "Научный"], [fiction_kraft, science_kraft], color=['blue', 'orange'])
plt.xlabel("Тип текста")
plt.ylabel("Значение вектора Крафта")
plt.title("Сравнение значений вектора Крафта")
plt.show()

# График энтропии
plt.figure(figsize=(6, 4))
plt.bar(["Художественный", "Научный"], [fiction_entropy, science_entropy], color=['blue', 'orange'])
plt.xlabel("Тип текста")
plt.ylabel("Энтропия")
plt.title("Сравнение энтропии текстов")
plt.show()

# Сохранение всех характеристик в CSV
csv_filename = "text_analysis_results.csv"
with open(csv_filename, "w", newline="", encoding="utf-8") as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["Тип текста", "Количество символов без пробелов", "Энтропия", "Средняя длина кода", "Избыточность кода", "Эффективность кода", "Вектор Крафта"])
    writer.writerow(["Художественный", fiction_chars_no_spaces, fiction_entropy, fiction_avg_length, fiction_redundancy, fiction_efficiency, fiction_kraft])
    writer.writerow(["Научный", science_chars_no_spaces, science_entropy, science_avg_length, science_redundancy, science_efficiency, science_kraft])

print(f"Результаты анализа сохранены в {csv_filename}")
