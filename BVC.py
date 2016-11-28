import requests 
requests.packages.urllib3.disable_warnings()

def getAnalysis(API_Key,WavPath):
    res = requests.post("https://token.beyondverbal.com/token",data={"grant_type":"client_credentials","apiKey":API_Key})
    token = res.json()['access_token']
    print(token)
    headers={"Authorization":"Bearer "+token}
    pp = requests.post("https://apiv3.beyondverbal.com/v3/recording/start",json={"dataFormat": { "type":"WAV" }},verify=False,headers=headers)
    print(pp.status_code)
    recordingId = pp.json()['recordingId']
    with open(WavPath,'rb') as wavdata:
        r = requests.post("https://apiv3.beyondverbal.com/v3/recording/"+recordingId,data=wavdata, verify=False, headers=headers)
        print(r.status_code)
        print(r.json())
        return r.json()


getAnalysis("API Key","C:\\YouFilePath.wav")
