import os
import requests
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.action_chains import ActionChains

# 第一步：通过API密钥验证登录成功
def login_with_api_key(login_url="https://hub.weirdhost.xyz/auth/login"):
    """
    使用 API 密钥通过 POST 请求进行登录，获取登录认证的令牌。
    """
    # 从环境变量获取 API 密钥
    api_key = os.environ.get('API_KEY')
    
    if not api_key:
        print("错误: 缺少 API_KEY 环境变量。请设置 API_KEY。")
        return None

    # 创建 API 请求头
    headers = {
        'Authorization': f'Bearer {api_key}',  # 使用 Bearer Token 进行认证
        'Content-Type': 'application/json'
    }

    # 发送 POST 请求进行登录验证
    try:
        response = requests.post(login_url, headers=headers)
        if response.status_code == 200:
            print("登录成功。")
            return response.json()  # 假设返回 JSON 中包含用户的认证信息或 token
        else:
            print(f"错误: 登录失败，状态码: {response.status_code}, 响应: {response.text}")
            return None
    except requests.RequestException as e:
        print(f"请求发生异常: {e}")
        return None


# 第二步：通过 Selenium 模拟点击 '시간추가' 按钮增加服务时间
def add_server_time_via_button(server_url="https://hub.weirdhost.xyz/server/0f4424f2"):
    """
    登录成功后，通过 Selenium 控制浏览器点击 '시간추가' 按钮增加服务器时间。
    """
    # 设置 Chrome 浏览器选项
    options = Options()
    options.add_argument("--headless")  # 如果不需要打开浏览器界面，可以使用 headless 模式

    # 初始化 WebDriver
    driver = webdriver.Chrome(service=Service('path_to_chromedriver'), options=options)

    try:
        # 访问服务器页面
        driver.get(server_url)
        print("正在访问服务器页面...")

        # 找到并点击 '시간추가' 按钮
        add_time_button = driver.find_element(By.XPATH, "//span[contains(text(), '시간추가')]")
        ActionChains(driver).move_to_element(add_time_button).click().perform()
        print("点击 '시간추가' 按钮，增加服务器时间。")

        time.sleep(2)  # 等待操作完成

        # 验证操作是否成功（此部分可以根据实际情况调整）
        if "시간이 추가되었습니다" in driver.page_source:
            print("服务器时间成功增加。")
            return True
        else:
            print("无法增加服务器时间，未检测到成功提示。")
            return False
    except Exception as e:
        print(f"发生错误: {e}")
        return False
    finally:
        driver.quit()


if __name__ == "__main__":
    print("开始执行任务...")

    # 步骤 1: 使用 API 密钥登录验证
    login_info = login_with_api_key()

    if login_info:
        # 步骤 2: 登录成功后，通过 Selenium 点击 '시간추가' 按钮增加时间
        success = add_server_time_via_button()

        if success:
            print("任务执行成功。")
            exit(0)
        else:
            print("任务执行失败：无法增加服务器时间。")
            exit(1)
    else:
        print("任务执行失败：登录失败。")
        exit(1)
