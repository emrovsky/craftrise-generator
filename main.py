import json
import random
import threading
import time

import capsolver
import loguru
import requests
import tls_client

capsolver.api_key = "CAP-5874678BAC71ABD1441A408670E98C47"
class CraftriseGen:
    def __init__(self):
        self.session = tls_client.Session(client_identifier="chrome_120")
        self.session.headers = {
            'accept': '*/*',
            'accept-language': 'tr-TR,tr;q=0.5',
            'cache-control': 'no-cache',
            'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'origin': 'https://www.craftrise.com.tr',
            'pragma': 'no-cache',
            'priority': 'u=1, i',
            'referer': 'https://www.craftrise.com.tr/',
            'sec-ch-ua': '"Chromium";v="124", "Brave";v="124", "Not-A.Brand";v="99"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'sec-gpc': '1',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',
            'x-requested-with': 'XMLHttpRequest',
        }
        self.proxy = random.choice(open("proxy.txt", "r").readlines()).strip()
        self.session.proxies = {'http': 'http://' + self.proxy.strip(), 'https': 'http://' + self.proxy.strip()}

    def create_nickname(self):
        r = requests.get(f"https://laby.net/api/v3/names?order_by=available_from&order=ASC&page={random.randint(1,200)}&popularity=0&min_length=3&max_length=16&is_og=none",headers={'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36'})
        return random.choice(r.json())["user_name"]
    def get_signup_page(self):
        r = self.session.get("https://www.craftrise.com.tr/")
        #print(r.cookies.get_dict()) #PHPSESSID
    def solve_captcha(self):
        captcha_token = capsolver.solve({
                "type": "ReCaptchaV3TaskProxyLess",
                "websiteURL": "https://www.craftrise.com.tr",
                "websiteKey": "6LfhmvEmAAAAAKCG7yu5dywabnggUDi5aFuJOgpf",
                "pageAction": "homepage"
            })['gRecaptchaResponse']
        loguru.logger.info(f"captcha çözüldü: {captcha_token[:50]}..")
        return captcha_token
    def create_account(self, username):
        password = "".join([password for x in range(8) if (password := random.choice('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'))])+str(random.randint(100,999)) + random.choice('!@#$%^&*()_+')
        data = {
            'username': username,
            'password1': password,
            'password2': password,
            'email1': f'{username}@gmail.com',
            'registerTick': 'true',
            'recaptcharesponse': self.solve_captcha()
        }


        response = self.session.post('https://www.craftrise.com.tr/posts/post-register.php', data=data)
        if response.json()["resultType"] == "success":
            loguru.logger.success(f"[{username}] hesap oluşturuldu.")
            open("accounts.txt", "a").write(f"{username}:{password}\n")
        else:
            loguru.logger.error(f"[{username}] hesap oluşturma işlemi başarısız: {response.json()['resultMessage']}")

def generate_account():
    gen = CraftriseGen()
    username = ((gen.create_nickname())+str(random.randint(100,999)))[:16]
    gen.get_signup_page()
    time.sleep(10)
    gen.create_account(username)

if __name__ == '__main__':
    accNumber = input("Kaç hesap oluşturulsun?: ")
    for i in range(int(accNumber)):
        threading.Thread(target=generate_account).start()
        time.sleep(0.5)
