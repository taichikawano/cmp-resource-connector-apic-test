import requests
import json
import sys

class Apicem():
    def __init__(self):
        self.ip =  "sandboxapic.cisco.com"
        self.username = "devnetuser"
        self.password = "Cisco123!"
        self.version = "v1"

apicem_config = Apicem()

requests.packages.urllib3.disable_warnings()

def get_X_auth_token(ip=apicem_config.ip,ver=apicem_config.version,uname=apicem_config.username,pword=apicem_config.password):
    """
    This function returns a new service ticket.
    Passing ip, version,username and password when use as standalone function
    to overwrite the configuration above.
    """

    # JSON input for the post ticket API request
    r_json = {
    "username": uname,
    "password": pword
    }
    # url for the post ticket API request
    post_url = "https://"+ip+"/api/"+ver+"/ticket"
    # All APIC-EM REST API query and response content type is JSON
    headers = {'content-type': 'application/json'}
    # POST request and response
    try:
        r = requests.post(post_url, data = json.dumps(r_json), headers=headers,verify=False)
        # remove '#' if need to print out response
        # print (r.text)

        # return service ticket
        return r.json()["response"]["serviceTicket"]
    except:
        # Something wrong, cannot get service ticket
        print ("Status: %s"%r.status_code)
        print ("Response: %s"%r.text)
        sys.exit ()

def get(ip=apicem_config.ip,ver=apicem_config.version,uname=apicem_config.username,pword=apicem_config.password,api='',params=''):
    """
    To simplify requests.get with default configuration.Return is the same as requests.get
    """
    ticket = get_X_auth_token()
    headers = {"X-Auth-Token": ticket}
    url = "https://"+ip+"/api/"+ver+"/"+api
    print ("\nExecuting GET '%s'\n"%url)
    try:
    # The request and response of "GET /network-device" API
        resp= requests.get(url,headers=headers,params=params,verify = False)
        return(resp)
    except:
       print ("Something wrong to GET /",api)
       sys.exit()

def post(ip=apicem_config.ip,ver=apicem_config.version,uname=apicem_config.username,pword=apicem_config.password,api='',data=''):
    """
    To simplify requests.post with default configuration.Return is the same as requests.post
    """
    ticket = get_X_auth_token()
    headers = {"content-type" : "application/json","X-Auth-Token": ticket}
    url = "https://"+ip+"/api/"+ver+"/"+api
    print ("\nExecuting POST '%s'\n"%url)
    try:
    # The request and response of "POST /network-device" API
        resp= requests.post(url,json.dumps(data),headers=headers,verify = False)
        return(resp)
    except:
       print ("Something wrong to POST /",api)
       sys.exit()

def put(ip=apicem_config.ip,ver=apicem_config.version,uname=apicem_config.username,pword=apicem_config.password,api='',data=''):
    """
    To simplify requests.put with default configuration.Return is the same as requests.put
    """
    ticket = get_X_auth_token()
    headers = {"content-type" : "application/json","X-Auth-Token": ticket}
    url = "https://"+ip+"/api/"+ver+"/"+api
    print ("\nExecuting PUT '%s'\n"%url)
    try:
    # The request and response of "PUT /network-device" API
        resp= requests.put(url,json.dumps(data),headers=headers,verify = False)
        return(resp)
    except:
       print ("Something wrong to PUT /",api)
       sys.exit()

def delete(ip=apicem_config.ip,ver=apicem_config.version,uname=apicem_config.username,pword=apicem_config.password,api='',params=''):
    """
    To simplify requests.delete with default configuration.Return is the same as requests.delete
    """
    ticket = get_X_auth_token()
    headers = {"X-Auth-Token": ticket,'content-type': 'application/json'}
    url = "https://"+ip+"/api/"+ver+"/"+api
    print ("\nExecuting DELETE '%s'\n"%url)
    try:
    # The request and response of "DELETE /network-device" API
        resp= requests.delete(url,headers=headers,params=params,verify = False)
        return(resp)
    except:
       print ("Something wrong to DELETE /",api)
       sys.exit()


def get_resources(event, context):
    
    r = context.api.get('/appliances')
    print(r.text)
    device = []
    
    try:
        # The request and response of "GET /network-device" API
        resp = get(api="network-device")
        status = resp.status_code
        print("Status: ",status)
        # Get the json-encoded content from response
        response_json = resp.json()
        # all network-device detail is in "response"
        device = response_json["response"]
    except:
        print ("Something wrong, cannot get network device information")
        sys.exit()
    
    print("OK")
        
    if status != 200:
        print ("Response status: %s,Something wrong !"%status)
        print (resp.text)
        sys.exit()
        
    if device == [] :   # response is empty, no network-device is discovered.
        print ("No network device found !")
        sys.exit()
        
    device_list = []
    
    for item in device:
        
        #[item["hostname"],item["managementIpAddress"],item["type"],item["id"]])

        tmp = {
            "id": item["id"],
            "type": "appliance", #"server", #
            "base": {
                "name": item["hostname"],
            },
            "metadata": {
                "location": "51.506001/-0.071521",
            },
            "details": {
                "appliance": {
                    "type_id": item["id"],
                }
            }
        }
        
        device_list.append(tmp)
        
    print(device_list)

    return device_list
