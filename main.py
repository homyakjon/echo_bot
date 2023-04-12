import requests
from bs4 import BeautifulSoup as bs
import time
import json


TOKEN = "6133853033:AAH2eC8f7IJrgC6ANOElQEOF_8f_xvuOGSU"
URL = 'https://api.telegram.org/bot'

url_jokes = 'https://anekdotov.net/anekdot/'


def get_jokes_list():
    resp = requests.get(url_jokes)
    soup = bs(resp.text, 'html.parser')
    parsed = soup.find_all('div', class_='anekdot' )
    return [obj.text for obj in parsed]


def request_updates(last_id) -> [int, dict]:
    headers = {'content-type': 'application/json'}
    params = {"offset": last_id + 1, "timeout": 30}
    resp = requests.get('https://api.telegram.org/bot' + TOKEN + '/getUpdates', headers=headers, params=params)
    list_of_updates = json.loads(resp.text)
    resp.close()
    for list_up in list_of_updates["result"]:
        if list_up["update_id"] > last_id:
            last_id = list_up["update_id"]
            print('Last_update_id: ', last_id)
    print(list_of_updates)
    return last_id, list_of_updates


def send_message(updates):
    for i in updates['result']:
        chat_id = i["message"]["chat"]["id"]
        text = i["message"]["text"]
        params = {"chat_id": chat_id, "text": text}

        get_text = requests.get('https://api.telegram.org/bot' + TOKEN + '/sendMessage',
                                headers={'Content-Type': 'application/json'}, params=params)
        get_text.close()


def run_telegram_bot(jokes):
    last_id = 0
    while True:
        last_id, updates = request_updates(last_id)  #
        send_message(updates)
        time.sleep(3)


def main():
    jokes = get_jokes_list()
    print("getting list of jokes: ", jokes)
    run_telegram_bot(jokes)


if __name__ == "__main__":
    main()
