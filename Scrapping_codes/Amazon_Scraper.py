from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd


class Product:
    """Represents a single product with its attributes."""
    def __init__(self):
        self.image_link = None
        self.brand = None
        self.model = None
        self.product_type = "Smartphone"
        self.name = None
        self.company = "Amazon"
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
            "product_image_link": self.image_link,
            "Brand": self.brand,
            "Model": self.model,
            "product_type": self.product_type,
            "product_name": self.name,
            "company_name": self.company,
            "seller_name": self.seller_name,
            "price_before_promotion": self.price_before,
            "price_after_promotion": self.price_after,
            "amount_promotion": self.amount_promotion,
            "promotion_percent": self.promotion_percent,
            "highlights_or_description": self.highlights,
            "overall_rating": self.overall_rating,
            "number_of_ratings": self.num_ratings,
            "color_name": self.color,
            "screen_size": self.screen_size,
            "model_number": self.model_number,
            "battery_size": self.battery_size,
            "processor_version": self.processor,
            "graphics_processor_version": self.graphics_processor,
            "internal_memory": self.internal_memory,
            "RAM_size": self.ram_size
        }


class AmazonScraper:
    """Scrapes Amazon for smartphone listings."""
    def __init__(self, base_url):
        self.base_url = base_url
        self.driver = webdriver.Chrome()
        self.data = []

    def get_product_links(self, page_number):
        """Fetches product links from the current page."""
        url = f"{self.base_url}&page={page_number}"
        try:
            self.driver.get(url)
            product_elements = WebDriverWait(self.driver, 10).until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".s-main-slot .s-result-item"))
            )
            links = []
            for element in product_elements:
                try:
                    link = element.find_element(By.CLASS_NAME, "a-link-normal").get_attribute("href")
                    if link:
                        links.append(link)
                except Exception:
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
                By.ID, "productTitle"
            ).text.strip()
        except Exception:
            product.name = None

        try:
            product.image_link = self.driver.find_element(
                By.ID, "imgTagWrapperId"
            ).find_element(By.TAG_NAME, "img").get_attribute("src")
        except Exception:
            product.image_link = None

        try:
            product.price_after = self.driver.find_element(
                By.CSS_SELECTOR, ".a-price .a-offscreen"
            ).text.strip()
        except Exception:
            product.price_after = None

        try:
            product.overall_rating = self.driver.find_element(
                By.ID, "acrPopover"
            ).get_attribute("title")
        except Exception:
            product.overall_rating = None

        try:
            product.num_ratings = self.driver.find_element(
                By.ID, "acrCustomerReviewText"
            ).text.strip()
        except Exception:
            product.num_ratings = None

        try:
            product_details = self.driver.find_element(By.ID, "productDetails_techSpec_section_1")
            rows = product_details.find_elements(By.TAG_NAME, "tr")
            for row in rows:
                key = row.find_element(By.TAG_NAME, "th").text.strip()
                value = row.find_element(By.TAG_NAME, "td").text.strip()
                if key == "Brand":
                    product.brand = value
                elif key == "Model Name":
                    product.model = value
                elif key == "Screen Size":
                    product.screen_size = value
                elif key == "Color":
                    product.color = value
                elif key == "RAM":
                    product.ram_size = value
                elif key == "Storage Capacity":
                    product.internal_memory = value
                elif key == "Processor":
                    product.processor = value
                elif key == "Battery":
                    product.battery_size = value
        except Exception:
            pass

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

    def save_to_csv(self, filename="amazon_products.csv"):
        """Saves the scraped data to a CSV file."""
        df = pd.DataFrame(self.data)
        df.to_csv(filename, index=False)
        print(f"Data saved to {filename}")

    def quit(self):
        """Closes the web driver."""
        self.driver.quit()


# Main Execution
if __name__ == "__main__":
    # Force Amazon language to English
    BASE_URL = "https://www.amazon.eg/s?k=smartphones&language=en_AE"
    scraper = AmazonScraper(BASE_URL)
    scraper.scrape_pages(max_pages=2)
    #scraper.save_to_csv()
    scraper.quit()