import os
import requests
import time

def add_server_time_via_api(server_url="https://hub.weirdhost.xyz/api/add_time"):
    """
    使用 API 密钥通过 API 增加服务器时间。
    假设平台提供了 API 密钥认证，并支持通过 POST 请求增加服务器时间。
    """
    # 从环境变量获取 API 密钥
    api_key = os.environ.get('API_KEY')
    
    if not api_key:
        print("错误: 缺少 API_KEY 环境变量。请设置 API_KEY。")
        return False

    # 创建 API 请求头
    headers = {
        'Authorization': f'Bearer {api_key}',  # 使用 Bearer Token 进行认证
        'Content-Type': 'application/json'
    }

    # 假设我们需要传递服务器 ID 和一些额外的参数来执行操作
    data = {
        'server_id': '0f4424f2',  # 示例服务器 ID，根据实际情况修改
        'action': 'add_time',  # 增加时间操作
    }

    print(f"正在向 API 发送请求，增加服务器时间...")
    
    try:
        # 发送 POST 请求以增加时间
        response = requests.post(server_url, headers=headers, json=data)

        if response.status_code == 200:
            print("服务器时间成功增加。")
            return True
        else:
            print(f"错误: 无法通过 API 增加时间，状态码: {response.status_code}, 响应: {response.text}")
            return False
    except requests.RequestException as e:
        print(f"请求发生异常: {e}")
        return False


if __name__ == "__main__":
    print("开始执行添加服务器时间任务...")
    success = add_server_time_via_api()
    
    if success:
        print("任务执行成功。")
        exit(0)
    else:
        print("任务执行失败。")
        exit(1)
