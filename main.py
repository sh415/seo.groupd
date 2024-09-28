import uvicorn
import os
import time
import random
import pyperclip
import requests
from random import *
from typing import List
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import WebDriverException
from webdriver_manager.chrome import ChromeDriverManager

app = FastAPI()

# CORS 미들웨어 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],  # 모든 HTTP 메소드 허용
    allow_headers=["*"],  # 모든 헤더 허용
)

# @app.post("/neighbors") 관련 메소드
def naver_login(driver, id, pwd):
    try:
        driver.get('https://nid.naver.com/nidlogin.login?/')
        time.sleep(3.0)

        input_id = driver.find_element(By.CSS_SELECTOR, '#id')
        input_id.click()
        pyperclip.copy(id)
        input_id.send_keys(Keys.CONTROL, 'v')
        time.sleep(2.0)

        input_pw = driver.find_element(By.CSS_SELECTOR, '#pw')
        input_pw.click()
        pyperclip.copy(pwd)
        input_pw.send_keys(Keys.CONTROL, 'v')
        time.sleep(2.0)

        input_sw = driver.find_element(By.CSS_SELECTOR, '.switch_checkbox')
        driver.execute_script("arguments[0].click();", input_sw)
        time.sleep(2.0)

        btn_login = driver.find_element(By.CSS_SELECTOR, '.btn_login')
        btn_login.click()
        time.sleep(3.0)

        return True
    
    except Exception as e:
        print(e)

# def new_device(driver):
#     try:
#         button_new_device = driver.find_element(By.ID, 'new.save')
#         button_new_device.click()
#         time.sleep(uniform(3.0, 5.0))

#         return True
    
#     except Exception as e:
#         print('new_device error', e)
#         return False

def switch_mainframe(driver, idx, comment):
    try:
        if len(driver.window_handles) > 1:
            driver.close()
            time.sleep(1.0)
            driver.switch_to.window(driver.window_handles[-1])
        else:
            driver.switch_to.window(driver.window_handles[-1])

        wait = WebDriverWait(driver, 10)
        frame = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#mainFrame')))
        driver.switch_to.frame(frame)
        framebody = driver.find_element(By.CSS_SELECTOR, 'body')

        currentURL = driver.current_url
        logNo = currentURL.split('/')[-1]

        sympathyFrame = framebody.find_element(By.CSS_SELECTOR, f'#sympathyFrm{logNo}')
        driver.switch_to.frame(sympathyFrame)
        sympathyFramebody = driver.find_element(By.CSS_SELECTOR, 'body')

        listSympathy = sympathyFramebody.find_element(By.CSS_SELECTOR, '.list_sympathy')
        items = listSympathy.find_elements(By.CSS_SELECTOR, '.item')

        item = items[idx]
        breaker = make_buddy(driver, item, comment)

        return breaker

    except Exception as e:
        print(e)

def make_buddy_save(msg):
    try:
        req = {'msg': msg} 
        response = requests.post("https://groupd-support.net/buddy/log", data = req)

    except Exception as e:
        print(e)

def make_buddy(driver, item, comment):
    try:
        ico = item.find_element(By.CSS_SELECTOR, '.ico')
        if ico.text == '서로이웃':
            return True
        
        item.find_element(By.CSS_SELECTOR, '.aline').click()
        time.sleep(uniform(0.5, 1.0))
        driver.switch_to.window(driver.window_handles[1])
        time.sleep(uniform(0.5, 1.0))
        driver.execute_script('document.querySelector("#each_buddy_add").click();')
        time.sleep(uniform(0.2, 0.5))
        driver.execute_script('document.querySelector(`.button_next`).click();')
        time.sleep(uniform(0.5, 1.0))

        # message = random.choice(comment)
        message = choice(comment)
        script = f'let element = document.getElementById("message"); element.value = "{message}";'
        driver.execute_script(script)
        time.sleep(uniform(0.2, 0.5))

        driver.execute_script('document.querySelector(`.button_next`).click();')
        time.sleep(uniform(0.5, 1.0))
        driver.execute_script('document.querySelector(`.button_close`).click();')
        time.sleep(uniform(0.5, 1.0))

        return True

    # except Exception as e:
    #     print(e)
    except WebDriverException as e:
        print(e.msg)
        make_buddy_save(e.msg)

        substring = '더 이상 이웃을 추가할 수 없습니다.'
        if e.msg.find(substring) != -1:
            print("텍스트에 포함되어 있습니다.")
            return False
        else:
            print("텍스트에 포함되어 있지 않습니다.")
            return True

def itmes_mainframe(driver):
    try:
        if len(driver.window_handles) > 1:
            driver.close()
            time.sleep(1.0)
            driver.switch_to.window(driver.window_handles[-1])
        else:
            driver.switch_to.window(driver.window_handles[-1])

        wait = WebDriverWait(driver, 10)
        frame = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#mainFrame')))
        driver.switch_to.frame(frame)
        framebody = driver.find_element(By.CSS_SELECTOR, 'body')

        currentURL = driver.current_url
        logNo = currentURL.split('/')[-1]

        sympathyFrame = framebody.find_element(By.CSS_SELECTOR, f'#sympathyFrm{logNo}')
        driver.switch_to.frame(sympathyFrame)
        sympathyFramebody = driver.find_element(By.CSS_SELECTOR, 'body')

        listSympathy = sympathyFramebody.find_element(By.CSS_SELECTOR, '.list_sympathy')
        items = listSympathy.find_elements(By.CSS_SELECTOR, '.item')

        return len(items)
    
    except Exception as e:
        print(e)

def next_mainframe(driver):
    try:
        if len(driver.window_handles) > 1:
            driver.close()
            time.sleep(1.0)
            driver.switch_to.window(driver.window_handles[-1])
        else:
            driver.switch_to.window(driver.window_handles[-1])

        wait = WebDriverWait(driver, 10)
        frame = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#mainFrame')))
        driver.switch_to.frame(frame)
        framebody = driver.find_element(By.CSS_SELECTOR, 'body')

        currentURL = driver.current_url
        logNo = currentURL.split('/')[-1]

        sympathyFrame = framebody.find_element(By.CSS_SELECTOR, f'#sympathyFrm{logNo}')
        driver.switch_to.frame(sympathyFrame)
        driver.execute_script('document.querySelector(`#_loadNext`).click()')

        return True
    
    except Exception as e:
        print(e)
        return False

def driverQuit(driver):
    try:
        driver.quit()
    except Exception as e:
        print(e)

@app.get("/")
def read_root():
    return {"Hello": "World"}

class RequestModel_Responses(BaseModel):
    domain: str

@app.post("/responses")
# async def send_response(request_body: dict):
#     domain = request_body.get("domain")
#     return JSONResponse(status_code = 200, content = True)

async def send_response(request_body: RequestModel_Responses):
    try:
        domain = request_body.domain
        print(domain)
        return JSONResponse(status_code = 200, content = True)
    except Exception as err:
        print(err)

class seoModel(BaseModel):
    id: str
    pwd: str
    url: str
    comment: List[str]

@app.post("/seo", description="네이버 서로이웃 추가 기능입니다. [Try it out] -> 로그인 아이디, 패스워드, 포스팅 주소 (예: https://blog.naver.com/flowerweve/223084911908) 를 입력 -> [Execute]")
def blog_neighbors(model: seoModel):
    try:
        id = model.id
        pwd = model.pwd
        url = model.url
        comment = model.comment

        # options = webdriver.ChromeOptions()
        # # options.add_argument('headless')
        # # options.add_argument("no-sandbox")
        # # options.add_argument('window-size=1920x1080')
        # # options.add_argument("disable-gpu")
        # # options.add_experimental_option('excludeSwitches', ['enable-logging'])
        # driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

        options = webdriver.ChromeOptions()
        driver_path = ChromeDriverManager().install()
        correct_driver_path = os.path.join(os.path.dirname(driver_path), "chromedriver.exe")
        driver = webdriver.Chrome(service=Service(executable_path=correct_driver_path), options=options)

        naver_login(driver, id, pwd)

        # isNew = False
        # isNew = new_device(driver)
        # if (isNew):
        #     print('새로운 기기(브라우저)에서 로그인 처리')

        wait = WebDriverWait(driver, 10)

        driver.get(url)
        time.sleep(3.0)
        # driver.save_screenshot("google_screenshot.png")
        # driver.quit()

        # 메인 프레임 내부로 이동
        frame = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#mainFrame')))
        driver.switch_to.frame(frame)
        framebody = driver.find_element(By.CSS_SELECTOR, 'body')

        # SympathyBtn 클릭
        sympathyBtn = framebody.find_element(By.CSS_SELECTOR, '.bu_arr')
        sympathyBtn.click()
        time.sleep(1.0)

        # SympathyBtn이 보일 때까지 스크롤
        driver.execute_script("arguments[0].scrollIntoView({ behavior: 'smooth', block: 'end' });", sympathyBtn)

        # 현재 URL 가져오기
        currentURL = driver.current_url
        logNo = currentURL.split('/')[-1]

        # SympathyFrame 내부로 이동
        sympathyFrame = framebody.find_element(By.CSS_SELECTOR, f'#sympathyFrm{logNo}')
        driver.switch_to.frame(sympathyFrame)
        sympathyFramebody = driver.find_element(By.CSS_SELECTOR, 'body')

        # items 리스트
        listSympathy = sympathyFramebody.find_element(By.CSS_SELECTOR, '.list_sympathy')
        items = listSympathy.find_elements(By.CSS_SELECTOR, '.item')
        items = len(items)

        breaker = False
        while (items) != 0:
            items = itmes_mainframe(driver)
            for idx in range (items):
                switch_value = switch_mainframe(driver, idx, comment)
                if not switch_value:
                    breaker = True
                    break
                time.sleep(1.0)

            if (breaker):
                break
                
            next = next_mainframe(driver)
            if not next:
                break
            time.sleep(1.0)
            items = itmes_mainframe(driver)
            
        return {"message": "Success!"}

    except Exception as e:
        print(e)

    finally:
        if driver:
            driverQuit(driver)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port = 7000)