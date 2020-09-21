import requests


def refresh_api(client_id, client_secret, refresh_token):
    # API Token Call
    headers = {"User-Agent": "Data Analytics"}
    url = "https://ruqqus.com/oauth/grant"
    data = {"client_id": client_id,
        "client_secret": client_secret,
        "grant_type": "refresh",
        "refresh_token": refresh_token
        }

    r=requests.post(url, headers=headers, data=data)

    token = r.json()['access_token']
    return token

def get_data(page_number, token):
    # Authorization header
    headers={"Authorization": "Bearer " + token,
        "User-Agent": "Data Analytics"}

    # Build URL
    url=f"https://ruqqus.com/api/v1/front/listing?sort=new&page={page_number}"

    # Call URL
    r=requests.get(url, headers=headers)
    try:
        return r.json()['data']
    except:
        return Null
