'''
This program will test SDWAN connection and REST API function to
SDWAN Devnet SANDBOX (no Python SDK)
'''
import requests
import urllib3

# requests.session creates an object that has all the features of a
# traditional "requests" object but retain information
# about the TCP connection and HTTP parameters (like authentication and COOKIES)

def sdwanlogin(session,inputdata):
    '''
    https://developer.cisco.com/docs/sdwan/#!authentication/how-to-authenticate
    Authentication to Cisco SDWAN (Viptela) is against the vManage orchestrator
    with a series of steps
    1) pass the authentication credentials in the body and retrive JSESSIONID Cookie credentials
       can be passed as a dictionary of two elements or a single element (commented below)
    2) Request a Cross site forgery request token (XSRF Token) that is required for POST operations
       with the JSESSIONID Cookie reusing the same session (carrying JESSIONID cookie) we can
       request an XSRF token that will be returned in the BODY of the response (if successful)
    3) Once Cookie is retained and the XSRF token is obtained, is possible to make requests
       to the vManage via REST API for both POST and GET operations
    '''
    # Step 1 --- Authentication
    response = session.post(f"{inputdata['baseurl']}{inputdata['securitycheckurl']}",
            headers={"Content-Type":"application/x-www-form-urlencoded"},
            data={"j_username":inputdata['username'],"j_password":inputdata['password']},
            verify=False)
    return response.text

def sdwantoken(session,inputdata):
    '''
    Step 2 --- Retrieve XSRF token and update the session headers to include it in future
               requests (cookie JESSIONID is retained)
    '''
    response = session.get(f"{inputdata['baseurl']}{inputdata['tokenurl']}",
            headers={"Content-Type":"application/json"},
            verify=False)
    xsrftoken = response.text
    session.headers.update({"X-XSRF-TOKEN":xsrftoken})
    return xsrftoken

def sdwanlistdevices(session,inputdata):
    '''
    Step 3 --- Execute requests (retrieve device list from vManage)
    '''
    try:
        response = session.get(f"{inputdata['baseurl']}{inputdata['devicelisturl']}",verify=False)
    except Exception:
        return "<html>"

    # Retrieve device list and print certain data for each device
    if response.text.split("\n")[0] != "<html>":
        devicelist = response.json()["data"]
        for device in devicelist:
            print(f"hostname: {device['host-name']:15} system IP: {device['system-ip']}")
    return response.text

if __name__ == "__main__":
    # Disable requests security warnings for SSL certificate
    urllib3.disable_warnings()

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
else:
    # Disable requests security warnings for SSL certificate
    urllib3.disable_warnings()
