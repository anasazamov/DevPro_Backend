import requests
from bs4 import BeautifulSoup
import json

def fetch_car_data(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    table_rows = soup.find_all('tr')
    
    cars_data = []
    for row in table_rows[1:]:  
        columns = row.find_all('td')
        car_info = {
            "date": columns[0].text.strip(),
            "car": columns[1].text.strip(),
            "model": columns[2].text.strip(),
            "transmission": columns[3].text.strip(),
            "transmission_type": columns[4].text.strip(),
            "status": columns[5].text.strip(),
        }
        cars_data.append(car_info)
    
    return cars_data


all_data = []
for i in range(1,9):
    car_data_url = f'https://www.carmodoo.com/consult/consultList.html?page={i}&myConsult=&id='
    car_data = fetch_car_data(car_data_url)
    for i in car_data:
        all_data.append(i)

# Saving the data to a JSON file
with open('car_data.json', 'w', encoding='utf-8') as f:
    json.dump(all_data, f, ensure_ascii=False, indent=4)

print("Data has been successfully saved to car_data.json.")
