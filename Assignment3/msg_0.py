import requests

url = "https://notify-api.line.me/api/notify"
token = <>
headers = {'Authorization': 'Bearer ' + token}

msg = {
    'message': "กินมันติดเหงือก กินเผือกติดฟัน"
}

res = requests.post(url, headers=headers, data=msg)
print(res.text)
