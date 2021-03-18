import requests


def response(arg):
    ans = requests.get(f'http://127.0.0.1:5000/api/jobs/delete/{arg}')
    return ans.text


before = requests.get(f'http://127.0.0.1:5000/api/jobs/all').text
test1 = response(1)  # Корректный запрос
test4 = response(123)  # Некорректный запрос: неверный id
test5 = response(0)  # Некорректный запрос: неверный id
test6 = response('any')  # Некорректный запрос: строковый аргумент
after = requests.get(f'http://127.0.0.1:5000/api/jobs/all').text
print(before, test1, test4, test5, test6, after, sep='\n')
