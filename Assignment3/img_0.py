import requests

url = "https://notify-api.line.me/api/notify"
token = "doYySITQHmse2EY0HSEL53wcaoCYCBak4TFPNS0CQsv"
headers = {'Authorization': 'Bearer ' + token}

msg = {
    'message': "Game Start",
    'imageThumbnail': "https://raw.githubusercontent.com/NuchPunnawichP/IoT__CU/main/Assignment3/Photo/apt.jpg",
    'imageFullsize': "https://raw.githubusercontent.com/NuchPunnawichP/IoT__CU/main/Assignment3/Photo/apt.jpg",
    'stickerPackageId': "1",
    'stickerId': "12"
}

res = requests.post(url, headers=headers, data=msg)
print(res.text)
