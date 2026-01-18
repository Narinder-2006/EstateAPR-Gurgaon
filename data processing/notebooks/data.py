from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import pandas as pd
import time
import json
from datetime import datetime

class MagicbricksSeleniumScraper:
    def __init__(self, headless=False):
        """Initialize Selenium WebDriver"""
        self.base_url = "https://www.magicbricks.com/property-for-sale/residential-real-estate"
        self.setup_driver(headless)
        
    def setup_driver(self, headless):
        """Setup Chrome driver with options"""
        chrome_options = Options()
        
        if headless:
            chrome_options.add_argument('--headless')
        
        # Anti-detection options
        chrome_options.add_argument('--disable-blink-features=AutomationControlled')
        chrome_options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36')
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--window-size=1920,1080')
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option('useAutomationExtension', False)
        
        self.driver = webdriver.Chrome(options=chrome_options)
        self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        self.wait = WebDriverWait(self.driver, 20)
        
        print("✅ Chrome driver initialized successfully")
    
    def get_text_safe(self, element):
        """Safely get text from element"""
        try:
            return element.text.strip() if element else ''
        except:
            return ''
    
    def get_attribute_safe(self, element, attr):
        """Safely get attribute from element"""
        try:
            return element.get_attribute(attr) if element else ''
        except:
            return ''
    
    def parse_property_card(self, card):
        """Parse individual property card"""
        try:
            data = {}
            
            # Get all text content first
            data['raw_html'] = card.get_attribute('outerHTML')
            data['raw_text'] = self.get_text_safe(card)
            
            # Property ID
            data['property_id'] = self.get_attribute_safe(card, 'data-id')
            
            # Title/Society Name
            try:
                title = card.find_element(By.CSS_SELECTOR, 'h2')
                data['title'] = self.get_text_safe(title)
            except:
                data['title'] = ''
            
            # Property Type
            try:
                prop_type = card.find_element(By.CSS_SELECTOR, 'span.mb-srp__card__summary__property-type')
                data['property_type'] = self.get_text_safe(prop_type)
            except:
                data['property_type'] = ''
            
            # Location
            try:
                location = card.find_element(By.CSS_SELECTOR, 'span.mb-srp__card__summary--value')
                data['location'] = self.get_text_safe(location)
            except:
                data['location'] = ''
            
            # Price
            try:
                price = card.find_element(By.CSS_SELECTOR, 'div.mb-srp__card__price--amount')
                data['price'] = self.get_text_safe(price)
            except:
                data['price'] = ''
            
            # Price per sqft
            try:
                price_sqft = card.find_element(By.CSS_SELECTOR, 'div.mb-srp__card__price--size')
                data['price_per_sqft'] = self.get_text_safe(price_sqft)
            except:
                data['price_per_sqft'] = ''
            
            # Summary items (BHK, Bathroom, Area, Floor, etc.)
            summary_items = []
            try:
                summaries = card.find_elements(By.CSS_SELECTOR, 'div.mb-srp__card__summary--list')
                for summary in summaries:
                    summary_items.append(self.get_text_safe(summary))
            except:
                pass
            data['summary'] = ' | '.join(summary_items)
            
            # Description
            try:
                desc = card.find_element(By.CSS_SELECTOR, 'div.mb-srp__card__desc')
                data['description'] = self.get_text_safe(desc)
            except:
                data['description'] = ''
            
            # Amenities
            try:
                amenities = card.find_element(By.CSS_SELECTOR, 'div.mb-srp__card__amenities')
                data['amenities'] = self.get_text_safe(amenities)
            except:
                data['amenities'] = ''
            
            # Tags
            tag_items = []
            try:
                tags = card.find_elements(By.CSS_SELECTOR, 'span.mb-srp__card__tag')
                for tag in tags:
                    tag_items.append(self.get_text_safe(tag))
            except:
                pass
            data['tags'] = ' | '.join(tag_items)
            
            # Link
            try:
                link = card.find_element(By.CSS_SELECTOR, 'a')
                data['property_link'] = self.get_attribute_safe(link, 'href')
            except:
                data['property_link'] = ''
            
            # Builder/Developer
            try:
                builder = card.find_element(By.CSS_SELECTOR, 'div.mb-srp__card__developer')
                data['builder'] = self.get_text_safe(builder)
            except:
                data['builder'] = ''
            
            # Posted date
            try:
                posted = card.find_element(By.CSS_SELECTOR, 'div.mb-srp__card__posted')
                data['posted_date'] = self.get_text_safe(posted)
            except:
                data['posted_date'] = ''
            
            return data if data.get('title') or data.get('price') else None
            
        except Exception as e:
            print(f"Error parsing card: {str(e)}")
            return None
    
    def scrape_page(self, page_num):
        """Scrape a single page"""
        try:
            # Build URL with page number
            url = f"{self.base_url}?bedroom=&proptype=Multistorey-Apartment,Builder-Floor-Apartment,Penthouse,Studio-Apartment,Residential-House,Villa&cityName=Gurgaon&page={page_num}"
            
            print(f"Navigating to page {page_num}...", end=' ')
            self.driver.get(url)
            
            # Wait for content to load
            time.sleep(3)
            
            # Try multiple selectors for property cards
            selectors = [
                'div.mb-srp__card',
                'div[class*="mb-srp__card"]',
                'div.mb-srp__list > div',
                'div[data-id]',
                'section.mb-srp__list > div'
            ]
            
            cards = []
            for selector in selectors:
                try:
                    cards = self.driver.find_elements(By.CSS_SELECTOR, selector)
                    if cards and len(cards) > 0:
                        print(f"Found {len(cards)} cards with selector: {selector}")
                        break
                except:
                    continue
            
            if not cards:
                print("No property cards found with any selector")
                # Save page source for debugging
                with open(f'debug_page_{page_num}.html', 'w', encoding='utf-8') as f:
                    f.write(self.driver.page_source)
                print(f"Page source saved to debug_page_{page_num}.html")
                return []
            
            # Parse each card
            properties = []
            for i, card in enumerate(cards):
                prop_data = self.parse_property_card(card)
                if prop_data:
                    properties.append(prop_data)
            
            print(f"SUCCESS - Extracted {len(properties)} properties")
            return properties
            
        except Exception as e:
            print(f"Error on page {page_num}: {str(e)}")
            return []
    
    def scrape_all(self, target_count=10000, max_pages=500, delay=3.0, save_interval=25):
        """Scrape all properties"""
        all_properties = []
        page = 1
        consecutive_failures = 0
        max_consecutive_failures = 5
        
        print(f"\n{'='*70}")
        print(f"Starting Selenium Scrape")
        print(f"Target: {target_count} properties | Max pages: {max_pages}")
        print(f"{'='*70}\n")
        
        try:
            while len(all_properties) < target_count and page <= max_pages:
                properties = self.scrape_page(page)
                
                if not properties or len(properties) == 0:
                    consecutive_failures += 1
                    print(f"⚠️  Consecutive failures: {consecutive_failures}/{max_consecutive_failures}")
                    
                    if consecutive_failures >= max_consecutive_failures:
                        print(f"\n❌ Stopping after {consecutive_failures} consecutive failures")
                        break
                    
                    # Increase delay after failures
                    time.sleep(delay * 2)
                else:
                    consecutive_failures = 0
                    all_properties.extend(properties)
                    
                    print(f"📊 Progress: {len(all_properties)}/{target_count} properties")
                    
                    # Save progress
                    if page % save_interval == 0:
                        self.save_progress(all_properties, f'magicbricks_selenium_backup_page_{page}.csv')
                        print(f"💾 Backup saved (Page {page})")
                
                # Check target
                if len(all_properties) >= target_count:
                    print(f"\n✅ Target reached! {len(all_properties)} properties collected")
                    break
                
                page += 1
                time.sleep(delay)
                
                # Status update
                if page % 10 == 0:
                    print(f"\n{'='*70}")
                    print(f"Status: Page {page} | Properties: {len(all_properties)}")
                    print(f"{'='*70}\n")
            
            return pd.DataFrame(all_properties)
            
        finally:
            self.cleanup()
    
    def save_progress(self, properties, filename):
        """Save progress to CSV"""
        df = pd.DataFrame(properties)
        df.to_csv(filename, index=False, encoding='utf-8-sig')
    
    def save_final(self, df, filename='magicbricks_raw_data.csv'):
        """Save final dataset"""
        # Remove duplicates
        original = len(df)
        df = df.drop_duplicates()
        removed = original - len(df)
        
        # Save
        df.to_csv(filename, index=False, encoding='utf-8-sig')
        
        # Summary
        summary = {
            'scrape_date': datetime.now().isoformat(),
            'total_properties': len(df),
            'duplicates_removed': removed,
            'columns': list(df.columns)
        }
        
        with open('scraping_summary.json', 'w') as f:
            json.dump(summary, f, indent=2)
        
        print(f"\n{'='*70}")
        print(f"📁 Data saved: {filename}")
        print(f"📊 Properties: {len(df)}")
        print(f"🗑️  Duplicates removed: {removed}")
        print(f"{'='*70}")
        
        return df
    
    def cleanup(self):
        """Close browser"""
        try:
            self.driver.quit()
            print("\n🔒 Browser closed")
        except:
            pass

# Main execution
if __name__ == "__main__":
    print("""
    ╔════════════════════════════════════════════════════════════════╗
    ║       Magicbricks Selenium Scraper - Gurgaon Properties        ║
    ║                    Browser Automation                          ║
    ╚════════════════════════════════════════════════════════════════╝
    """)
    
    print("\n⚠️  PREREQUISITES:")
    print("   1. Install: pip install selenium pandas")
    print("   2. Download ChromeDriver: https://chromedriver.chromium.org/")
    print("   3. Add ChromeDriver to PATH or same folder as script")
    print()
    
    # Configuration
    TARGET = 7000
    MAX_PAGES = 500
    DELAY = 3.0
    SAVE_INTERVAL = 25
    HEADLESS =False  # Set True to run without opening browser window
    
    print(f"Configuration:")
    print(f"  Target: {TARGET} properties")
    print(f"  Max Pages: {MAX_PAGES}")
    print(f"  Delay: {DELAY}s")
    print(f"  Headless: {HEADLESS}")
    print()
    
    input("Press Enter to start... (Ctrl+C to cancel)")
    print()
    
    try:
        scraper = MagicbricksSeleniumScraper(headless=HEADLESS)
        
        df = scraper.scrape_all(
            target_count=TARGET,
            max_pages=MAX_PAGES,
            delay=DELAY,
            save_interval=SAVE_INTERVAL
        )
        
        if len(df) > 0:
            scraper.save_final(df)
            
            print("\n📈 Preview:")
            print(df.head())
            print(f"\n📊 Shape: {df.shape}")
            print("\n✅ Scraping completed successfully!")
            print("➡️  Next: Run the cleaning script")
        else:
            print("\n❌ No data collected")
            print("Check debug_page_*.html files for website structure")
            
    except KeyboardInterrupt:
        print("\n\n⚠️  Scraping interrupted by user")
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()