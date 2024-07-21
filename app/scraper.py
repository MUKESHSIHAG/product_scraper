import os
import httpx
from bs4 import BeautifulSoup
from .models import Product
from .utils import save_to_json, load_from_json
from .settings import settings
import aiohttp
import asyncio
import re

class Scraper:
    def __init__(self, page_limit=settings.page_limit, proxy=settings.proxy):
        self.page_limit = page_limit
        self.proxy = proxy
        self.base_url = "https://dentalstall.com/shop/"
        self.products = []
        self.retry_count = 3
        self.retry_delay = 5

    async def fetch_page(self, session, url):
        retries = 0
        while retries < self.retry_count:
            try:
                async with session.get(url, proxy=self.proxy) as response:
                    response.raise_for_status()
                    return await response.text()
            except Exception as e:
                retries += 1
                await asyncio.sleep(self.retry_delay)
        return None

    async def scrape_page(self, page_number):
        if page_number == 1:
            url = self.base_url
        else:
            url = f"{self.base_url}page/{page_number}/"
        async with aiohttp.ClientSession() as session:
            page_content = await self.fetch_page(session, url)
        if page_content:
            soup = BeautifulSoup(page_content, "html.parser")
            products = soup.find_all("div", class_="product-inner")
            for product in products:
                title = product.find("h2", class_="woo-loop-product__title").text.strip()
                price_text = product.find("span", class_="woocommerce-Price-amount amount").text
                price = float(re.sub(r'[^\d.]', '', price_text))
                image_url = product.find("img", class_="attachment-woocommerce_thumbnail size-woocommerce_thumbnail")["data-lazy-src"]
                image_path = self.download_image(image_url)
                self.products.append(Product(product_title=title, product_price=price, path_to_image=image_path))

    def download_image(self, url):
        image_name = os.path.basename(url)
        image_path = os.path.join("images", image_name)
        if not os.path.exists("images"):
            os.makedirs("images")
        response = httpx.get(url)
        with open(image_path, 'wb') as f:
            f.write(response.content)
        return image_path

    async def scrape(self):
        tasks = []
        for page_number in range(1, self.page_limit + 1):
            tasks.append(self.scrape_page(page_number))
        await asyncio.gather(*tasks)
        self.save_to_db()
        print(f"Scraped {len(self.products)} products.")

    def save_to_db(self):
        existing_data = load_from_json()
        for product in self.products:
            if not any(p['product_title'] == product.product_title and p['product_price'] == product.product_price for p in existing_data):
                existing_data.append(product.dict())
        save_to_json(existing_data)
