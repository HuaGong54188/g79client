# -*- encoding: utf-8 -*
__all__ = [
   "LoginX19",
]

class LoginError(Exception):
    def __init__(self, message: str) -> None:
        self.__message = message

    def __str__(self) -> str:
        return f"LoginError: {self.__message}"

from .crypto import CryptoX19
import json, requests, traceback


class NetEaseClientProxyX19(object):
    def __init__(self, sauth: str) -> None:
        self.__sauth = sauth
        i = 0
        while True:
            try:
                self.__user_id, self.__user_token = self.__login()
                break
            except Exception as e:
                traceback.print_exc()
                print(str(e))
                i += 1
                if i > 5:
                    raise e
        self.init()

    def init(self):
        pass

    def __load_encrypt_json(self, string: str) -> dict:
        length, layer = len(string), 0
        for index in range(0, length):
            if string[index] == "{":
                layer += 1

            elif string[index] == "}":
                layer -= 1

            if layer == 0:
                return json.loads(string[:index + 1])

    @property
    def user_id(self) -> str:
        return self.__user_id

    @property
    def __release_server(self):
        return requests.get(
            url="https://x19.update.netease.com/serverlist/release.json",
            headers={
                "User-Agent": "WPFLauncher/0.0.0.0"
            }
        ).json()

    def __request_login_otp(self) -> dict:
        #                          self.__release_server["CoreServerUrl"]
        return requests.post(f"https://x19obtcore.nie.netease.com:8443/login-otp", self.__sauth, headers={"Content-Type": "application/json"}).json()

    def __request_auth_otp(self, login_otp_response: dict) -> dict:
        sauth = json.loads(self.__sauth)
        sauth_json = json.loads(sauth["sauth_json"])
        #print(login_otp_response)
        sdk_ver = ""
        if sauth_json["sdk_version"] != "3.4.0":
            sdk_ver = sauth_json["sdk_version"]
#        print(sauth_json)
        env = None
        if sauth_json["app_channel"] == "netease" and sauth_json["sdk_version"] == "3.9.0":
            env = 0
        otp_pwd = False
        lock_time = None
        hasMessage = False
        hasGmail = False
        is_register = False
        entity_id = None
        if "realname" in sauth_json:
            otp_pwd = 0
            lock_time = 0
            hasMessage = True
            hasGmail = True
            is_register = True
            entity_id = 0
        if sauth_json["platform"] == "ad":
            otp_pwd = None
        request_data = json.dumps(
            {
                "version": {
                    "version": "0.0.0.0",
                    "launcher_md5": "",
                    "updater_md5": ""
                },
                "aid": str(login_otp_response["entity"]["aid"]),
                "otp_token": login_otp_response["entity"]["otp_token"],
                "sauth_json": sauth["sauth_json"],
                # "sa_data": json.dumps({
                    # 'app_channel': sauth_json["app_channel"],
                    # 'app_ver': '0.0.0.0',
                    # 'core_num': '4',
                    # 'cpu_digit': '64',
                    # 'cpu_hz': '3200000',
                    # 'cpu_name': 'placeholder',
                    # 'device_height': '1600',
                    # 'device_model': 'HUAWEI HBN-AL00',
                    # 'device_width': '900',
                    # 'disk': '',
                    # 'emulator': 0,
                    # 'first_udid': sauth_json["udid"],
                    # 'is_guest': 0,
                    # 'launcher_type': 'PE_C++',
                    # 'mac_addr': '02:00:00:00:00:00',
                    # 'network': 'CHANNEL_UNKNOW',
                    # 'os_name': 'android',
                    # 'os_ver': '12',
                    # 'ram': '6238900224',
                    # 'rom': '134208294912',
                    # 'root': False,
                    # 'sdk_ver': sdk_ver,
                    # 'start_type': 'default',
                    # 'udid': sauth_json["udid"]
                # }),
                "sa_data": json.dumps({
                    "os_name": "windows",
                    "os_ver": "Microsoft Windows 11",
                    "mac_addr": "A11CF42FB51B",
                    "udid": sauth_json["udid"],
                    "app_ver": "0.0.0.0",
                    "sdk_ver": sdk_ver,
                    "network": "",
                    "disk": "613c0780",
                    "is64bit": "1",
                    "video_card1": "Nvidia RTX 4090",
                    "video_card2": "",
                    "video_card3": "",
                    "video_card4": "",
                    "launcher_type": "PC_java",
                    "pay_channel": "netease"
                }),
                "sdkuid": sauth_json["sdkuid"],
                "hasMessage": hasMessage,
                "hasGmail": hasGmail,
                "otp_pwd": otp_pwd,
                "lock_time": lock_time,
                "env": env,
                "min_engine_version": None,
                "min_patch_version": None,
                "verify_status": 0,
                "unisdk_login_json": None,
                "token": sauth_json["sessionid"],
                "is_register": is_register,
                "entity_id": entity_id
            }
        )
        decrypted_response = CryptoX19.HttpDecrypt(requests.post(
            #     self.__release_server["CoreServerUrl"]
            url=f"https://x19obtcore.nie.netease.com:8443/authentication-otp",
            headers={
                "Content-Type": "application/json; charset=utf-8",
                "User-Agent": "WPFLauncher/0.0.0.0",
                "user-id": "",
                "user-token": CryptoX19.CalculateDynamicToken("/authentication-otp", request_data, "")
            },
            data=CryptoX19.HttpEncrypt(request_data.encode())
        ).content)
        return self.__load_encrypt_json(decrypted_response.decode("unicode_escape"))

    def __login(self) -> tuple[str, str]:
        login_otp_response = self.__request_login_otp()
#        print(login_otp_response)
        if login_otp_response["code"] != 0: raise LoginError(f"login-otp response error: {login_otp_response}")

        auth_otp_response = self.__request_auth_otp(login_otp_response)
#        print(auth_otp_response)
        if auth_otp_response["code"] != 0: raise LoginError(f"auth-otp response error: {auth_otp_response}")

        return auth_otp_response["entity"]["entity_id"], auth_otp_response["entity"]["token"]

    def request(self, method: str, url: str, api: str, headers: dict = {}, json: dict = {}) -> requests.Response:
        return requests.request(
            method=method,
            url=url + api,
            json=json,
            headers={
                "Content-Type": "application/json; charset=utf-8",
                "User-Agent": "WPFLauncher/0.0.0.0",
                "user-id": self.__user_id,
                "user-token": CryptoX19.CalculateDynamicToken(api, __import__("json").dumps(json), self.__user_token),
                **headers
            }
        )

    def encrypt_request(self, method: str, url: str, api: str, json: dict = {}) -> dict:
        return self.__load_encrypt_json(CryptoX19.HttpDecrypt(requests.Session().send(requests.Request(
            method=method,
            url=url + api,
            headers={
                "Content-Type": "application/_json; charset=utf-8",
                "User-Agent": "WPFLauncher/0.0.0.0",
                "user-id": self.__user_id,
                "user-token": CryptoX19.CalculateDynamicToken(api, __import__("json").dumps(json), self.__user_token)
            },
            data=CryptoX19.HttpEncrypt(bytes(__import__("json").dumps(json).encode())),
        ).prepare()).content).decode("unicode_escape"))


def login_x19(sauth: str) -> NetEaseClientProxyX19:
    return NetEaseClientProxyX19(sauth)
