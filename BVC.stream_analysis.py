import requests,threading
from socketIO_client import SocketIO, LoggingNamespace

requests.packages.urllib3.disable_warnings()


def results(*args):
    print("\r\n",  args )

def post(recordingId,headers,wavdata,e):
    r =requests.post("https://apiv3.beyondverbal.com/v3/recording/"+recordingId,data=wavdata, verify=False, headers=headers)
    e.set()
    #print result full analysis : 
    #print(r.json())

def analyze(API_Key,wavdata):
    with SocketIO("http://analysis.beyondverbal.com", 80, LoggingNamespace) as socketIO:
        e = threading.Event()
        res = requests.post("https://token.beyondverbal.com/token",data={"grant_type":"client_credentials","apiKey":API_Key},verify=False)
        token = res.json()['access_token']
        headers={"Authorization":"Bearer "+token}
        pp = requests.post("https://apiv3.beyondverbal.com/v3/recording/start",json={"dataFormat": { "type":"WAV" }},verify=False,headers=headers)
        recordingId = pp.json()['recordingId']
        socketIO.on('update', results)
        socketIO.emit('join', recordingId)
        my_thread = threading.Thread(target=post, name="post", args=(recordingId,headers,wavdata,e))
        my_thread.start()
        socketIO.wait(seconds=5)
        while not e.is_set():
            socketIO.wait(seconds=1)
        socketIO._close()
        
    
#read data from file or other sorce
with open("C:\\FilePath.wav",'rb') as wavdata: 
   analyze("Put API Key",wavdata)
