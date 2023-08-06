import sys,os,requests,threading,time,json,subprocess
import threading

url = ''
number = ''
times = ''


def jibu():
    global url,times,number
    config = sys.argv
    config.pop(0)

    url = config[0]
    number = config[1]
    times = config[2]


    t1 = threading.Thread(target=locust)
    t2 = threading.Thread(target=getInfo)

    t1.start()
    t2.start()



def locust():
    try:
        global url,number
        cmd = 'locust -f _locust.py --host='+url
        subprocess.Popen(cmd, shell=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
    except:

        pass

def getInfo():
    global number,times
    for i in range(0,3):
        print(3-i)
        time.sleep(1)
        
    headers = {
        'Connection': 'keep-alive',
        'Host': 'localhost:8089',
        'Origin': 'http://localhost:8089',
        'Referer': 'http://localhost:8089/',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36',
        'X-Requested-With': 'XMLHttpRequest'
    }

    locustUrl = 'http://localhost:8089/swarm'
    RequestUrl = 'http://localhost:8089/stats/requests'
    Data = {
        'locust_count':number,
        'hatch_rate':'10'
    }

    response = requests.post(locustUrl,data=Data)

    while True:
        Response = requests.get(RequestUrl,headers = headers).text
        back =json.loads(Response)
        RequestTimes = str(back['stats'][0]['num_requests'])
        userCount = str(back['user_count'])
        median = str(back['stats'][0]['median_response_time'])
        failures = str(back['stats'][0]['num_failures'])
        success = str(int(RequestTimes) -int(failures)) 

        print('User_count:'+ userCount + ', Request_times:' +RequestTimes + ', Success:' + success + ', Failure:' + failures + ', MedianResponse_time:' + median)
        if int(RequestTimes) > int(times):
            print('finished ,please input 1-3 times Ctrl + C ')
            break
        time.sleep(2)
