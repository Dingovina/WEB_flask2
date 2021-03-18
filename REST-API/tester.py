import requests


def response(id, arg):
    new_id = arg['new_id']
    new_title = arg['new_title']
    new_leader = arg['new_leader']
    new_size = arg['new_size']
    new_coll = arg['new_coll']
    new_finish = arg['new_finish']
    ans = requests.get(f'http://127.0.0.1:5000/api/jobs/correct/{id}/{new_id}/{new_title}/{new_leader}/{new_size}/{new_coll}/{new_finish}')
    return ans.text


before = requests.get(f'http://127.0.0.1:5000/api/jobs/all').text
args = {'new_id': 7,
        'new_title': 'NEW JOB',
        'new_leader': 1,
        'new_size': 1,
        'new_coll': 1,
        'new_finish': True}
test1 = response(6, args)  # Корректный запрос
args = {'new_id': 11,
        'new_title': 'NEW JOB',
        'new_leader': 1,
        'new_size': 1,
        'new_coll': 1,
        'new_finish': True}
test2 = response(1, args)   # Некорректный старый id
args = {'new_id': 12,
        'new_title': 'NEW JOB',
        'new_leader': 1,
        'new_size': 1,
        'new_coll': 1,
        'new_finish': 1}
test3 = response(7, args)  # Некорректный параметр new_finish
args = {'new_id': 123,
        'new_title': 'NEW JOB',
        'new_leader': 1,
        'new_size': 1,
        'new_coll': 1,
        'new_finish': True}
test4 = response(10, args)  # Некорректный новый id
after = requests.get(f'http://127.0.0.1:5000/api/jobs/all').text
print(before, test1, after, test2, test3, test4, sep='\n')

