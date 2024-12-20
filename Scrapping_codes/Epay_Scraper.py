from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import numpy as np


class Product:
    """Represents a single product with its attributes."""
    def __init__(self):
        self.image_link = None
        self.brand = None
        self.model = None
        self.ebay_product_id = None
        self.product_type = "Smartphone"
        self.name = None
        self.company = "eBay"
        self.seller_name = None
        self.price_before = None
        self.price_after = None
        self.amount_promotion = None
        self.promotion_percent = None
        self.highlights = None
        self.overall_rating = None
        self.num_ratings = None
        self.color = None
        self.screen_size = None
        self.model_number = None
        self.battery_size = None
        self.processor = None
        self.graphics_processor = None
        self.internal_memory = None
        self.ram_size = None

    def to_dict(self):
        """Converts the product attributes into a dictionary."""
        return {
            "product_imag_link": self.image_link,
            "Brand": self.brand,
            "Model": self.model,
            "eBay_Product_ID_ePID": self.ebay_product_id,
            "product_type": self.product_type,
            "name_of_product": self.name,
            "company_name": self.company,
            "seller_name": self.seller_name,
            "price_before_promotion": self.price_before,
            "price_after_promotion": self.price_after,
            "amount_promotion": self.amount_promotion,
            "promotion_percent": self.promotion_percent,
            "Highlights_or_Description_of_product": self.highlights,
            "overall_rating": self.overall_rating,
            "number_of_rating": self.num_ratings,
            "Color_name": self.color,
            "Screen_Size": self.screen_size,
            "Model_Number": self.model_number,
            "battery_size": self.battery_size,
            "Processor_version": self.processor,
            "Graphics_Processor_version": self.graphics_processor,
            "internal_memory": self.internal_memory,
            "RAM_Size": self.ram_size
        }


class eBayScraper:
    """Scrapes eBay for smartphone listings."""
    def __init__(self, base_url):
        self.base_url = base_url
        self.driver = webdriver.Chrome()
        self.data = []

    def get_product_links(self, page_number):
        """Fetches product links from the current page."""
        url = f"{self.base_url}&_pgn={page_number}"
        try:
            self.driver.get(url)
            products_ul = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "b-list__items_nofooter"))
            )
            product_elements = products_ul.find_elements(By.TAG_NAME, "li")
            links = []
            for element in product_elements:
                try:
                    link = element.find_element(By.CLASS_NAME, "s-item__info").find_element(By.TAG_NAME, "a").get_attribute("href")
                    links.append(link)
                except:
                    continue
            return links
        except Exception as e:
            print(f"Error fetching product links on page {page_number}: {e}")
            return []

    def extract_product_details(self, product_link):
        """Extracts details of a single product."""
        product = Product()
        self.driver.get(product_link)

        try:
            product.name = self.driver.find_element(
                By.CLASS_NAME, "x-item-title__mainTitle"
            ).find_element(By.TAG_NAME, "span").text
        except:
            product.name = None

        try:
            product.seller_name = self.driver.find_element(
                By.CLASS_NAME, "x-sellercard-atf_info_about-seller"
            ).find_element(By.TAG_NAME, "span").text
        except:
            product.seller_name = None

        try:
            product.image_link = self.driver.find_element(
                By.CLASS_NAME, "ux-image-carousel-item"
            ).find_element(By.TAG_NAME, "img").get_attribute("src")
        except:
            product.image_link = None

        try:
            product.price_after = self.driver.find_element(
                By.CLASS_NAME, "x-price-primary"
            ).find_element(By.TAG_NAME, "span").text
        except:
            product.price_after = None

        try:
            details = {}
            rows = self.driver.find_elements(By.CLASS_NAME, "ux-labels-values__labels")
            values = self.driver.find_elements(By.CLASS_NAME, "ux-labels-values__values")
            for row, value in zip(rows, values):
                details[row.text] = value.text

            product.brand = details.get("Brand", None)
            product.model = details.get("Model", None)
            product.screen_size = details.get("Screen Size", None)
            product.color = details.get("Color", None)
            product.internal_memory = details.get("Storage Capacity", None)
            product.ram_size = details.get("RAM", None)
            product.processor = details.get("Processor", None)
            product.ebay_product_id = details.get("eBay Product ID (ePID)", None)

        except Exception as e:
            print(f"Error extracting product details: {e}")

        return product

    def scrape_pages(self, max_pages=3):
        """Scrapes multiple pages of products."""
        for page in range(1, max_pages + 1):
            print(f"Scraping page {page}...")
            product_links = self.get_product_links(page)
            if not product_links:
                break
            for link in product_links:
                product = self.extract_product_details(link)
                self.data.append(product.to_dict())
                print(product.to_dict())

    def save_to_csv(self, filename="ebay_products.csv"):
        """Saves the scraped data to a CSV file."""
        df = pd.DataFrame(self.data)
        df.to_csv(filename, index=False)
        print(f"Data saved to {filename}")

    def quit(self):
        """Closes the web driver."""
        self.driver.quit()


# Main Execution
if __name__ == "__main__":
    BASE_URL = "https://www.ebay.com/b/Cell-Phones-Smartphones/9355/bn_320094?LH_ItemCondition=1000&mag=1"
    scraper = eBayScraper(BASE_URL)
    scraper.scrape_pages(max_pages=2)
    scraper.save_to_csv()
    scraper.quit()
