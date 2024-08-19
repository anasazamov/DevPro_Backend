import requests
from bs4 import BeautifulSoup

# Saytdan mahsulotlarni olish
def get_products_from_olcha():
    url = "https://olcha.uz/ru"
    response = requests.get(url)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, 'html.parser')

    # Mahsulotlarni topish (sahifa tuzilishiga qarab o'zgartirish kerak bo'lishi mumkin)
    products = soup.find_all('div', class_='product-item')

    product_list = []
    for product in products:
        try:
            name = product.find('a', class_='product-title').text.strip()
            price = product.find('div', class_='product-price').text.strip()
            description = product.find('div', class_='product-description').text.strip()
        except AttributeError:
            continue

        product_list.append({
            "name": name,
            "price": price,
            "description": description
        })

    return product_list

# Mahsulotlarni backendga yuborish
def send_products_to_backend(product_list):
    endpoint_url = "http://127.0.0.1:8000/products/"  # Backend endpoint URL

    for product in product_list:
        data = {
            "name": product['name'],
            "price": product['price'],
            "description": product['description']
        }

        response = requests.post(endpoint_url, json=data)
        if response.status_code == 201:
            print(f"Mahsulot yaratildi: {product['name']}")
        else:
            print(f"Xato: {response.status_code}, Mahsulot: {product['name']}")

if __name__ == "__main__":
    products = get_products_from_olcha()
    send_products_to_backend(products)
