import requests,time

session = requests.Session()
session.maxsize = 100
start_time = time.time()
url = 'http://34.125.89.30:5008/checkout_with_login'

jwt_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoieWNtZGVmbWU5cWc4QlNSTVNQcVYxcEtaZkg5MyIsInNlc3Npb25faWQiOiJnaHNnZGhzaDc4NzM2NzNod2dpa2siLCJleHAiOjE2OTQwNzEzNTl9.tgeFqo6vgPbP5emYhIw2fY6QKBAUiB_Bi9D93gKbh-k"

item_id = '201819_03_01'


response = session.post(url, json={'item_id': item_id,'count':1,'is_active':'1',"discount_code":'',"address_code":'550e8400-e29b-41d4-a716-446655440000'}, headers={'Authorization': f'Bearer {jwt_token}'})
time= time.time()-start_time
print(time)

print(response.text)
if response.status_code == 200:
    print('Items added to cart successfully')
else:
    print('Failed to add items to cart')


