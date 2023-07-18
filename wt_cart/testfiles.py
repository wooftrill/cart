import requests,time

session = requests.Session()
session.maxsize = 100
start_time = time.time()
url = 'http://localhost:5008/show_with_login'
jwt_token = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjoidTVBUDJTaW9UZlFhQVdlS2FrZTh6T2wyZmRkMiIsInNlc3Npb25faWQiOiJkZWJ0ZXN0NTZtb3U3ODAxMnRlc3RsIiwiZXhwIjoxNjg5NjQ5OTU5fQ.S5qpIzD6xMbda1o3z18HZFLQdRkKi5nL86gI2gn7Qso'
item_id = '201816_03_01'


response = session.post(url, json={'item_id': item_id,'count':1,'is_active':'1'}, headers={'Authorization': f'Bearer {jwt_token}'})
time= time.time()-start_time
print(time)

print(response.text)
if response.status_code == 200:
    print('Items added to cart successfully')
else:
    print('Failed to add items to cart')


