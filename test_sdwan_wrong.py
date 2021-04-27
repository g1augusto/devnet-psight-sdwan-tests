import sdwan,pytest
# Disable requests security warnings for SSL certificate

# requests.session creates an object that has all the features of a traditional "requests" object but retain information
# about the TCP connection and HTTP parameters (like authentication and COOKIES)

GOOD = 0
USERNAME = 1
BASE = 2
DEVICE = 3

 

@pytest.fixture(scope = 'module')
def correctdata():
    # Disable requests security warnings for SSL certificate
    sdwan.requests.packages.urllib3.disable_warnings()

    data = {"baseurl":"https://sandbox-sdwan-1.cisco.com",
            "securitycheckurl" : "/j_security_check",
            "tokenurl" : "/dataservice/client/token",
            "devicelisturl" : "/dataservice/device",
            "username" : "devnetuser",
            "password" : "RG!_Yw919_83"}

    return sdwan.requests.session(),data

@pytest.fixture(scope = 'module')
def wrongdatauser():
    # Disable requests security warnings for SSL certificate
    sdwan.requests.packages.urllib3.disable_warnings()

    data = {"baseurl":"https://sandbox-sdwan-1.cisco.com",
            "securitycheckurl" : "/j_security_check",
            "tokenurl" : "/dataservice/client/token",
            "devicelisturl" : "/dataservice/device",
            "username" : "devnetuse",
            "password" : "RG!_Yw919_83"}
    return sdwan.requests.session(),data


def test_sdwanlogin_OK(correctdata):
    assert sdwan.sdwanlogin(*correctdata) == ""
    print(correctdata[0].cookies.get_dict())

def test_sdwanlogin_KO(wrongdatauser):
    assert sdwan.sdwanlogin(*wrongdatauser) != ""

def test_sdwantoken_OK(correctdata):
    print(correctdata[0].cookies.get_dict())
    assert sdwan.sdwantoken(*correctdata).split("\n")[0] != "<html>"

def test_sdwantoken_KO(wrongdatauser):
    assert sdwan.sdwantoken(*wrongdatauser).split("\n")[0] != "<html>"

def test_sdwanlistdevices_OK(correctdata):
    assert sdwan.sdwanlistdevices(*correctdata).split("\n")[0] != "<html>"

def test_sdwanlistdevices_KO(wrongdatauser):
    assert sdwan.sdwanlistdevices(*wrongdatauser).split("\n")[0] != "<html>"

"""
def sdwanlistdevices(session,inputdata):

    # Step 3 --- Execute requests (retrieve device list from vManage)
    response = session.get(f"{inputdata['baseurl']}{inputdata['devicelisturl']}",verify=False)

    # Retrieve device list and print certain data for each device
    devicelist = response.json()["data"]
    for device in devicelist:
        print(f"hostname: {device['host-name']:15} system IP: {device['system-ip']}")

if __name__ == "__main__":
    data = {"baseurl":"https://sandbox-sdwan-1.cisco.com",
            "securitycheckurl" : "/j_security_check",
            "tokenurl" : "/dataservice/client/token",
            "devicelisturl" : "/dataservice/device",
            "username" : "devnetuser",
            "password" : "RG!_Yw919_83"}
    mysession = requests.session()
    sdwanlogin(mysession,data)
    sdwantoken(mysession,data)
    sdwanlistdevices(mysession,data)
"""
