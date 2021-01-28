import requests
import datetime
import time
import uuid
import base64
import hashlib
import xmltodict
import json


def get_default_gateway_ip(ip):
    if ip is not None and len(ip) > 0:
        ips = ip.split(".")
        if len(ips) == 4:
            return ips[0] + "." + ips[1] + "." + ips[2] + ".1"
        else:
            return None
    else:
        return None


def get_device_time(device_ip):
    try:
        header_value = {
            "Content-Type": 'application/soap+xml; charset=utf-8; action="http://www.onvif.org/ver10/device/wsdl/GetSystemDateAndTime"'
        }
        data_value = '''<s:Envelope
    xmlns:s="http://www.w3.org/2003/05/soap-envelope">
    <s:Header>
    </s:Header>
    <s:Body
        xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
        xmlns:xsd="http://www.w3.org/2001/XMLSchema">
        <GetSystemDateAndTime
            xmlns="http://www.onvif.org/ver10/device/wsdl"/>
        </s:Body>
</s:Envelope>'''
        result = requests.post(
            "http://" + device_ip + "/onvif/device_service", headers=header_value,
            data=data_value, timeout=5)
        content = str(result.content, encoding="utf-8")
        if "404 Not Found" in content:
            result = requests.post(
                "http://" + device_ip + ":8080/onvif/device_service", headers=header_value,
                data=data_value, timeout=5)
            content = str(result.content, encoding="utf-8")
        return content
    except Exception as e:
        print(device_ip + " get time error")
        print(e)
        return 'failed'


def generate_digest_password(device_ip, password):
    result = get_device_time(device_ip)
    print(result)
    xmlparse = xmltodict.parse(result)

    jsonstr = json.dumps(xmlparse, indent=1)
    json_data = json.loads(jsonstr, strict=False)
    if "s:Envelope" in jsonstr:
        year = int(
            json_data["s:Envelope"]["s:Body"]["tds:GetSystemDateAndTimeResponse"]["tds:SystemDateAndTime"][
                "tt:UTCDateTime"][
                "tt:Date"]["tt:Year"])
        month = int(
            json_data["s:Envelope"]["s:Body"]["tds:GetSystemDateAndTimeResponse"]["tds:SystemDateAndTime"][
                "tt:UTCDateTime"][
                "tt:Date"]["tt:Month"])
        day = int(
            json_data["s:Envelope"]["s:Body"]["tds:GetSystemDateAndTimeResponse"]["tds:SystemDateAndTime"][
                "tt:UTCDateTime"][
                "tt:Date"]["tt:Day"])
        hour = int(
            json_data["s:Envelope"]["s:Body"]["tds:GetSystemDateAndTimeResponse"]["tds:SystemDateAndTime"][
                "tt:UTCDateTime"][
                "tt:Time"]["tt:Hour"])
        minute = int(
            json_data["s:Envelope"]["s:Body"]["tds:GetSystemDateAndTimeResponse"]["tds:SystemDateAndTime"][
                "tt:UTCDateTime"][
                "tt:Time"]["tt:Minute"])
        second = int(
            json_data["s:Envelope"]["s:Body"]["tds:GetSystemDateAndTimeResponse"]["tds:SystemDateAndTime"][
                "tt:UTCDateTime"][
                "tt:Time"]["tt:Second"])
    else:
        year = int(
            json_data["SOAP-ENV:Envelope"]["SOAP-ENV:Body"]["tds:GetSystemDateAndTimeResponse"][
                "tds:SystemDateAndTime"][
                "tt:UTCDateTime"][
                "tt:Date"]["tt:Year"])
        month = int(
            json_data["SOAP-ENV:Envelope"]["SOAP-ENV:Body"]["tds:GetSystemDateAndTimeResponse"][
                "tds:SystemDateAndTime"][
                "tt:UTCDateTime"][
                "tt:Date"]["tt:Month"])
        day = int(
            json_data["SOAP-ENV:Envelope"]["SOAP-ENV:Body"]["tds:GetSystemDateAndTimeResponse"][
                "tds:SystemDateAndTime"][
                "tt:UTCDateTime"][
                "tt:Date"]["tt:Day"])
        hour = int(
            json_data["SOAP-ENV:Envelope"]["SOAP-ENV:Body"]["tds:GetSystemDateAndTimeResponse"][
                "tds:SystemDateAndTime"][
                "tt:UTCDateTime"][
                "tt:Time"]["tt:Hour"])
        minute = int(
            json_data["SOAP-ENV:Envelope"]["SOAP-ENV:Body"]["tds:GetSystemDateAndTimeResponse"][
                "tds:SystemDateAndTime"][
                "tt:UTCDateTime"][
                "tt:Time"]["tt:Minute"])
        second = int(
            json_data["SOAP-ENV:Envelope"]["SOAP-ENV:Body"]["tds:GetSystemDateAndTimeResponse"][
                "tds:SystemDateAndTime"][
                "tt:UTCDateTime"][
                "tt:Time"]["tt:Second"])
    cam_date = datetime.datetime(year, month, day, hour, minute, second)
    print(cam_date)
    dt_diff = cam_date - datetime.datetime.utcnow()
    print(dt_diff)
    dt_adjusted = str(dt_diff + datetime.datetime.utcnow()).replace(" ", "T") + 'Z'

    nonce = base64.b64encode(uuid.uuid4().bytes).decode('utf-8')

    nonce_en = nonce.encode("utf-8")
    timestamp_en = dt_adjusted.encode("utf-8")
    password = password.encode("utf-8")

    nonce_d = base64.standard_b64decode(nonce_en)
    c_sha = hashlib.sha1()
    c_sha.update(nonce_d + timestamp_en + password)
    c_sha1 = c_sha.digest()
    pwd_digest = base64.b64encode(c_sha1).decode('utf-8')
    print(nonce, dt_adjusted, pwd_digest)
    return nonce, dt_adjusted, pwd_digest


def update_device_default_gateway(device_ip, username, password, gateway_ip):
    try:

        nonce, timestamp, pwd_digest = generate_digest_password(device_ip, password)

        header_value = {
            "Content-Type": 'application/soap+xml; charset=utf-8; action="http://www.onvif.org/ver10/device/wsdl/SetNetworkDefaultGateway"',
            "Accept-Encoding": 'gzip, deflate'
        }
        data_value = '''<s:Envelope
    xmlns:s="http://www.w3.org/2003/05/soap-envelope">
    <s:Header>
        <Security s:mustUnderstand="1"
            xmlns="http://docs.oasis-open.org/wss/2004/01/oasis-200401-wss-wssecurity-secext-1.0.xsd">
            <UsernameToken>
                <Username>''' + str(username).strip() + '''</Username>
                <Password Type="http://docs.oasis-open.org/wss/2004/01/oasis-200401-wss-username-token-profile-1.0#PasswordDigest">''' + str(
            pwd_digest).strip() + '''</Password>
                <Nonce EncodingType="http://docs.oasis-open.org/wss/2004/01/oasis-200401-wss-soap-message-security-1.0#Base64Binary">''' + str(
            nonce).strip() + '''</Nonce>
                <Created
                    xmlns="http://docs.oasis-open.org/wss/2004/01/oasis-200401-wss-wssecurity-utility-1.0.xsd">''' + str(
            timestamp).strip() + '''</Created>
            </UsernameToken>
        </Security>
    </s:Header>
    <s:Body
        xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
        xmlns:xsd="http://www.w3.org/2001/XMLSchema">
        <SetNetworkDefaultGateway
            xmlns="http://www.onvif.org/ver10/device/wsdl">
            <IPv4Address>''' + str(gateway_ip).strip() + '''</IPv4Address>
        </SetNetworkDefaultGateway>
    </s:Body>
</s:Envelope>'''
        print(data_value)
        result = requests.post(
            "http://" + device_ip + "/onvif/device_service", headers=header_value,
            data=data_value, timeout=5)
        content = str(result.content, encoding="utf-8")
        if "404 Not Found" in content:
            result = requests.post(
                "http://" + device_ip + ":8080/onvif/device_service", headers=header_value,
                data=data_value, timeout=5)
            content = str(result.content, encoding="utf-8")
        print(content)
        if len(content) != 0:
            if 'SetNetworkDefaultGatewayResponse' in content:
                print(device_ip + " update gateway success")
                return 'success'
            else:
                print(device_ip + " update gateway failed")
                return 'failed'
        else:
            print(device_ip + " update gateway content length is 0")
            return 'failed'
    except Exception as e:
        print(device_ip + " update gateway error")
        print(e)
        return 'failed'


def update_device_ip(device_ip, username, password, new_ip):
    try:
        nonce, timestamp, pwd_digest = generate_digest_password(device_ip, password)
        header_value = {
            "Content-Type": 'application/soap+xml; charset=utf-8; action="http://www.onvif.org/ver10/device/wsdl/SetNetworkInterfaces"',
            "Accept-Encoding": 'gzip, deflate'
        }
        data_value = '''<s:Envelope
    xmlns:s="http://www.w3.org/2003/05/soap-envelope">
    <s:Header>
        <Security s:mustUnderstand="1"
            xmlns="http://docs.oasis-open.org/wss/2004/01/oasis-200401-wss-wssecurity-secext-1.0.xsd">
            <UsernameToken>
                <Username>''' + str(username).strip() + '''</Username>
                <Password Type="http://docs.oasis-open.org/wss/2004/01/oasis-200401-wss-username-token-profile-1.0#PasswordDigest">''' + str(
            pwd_digest).strip() + '''</Password>
                <Nonce EncodingType="http://docs.oasis-open.org/wss/2004/01/oasis-200401-wss-soap-message-security-1.0#Base64Binary">''' + str(
            nonce).strip() + '''</Nonce>
                <Created
                    xmlns="http://docs.oasis-open.org/wss/2004/01/oasis-200401-wss-wssecurity-utility-1.0.xsd">''' + str(
            timestamp).strip() + '''</Created>
            </UsernameToken>
        </Security>
    </s:Header>
    <s:Body
        xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
        xmlns:xsd="http://www.w3.org/2001/XMLSchema">
        <SetNetworkInterfaces
            xmlns="http://www.onvif.org/ver10/device/wsdl">
            <InterfaceToken>eth0</InterfaceToken>
            <NetworkInterface>
                <Enabled
                    xmlns="http://www.onvif.org/ver10/schema">true</Enabled>
                <MTU
                    xmlns="http://www.onvif.org/ver10/schema">1500</MTU>
                <IPv4
                    xmlns="http://www.onvif.org/ver10/schema">
                    <Enabled>true</Enabled>
                    <Manual>
                        <Address>''' + str(new_ip).strip() + '''</Address>
                        <PrefixLength>24</PrefixLength>
                    </Manual>
                    <DHCP>false</DHCP>
                </IPv4>
            </NetworkInterface>
        </SetNetworkInterfaces>
    </s:Body>
</s:Envelope>'''
        print(data_value)
        result = requests.post(
            "http://" + device_ip + "/onvif/device_service", headers=header_value,
            data=data_value, timeout=5)
        content = str(result.content, encoding="utf-8")
        if "404 Not Found" in content:
            result = requests.post(
                "http://" + device_ip + ":8080/onvif/device_service", headers=header_value,
                data=data_value, timeout=5)
            content = str(result.content, encoding="utf-8")
        print(content)
        if len(content) != 0:
            if 'SetNetworkInterfacesResponse' in content:
                print(device_ip + " update ip success")
                return 'success'
            else:
                print(device_ip + " update ip failed")
                return 'failed'
        else:
            print(device_ip + " update ip content length is 0")
            return 'failed'
    except Exception as e:
        print(device_ip + " update ip error")
        print(e)
        return 'failed'


def update_ip(device_ip, username, password, new_ip, gateway_ip):
    try:
        # gateway_ip = get_default_gateway_ip(new_ip)
        if gateway_ip is not None:
            result = update_device_default_gateway(device_ip, username, password, gateway_ip)
            if result == 'success':
                return update_device_ip(device_ip, username, password, new_ip)
            elif result == 'failed':
                print("update_device_default_gateway failed")
                return 'failed'
        else:
            print("gateway_ip is None")
            return 'failed'

    except Exception as e:
        print("update_ip error")
        print(e)
        return 'failed'


def get_posix_timezone(n_zone):
    if n_zone == '-12:00':
        now_zone = "AOE12"
    elif n_zone == '-11:00':
        now_zone = "NUT11"
    elif n_zone == '-10:00':
        now_zone = "HST11HDT,M3.2.0/2:00:00,M11.1.0/2:00:00"
    elif n_zone == '-09:30':
        now_zone = "MART9:30,M3.2.0/2:00:00,M11.1.0/2:00:00"
    elif n_zone == '-09:00':
        now_zone = "ASKT9AKDT,M3.2.0/2:00:00,M11.1.0/2:00:00"
    elif n_zone == '-08:00':
        now_zone = "PST8PDT,M3.2.0/2:00:00,M11.1.0/2:00:00"
    elif n_zone == '-07:00':
        now_zone = "MST7MDT,M3.2.0/2:00:00,M11.1.0/2:00:00"
    elif n_zone == '-06:00':
        now_zone = "CST6CDT,M3.2.0/2:00:00,M11.1.0/2:00:00"
    elif n_zone == '-06:00':
        now_zone = "EST5EDT,M3.2.0/2:00:00,M11.1.0/2:00:00"
    elif n_zone == '-03:00':
        now_zone = "ART3"
    elif n_zone == '-02:30':
        now_zone = "NDT3:30NST,M3.2.0/2:00:00,M11.1.0/2:00:00"
    elif n_zone == '-02:00':
        now_zone = "WGST3WGT,M3.2.0/2:00:00,M11.1.0/2:00:00"
    elif n_zone == '-01:00':
        now_zone = "CVT1"
    elif n_zone == '00:00':
        now_zone = "GMT"
    elif n_zone == '+01:00':
        now_zone = "BST0GMT,M3.2.0/2:00:00,M11.1.0/2:00:00"
    elif n_zone == '+02:00':
        now_zone = "CEST-1CET,M3.2.0/2:00:00,M11.1.0/2:00:00"
    elif n_zone == '+03:00':
        now_zone = "MSK-3"
    elif n_zone == '+04:00':
        now_zone = "GST-4"
    elif n_zone == '+04:30':
        now_zone = "IRDT-3:30IRST,M3.2.0/2:00:00,M11.1.0/2:00:00"
    elif n_zone == '+05:00':
        now_zone = "UZT-5"
    elif n_zone == '+05:30':
        now_zone = "IST-5:30"
    elif n_zone == '+05:45':
        now_zone = "NPT-5:45"
    elif n_zone == '+06:00':
        now_zone = "BST-6"
    elif n_zone == '+06:30':
        now_zone = "MMT-6:30"
    elif n_zone == '+07:00':
        now_zone = "WIB-7"
    elif n_zone == '+08:00':
        now_zone = "CST-8"
    elif n_zone == '+08:45':
        now_zone = "ACWST-8:45"
    elif n_zone == '+09:00':
        now_zone = "JST-9"
    elif n_zone == '+09:30':
        now_zone = "ACST-8:30ACDT,M3.2.0/2:00:00,M11.1.0/2:00:00"
    elif n_zone == '+10:00':
        now_zone = "AEST-9AEDT,M3.2.0/2:00:00,M11.1.0/2:00:00"
    elif n_zone == '+10:30':
        now_zone = "LHST-9:30LHDT,M3.2.0/2:00:00,M11.1.0/2:00:00"
    elif n_zone == '+11:00':
        now_zone = "SBT-11"
    elif n_zone == '+12:00':
        now_zone = "ANAT-12"
    elif n_zone == '+12:45':
        now_zone = "CHAST-11:45CHADT,M3.2.0/2:00:00,M11.1.0/2:00:00"
    elif n_zone == '+13:00':
        now_zone = "TOT-12TOST,M3.2.0/2:00:00,M11.1.0/2:00:00"
    elif n_zone == '+14:00':
        now_zone = "LINT-14"
    else:
        now_zone = "GMT"
    return now_zone


def update_device_time(device_ip, username, password):
    try:
        now_local = datetime.datetime.now(datetime.timezone.utc).astimezone()
        now_utc = datetime.datetime.now(datetime.timezone.utc)
        n_zone = str(now_local)[-6:]
        now_zone = get_posix_timezone(n_zone)

        nonce, timestamp, pwd_digest = generate_digest_password(device_ip, password)

        header_value = {
            "Content-Type": 'application/soap+xml; charset=utf-8; action="http://www.onvif.org/ver10/device/wsdl/SetSystemDateAndTime"'
        }
        data_value = '''<s:Envelope
    xmlns:s="http://www.w3.org/2003/05/soap-envelope">
    <s:Header>
        <Security s:mustUnderstand="1"
            xmlns="http://docs.oasis-open.org/wss/2004/01/oasis-200401-wss-wssecurity-secext-1.0.xsd">
            <UsernameToken>
                <Username>''' + str(username).strip() + '''</Username>
                <Password Type="http://docs.oasis-open.org/wss/2004/01/oasis-200401-wss-username-token-profile-1.0#PasswordDigest">''' + str(
            pwd_digest).strip() + '''</Password>
                <Nonce EncodingType="http://docs.oasis-open.org/wss/2004/01/oasis-200401-wss-soap-message-security-1.0#Base64Binary">''' + str(
            nonce).strip() + '''</Nonce>
                <Created
                    xmlns="http://docs.oasis-open.org/wss/2004/01/oasis-200401-wss-wssecurity-utility-1.0.xsd">''' + str(
            timestamp).strip() + '''</Created>
            </UsernameToken>
        </Security>
    </s:Header>
    <s:Body
        xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
        xmlns:xsd="http://www.w3.org/2001/XMLSchema">
        <SetSystemDateAndTime
            xmlns="http://www.onvif.org/ver10/device/wsdl">
            <DateTimeType>Manual</DateTimeType>
            <DaylightSavings>''' + str('true' if time.localtime().tm_isdst == 1 else 'false') + '''</DaylightSavings>
            <TimeZone>
                <TZ
                    xmlns="http://www.onvif.org/ver10/schema">''' + now_zone + '''</TZ>
            </TimeZone>
            <UTCDateTime>
                <Time
                    xmlns="http://www.onvif.org/ver10/schema">
                    <Hour>''' + str(now_utc.hour) + '''</Hour>
                    <Minute>''' + str(now_utc.minute) + '''</Minute>
                    <Second>''' + str(now_utc.second) + '''</Second>
                </Time>
                <Date
                    xmlns="http://www.onvif.org/ver10/schema">
                    <Year>''' + str(now_utc.year) + '''</Year>
                    <Month>''' + str(now_utc.month) + '''</Month>
                    <Day>''' + str(now_utc.day) + '''</Day>
                </Date>
            </UTCDateTime>
        </SetSystemDateAndTime>
    </s:Body>
</s:Envelope>'''
        print(data_value)
        result = requests.post(
            "http://" + device_ip + "/onvif/device_service", headers=header_value,
            data=data_value, timeout=5)
        content = str(result.content, encoding="utf-8")
        if "404 Not Found" in content:
            result = requests.post(
                "http://" + device_ip + ":8080/onvif/device_service", headers=header_value,
                data=data_value, timeout=5)
            content = str(result.content, encoding="utf-8")
        print(content)
        if len(content) != 0:
            if 'SetSystemDateAndTimeResponse' in content:
                print(device_ip + " update time success")
                return 'success'
            else:
                print(device_ip + " update time failed")
                return 'failed'
        else:
            print(device_ip + " update time content length is 0")
            return 'failed'
    except Exception as e:
        print(device_ip + " update time error")
        print(e)
        return 'failed'
