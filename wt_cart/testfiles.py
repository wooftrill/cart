import requests,time

session = requests.Session()
session.maxsize = 100
start_time = time.time()
url = 'http://localhost:5003/show_with_login'
jwt_token = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjoidTVBUDJTaW9UZlFhQVdlS2FrZTh6T2wyZmRkMiIsInNlc3Npb25faWQiOiJ3ZXdld2VyZGQiLCJleHAiOjE2ODM3NzY2OTF9.N4SpV0yIbk_SC8LNxlgKc4tpUph8qhzSSNBQKKz8Uko'
item_id = 'c122'


response = session.post(url, json={'item_id': item_id,'count':3,'is_active':0}, headers={'Authorization': f'Bearer {jwt_token}'})
time= time.time()-start_time
print(time)

print(response.text)
if response.status_code == 200:
    print('Items added to cart successfully')
else:
    print('Failed to add items to cart')


