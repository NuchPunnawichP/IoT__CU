import requests

url = "https://notify-api.line.me/api/notify"
token = "doYySITQHmse2EY0HSEL53wcaoCYCBak4TFPNS0CQsv"
headers = {'Authorization': 'Bearer ' + token}

msg = {
    'message': "กินมันติดเหงือก กินเผือกติดฟัน"
}

res = requests.post(url, headers=headers, data=msg)
print(res.text)
