import sdwan,pytest

# Fixures are executed on each test function and are suited for repetitive operations (data input and initializations)
# in these tests we have fixture for correct input data and wrong input data (wrong username)
# three operations are performed
# 1) remove SSL certificate warnings from requests library (imported through sdwan.py script)
# 2) create a data dictionary with all parameters for the main functions of sdwan.py and return to the calling function
# 3) instantiate a new session object from requests library, this will be returned and used by every test function
# NOTE : SDWAN requires a persistent session object across all tests (Cookies and XSFR token), to achieve this
#        is necessary to use the [scope = 'module'] parameter for the fixture 
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

# Test login function
# NOTE: we are passing the <correctdata> function in input that returns the session object and the input data structure
#       and to use it in the sdwanlogin function (that accept two parameters) we are UNPACKING it, meaning that the two returned
#       values are used as input parameters individually
def test_sdwanlogin_OK(correctdata):
    assert sdwan.sdwanlogin(*correctdata) == ""
    print(correctdata[0].cookies.get_dict())

def test_sdwanlogin_KO(wrongdatauser):
    assert sdwan.sdwanlogin(*wrongdatauser) != ""

def test_sdwantoken_OK(correctdata):
    print(correctdata[0].cookies.get_dict())
    assert sdwan.sdwantoken(*correctdata).split("\n")[0] != "<html>"

def test_sdwantoken_KO(wrongdatauser):
    assert sdwan.sdwantoken(*wrongdatauser).split("\n")[0] == "<html>"

def test_sdwanlistdevices_OK(correctdata):
    assert sdwan.sdwanlistdevices(*correctdata).split("\n")[0] != "<html>"

def test_sdwanlistdevices_KO(wrongdatauser):
    assert sdwan.sdwanlistdevices(*wrongdatauser).split("\n")[0] == "<html>"

