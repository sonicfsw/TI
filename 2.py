import pandas as pd
import numpy as np
from collections import Counter

text = "София Балачкова"

# 1 Подсчитаем частоты появления символов
char_counts = Counter(text)
total_chars = sum(char_counts.values())

# 2 Вычисляем вероятности появления символов
char_probs = {char: count / total_chars for char, count in char_counts.items()}

# 3 Сортируем символы по убыванию вероятности
sorted_chars = sorted(char_probs.items(), key=lambda x: x[1], reverse=True)

# Функция построения кода Фано
def shannon_fano(symbols):
    if len(symbols) == 1:
        return {symbols[0][0]: ""}

    total_prob = sum([prob for _, prob in symbols])
    cumulative_prob = 0
    split_index = 0

    for i, (_, prob) in enumerate(symbols):
        cumulative_prob += prob
        if cumulative_prob >= total_prob / 2:
            split_index = i
            break

    left_part = symbols[:split_index + 1]
    right_part = symbols[split_index + 1:]

    left_codes = shannon_fano(left_part)
    right_codes = shannon_fano(right_part)

    for key in left_codes:
        left_codes[key] = '0' + left_codes[key]
    for key in right_codes:
        right_codes[key] = '1' + right_codes[key]

    left_codes.update(right_codes)
    return left_codes

# 4 код Фано
fano_codes = shannon_fano(sorted_chars)

# 5неравенство Крафта
kraft_sum = sum(2 ** -len(code) for code in fano_codes.values())

# Подготовка данных для вывода
df_fano = pd.DataFrame({
    "Символ": [char for char, _ in sorted_chars],
    "Частота": [char_counts[char] for char, _ in sorted_chars],
    "Вероятность": [char_probs[char] for char, _ in sorted_chars],
    "Код Фано": [fano_codes[char] for char, _ in sorted_chars]
})


# 6. Кодирование первой буквы фамилии (Б) кодом Хэмминга (7,4)
# Функция кодирования в Хэмминга (7,4)
def hamming74_encode(data_bits):
    p1 = data_bits[0] ^ data_bits[1] ^ data_bits[3]
    p2 = data_bits[0] ^ data_bits[2] ^ data_bits[3]
    p3 = data_bits[1] ^ data_bits[2] ^ data_bits[3]
    return [p1, p2, data_bits[0], p3, data_bits[1], data_bits[2], data_bits[3]]

# Кодируем 'Б' в двоичную систему
char_b_binary = format(ord('Б'), '08b')  # Получаем 8-битный ASCII-код
data_bits = [int(bit) for bit in char_b_binary[:4]]  # Берём первые 4 бита
hamming_code = hamming74_encode(data_bits)
# Добавляем еще один код Хэмминга (для 8-битного представления)
data_bits2 = [int(bit) for bit in char_b_binary[4:]]
hamming_code2 = hamming74_encode(data_bits2)
# Соединяем два 7-битных слова (итого 14 бит)
hamming_full_code = hamming_code + hamming_code2

# 7. Вносим ошибку в 14-й разряд (меняем бит)
hamming_full_code[13] ^= 1  # Инвертируем бит в 14 позиции
# Функция исправления ошибки
def hamming74_correct(encoded_bits):
    p1 = encoded_bits[0] ^ encoded_bits[2] ^ encoded_bits[4] ^ encoded_bits[6]
    p2 = encoded_bits[1] ^ encoded_bits[2] ^ encoded_bits[5] ^ encoded_bits[6]
    p3 = encoded_bits[3] ^ encoded_bits[4] ^ encoded_bits[5] ^ encoded_bits[6]

    error_pos = p1 * 1 + p2 * 2 + p3 * 4

    if error_pos > 0:
        encoded_bits[error_pos - 1] ^= 1  # Исправляем ошибку
    return encoded_bits

# Исправляем ошибки
corrected_hamming_code1 = hamming74_correct(hamming_code)
corrected_hamming_code2 = hamming74_correct(hamming_code2)
# Объединяем исправленные части
corrected_hamming_full_code = corrected_hamming_code1 + corrected_hamming_code2

print("\n--- Кодирование Фано ---")
print(df_fano)
print("\n--- Код Хэмминга ---")
df_hamming = pd.DataFrame({
    "Бит №": list(range(1, 15)),
    "Код Хэмминга": hamming_full_code,
    "Исправленный код": corrected_hamming_full_code
})
print(df_hamming)

# Сохранение в файл (если хочешь открыть в Excel)
df_fano.to_csv("fano_code.csv", index=False, encoding="utf-8-sig")
df_hamming.to_csv("hamming_code.csv", index=False, encoding="utf-8-sig")
# Проверка результата Крафта
kraft_result = "Неравенство Крафта выполняется" if kraft_sum <= 1 else "Неравенство Крафта не выполняется"
print("\nПроверка неравенства Крафта:", kraft_result)
