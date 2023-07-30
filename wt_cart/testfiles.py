import requests,time

session = requests.Session()
session.maxsize = 100
start_time = time.time()
url = 'http://localhost:5008/checkout_with_login'

jwt_token = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjoieWNtZGVmbWU5cWc4QlNSTVNQcVYxcEtaZkg5MyIsInNlc3Npb25faWQiOiJnaGZoZ2Rmc3R1a2ZkdGRoaGZnc2QiLCJleHAiOjE2OTA2MzMwNTl9.17fBR728u4QeqvGITA89cKQE6lNGK34e4EDqSzBWHqM'
item_id = '201816_03_02'


response = session.post(url, json={'item_id': item_id,'count':1,'is_active':'1'}, headers={'Authorization': f'Bearer {jwt_token}'})
time= time.time()-start_time
print(time)

print(response.text)
if response.status_code == 200:
    print('Items added to cart successfully')
else:
    print('Failed to add items to cart')


