import requests
import time
from bs4 import BeautifulSoup
import pandas as pd


def handle_response(response,MaxTrials=3,CurrentTrial=0):
    
        status = response.status_code

        if status == 200:
            print("Success")

        elif CurrentTrial < MaxTrials:
            print(f"Error: {status}")
            if status == 429:
                print("Error: Too many requests")
                time.sleep(15*CurrentTrial)
                return False
            else:
                time.sleep(5*CurrentTrial)
                return False
        else:
            print("Error: Max Trials reached")
            return None
    
        return response

def make_request(CompanyURL,MaxTrials=3,CurrentTrial=0):
    payload = {}
    headers = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'accept-language': 'en-US,en;q=0.9',
    'cache-control': 'max-age=0',
    'cookie': 'lang=v=2&lang=en-us; bcookie="v=2&7aafa9fa-80bb-4ce9-8e58-258f7098a230"; JSESSIONID=ajax:7091056752031294795; bscookie="v=1&202409192328445eee63e6-ebb7-42ff-875d-0fa354080d90AQEYBL-g0GHt3qgVmskTAwIKrBcSU_UB"; _gcl_au=1.1.2089583266.1726788524; AMCVS_14215E3D5995C57C0A495C55%40AdobeOrg=1; lidc="b=VGST09:s=V:r=V:a=V:p=V:g=3000:u=1:x=1:i=1726788752:t=1726875152:v=2:sig=AQGjYHcYWON2_plKudYDAzzdNRZGutip"; _uetsid=e99c613076de11ef9b4663fa46f07827; _uetvid=e99c9de076de11ef99a55f1b4a8d232b; aam_uuid=13676313366740523261239266915417371647; AMCV_14215E3D5995C57C0A495C55%40AdobeOrg=-637568504%7CMCIDTS%7C19986%7CMCMID%7C13122036689852649411296453458398429236%7CMCAAMLH-1727400769%7C7%7CMCAAMB-1727400769%7C6G1ynYcLPuiQxYZrsz_pkqfLG9yMXBpb2zX5dvJdYQJzPXImdj0y%7CMCOPTOUT-1726803169s%7CNONE%7CvVersion%7C5.1.1; bcookie="v=2&de48fc50-3246-4850-898b-88edb58255af"; lang=v=2&lang=en-us; lidc="b=VGST07:s=V:r=V:a=V:p=V:g=3060:u=1:x=1:i=1726862006:t=1726948406:v=2:sig=AQH7qeonWJpC1ySI_F9AHYUpVZZXu5nL"; JSESSIONID=ajax:6123196309613059981',
    'dnt': '1',
    'priority': 'u=0, i',
    'referer': 'https://www.linkedin.com/jobs/view/dentist-public-health-at-emploissant%C3%A9-emplois-en-sant%C3%A9-et-services-sociaux-4027616427/?original_referer=',
    'sec-ch-ua': '"Chromium";v="128", "Not;A=Brand";v="24", "Google Chrome";v="128"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-user': '?1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36'
    }

    response = requests.request("GET", CompanyURL, headers=headers, data=payload)

    response = handle_response(response,MaxTrials=MaxTrials,CurrentTrial=CurrentTrial)
    if response == False:
        return make_request(CompanyURL,CurrentTrial=CurrentTrial+1,MaxTrials=MaxTrials)
    elif response == None:
        return None
    else:
        return response
    
def parse_response(response):
    soup = BeautifulSoup(response.text, 'html.parser')
    data = {}

    elements = soup.find_all('div', class_='mb-2 flex papabear:mr-3 mamabear:mr-3 babybear:flex-wrap')
    for element in elements:
        key = element.find('dt').get_text(strip=True)
        value = element.find('dd').get_text(strip=True)
        data[key] = value

    df = pd.DataFrame([data])
    df.columns = [col.replace(' ', '_').lower() for col in df.columns]
    return df


def get_company_details(CompanyURL,MaxTrials=3,CurrentTrial=0):
    response = make_request(CompanyURL,MaxTrials=MaxTrials,CurrentTrial=CurrentTrial)
    if response == None:
        return pd.DataFrame()
    else:
        return parse_response(response)

