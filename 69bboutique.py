import pandas as pd
import requests
from bs4 import BeautifulSoup

class Scraper69bboutique:
    """ 
    A web scraper for 69bboutique.com to extract product information.

    Attributes:
    - base_url (str): The base URL of the website.
    - total_pages (int): Total number of pages to scrape.
    - products (list): A list to store scraped product information.

    Methods:
    - get_total_pages(): Retrieves the total number of pages from the website pagination.
    - scrape(): Initiates the scraping process for all pages.
    - scrape_page(page): Scrapes product information from a specific page.
    - scrape_product(item): Scrapes detailed product information from a product page.
    - get_product_name(soup): Extracts the product name from a product page.
    - get_product_price(soup): Extracts the product price from a product page.
    - get_product_sizes(soup): Extracts available sizes of the product from a product page.
    - get_collection_name(soup): Extracts the collection name of the product from a product page.
    - get_about_the_collection(soup): Extracts the description of the collection from a product page.
    - get_fabric_type(soup): Extracts the fabric type of the product from a product page.
    - to_dataframe(): Converts the scraped data into a pandas DataFrame.
    """

    def __init__(self):
        self.base_url = 'https://69bboutique.com/collections/new-in-1?page={}'
        self.total_pages = self.get_total_pages()
        self.products = []


    def get_total_pages(self):
        """ 
        Returns the total number of pages available on the website.

        This method sends a GET request to the homepage of the website, parses the content using BeautifulSoup,
        and extracts the total page number from the HTML element representing the current page.
        The total page number is obtained by extracting the last part of the page information text.
    
        Returns:
            int: The total number of pages available on the website.
        """
        responce = requests.get('https://69bboutique.com/collections/new-in-1?page=1')
        soup = BeautifulSoup(responce.content, 'lxml')
        pagination_div = soup.find('div', class_='pagination')
        if pagination_div:
            total_pages = pagination_div.find_all('a')[-2].text.strip()
            return int(total_pages)
        else:
            return 1

    def scrape(self):
        for page in range(1, self.total_pages + 1):
            self.scrape_page(page)

    def scrape_page(self, page):
        """ 
        Scrapes product information from a specific page of the website.

        This method retrieves product items from the specified page URL, parses their content,
        and delegates the scraping of each product to the 'scrape_product' method.

        Args:
            page (int): The page number to scrape.

        Returns:
            None
        """
        url = self.base_url.format(page)
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'lxml')
        product_grid = soup.find('div', class_='grid grid--uniform')
        product_items = product_grid.find_all('div', attrs={'data-aos': 'fade-up'})

        for item in product_items:
            self.scrape_product(item)

    def scrape_product(self, item):
        """ 
        Scrapes product details from a product page.

        Extracts product name, price, available sizes, collection name, collection description, and fabric type from the given product item.

        Args:
            item (BeautifulSoup Tag): Tag representing a product item.

        Returns:
            None. Extracted product details are appended to the 'products' list.
        """
        link_end = item.a.get('href')
        product_url = 'https://69bboutique.com' + link_end
        product_soup = BeautifulSoup(requests.get(product_url).content, 'lxml')

        product_name = self.get_product_name(product_soup)
        product_price = self.get_product_price(product_soup)
        sizes = self.get_product_sizes(product_soup)
        collection_name = self.get_collection_name(product_soup)
        about_the_collection = self.get_about_the_collection(product_soup)
        fabric_type = self.get_fabric_type(product_soup)

        self.products.append([product_name,product_price, sizes, collection_name, about_the_collection, fabric_type])

    @staticmethod
    def get_product_name(soup):
        """
        Extracts the name of the product from the product page.

        This static method receives a BeautifulSoup object representing the product page.
        It finds and returns the name of the product by locating the appropriate HTML element.

        Args:
            soup (BeautifulSoup object): Parsed HTML content of the product page.

        Returns:
            str: The name of the product.
        """
        return soup.find('h1', class_='product__title').text.strip()

    @staticmethod
    def get_product_price(soup):
        """
        Extracts the price of the product from the product page.

        This static method receives a BeautifulSoup object representing the product page.
        It finds and returns the price of the product by locating the appropriate HTML element.

        Args:
            soup (BeautifulSoup object): Parsed HTML content of the product page.

        Returns:
            str: The price of the product.
        """
        return soup.find('div', class_='product__price h2--accent').text.strip().replace('£', '')
    
    @staticmethod
    def get_product_sizes(soup):
        """ 
        Extracts the available sizes of the product from the product page.

        This static method receives a BeautifulSoup object representing the product page.
        It finds and returns the available sizes of the product by locating the appropriate HTML element.

        Args:
            soup (BeautifulSoup object): Parsed HTML content of the product page.

        Returns:
            list or None: List of available sizes or None if not found.
        """
        size_select = soup.find('select', id='SingleOptionSelector-0')
        if size_select:
            return [option.text.strip() for option in size_select.find_all('option')]
        return None
    
    @staticmethod
    def get_collection_name(soup):
        """
        Extracts the collection name of the product from the product page.

        This static method receives a BeautifulSoup object representing the product page.
        It finds and returns the collection name of the product by locating the appropriate HTML element.

        Args:
            soup (BeautifulSoup object): Parsed HTML content of the product page.

        Returns:
            str: The collection name of the product.
        """
        return soup.find('a', class_='border-bottom-link').text.strip()
    
    @staticmethod
    def get_about_the_collection(soup):
        """
        Extracts the description of the collection from the product page.

        This static method receives a BeautifulSoup object representing the product page.
        It finds and returns the description of the collection by locating the appropriate HTML element.

        Args:
            soup (BeautifulSoup object): Parsed HTML content of the product page.

        Returns:
            str or None: Description of the collection or None if not found.
        """
        try:
            accordion_contents = soup.find_all('div', class_='rte accordion-content accordion-content--3')
            return accordion_contents[1].text.strip().replace('\n\ufeffShop Our Collection', '') if len(accordion_contents) > 1 else None
        except (IndexError, AttributeError):
            return None

    @staticmethod
    def get_fabric_type(soup):
        """
        Extracts the fabric type of the product from the product page.

        This static method receives a BeautifulSoup object representing the product page.
        It finds and returns the fabric type of the product by locating the appropriate HTML element.

        Args:
            soup (BeautifulSoup object): Parsed HTML content of the product page.

        Returns:
            str or None: The fabric type of the product or None if not found.
        """
        try:
            fabric_type_div = soup.find('div', class_='custom-product-label')
            return fabric_type_div.text.strip() if fabric_type_div else None
        except AttributeError:
            return None

    def to_dataframe(self):
        return pd.DataFrame(self.products, columns=["Product Name", "Price (£)", "Available Sizes", "Collection", "Collection Description", "Fabric Type"])

scraper = Scraper69bboutique()
scraper.scrape()
df = scraper.to_dataframe()
df.head()
