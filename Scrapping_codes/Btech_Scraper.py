from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import undetected_chromedriver as uc
import pandas as pd
import re
from concurrent.futures import ThreadPoolExecutor
import threading


class MobileScraper:
    def __init__(self, url, target_models, max_workers=5):
        """
        Initializes the MobileScraper with the target URL and models.
        
        Args:
        - url (str): The main URL to scrape.
        - target_models (list): List of target mobile model names.
        - max_workers (int): Number of threads for concurrent processing.
        """
        self.url = url
        self.target_models = target_models
        self.max_workers = max_workers
        self.mobile_data = []
        self.driver_lock = threading.Lock()
        self.driver = self._initialize_driver()

    def _initialize_driver(self):
        """Initialize the Chrome WebDriver with options."""
        options = uc.ChromeOptions()
        options.headless = True
        return uc.Chrome(options=options)

    def scrape_main_page(self):
        """Scrape the main page and filter mobiles based on target models."""
        self.driver.get(self.url)
        soup = BeautifulSoup(self.driver.page_source, "lxml")
        mobile_containers = soup.find_all(
            "div", {"class": "product-item-view", "data-bind": "attr:{id:'product_view_'+$index()}"}
        )
        print(f"Total mobiles found: {len(mobile_containers)}")

        selected_mobiles = []
        for mobile in mobile_containers:
            mobile_name = mobile.find('h2', {"class": "plpTitle"}).text.strip()
            if any(model.lower() in mobile_name.lower() for model in self.target_models):
                selected_mobiles.append({
                    "name": mobile_name,
                    "image": mobile.find('img', {"class": "product-image-photo"})['src'],
                    "url": mobile.find('a', {"class": "listingWrapperSection"})['href'],
                    "price_before": mobile.find('span', {"class": "price-wrapper", "data-bind": "text: $data.final_regular_price"}).text.strip() if mobile.find('span', {"class": "price-wrapper", "data-bind": "text: $data.final_regular_price"}) else None,
                    "price_after": mobile.find('span', {"class": "price-wrapper", "data-bind": "text: $data.final_minimum_price"}).text.strip() if mobile.find('span', {"class": "price-wrapper", "data-bind": "text: $data.final_minimum_price"}) else None,
                })
        print(f"Selected mobiles: {len(selected_mobiles)}")
        return selected_mobiles

    def _scrape_mobile_details(self, mobile):
        """Scrape additional details for a single mobile."""
        try:
            with self.driver_lock:
                self.driver.get(mobile['url'])
                WebDriverWait(self.driver, 10).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "body")))
                mobile_soup = BeautifulSoup(self.driver.page_source, "lxml")

            # Extract additional details
            rating = mobile_soup.find('div', {"class": "top-avg-rating-count"})
            num_ratings = mobile_soup.find('span', {"class": "review-count"})

            color = mobile_soup.find("td", {"class": "col data color_val", "data-th": "Color"})
            screen_info = mobile_soup.find_all('div', {"class": "detail"})[2].text.strip()[8:] if len(mobile_soup.find_all('div', {"class": "detail"})) > 2 else None
            resolution_match = re.search(r"\b\d{3,4}\s*x\s*\d{3,4}\b", screen_info or "")
            resolution = resolution_match.group(0) if resolution_match else None

            storage = mobile_soup.find("td", {"class": "col data storage_capacity_val", "data-th": "Storage Capacity"})
            battery = mobile_soup.find("td", {"class": "col data battery_capacity1_val", "data-th": "Battery Capacity"})
            processor = mobile_soup.find("td", {"class": "col data chipset_manufacturer_val", "data-th": "Processor Manufacturer"})
            ram = mobile_soup.find("td", {"class": "col data ram_val", "data-th": "RAM"})

            return {
                "Name": mobile['name'],
                "Image": mobile['image'],
                "Price Before Promotion": mobile['price_before'],
                "Price After Promotion": mobile['price_after'],
                "Rating": rating.text.strip() if rating else None,
                "Number of Ratings": num_ratings['data-review-count'] if num_ratings else None,
                "Color": color.text.strip() if color else None,
                "Resolution": resolution,
                "Storage": storage.text.strip() if storage else None,
                "Battery": battery.text.strip() if battery else None,
                "Processor": processor.text.strip() if processor else None,
                "RAM": ram.text.strip() if ram else None,
                "URL": mobile['url']
            }
        except Exception as e:
            print(f"Error processing mobile: {e}")
            return None

    def scrape_mobile_details(self, selected_mobiles):
        """Scrape details for all selected mobiles concurrently."""
        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            results = executor.map(self._scrape_mobile_details, selected_mobiles)
            self.mobile_data = [result for result in results if result]

    def to_dataframe(self):
        """Convert the scraped data to a pandas DataFrame."""
        return pd.DataFrame(self.mobile_data)

    def close_driver(self):
        """Close the Selenium WebDriver."""
        self.driver.quit()


# Main execution
if __name__ == "__main__":
    TARGET_MODELS = [
        "Apple Iphone 11", "Apple Iphone 12", "Apple Iphone 13", "Apple Iphone 14", "Apple Iphone 15",
        "Samsung Galaxy S21 Ultra", "Samsung Galaxy S22 Ultra", "Samsung Galaxy S23 Ultra", "Samsung Galaxy S24 Ultra"
    ]
    URL = "https://btech.com/en/moblies/mobile-phones-smartphones/smartphones.html"

    scraper = MobileScraper(URL, TARGET_MODELS)
    try:
        selected_mobiles = scraper.scrape_main_page()
        scraper.scrape_mobile_details(selected_mobiles)
        df = scraper.to_dataframe()
        print(df.head())
    finally:
        scraper.close_driver()
