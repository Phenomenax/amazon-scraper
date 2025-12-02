import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
import urllib.parse


class Scraper:
    BASE_URL = "https://www.amazon.com.au/s?k="

    def __init__(self, query):
        ua = UserAgent()
        self.headers = {
            'User-Agent': ua.random,
            'Accept-Language': 'en-US,en;q=0.9',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Referer': 'https://www.google.com/',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'DNT': '1',
        } 
        self.query = urllib.parse.quote_plus(query)
        self.url = f"{self.BASE_URL}{self.query}"

    def fetch_page(self):
        print(f"Searching for: {self.query} on Amazon AU")
        print(f"URL: {self.url}")
        try:
            response = requests.get(self.url, headers=self.headers)
            print(f"Status Code: {response.status_code}")
            
            if response.status_code != 200:
                print("Failed to retrieve page.")
                return None

            if "api-services-support@amazon.com" in response.text or "captcha" in response.text.lower():
                print("Blocked by Amazon (CAPTCHA or anti-bot).")
                # Save html for debugging
                with open("debug_blocked.html", "w", encoding="utf-8") as f:
                    f.write(response.text)
                return None

            return response.content
        
        except requests.exceptions.RequestException as e:
            print(f"Error fetching data: {e}")
            return None

    def parse_results(self, html_content):
        if not html_content:
            return []
            
        soup = BeautifulSoup(html_content, 'html.parser')
        results = []
        
        # Debug: Print title of page
        print(f"Page Title: {soup.title.string if soup.title else 'No title'}")

        # Save debug HTML unconditionally for inspection
        with open("debug.html", "w", encoding="utf-8") as f:
            f.write(soup.prettify())

        items = soup.select('div[data-component-type="s-search-result"]')
        print(f"Found {len(items)} items on page.")
        
        for item in items:
            # Selectors based on mobile/modern view analysis
            title_element = item.select_one('div[data-cy="title-recipe"] h2 span')
            price_element = item.select_one('.a-price .a-offscreen')
            link_element = item.select_one('div[data-cy="title-recipe"] a')
            
            if title_element and price_element and link_element:
                title = title_element.get_text().strip()
                
                # Extract price string (e.g., "AUD 18.10" or "$18.10")
                price_text = price_element.get_text().strip()
                # Remove currency symbols and non-numeric chars except dot
                price_clean = ''.join(c for c in price_text if c.isdigit() or c == '.')
                
                try:
                    price = float(price_clean)
                except ValueError:
                    continue
                
                link = "https://www.amazon.com.au" + link_element['href']
                
                results.append({
                    'title': title,
                    'price': price,
                    'link': link
                })
        
        return results

    def scrape(self):
        html_content = self.fetch_page()
        if not html_content:
            return []
        
        products = self.parse_results(html_content)
        
        # Sort by price and take top 5
        products.sort(key=lambda x: x['price'])
        return products[:5]

def main():
    query = input("Enter product name to search: ")
    if not query:
        print("Please enter a valid product name.")
        return
    
    scraper = Scraper(query)
    results = scraper.scrape()
    
    if results:
        print(f"\nTop 5 cheapest results for '{query}':")
        for i, product in enumerate(results, 1):
            print(f"{i}. {product['title']}")
            print(f"   Price: ${product['price']:.2f}")
            print(f"   Link: {product['link']}")
            print("-" * 50)
    else:
        print("No results found.")

if __name__ == "__main__":
    main()