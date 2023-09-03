import requests,time

session = requests.Session()
session.maxsize = 100
start_time = time.time()
url = 'http://localhost:5008/checkout_with_login'

jwt_token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjoieWNtZGVmbWU5cWc4QlNSTVNQcVYxcEtaZkg5MyIsInNlc3Npb25faWQiOiJnaHNnZGhzaDc4NzM2NzNod2dpa2siLCJleHAiOjE2OTM3NTg0ODV9.JKux6sX-IYlcjg0ZA02ZvYgz1ICpa46nXrdyMIsaiCs"

item_id = '201816_03_01'


response = session.post(url, json={'item_id': item_id,'count':1,'is_active':'1','discount_code':'','address_code': "2"}, headers={'Authorization': f'Bearer {jwt_token}'})
time= time.time()-start_time
print(time)

print(response.text)
if response.status_code == 200:
    print('Items added to cart successfully')
else:
    print('Failed to add items to cart')


