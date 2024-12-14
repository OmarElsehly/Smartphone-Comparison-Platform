from bs4 import BeautifulSoup
import requests
import pandas as pd
from concurrent.futures import ThreadPoolExecutor
from abc import ABC, abstractmethod

# Base class for Scraper
class Scraper(ABC):
    def __init__(self, base_url, session=None):
        self.base_url = base_url
        self.session = session or requests.Session()
    
    @abstractmethod
    def extract_links(self, url):
        pass

    @abstractmethod
    def extract_product_info(self, url):
        pass


# Subclass for Product Scraping
class ProductScraper(Scraper):
    def extract_links(self, url):
        """Extract product links from a given page."""
        response = self.session.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')
        div_block = soup.find('div', class_='sc-61baf88b-7 dRkNeo grid')
        site = 'https://noon.com'
        return [
            site + a_tag.get('href')
            for span_block in div_block.find_all('span')
            for a_tag in span_block.find_all('a') if a_tag.get('href')
        ] if div_block else []

    def extract_product_info(self, url):
        """Extract detailed product information from a given link."""
        response = self.session.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')

        def get_text_or_none(parent, selector, attr=None):
            """Utility to safely extract text or attributes."""
            element = parent.select_one(selector)
            return element.get(attr) if attr and element else (element.get_text(strip=True) if element else None)

        # Extract information
        product_data = {
            'Image Link': get_text_or_none(soup, 'meta[property="og:image"]', 'content'),
            'Product Type': get_text_or_none(soup, 'div.sc-54ed93c4-2.ijtKtO div:last-child'),
            'Seller Name': get_text_or_none(soup, 'div.sc-b14a1e88-0.bAFCnA span.allOffers'),
            'Company Name': get_text_or_none(soup, 'div.sc-de5a1c50-16.glXiuW'),
            'Product Description': get_text_or_none(soup, 'div.sc-de5a1c50-2.jHemIn h1.sc-de5a1c50-17.dJnofv'),
            'Model Number': get_text_or_none(soup, 'div.sc-de5a1c50-12.hPnfrq .modelNumber'),
            'Price Before Promotion': get_text_or_none(soup, 'div.sc-14650a92-3.clxNMW .priceWas').replace('EGP', '') if get_text_or_none(soup, 'div.sc-14650a92-3.clxNMW .priceWas') else None,
            'Price After Promotion': get_text_or_none(soup, 'div.sc-14650a92-0.dROEqP .priceNow').replace('EGP', '') if get_text_or_none(soup, 'div.sc-14650a92-0.dROEqP .priceNow') else None,
            'Savings': get_text_or_none(soup, 'div.sc-14650a92-0.dROEqP .priceSaving'),
            'Promotion in Percent': get_text_or_none(soup, 'div.sc-14650a92-0.dROEqP .profit'),
            'Highlights': get_text_or_none(soup, 'div.sc-97eb4126-2.oPZpQ ul'),
            'Colour Name': self.extract_table_value(soup, 'Colour Name'),
            'Rating': get_text_or_none(soup, 'div.sc-9cb63f72-2.dGLdNc'),
            'Number of Ratings': get_text_or_none(soup, 'span.sc-9cb63f72-5.DkxLK'),
            'Screen Size': self.extract_table_value(soup, 'Screen Size'),
            'Internal Memory': self.extract_table_value(soup, 'Internal Memory'),
            'Battery Size': self.extract_table_value(soup, 'Battery Size'),
            'RAM Size': self.extract_table_value(soup, 'RAM Size'),
            'Processor Version': self.extract_table_value(soup, 'Processor Version'),
            'Graphics Processor Version': self.extract_table_value(soup, 'Graphics Processor Version'),
        }
        return product_data

    def extract_table_value(self, soup, attribute_name):
        """Extract a specific attribute from a table."""
        parent_div = soup.find('div', class_='sc-966c8510-2 dROUvm')
        table_body = parent_div.find('tbody') if parent_div else None
        if table_body:
            for row in table_body.find_all('tr'):
                cells = row.find_all('td')
                if cells and attribute_name in cells[0].get_text(strip=True):
                    return cells[1].get_text(strip=True) if len(cells) > 1 else None
        return None


# Main Execution
if __name__ == '__main__':
    base_url = 'https://www.noon.com/egypt-en/electronics-and-mobiles/?limit=30&page={}&sort%5Bby%5D=popularity&sort%5Bdir%5D=desc'
    scraper = ProductScraper(base_url)

    # Collect all product links
    all_links = []
    for page_num in range(1, 5):
        page_url = base_url.format(page_num)
        all_links.extend(scraper.extract_links(page_url))

    # Fetch product details using threads
    with ThreadPoolExecutor(max_workers=10) as executor:
        results = list(executor.map(scraper.extract_product_info, all_links))

    # Save results to Excel and CSV
    df = pd.DataFrame(results)
    df.to_excel('Final_Products.xlsx', index=False)
    df.to_csv('Final_Products.csv', index=False)
    print("Data scraping completed and saved!")
