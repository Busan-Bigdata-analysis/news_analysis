import requests
import json

def urlKaKao():
    url = 'https://kauth.kakao.com/oauth/token'
    rest_api_key = 'f4d02835e8f23456b653c2fd7ba6c85d'
    redirect_uri = 'https://example.com/oauth'
    authorize_code = 'pW7vaO549QfHnUlsayIJVsJQpezRf-1opM5HQw7A5slDyPNE7I6f1WfO0e5ja9IJa93ImQo9c00AAAGDWV7QYA'

    data = {
        'grant_type':'authorization_code',
        'client_id':rest_api_key,
        'redirect_uri':redirect_uri,
        'code': authorize_code,
        'scope': 'talk_message'
        }

    response = requests.post(url, data=data)
    tokens = response.json()
    print(tokens)

    # json 저장
    with open("kakao_code.json","w") as fp:
        json.dump(tokens, fp)

def sendKaKao():
    with open("kakao_code.json","r") as fp:
        tokens = json.load(fp)

    url="https://kapi.kakao.com/v2/api/talk/memo/default/send"

    # kapi.kakao.com/v2/api/talk/memo/default/send 

    headers={
        "Authorization" : "Bearer " + tokens["access_token"]
    }

    data={
        "template_object": json.dumps({
            "object_type":"text",
            "text":"Hello, world!",
            "link":{
                "web_url":"www.naver.com"
            }
        })
    }
    
    response = requests.post(url, headers=headers, data=data)
    print(response.status_code)
    if response.json().get('result_code') == 0:
        print('메시지를 성공적으로 보냈습니다.')
    else:
	    print('메시지를 성공적으로 보내지 못했습니다. 오류메시지 : ' + str(response.json()))