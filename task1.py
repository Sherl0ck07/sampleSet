import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import logging
import time

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def fetch_instagram_latest_post(username="bbcnews"):
    """
    Fetch the latest Instagram post's caption and image URL from a given username.
    
    Parameters:
        username (str): Instagram handle of the account (default is 'bbcnews').
    
    Returns:
        dict: A dictionary with 'caption' and 'image_url' keys, or None if failed.
    """
    url = f"https://www.instagram.com/{username}/"
    
    # Setup Chrome options
    options = Options()
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    
    try:
        driver = uc.Chrome(options=options)
        driver.get(url)
        logging.info(f"Accessing Instagram profile: {url}")
        
        # Wait for page load
        time.sleep(5)
        wait = WebDriverWait(driver, 10)

        # Bypass login popup
        try:
            login_prompt = wait.until(
                EC.presence_of_element_located((By.XPATH, "/html/body/div[5]/div[2]/div/div/div[1]/div/div[2]/div/div/div/div/div[2]/div/div[1]"))
            )
            login_prompt.click()
            logging.info("Login prompt avoided ✅")
        except:
            logging.info("Login box did NOT appear ❌")

        # Extract latest post URL
        try:
            latest_post = wait.until(
                EC.presence_of_element_located((By.XPATH, "//article//a"))
            )
            latest_post_href = latest_post.get_attribute("href")
            logging.info(f"Latest Post URL: {latest_post_href}")
            driver.get(latest_post_href)
            time.sleep(3)
        except Exception as e:
            logging.error(f"Error fetching post URL: {e}")
            return None

        # Extract latest post image URL
        try:
            latest_post_img = wait.until(
                EC.presence_of_element_located((By.XPATH, "//article//img[contains(@class, 'x5yr21d')]"))
            )
            img_url = latest_post_img.get_attribute("src")
            logging.info(f"Latest Post Image URL: {img_url}")
        except Exception as e:
            logging.error(f"Error fetching image: {e}")
            img_url = None

        # Extract caption text
        try:
            caption_element = wait.until(
                EC.presence_of_element_located((By.XPATH, "/html/body/div[1]/div/div/div[2]/div/div/div[1]/div[1]/div[1]/section/main/div[2]/div[1]/article/div/div[2]/div/div[2]/div[1]/ul/div[1]/li/div/div/div[2]/div[1]/h1"))
            )
            caption_text = caption_element.text
            logging.info(f"Caption: {caption_text}")
        except Exception as e:
            logging.error(f"Error fetching caption: {e}")
            caption_text = None

        # Close driver
        driver.quit()

        return {"caption": caption_text, "image_url": img_url}
    
    except Exception as e:
        logging.error(f"Unexpected error: {e}")
        return None

if __name__ == "__main__":
    result = fetch_instagram_latest_post()
    if result:
        print(f"Caption: {result['caption']}")
        print(f"Image URL: {result['image_url']}")
    else:
        print("Failed to fetch Instagram post.")