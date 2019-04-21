# Преобразование чисел в слова, денежные еденицы, порядковые номера, года 

# Три языка Беларуский, Русский, Английский 

# Использывание: 

from numbers_to_words import num2words
print(num2words(42.42, lang='by', to ='currency', currency = "RUB"))
сорак два рубля, сорак дзве капейкі

print(num2words(42.42, lang='by', to ='currency', currency = "EUR"))
сорак два еўра, сорак два цэнта

print(num2words(42.42, lang='by', to ='currency', currency = "USD"))
сорак два даляра, сорак два цэнта

to: Конвертер для использования. Поддерживаемые значения:

cardinal (default)
ordinal 
ordinal_num
year
currency