import requests
import json
import uuid
import random
from X19Client import X19Client as G79Client
from X19Client.network.crypto import CryptoX19
from sharpbackdoor_crypto import http_encrypt, http_decrypt
def get_valid_json(decrypted_body):
    # Find valid JSON boundary
    blocks_count = 0
    readable_length = 0
    for i, byte in enumerate(decrypted_body):
        if byte == 0x7B:  # '{'
            blocks_count += 1
        elif byte == 0x7D:  # '}'
            blocks_count -= 1
        
        if blocks_count == 0 and i != 0:
            readable_length = i + 1
            break
    
    # Extract valid data
    if readable_length != 0:
        valid_data = decrypted_body[:readable_length]
    else:
        valid_data = decrypted_body
    return valid_data

engine_version = "3.4.5.272725"
latest_version = requests.get("https://g79.update.netease.com/patch_list/production/g79_rn_patchlist").json()["ios"][-1]
release_json = requests.get("https://g79.update.netease.com/serverlist/ios_release.0.25.json").json()
seed = str(uuid.uuid4())
message_part = "2b3e7ca013bb30a74d822579860c042b"
client_login_sn = "db797f983ca314e00626b9212705d8cc"
cookie = r'{"sauth_json":"{\"gameid\":\"x19\",\"login_channel\":\"netease\",\"app_channel\":\"netease\",\"platform\":\"pc\",\"sdkuid\":\"aibgraaeqsiluplt\",\"sessionid\":\"1-eyJzIjogIjQyMWM1cTAzNTZodDZpOTVlemdhcnYwdDRxNmw4cmx4IiwgIm9kaSI6ICJhbWF3cmFhYWF3cjV0MmM1LWQiLCAic2kiOiAiMDViNzNkOGFkZTU5OTc1ODRjYWEwMWZjYjFiNmRkNDc0OTI3OTMzNiIsICJ1IjogImFpYmdyYWFlcXNpbHVwbHQiLCAidCI6IDIsICJnX2kiOiAiYWVjZnJ4b2R5cWFhYWFqcCJ9\",\"sdk_version\":\"3.9.0\",\"udid\":\"chm9ug3treqfrl6z76p5jkd6vwjjseh8\",\"deviceid\":\"amawraaaawr5t2c5-d\",\"aim_info\":\"{\\\"aim\\\":\\\"127.0.0.1\\\",\\\"country\\\":\\\"CN\\\",\\\"tz\\\":\\\"+0800\\\",\\\"tzid\\\":\\\"\\\"}\",\"client_login_sn\":\"31D8662F5B47BA295FDA307964F93C2B\",\"gas_token\":\"\",\"source_platform\":\"pc\",\"ip\":\"127.0.0.1\"}"}'
cookie_data = json.loads(cookie)
sauth = json.loads(cookie_data["sauth_json"])
peauth = {
    "engine_version": engine_version,
    "extra_param": "extra",
    "message": f"{engine_version}apple{latest_version}{message_part}{seed}",
    "patch_version": latest_version,
    "pay_channel": "",
    "sa_data": json.dumps({
        "app_channel": "app_store",
        "app_ver": latest_version,
        "core_num": "6",
        "cpu_digit": "0",
        "cpu_hz": "",
        "cpu_name": "",
        "device_height": "2796",
        "device_model": "iPhone16,2",
        "device_width": "1290",
        "disk": "",
        "emulator": 0,
        "first_udid": sauth["udid"],
        "is_guest": 0,
        "launcher_type": "PE_C++",
        "mac_addr": "02:00:00:00:00:00",
        "network": "--",
        "os_name": "iOS",
        "os_ver": "18.1.1",
        "ram": "8034369536",
        "rom": "",
        "root": False,
        "sdk_ver": "5.9.0",
        "start_type": "default",
        "udid": sauth["udid"]
    }, separators=(',',':')),
    "sauth_json": {
        "aim_info": json.dumps({
            "aim": "",
            "country": "CN",
            "tz": "+0800",
            "tzid": r"Asia\/Shanghai"
        }, separators=(',',':')),
        "app_channel": "app_store",
        "client_login_sn": client_login_sn,
        "deviceid": sauth["deviceid"],
        "gameid": "x19",
        "get_access_token": "1",
        "ip": "",
        "login_channel": "netease",
        "platform": "ios",
        "sdk_version": "5.9.0",
        "sdkuid": sauth["sdkuid"],
        "sessionid": sauth["sessionid"],
        "udid": sauth["udid"]
    },
    "seed": seed,
    "sign": "AAAAAAAAAAAAAAAAAAAAAA=="
}

payload = http_encrypt(json.dumps(peauth, separators=(',',':')).encode()).hex()
headers = {
  'User-Agent': "libhttpclient/1.0.0.0",
  'Accept-Encoding': "gzip",
  'Content-Type': "application/json"
}

response = requests.post(f'{release_json["CoreServerUrl"]}/pe-authentication', data=payload, headers=headers)
g79_login_data = json.loads(get_valid_json(http_decrypt(bytes.fromhex(response.text))))
if g79_login_data["code"] != 0 :
    raise "登录失败"

client = G79Client.__new__(G79Client)
g79_login_entity = g79_login_data["entity"]
user_id = g79_login_entity["entity_id"]
user_token = g79_login_entity["token"]
client._NetEaseClientProxyX19__user_id = user_id
client._NetEaseClientProxyX19__user_token = user_token

response = client.request("post", release_json["CoreServerUrl"], "/pe-user-detail/get").json()
if response["code"] != 0 :
    raise "获取用户信息失败"
user_entity = response["entity"]
uid = str(user_id)
username = user_entity["name"]
if username == "":
    name = "FIN互通" + str(random.randint(0, 999999)).zfill(6)
    response = client.request("post", "https://g79apigatewayobt.minecraft.cn", "/pe-nickname-setting/update", json={"name":name}).json()
    if response["code"] != 0 :
        raise "修改名字失败: " + response["message"]
    username = name

growth_level = int(user_entity["level"])
print(username)
print(growth_level)

response = client.SearchRentalServerByName("48285363")
if response.code != 0 or len(response.entities) == 0:
    raise "获取租赁服信息失败"
server_id = str(response.entities[0].entity_id)

response = client.EnterRentalServerWorld(server_id)
if response.code != 0:
    raise "获取租赁服地址失败"
server_entity = response.entity

ip_address = server_entity.mcserver_host + ":" + str(server_entity.mcserver_port)
print(ip_address)
authv2 = {
    "bit": "64",
    "clientKey": "MHYwEAYHKoZIzj0CAQYFK4EEACIDYgAEzmz6+EK8UC40g5XsqoAjqURAKP6uCAMmXJeEyzR/8BkZ1vVXpFTMF/AmBl3Tf+gvDFPJkT9Bm3bAO0IeXo+ssMOsJX4NFPLM4+YEohwJrJyRaMptmh1nvWue4J5+vbZW", #"MHYwEAYHKoZIzj0CAQYFK4EEACIDYgAEnBgnx34mziLxsKpKw1Z6lOmYooZf7UISlSyMds1JhUfvHb/CsJHf9+72InRCTW07Ddyk0IMAB3u1XsirTGmDHsxxr+h9waJR8ZKsIc37TD0dRGXcBCdxtKiMUMrEIJ01",
    "displayName": username,
    "engineVersion": engine_version,
    "netease_sid": f"{server_id}:RentalGame",
    "os_name": "iOS",
    "patchVersion": latest_version,
    "uid": int(uid)
}

authv2_json = json.dumps(authv2)
api = "/authentication-v2"
url = release_json["AuthServerUrl"] + api
authv2_data = http_encrypt(authv2_json.encode()).hex()
response = requests.post(
    url=url,
    data=authv2_data,
    headers={
        "User-Agent": "libhttpclient/1.0.0.0",
        "Accept-Encoding": "gzip",
        "Content-Type": "application/json",
        "user-id": uid,
        "user-token": CryptoX19.CalculateDynamicToken(api, authv2_json, user_token).encode().hex(),
    }
)
chainInfo = get_valid_json(http_decrypt(bytes.fromhex(response.text))).decode()
print(chainInfo)