import requests


def response(arg):
    ans = requests.get(f'http://127.0.0.1:5000/api/jobs/{arg}')
    return ans.json()


test1 = response(1)         # Корректный запрос
test2 = response(2)         # Корректный запрос
test3 = response('all')     # Корректный запрос на получение всех работ
test4 = response(123)       # Некорректный запрос: неверный id
test5 = response(0)         # Некорректный запрос: неверный id
test6 = response('any')     # Некорректный запрос: строковый аргумент
print(test1, test2, test3, test4, test5, test6, sep='\n')