import requests, json

params = {}

with open('password.json') as f:
    params = json.loads(f.read())

params['grant_type'] = 'password'

r = requests.post('http://beta.online-go.com/oauth2/access_token', data=params)
print(r)
print(r.text)

stuff = json.loads(r.text)

print(stuff['access_token'])

headers = {
    'Authorization': 'Bearer ' + stuff['access_token']}

data = json.dumps({'moves': 'bc'})

r = requests.get('http://beta.online-go.com/api/v1/reviews/59/', headers=headers, data=data)

print(r.text)
