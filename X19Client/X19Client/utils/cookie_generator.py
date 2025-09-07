# -*- encoding: utf-8 -*-
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
from urllib.parse import urlencode, parse_qs
import binascii, json, random, requests, string, time, uuid
from .cryption import netease_decryption_4o_0xfm_aes_cbc_256

class CookieGenerator(object):
    # Common
    def __generate_random_string(self, length: int, characters: str = string.ascii_letters + string.digits) -> str:
        return "".join(random.choice(characters) for _ in range(length))

    def __set_url_parameters(self, url: str, parameters: dict) -> str:
        return f"{url}?{urlencode(parameters)}"

    def __encode_cookie(self, cookies: dict) -> str:
        return "; ".join(f"{key}={value}" for key, value in cookies.items())

    # NetEase
    def __generate_unique_id(self) -> str:
        return str(uuid.uuid4()) + "".join(random.choice(string.digits) for _ in range(13))

    def __generate_transaction_id(self) -> str:
        return str(uuid.uuid4()) + "-1"

    def __encrypt_login_params(self, raw_content: str, device_key: str) -> str:
        return binascii.hexlify(AES.new(binascii.unhexlify(device_key), AES.MODE_ECB).encrypt(pad(raw_content.encode("utf-8"),AES.block_size, style="pkcs7"))).decode("utf-8").lower()

    def RequestForDevice(self, udid: str) -> requests.Response:
        return requests.post(
        "https://service.mkey.163.com/mpay/games/aecfrxodyqaaaajp-g-x19/devices", {
                "mac": self.__generate_random_string(32, "0123456789abcdef"),
                "urs_udid": self.__generate_random_string(40, "0123456789abcdef"),
                "init_urs_device": "0",
                "unique_id": self.__generate_unique_id(),
                "brand": "Redmi",
                "device_name": "miro",
                "device_type": "mobile",
                "device_model": "miro",
                "resolution": "1080*1920",
                "system_name": "Android",
                "system_version": "31",
                "udid": udid,
                "app_channel": "netease",
                "game_id": "aecfrxodyqaaaajp-g-x19",
                "gv": "840255180",
                "gvn": "3.0.5.255180",
                "cv": "a4.8.0",
                "sv": "32",
                "app_type": "games",
                "app_mode": "2",
                "mcount_app_key": "EEkEEXLymcNjM42yLY3Bn6AO15aGy4yq",
                "mcount_transaction_id": self.__generate_transaction_id(),
                "_cloud_extra_base64": "e30=",
                "sc": "1"
            }
        )

    def LoginByGuest(self, udid, device_id: str, device_key: str) -> requests.Response:
        return requests.post(
            f"https://service.mkey.163.com/mpay/games/aecfrxodyqaaaajp-g-x19/devices/{device_id}/users/by_guest", {
                "opt_fields": "nickname,avatar,realname_status,mobile_bind_status,exit_popup_info",
                "params": self.__encrypt_login_params("{}", device_key),
                "game_id": "aecfrxodyqaaaajp-g-x19",
                "gv": "840255180",
                "gvn": "3.0.5.255180",
                "cv": "a4.8.0",
                "sv": "32",
                "app_type": "games",
                "app_mode": "2",
                "app_channel": "netease",
                "mcount_app_key": "EEkEEXLymcNjM42yLY3Bn6AO15aGy4yq",
                "mcount_transaction_id": self.__generate_transaction_id(),
                "_cloud_extra_base64": "e30=",
                "sc": "1"
            }
        )

    def LoginByPassword(self, username: str, password: str, unique_id: str, device_id: str, device_key: str) -> requests.Response: raise NotImplementedError

    def LoginByToken(self, username: str, token: str, sdkuid: str, device_id: str) -> requests.Response: raise NotImplementedError

    # 4399
    def __log_init(self) -> requests.Response:
        """
        :return:

        """
        return requests.get(
            headers={
                "Connection": "Keep-Alive",
                "Host": "stat.api.4399.com",
                "User-Agent": "WinHttpClient"
            },
            url="http://stat.api.4399.com/micro_game/log.js",
            params={
                "op": "init",
                "g": "500352",
                "u": "",
                "ua": "Microsoft-Windows-8|2560*1600",
                "d": "04-BF-1B-BF-08-EA",
                "type": "0",
                "v": "1.3.5"
            }
        )

    def __sdk_init(self) -> requests.Response:
        """
        :return:
        {
           "code" : 10000,
           "data" : {
              "loginUrl" : "http://ptlogin.4399.com/resource/ucenter.html?action=login&appId=kid_wdsj&loginLevel=8&regLevel=8&bizId=2201001794&externalLogin=qq&qrLogin=true&layout=vertical&level=101&css=http://microgame.5054399.net/v2/resource/cssSdk/default/login.css&v=2018_11_26_16&postLoginHandler=redirect&checkLoginUserCookie=true&redirectUrl=http%3A%2F%2Fcdn.h5wan.4399sj.com%2Fmicroterminal-h5-frame%3Fgame_id%3D500352%26rand_time%3D1736411193",
              "payUnionId" : "90073",
              "payUrl" : "http://cz.4399.com/weiduan.html"
           },
           "msg" : "success"
        }
        """
        return requests.get(
            headers={
                "Connection": "Keep-Alive",
                "Host": "microgame.5054399.net",
                "User-Agent": "WinHttpClient"
            },
            url="http://stat.api.4399.com/micro_game/log.js",
            params={
                "game_id": "500352",
                "sdk_version": "1.3.5"
            }
        )

    def __sdk_game_status(self, sign: str) -> requests.Response:
        """
        :return:
        {
           "code" : 10000,
           "data" : {
              "popContent" : "当前游戏已停止运营，不再提供相关服务。",
              "status" : 2
           },
           "msg" : "success"
        }
        """
        return requests.post(
            headers={
                "Cache-Control": "no-cache",
                "Connection": "Keep-Alive",
                "Content-Type": "application/x-www-form-urlencoded",
                "Host": "microgame.5054399.net",
                "User-Agent": "WinHttpClient"
            },
            url="http://microgame.5054399.net/v2/service/sdk/gameStatus",
            files={
                "game_id": "500352",
                "sign": sign,
                "time": int(time.time())
            }
        )

    def __user_center_login(self, username: str, phlogact: str) -> requests.Response:
        """
        :return:
        ../cache/center_login.html
        """
        return requests.get(
            headers={
                "Accept": "image/gif, image/jpeg, image/pjpeg, application/x-ms-application, application/xaml+xml, application/x-ms-xbap, */*",
                "Accept-Encoding": "gzip, deflate",
                "Accept-Language": "en-GB,en;q=0.8,zh-Hans-CN;q=0.5,zh-Hans;q=0.2",
                "Connection": "Keep-Alive",
                "Host": "ptlogin.4399.com",
                "User-Agent": "Mozilla/5.0 (Windows NT 6.2; WOW64; Trident/7.0; rv:11.0) like Gecko"
            },
            cookies={
                "ptusertype": "kid_wdsj.4399_login",
                "Pnick": "0",
                "Qnick": "",
                "Puser": username.lower(),
                "phlogact": phlogact
            },
            url="http://ptlogin.4399.com/resource/ucenter.html",
            params={
                "action": "login",
                "appId": "kid_wdsj",
                "loginLevel": "8",
                "regLevel": "8",
                "bizId": "2201001794",
                "externalLogin": "qq",
                "qrLogin": "true",
                "layout": "vertical",
                "level": "101",
                "css": "http://microgame.5054399.net/v2/resource/cssSdk/default/login.css",
                "v": "2018_11_26_16",
                "postLoginHandler": "redirect",
                "checkLoginUserCookie": "true",
                "redirectUrl": f"http://cdn.h5wan.4399sj.com/microterminal-h5-frame?game_id=500352&rand_time={int(time.time())}"
            }
        )

    def __user_center_js(self, username: str, phlogact: str) -> requests.Response:
        """
        :return:
        ../cache/center.js
        """
        return requests.get(
            headers={
                "Accept": "*/*",
                "Accept-Encoding": "gzip, deflate",
                "Accept-Language": "en-GB,en;q=0.8,zh-Hans-CN;q=0.5,zh-Hans;q=0.2",
                "Connection": "Keep-Alive",
                "Host": "ptlogin.4399.com",
                "Referer": "http://ptlogin.4399.com/resource/ucenter.html",
                "User-Agent": "Mozilla/5.0 (Windows NT 6.2; WOW64; Trident/7.0; rv:11.0) like Gecko"
            },
            cookies={
                "ptusertype": "kid_wdsj.4399_login",
                "Pnick": "0",
                "Qnick": "",
                "Puser": username.lower(),
                "phlogact": phlogact
            },
            url="http://ptlogin.4399.com/resource/ucenter.html",
            params={
                "action": "login",
                "appId": "kid_wdsj",
                "loginLevel": "8",
                "regLevel": "8",
                "bizId": "2201001794",
                "externalLogin": "qq",
                "qrLogin": "true",
                "layout": "vertical",
                "level": "101",
                "css": "http://microgame.5054399.net/v2/resource/cssSdk/default/login.css",
                "v": "2018_11_26_16",
                "postLoginHandler": "redirect",
                "checkLoginUserCookie": "true",
                "redirectUrl": f"http://cdn.h5wan.4399sj.com/microterminal-h5-frame?game_id=500352&rand_time={int(time.time())}"
            }
        )

    def __pt_login_frame(self, username: str, phlogact: str) -> requests.Response:
        """
        :return:
        ../cache/center.js
        """
        return requests.get(
            headers={
                "Accept": "image/gif, image/jpeg, image/pjpeg, application/x-ms-application, application/xaml+xml, application/x-ms-xbap, */*",
                "Accept-Encoding": "gzip, deflate",
                "Accept-Language": "en-GB,en;q=0.8,zh-Hans-CN;q=0.5,zh-Hans;q=0.2",
                "Connection": "Keep-Alive",
                "Host": "ptlogin.4399.com",
                "Referer": "http://ptlogin.4399.com/resource/ucenter.html",
                "User-Agent": "Mozilla/5.0 (Windows NT 6.2; WOW64; Trident/7.0; rv:11.0) like Gecko"
            },
            cookies={
                "ptusertype": "kid_wdsj.4399_login",
                "Pnick": "0",
                "Qnick": "",
                "Puser": username.lower(),
                "phlogact": phlogact
            },
            url="http://ptlogin.4399.com/ptlogin/loginFrame.do",
            params={
                "postLoginHandler": "default",
                "displayMode": "popup",
                "css": "http://microgame.5054399.net/v2/resource/cssSdk/default/login.css",
                "bizId": "2201001794",
                "appId": "kid_wdsj",
                "gameId": "wd",
                "username": username.lower(),
                "externalLogin": "qq",
                "mainDivId": "popup_login_div",
                "autoLogin": "true",
                "includeFcmInfo": "false",
                "qrLogin": "true",
                "userNameLabel": "4399\u7528\u6237\u540d",
                "userNameTip": "\u8bf7\u8f93\u51654399\u7528\u6237\u540d",
                "welcomeTip": "\u6b22\u8fce\u56de\u52304399",
                "level": "8",
                "regLevel": "8",
                "iframeId": "popup_login_frame",
                "v": str(int(time.time() * 1000)),
            }
        )

    def __pt_login_do(self, username: str, phlogact: str, password: str, session_id: str) -> requests.Response:
        """
        :return:
        ../pt_login_do
        """
        return requests.post(
            headers={
                "Accept": "image/gif, image/jpeg, image/pjpeg, application/x-ms-application, application/xaml+xml, application/x-ms-xbap, */*",
                "Accept-Encoding": "gzip, deflate",
                "Accept-Language": "en-GB,en;q=0.8,zh-Hans-CN;q=0.5,zh-Hans;q=0.2",
                "Cache-Control": "no-cache",
                "Connection": "Keep-Alive",
                "Host": "ptlogin.4399.com",
                "Referer": "http://ptlogin.4399.com/ptlogin/loginFrame.do",
                "User-Agent": "Mozilla/5.0 (Windows NT 6.2; WOW64; Trident/7.0; rv:11.0) like Gecko"
            },
            cookies= {
                    "ptusertype": "kid_wdsj.4399_login",
                    "Pnick": "0",
                    "Qnick": "",
                    "Puser": username.lower(),
                    "phlogact": phlogact,
                    "USESSIONID": session_id
            },
            url="http://ptlogin.4399.com/ptlogin/login.do",
            params={
                "v": "1"
            },
            data={
                "loginFrom": "uframe",
                "postLoginHandler": "default",
                "layoutSelfAdapting": "true",
                "externalLogin": "qq",
                "displayMode": "popup",
                "layout": "vertical",
                "bizId": "2201001794",
                "appId": "kid_wdsj",
                "gameId": "wd",
                "css": "http://microgame.5054399.net/v2/resource/cssSdk/default/login.css",
                "mainDivId": "popup_login_div",
                "includeFcmInfo": "false",
                "level": "8",
                "regLevel": "8",
                "userNameLabel": "4399\u7528\u6237\u540d",
                "userNameTip": "\u8bf7\u8f93\u51654399\u7528\u6237\u540d",
                "welcomeTip": "\u6b22\u8fce\u56de\u52304399",
                "sec": "1",
                "password": password,
                "iframeId": "popup_login_frame",
                "username": username.lower()
            }
        )

    def __resource_messenger(self) -> requests.Response:
        """
        :return:

        """
        return requests.get(
            headers={
                "Accept": "*/*",
                "Accept-Encoding": "gzip, deflate",
                "Accept-Language": "en-GB,en;q=0.8,zh-Hans-CN;q=0.5,zh-Hans;q=0.2",
                "Connection": "Keep-Alive",
                "Host": "ptlogin.3304399.net",
                "If-Modified-Since": "Thu, 12 Dec 2024 07:37:08 GMT",
                "If-None-Match": "\"675a92a4-c38\"",
                "Referer": "http://ptlogin.4399.com/ptlogin/login.do?v=1",
                "User-Agent": "Mozilla/5.0 (Windows NT 6.2; WOW64; Trident/7.0; rv:11.0) like Gecko"
            },
            url=self.__set_url_parameters("http://ptlogin.3304399.net/resource/messenger.js", {
                "v": "299"
            })
        )

    def __pt_login_check_kid_login_user_cookie(self, pnick: str, qnick: str, xauth: str, username: str, phlogact: str, session_id: str, uauth: str, pauth: str) -> requests.Response:
        """
        :return:

        """
        return requests.get(
            headers={
                "Accept": "image/gif, image/jpeg, image/pjpeg, application/x-ms-application, application/xaml+xml, application/x-ms-xbap, */*",
                "Accept-Encoding": "gzip, deflate",
                "Accept-Language": "en-GB,en;q=0.8,zh-Hans-CN;q=0.5,zh-Hans;q=0.2",
                "Connection": "Keep-Alive",
                "Host": "ptlogin.4399.com",
                "Referer": "http://ptlogin.4399.com/ptlogin/login.do?v=1",
                "User-Agent": "Mozilla/5.0 (Windows NT 6.2; WOW64; Trident/7.0; rv:11.0) like Gecko"
            },
            cookies={
                    "ptusertype": "kid_wdsj.4399_login",
                    "Pnick": pnick,
                    "Qnick": qnick,
                    "Xauth": xauth,
                    "Puser": username.lower(),
                    "phlogact": phlogact,
                    "USESSIONID": session_id,
                    "Uauth": uauth,
                    "Pauth": pauth,
                    "ck_accname": username.lower()
            },
            url="http://ptlogin.4399.com/ptlogin/checkKidLoginUserCookie.do",
            params={
                "appId": "kid_wdsj",
                "gameUrl": "http://cdn.h5wan.4399sj.com/microterminal-h5-frame?game_id=500352",
                "rand_time": uauth.split("|")[4],
                "nick": pnick,
                "onLineStart": "false",
                "show": "1",
                "isCrossDomain": "1",
                "retUrl": "http://ptlogin.4399.com/resource/ucenter.html"
                # "retUrl": self.__set_url_parameters("http://ptlogin.4399.com/resource/ucenter.html", {
                #     "action": "login",
                #     "appId": "kid_wdsj",
                #     "loginLevel": "8",
                #     "regLevel": "8",
                #     "bizId": "2201001794",
                #     "externalLogin": "qq",
                #     "qrLogin": "true",
                #     "layout": "vertical",
                #     "level": "101",
                #     "css": "http://microgame.5054399.net/v2/resource/cssSdk/default/login.css",
                #     "v": "2018_11_26_16",
                #     "postLoginHandler": "redirect",
                #     "checkLoginUserCookie": "true",
                #     "redirectUrl": f"http://cdn.h5wan.4399sj.com/microterminal-h5-frame?game_id=500352&rand_time={int(time.time())}"
                # })
            },
            allow_redirects=False
        )

    def __microterminal_h5_frame(self, nick: str, sig: str, uid: str, username: str) -> requests.Response:
        return requests.get(
            headers={
                "Accept": "image/gif, image/jpeg, image/pjpeg, application/x-ms-application, application/xaml+xml, application/x-ms-xbap, */*",
                "Accept-Encoding": "gzip, deflate",
                "Accept-Language": "en-GB,en;q=0.8,zh-Hans-CN;q=0.5,zh-Hans;q=0.2",
                "Connection": "Keep-Alive",
                "Host": "cdn.h5wan.4399sj.com",
                "Referer": "http://ptlogin.4399.com/ptlogin/login.do?v=1",
                "User-Agent": "Mozilla/5.0 (Windows NT 6.2; WOW64; Trident/7.0; rv:11.0) like Gecko"
            },
            url=self.__set_url_parameters("http://cdn.h5wan.4399sj.com/microterminal-h5-frame/", {
                "game_id": "500352",
                "nick": nick,
                "sig": sig,
                "uid": uid,
                "fcm": "0",
                "show": "1",
                "isCrossDomain": "1",
                "rand_time": str(int(time.time())),
                "ptusertype": "4399",
                "time": str(int(time.time() * 1000)),
                "validateState": "1",
                "username": username.lower()
            })
        )

    def __sdk_info(self, location: str) -> requests.Response:
        return requests.post(
            headers={
                "Accept": "*/*",
                "Accept-Encoding": "gzip, deflate",
                "Accept-Language": "en-GB,en;q=0.8,zh-Hans-CN;q=0.5,zh-Hans;q=0.2",
                "Connection": "Keep-Alive",
                "Host": "microgame.5054399.net",
                "Referer": location,
                "User-Agent": "Mozilla/5.0 (Windows NT 6.2; WOW64; Trident/7.0; rv:11.0) like Gecko"
            },
            url="https://microgame.5054399.net/v2/service/sdk/info",
            params={
                "callback": f"",
                "queryStr": location.split("?")[1],
                "_": str(int(time.time() * 1000))
            }
        )

    def login_by_4399_password(self, username: str, password: str, phlogact: str = "") -> str:
    
        session_id = str(uuid.uuid4())
        self.__log_init()
        self.__sdk_init()
        #print(self.__user_center_login(username, phlogact).cookies.items())
        #print(self.__user_center_js(username, phlogact).cookies.items())
        #print(self.__pt_login_frame(username, phlogact).cookies.items())
        cookies = {key: value for key, value in self.__pt_login_do(username, phlogact, password, session_id).cookies.items()}
        #print(cookies)
        location = self.__pt_login_check_kid_login_user_cookie(cookies["Pnick"], cookies["Qnick"], cookies["Xauth"], username, phlogact, session_id, cookies["Uauth"], cookies["Pauth"]).headers.get("Location")
        sdk_login_data = {element.split("=")[0]: element.split("=")[1] for element in self.__sdk_info(location).json()["data"]["sdk_login_data"].split("&")}
        #print(sdk_login_data)
        import requests
        url = "https://m.4399api.com/openapiv2/oauth.html"
        
        payload = {
          'state': cookies["Pauth"],#"834981265|a83979add4283de3d435d078f4daa929|44770|20250503145446b7cf57fa469c46d6fec50b04ca07519b00b6970dc31d9adb|a85e77c37e7ae179779000eab5fbc7fd|ce86d28c433db63b9e54ea2fb14a20b6|1747572986|4399",
          'source': "4399",
          'device': "{\"DEVICE_IDENTIFIER\":\"20250503145446b7cf57fa469c46d6fec50b04ca07519b00b6970dc31d9adb\",\"SCREEN_RESOLUTION\":\"1600*900\",\"DEVICE_MODEL\":\"HBN-AL00\",\"DEVICE_MODEL_VERSION\":\"12\",\"SYSTEM_VERSION\":\"12\",\"PLATFORM_TYPE\":\"Android\",\"SDK_VERSION\":\"3.12.2.503\",\"GAME_KEY\":\"115716\",\"GAME_VERSION\":\"3.3.15.267994\",\"BID\":\"com.netease.mc.m4399\",\"RUNTIME\":\"Origin\",\"CANAL_IDENTIFIER\":\"\",\"UDID\":\"1101g80WoScsVFj9zV11ua8d7\",\"DEBUG\":\"false\",\"NETWORK_TYPE\":\"WIFI\",\"GAME_BOX_VERSION\":\"8.9.0.31\",\"VIP_INFO\":\"{\\\"level\\\":0,\\\"score\\\":0}\",\"TEAM\":2,\"DEVICE_IDENTIFIER_SM\":\"20250503144608617dc1673ee7d7c9cd9e56bc1ccf48b201553d6b03335eb7\",\"SERVER_SERIAL\":\"0\",\"UID\":\"834981265\"}",
          '': ""
        }
        
        headers = {
          'User-Agent': "Dalvik/2.1.0 (Linux; U; Android 12; HBN-AL00 Build/21288e3.0) 4399android 4399OperateSDK",
          'Connection': "Keep-Alive",
          'Accept-Encoding': "gzip"
        }
        
        response = requests.post(url, data=payload, headers=headers)
        
        #print(response.text)
        import requests

        url = f"https://apps.4399.com/online/heartbeat?duration=1&access_token={sdk_login_data.get("token")}&uid={sdk_login_data.get("uid")}&gid=115716&device_model=HBN-AL00&sdk_version=3.12.2.503&rich_text_tip=1&ptid=2&version=2&token="
        
        headers = {
          'User-Agent': "Dalvik/2.1.0 (Linux; U; Android 12; HBN-AL00 Build/21288e3.0) 4399android 4399OperateSDK",
          'Connection': "Keep-Alive",
          'Accept-Encoding': "gzip"
        }
        
        response = requests.get(url, headers=headers)
        
        #print(response.text)
        d = response.json()

        url = "https://m.4399api.com/openapiv2/oauth-getinfobyrefresh.html"
        payload = {
          'refresh_token': d["result"]["token"],
          'source': "4399",
          'device': json.dumps({
              'DEVICE_IDENTIFIER': self.__generate_random_string(32, "0123456789abcdef"),
              'SCREEN_RESOLUTION': '1600*900',
              'DEVICE_MODEL': 'HBN-AL00',
              'DEVICE_MODEL_VERSION': '12',
              'SYSTEM_VERSION': '12',
              'PLATFORM_TYPE': 'Android',
              'SDK_VERSION': '3.12.2.503',
              'GAME_KEY': '115716',
              'GAME_VERSION': '3.3.15.267994',
              'BID': 'com.netease.mc.m4399',
              'RUNTIME': 'Origin',
              'CANAL_IDENTIFIER': '',
              'UDID': self.__generate_random_string(32, "0123456789abcdef"),
              'DEBUG': 'true',
              'NETWORK_TYPE': 'WIFI',
              'GAME_BOX_VERSION': '8.9.0.31',
              'VIP_INFO': '',
              'TEAM': 2,
              'DEVICE_IDENTIFIER_SM': self.__generate_random_string(32, "0123456789abcdef"),
              'SERVER_SERIAL': '0',
              'UID': sdk_login_data.get("uid")
          }),
          '': ""
        }
        
        headers = {
          'User-Agent': "Dalvik/2.1.0 (Linux; U; Android 12; HBN-AL00 Build/21288e3.0) 4399android 4399OperateSDK",
          'Connection': "Keep-Alive",
          'Accept-Encoding': "gzip"
        }
        
        response = requests.post(url, data=payload, headers=headers)
        
        #print(response.text)
        return json.dumps({
            "sauth_json": json.dumps({
                "timestamp": sdk_login_data.get("time"),
                "userid": sdk_login_data.get("username"),
                "realname": json.dumps({
                    "realname_type": ""
                }, separators=(',', ':')),
                "gameid": "x19",
                "login_channel": "4399pc",
                "app_channel": "4399pc",
                "platform": "pc",
                "sdkuid": sdk_login_data.get("uid"),
                "sessionid": sdk_login_data.get("token"),
                "sdk_version": "1.0.0",
                "udid": self.__generate_random_string(32, "0123456789abcdef"),
                "deviceid": self.__generate_random_string(32, "0123456789ABCDEF"),
                "aim_info": json.dumps({
                    "aim": "100.100.100.100",
                    "country": "CN",
                    "tz": "+0800",
                    "tzid": ""
                }, separators=(',', ':')),
                "client_login_sn": uuid.uuid4().hex,
                "gas_token": "",
                "source_platform": "pc",
                "ip": "0.0.0.0"
            }, separators=(',', ':'))
        }, separators=(',', ':'))

    def LoginBy4399Cookie(self, pnick: str, qnick: str, xauth: str, username: str, phlogact: str, session_id: str, uauth: str, pauth: str) -> str:
        location = self.__pt_login_check_kid_login_user_cookie(pnick, qnick, xauth, username, phlogact, session_id, uauth, pauth).headers.get("Location")
        sdk_login_data = {element.split("=")[0]: element.split("=")[1] for element in self.__sdk_info(location).json()["data"]["sdk_login_data"].split("&")}
        return json.dumps({
            "sauth_json": json.dumps({
                "timestamp": sdk_login_data.get("time"),
                "userid": sdk_login_data.get("username"),
                "realname": json.dumps({
                    "realname_type": "0"
                }, separators=(',', ':')),
                "gameid": "x19",
                "login_channel": "4399pc",
                "app_channel": "4399pc",
                "platform": "pc",
                "sdkuid": sdk_login_data.get("uid"),
                "sessionid": sdk_login_data.get("token"),
                "sdk_version": "1.0.0",
                "udid": self.__generate_random_string(32, "0123456789abcdef"),
                "deviceid": self.__generate_random_string(32, "0123456789ABCDEF"),
                "aim_info": json.dumps({
                    "aim": "100.100.100.100",
                    "country": "CN",
                    "tz": "+0800",
                    "tzid": ""
                }, separators=(',', ':')),
                "client_login_sn": uuid.uuid4().hex,
                "gas_token": "",
                "source_platform": "pc",
                "ip": "0.0.0.0"
            }, separators=(',', ':'))
        }, separators=(',', ':'))

    def login_by_pe_auth(self, peauth: str) -> str:
        peauth_login_data = json.loads(netease_decryption_4o_0xfm_aes_cbc_256(peauth))
        sauth = peauth_login_data["sauth_json"]
        #{"engine_version": "3.3.15.267994", "extra_param": "extra", "message": "3.3.15.26799439512ea3f9a8d3a45356e1a51435b9533.3.53.272615c8c810c015614421bfb70b1d245b90522b3e7ca013bb30a74d822579860c042b9955d141-484e-43d7-a294-ab3d61b57d54", "patch_version": "3.3.53.272615", "pay_channel": "", "sa_data": "{\"app_channel\":\"oppo\",\"app_ver\":\"3.3.53.272615\",\"core_num\":\"4\",\"cpu_digit\":\"64\",\"cpu_hz\":\"3200000\",\"cpu_name\":\"placeholder\",\"device_height\":\"1600\",\"device_model\":\"HUAWEI HBN-AL00\",\"device_width\":\"900\",\"disk\":\"\",\"emulator\":0,\"first_udid\":\"04ce2812d5a2e7ce\",\"is_guest\":0,\"launcher_type\":\"PE_C++\",\"mac_addr\":\"02:00:00:00:00:00\",\"network\":\"CHANNEL_UNKNOW\",\"os_name\":\"android\",\"os_ver\":\"12\",\"ram\":\"6238900224\",\"rom\":\"134208294912\",\"root\":true,\"sdk_ver\":\"5030208\",\"start_type\":\"default\",\"udid\":\"04ce2812d5a2e7ce\"}\n", "sauth_json": {"aim_info": "{\"aim\":\"112.13.40.61\",\"country\":\"CN\",\"tz\":\"+0800\",\"tzid\":\"Asia\\/Shanghai\",\"celluar_ip\":\"\",\"operator\":\"460000\",\"is_vpn_enabled\":\"false\"}", "app_channel": "oppo", "client_login_sn": "dd5ed87b26427bdbaf861f3ff2f48711", "extra_data": "{\"adv_channel\":\"0\",\"adid\":\"0\"}", "gameid": "x19", "get_access_token": "1", "ip": "112.13.40.61", "is_unisdk_guest": 0, "login_channel": "oppo", "platform": "ad", "realname": "{\"realname_type\":0,\"age\":47,\"respCode\":0,\"respMsg\":\"success\"}", "sdk_version": "5030208", "sdkuid": "472231845", "sessionid": "TICKET_Ajnx0SLbfzTxUbqR/5oEvxzVM1pZ4Iz97Wt/sKxLGhBKqR+Jf9dX/b4r1i6vNFIqU1OUYwWmJqHd2cDIlfkziMu/w7VRzaD+6EAc1UUWYdOrNae72gEHLnOQz020AIx3T9VB0dNpxFQg+RJcue+aH5j0wDTM6yrQYTITHt6VDj306XMhVDsF79nhCnqJBZ73cUgSfoHaRKx8wzo+Q9R38pKx/fsiWETkTAt06H6tkkUdWIU79PbRprzbB58xQ/+GMc1kclz9WQwomZZO88sXJcD4JZzijjt6aW1rrrZwfVbtbq+uG04g+9j9nRXPHTuoSr1ZJ9wJQk5fdroPA4vOCeb4Ty1eEbkjBxtRWBsIBCouJJevXFbkbDnRrRm2L0d1Nl16LHAhykTKxsbXMuFjbTcfmxV11IYW1aA05ipsydt3U1i+SVmpbPoVvMh3xdXapcSad4MOMNmBvssmBfQYbo4g2leGkRsqe1VYqVAk3wk=", "source_app_channel": "oppo", "source_platform": "ad", "step": "935197360", "step2": "1258952318", "udid": "04ce2812d5a2e7ce"}, "seed": "9955d141-484e-43d7-a294-ab3d61b57d54", "sign": "QZkO5onyZb2JogFKKZDERw=="}
        #'{"sauth_json":"{\"gameid\":\"x19\",\"login_channel\":\"netease\",\"app_channel\":\"netease\",\"platform\":\"pc\",\"sdkuid\":\"aebghyp735z2qlby\",\"sessionid\":\"1-eyJzaSI6ICI4OTA0MzZkN2ZlYmRiMzgzMzJlMjNlYjQyMmQ3ZGQ3ZjIzMjYxMDBiIiwgImdfaSI6ICJhZWNmcnhvZHlxYWFhYWpwIiwgInMiOiAiNDNibXcycXQ2aHdwaTc4cTQycnZreWV5bmdxdHVpemIiLCAidSI6ICJhZWJnaHlwNzM1ejJxbGJ5IiwgInQiOiAyfSAg\",\"sdk_version\":\"3.4.0\",\"udid\":\"a243fab73cee4827a0a2f0b0edb5c10a\",\"deviceid\":\"amawhyiaanju6a2w-d\",\"aim_info\":\"{\\\"aim\\\":\\\"100.100.100.100\\\",\\\"country\\\":\\\"CN\\\",\\\"tz\\\":\\\"+0800\\\",\\\"tzid\\\":\\\"\\\"}\"}"}'
        return json.dumps({
            "sauth_json": json.dumps({
#                "timestamp": sdk_login_data.get("time"),
#                "userid": sdk_login_data.get("username"),
                "realname": json.dumps({
                    "realname_type": "0"
                }, separators=(',', ':')),
                "gameid": "x19",
                "login_channel": sauth["login_channel"],
                "app_channel": sauth["app_channel"],
                "platform": sauth["platform"],
                "sdkuid": sauth["sdkuid"],
                "sessionid": sauth["sessionid"],
                "sdk_version": "1.0.0",
                "udid": sauth["udid"],
                "deviceid": self.__generate_random_string(32, "0123456789ABCDEF"),
                "aim_info": json.dumps({
                    "aim": "100.100.100.100",
                    "country": "CN",
                    "tz": "+0800",
                    "tzid": ""
                }, separators=(',', ':')),
                "client_login_sn": sauth["client_login_sn"],
                "gas_token": "",
                "source_platform": "ad",
                "ip": "0.0.0.0"
            }, separators=(',', ':'))
        }, separators=(',', ':'))