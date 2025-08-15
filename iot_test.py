import time
import uuid
import hashlib
import urllib.request
import json
from urllib.parse import urlencode

# 常量定义
IOT_APP_NAME = "apptest"  # 替换为实际的应用名
APP_SECRET = "predf556ef607b8b583baa5e8b6afc5a205end"  # 替换为实际的密钥


def query_robot_status(product_id, iot_robot_api_v2):
    """
    查询机器人状态的完整方法，整合了所有相关功能

    Args:
        product_id: 产品ID
        iot_robot_api_v2: API基础URL

    Returns:
        API响应的JSON数据
    """
    # 第一步：基础参数
    param_map = init_base_param()
    # 添加额外参数
    param_map["productId"] = product_id
    param_map["uuid"] = int(time.time() * 1000)

    # 第二步：计算签名 (sign)

    sign_value = sign(param_map, APP_SECRET)

    print(param_map.get('ts'))
    print(sign_value)
    # 将签名添加到参数中
    param_map["sign"] = sign_value

    # 第三步：构建URL并发送请求
    url = f"{iot_robot_api_v2}/openapi/v1/robot/status"
    full_url = f"{url}?{urlencode(param_map)}"

    # 发送GET请求
    with urllib.request.urlopen(full_url) as response:
        result = response.read()
        return json.loads(result)

def init_base_param():
    # 基础参数
    param_map = {
        "appname": IOT_APP_NAME,
        "ts": str(int(time.time() * 1000)),
        "requestId": str(uuid.uuid4())
    }
    return param_map
def is_ignore(key, value):
    # 忽略空值和 sign 参数
    if value is None or key == "appname":
        return True
    if value is None or key == "secret":
        return True
    if value is None or key == "ts":
        return True
    if value is None or key == "sign":
        return True
    # 忽略空字符串
    if isinstance(value, str) and value == "":
        return True
    return False
def sign(params, app_secret):
    sort_nested_parameters(params)  # 先对嵌套参数排序

    # 创建参数列表
    param_list = []
    for key, value in params.items():
        if is_ignore(key, value):
            continue
        if isinstance(value, str) and value == "":
            continue
        key_value = f"{key}:{value}"
        param_list.append(key_value)

    # 按ASCII顺序排序
    param_list.sort()

    # 构建排序后的参数字符串（如需保留，可加如下代码）
    # sorted_params = "\n".join(param_list)

    # 添加签名所需的额外参数
    param_list.append(f"appname:{params.get('appname')}")
    param_list.append(f"secret:{app_secret}")
    param_list.append(f"ts:{params.get('ts')}")

    # 拼接字符串并计算MD5
    joined_params = "|".join(param_list)
    return hashlib.md5(joined_params.encode()).hexdigest()
def sort_nested_parameters(params):
    """
    对复杂参数（如列表中的 dict）进行 ASCII 排序，原地修改 params。
    """
    if not isinstance(params, dict):
        return

    for key, value in params.items():
        if isinstance(value, list):
            sorted_item_params_list = []
            string_values = []
            for item in value:
                if isinstance(item, dict):
                    # 对 dict 按 key 排序
                    sorted_item_params = dict(sorted(item.items()))
                    sorted_item_params_list.append(sorted_item_params)
                else:
                    # 不是 dict（如 str/int），保持原有顺序
                    string_values.append(item)
            # 清空原列表
            value.clear()
            # 添加排序后的 dict
            value.extend(sorted_item_params_list)
            # 添加原有顺序的非 dict
            value.extend(string_values)
        # TODO: 其他复杂类型（如 dict 嵌套 dict）可按需递归处理
def postReq(param_map):
    url = f"{iot_robot_api_v2}/openapi/v1/robot/status"
    data = json.dumps(param_map).encode('utf-8')
    headers = {'Content-Type': 'application/json'}

    req = urllib.request.Request(url, data=data, headers=headers, method='POST')

    with urllib.request.urlopen(req) as response:
        result = response.read()
        print(result)
def encode_multipart_formdata(fields):
    boundary = uuid.uuid4().hex
    lines = []
    for key, value in fields.items():
        lines.append(f'--{boundary}')
        lines.append(f'Content-Disposition: form-data; name="{key}"')
        lines.append('')
        lines.append(str(value))
    lines.append(f'--{boundary}--')
    lines.append('')
    body = '\r\n'.join(lines).encode('utf-8')
    content_type = f'multipart/form-data; boundary={boundary}'
    return body, content_type
def postReqForm(param_map):
    url = "https://openapi-hk.cn/openapi/v1/robot/status"
    body, content_type = encode_multipart_formdata(param_map)
    headers = {'Content-Type': content_type}

    req = urllib.request.Request(url, data=body, headers=headers, method='POST')

    with urllib.request.urlopen(req) as response:
        result = response.read()
        print(result)

# 使用示例
if __name__ == "__main__":
    # 替换为实际的API基础URL和产品ID
    iot_robot_api_v2 = "https://openapi-hk-new.com.cn"
    product_id = "HOTYC04SZ202104143987599"

    result = query_robot_status(product_id, iot_robot_api_v2)
    print(json.dumps(result, ensure_ascii=False, indent=2))