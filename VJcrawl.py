import os
import requests
import json
import time

timeWait = 0
uname = 'your username here'
unickname = 'your nickname here'
upsw = 'your password here'

strSuc = 'success'
strFai = 'Username/Email and password don\'t match!'


trueHeaders1 = {
    'accept': '*/*',
    'accept-encoding': 'gzip, deflate, br',
    'accept-language': 'zh-CN,zh;q=0.9',
    'origin': 'https://vjudge.net',
    'referer': 'https//vjudge.net/status',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36',
    'x-requested-with': 'XMLHttpRequest'
}
trueHeaders2 = {
    'accept': '*/*',
    'accept-encoding': 'gzip, deflate, br',
    'accept-language': 'zh-CN,zh;q=0.9',
    'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'origin': 'https://vjudge.net',
    'referer': 'https//vjudge.net/status',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36',
    'x-requested-with': 'XMLHttpRequest'
}
trueHeaders3 = {
    'accept': 'application/json, text/javascript, */*; q=0.01',
    'accept-encoding': 'gzip, deflate, br',
    'accept-language': 'zh-CN,zh;q=0.9',
    'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'origin': 'https://vjudge.net',
    'referer': 'https://vjudge.net/status',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36',
    'x-requested-with': 'XMLHttpRequest'
}
trueFromData3 = 'draw=1&columns[0][data]=0&columns[0][name]=&columns[0][searchable]=true&columns[0][orderable]=false&columns[0][search][value]=&columns[0][search][regex]=false&columns[1][data]=1&columns[1][name]=&columns[1][searchable]=true&columns[1][orderable]=false&columns[1][search][value]=&columns[1][search][regex]=false&columns[2][data]=2&columns[2][name]=&columns[2][searchable]=true&columns[2][orderable]=false&columns[2][search][value]=&columns[2][search][regex]=false&columns[3][data]=3&columns[3][name]=&columns[3][searchable]=true&columns[3][orderable]=false&columns[3][search][value]=&columns[3][search][regex]=false&columns[4][data]=4&columns[4][name]=&columns[4][searchable]=true&columns[4][orderable]=false&columns[4][search][value]=&columns[4][search][regex]=false&columns[5][data]=5&columns[5][name]=&columns[5][searchable]=true&columns[5][orderable]=false&columns[5][search][value]=&columns[5][search][regex]=false&columns[6][data]=6&columns[6][name]=&columns[6][searchable]=true&columns[6][orderable]=false&columns[6][search][value]=&columns[6][search][regex]=false&columns[7][data]=7&columns[7][name]=&columns[7][searchable]=true&columns[7][orderable]=false&columns[7][search][value]=&columns[7][search][regex]=false&columns[8][data]=8&columns[8][name]=&columns[8][searchable]=true&columns[8][orderable]=false&columns[8][search][value]=&columns[8][search][regex]=false&columns[9][data]=9&columns[9][name]=&columns[9][searchable]=true&columns[9][orderable]=false&columns[9][search][value]=&columns[9][search][regex]=false&start=0&length=20&search[value]=&search[regex]=false&un='+unickname+'&OJId=All&probNum=&res=0&language=&onlyFollowee=false'

trueHeaders4 = {
    'accept': '*/*',
    'accept-encoding': 'gzip, deflate, br',
    'accept-language': 'zh-CN,zh;q=0.9',
    'origin': 'https://vjudge.net',
    'referer': 'https://vjudge.net/status',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36',
    'x-requested-with': 'XMLHttpRequest'
}


def formtodict(data: str, **setting):
    ret = {}
    for ele in data.split('&'):
        ret[ele.split('=')[0]] = ele.split('=')[1]
    for ele in setting.keys():
        ret[ele] = setting[ele]
    return ret


# steps
'''
[
    {
        url:xxxxxxxxxxxxx,
        headers:xxxxxxxxx,
        data:xxxxxxxxxxxx
    },
    {

    }
]
'''
steps = []
steps.append({'url': 'https://vjudge.net/user/checkLogInStatus',
              'headers': trueHeaders1, 'data': ''})
steps.append({'url': 'https://vjudge.net/user/login',
              'headers': trueHeaders2, 'data': 'username='+uname+'&password='+upsw})


def logIn(steps: list) -> dict:
    cookie = {}
    for step in steps:
        time.sleep(timeWait)
        res = requests.post(
            url=step['url'],
            headers=step['headers'],
            cookies=cookie,
            data=step['data'],
        )
    cookie = dict(cookie, **res.cookies)
    return cookie


def getList():
    result = list()
    for page in range(1, 10000):
        print('Dowloading:              Page#'+str(page), end='')
        if page % 5 == 1:
            cookie = logIn(steps)
        formData3 = formtodict(trueFromData3, un=unickname,
                               draw=page + 1, length=20, start=(page-1)*20)
        res3 = requests.post(url='https://vjudge.net/status/data',
                             headers=trueHeaders3, cookies=cookie, data=formData3)
        statusList = json.loads(res3.text)['data']

        print('----------->', len(statusList), ' records')
        if len(statusList) == 0:
            break
        else:
            result.extend(statusList)
    return result


# given statuslist
def getDetail():
    cookie = logIn(steps)
    for index in range(0, len(statusList)):
        time.sleep(timeWait)
        status = statusList[index]
        runId = status['runId']
        while True:
            print(time.localtime())
            nRetry = 0
            try:
                res4 = requests.post(
                    url="https://vjudge.net/solution/data/"+str(runId),
                    headers=trueHeaders4,
                    cookies=cookie,
                )
                break
            except:
                nRetry += 1
                print("failed ", nRetry, " times.")
                if nRetry % 5 == 0:
                    cookie = logIn(steps)
                    print('reloged')
        status['detail'] = json.loads(res4.text)
        print('Downloading:', runId, '               ',
              index, '/', len(statusList))


def printToFolders():
    statusList = eval(open('detailList.json', 'r').read())
    writePath = os.path.abspath('.\\code\\')
    for status in statusList:
        mypath = writePath+'\\'+status['oj']+'\\'+status['probNum']+'\\'
        filename = '%s_%d.cpp' % (status['status'], status['runId'])
        if not os.path.exists(mypath):
            os.makedirs(mypath)
        code = status['detail'].pop('code')
        with open(mypath+filename, 'w') as fin:
            fin.write('/*\n')
            fin.write(json.dumps(status['detail'], indent=2))
            fin.write('\n*/\n')
            fin.write(code)


if __name__ == '__main__':

    # get list
    statusList = getList()

    # save list
    open('statusList.json', 'w').write(str(statusList))

    # read list
    statusList = eval(open('statusList.json', 'r').read())

    # get detail
    getDetail()

    #save detail
    open('detailList.json','w').write(str(statusList))

    #read detail
    statusList=eval(open('detailList.json').read())

    # print detail
    printToFolders()
