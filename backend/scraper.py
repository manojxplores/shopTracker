from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from amazoncaptcha import AmazonCaptcha

def solve_captcha(driver):
    try:
        captcha_img = driver.find_element(By.TAG_NAME, "img").get_attribute("src")
        captcha = AmazonCaptcha.fromlink(captcha_img)
        solution = captcha.solve()

        input_ele = driver.find_element(By.NAME, "field-keywords")
        input_ele.send_keys(solution, Keys.ENTER)
    except Exception as e:
        print(f"Error solving CAPTCHA : {e}")

def get_product(URL):
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_experimental_option("detach", True)
    driver = webdriver.Chrome(chrome_options)
    try:
        driver.get(URL)
        search_product = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.ID, "centerCol"))
        )
        title_ele = search_product.find_element(By.ID, value="productTitle")
        price_ele = search_product.find_element(By.CLASS_NAME, value="a-price-whole")
        return {"title" : title_ele.text, "price" : price_ele.text, "product_url" : URL}

    except Exception as e:
        if "captcha" in driver.page_source:
            solve_captcha(driver)
            return get_product(URL)
        else:
            raise e
    finally:
        driver.quit()


