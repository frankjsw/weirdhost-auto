import os
import time
import requests
from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeoutError

def add_server_time(server_url="https://hub.weirdhost.xyz/server/0f4424f2"):
    """
    通过 API Key 验证登录 hub.weirdhost.xyz 并点击 “시간추가” 按钮。
    优先使用 API_KEY 登录。
    """

    api_key = os.environ.get('API_KEY')
    if not api_key:
        print("错误: 缺少 API_KEY 环境变量。")
        return False

    base_url = "https://hub.weirdhost.xyz"

    # === Step 1: 验证 API Key 是否有效 ===
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Accept": "application/json",
        "Content-Type": "application/json"
    }

    print("正在验证 API Key 是否有效...")
    try:
        resp = requests.get(f"{base_url}/api/client", headers=headers, timeout=15)
        if resp.status_code != 200:
            print(f"API Key 登录失败: {resp.status_code} - {resp.text}")
            return False
        print("API Key 登录成功 ✅")
    except Exception as e:
        print(f"API 验证时出错: {e}")
        return False

    # === Step 2: 使用 Playwright 打开页面并点击按钮 ===
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context()

        # 注入 API Key 到 LocalStorage（模拟登录状态）
        page = context.new_page()
        print("正在设置 API Key 到 LocalStorage，以便网页识别登录状态...")
        page.goto(f"{base_url}/", wait_until="domcontentloaded")
        page.evaluate(f"""
            localStorage.setItem('pterodactyl::auth_token', '{api_key}');
        """)

        # 刷新到服务器页面
        print(f"正在访问服务器页面: {server_url}")
        page.goto(server_url, wait_until="domcontentloaded", timeout=90000)

        # === Step 3: 查找并点击 “시간추가” 按钮 ===
        print("等待页面元素加载...")
        page.wait_for_timeout(5000)  # 等待React渲染

        # 更宽松的选择器，匹配包含“시간”文字的按钮
        add_button_selector = 'button:has(span:has-text("시간"))'
        print(f"正在查找按钮: {add_button_selector}")

        try:
            add_button = page.locator(add_button_selector)
            add_button.wait_for(state='visible', timeout=60000)
            add_button.click()
            print("✅ 成功点击 '시간추가' 按钮。")
            page.screenshot(path="after_click.png")
            time.sleep(5)
            print("🎉 任务完成。")
            browser.close()
            return True
        except PlaywrightTimeoutError:
            print("❌ 错误: 未找到按钮，保存页面截图供调试。")
            page.screenshot(path="button_not_found.png")
            browser.close()
            return False

if __name__ == "__main__":
    print("开始执行添加服务器时间任务...")
    success = add_server_time()
    if success:
        print("任务执行成功 ✅")
        exit(0)
    else:
        print("任务执行失败 ❌")
        exit(1)
