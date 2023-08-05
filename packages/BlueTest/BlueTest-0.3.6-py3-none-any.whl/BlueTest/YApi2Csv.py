import csv
import requests
from parm import *


class Api2Csv():
    def __init__(self,projects,csvname,apipath,api_user,api_pwd,project_url,login_path,user,pwd,tmp):
        self.start = True
        self.projects = projects  #项目id
        self.csvname = csvname  #写入的csv文件名称
        self.apipath = apipath  #Yapi的域名
        self.api_user=api_user #Yapi登录用户名
        self.api_pwd=api_pwd #Yapi登录密码

        self.project_url = project_url  # 项目域名
        self.login_path=login_path  #项目登录path
        self.user=user  #项目登录用户名
        self.pwd=pwd  #项目登录密码
        self.tmp = tmp  #可能会缺少的path

    def getSession(self):
        s = requests.session()
        response = s.post(url=self.apipath + "/api/user/login_by_ldap",
                          data={'email': self.api_user, 'password': self.api_pwd})
        return s

    def interfaceList(self):  #根据项目id返回该项目下所有的接口
        interfaces = []
        for id in self.projects:
            rep = self.getSession().get(url=self.apipath+'/api/interface/list',
                        params={"page": 1, "limit": 20, "project_id": id})
            toatal_page = rep.json()['data']['total']
            for page in range(1, toatal_page + 1):
                response = self.getSession().get(url=self.apipath+'/api/interface/list',
                                 params={"page": page, "limit": 20, "project_id": id})
                data = response.json()['data']['list']
                for i in data:
                    interfaces.append(i['_id'])
        return interfaces

    def dataFreshGet(self):  #当请求方法为get时params的拼接方法
        req_query = self.response.json()['data']['req_query']
        UrlParams = ""
        for query in req_query:
            if 'example' not in str(query):
                UrlParams += query['name'] + '=' + '' + "&"
            if 'example' in str(query):
                UrlParams += query['name'] + '=' + query['example'] + "&"
        UrlParams = UrlParams[:-1]
        return UrlParams

    def dataFreshPost(self): #当请求方法为post时data的拼接方法
        Data = []
        req_body_form = self.response.json()['data']['req_body_form']
        for body in req_body_form:
            if 'example' in str(body):
                Data_Body = {"key": body["name"], "value": body["example"]}
                Data.append(Data_Body)
            if 'example' not in str(body):
                Data_Body = {"key": body["name"], "value": ""}
                Data.append(Data_Body)

    def writeCsv(self,data):  #写csv文件
        out = open("./srcdata/%s.csv" % self.csvname, 'a', newline='')
        csv_write = csv.writer(out, dialect='excel')
        if self.start:
            csv_write.writerow(csv_parm.CHINA_KEY)
            self.start = False
        csv_write.writerow(['START'])
        csv_write.writerow(csv_parm.KEY)
        csv_write.writerow(data)
        csv_write.writerow(['END'])
        print("write over")

    def writeSolo(self,id): #写单行数据
        self.response = self.getSession().get(self.apipath+'/api/interface/get', params={"id": id})
        self.Name = str(self.response.json()['data']['path']).split('/')[-1]
        self.path = self.tmp+ self.response.json()['data']['path']   # 有的接口返回path不完整，需加上 如/sale,/education
        self.ResualPath = '.'+ self.tmp + self.response.json()['data']['path']
        self.Method = self.response.json()['data']['method']
        self.Describe = self.response.json()['data']['title']
        self.Url = self.project_url + self.path
        Headers = self.header
        if self.Method == "GET":
            UrlParams = self.dataFreshGet()
            data = ['', '', self.Name, self.Describe, self.ResualPath, self.Method, self.Url, Headers, 'null',
                         'params', UrlParams, '']
        elif self.Method == "POST" or self.Method == "DELETE":
            Data = self.dataFreshPost()
            data = ['', '', self.Name, self.Describe, self.ResualPath, self.Method, self.Url, Headers, Data, 'params', '', '']
        else:
            raise Exception("Error")
        self.writeCsv(data)


    def getHeader(self):
        res = requests.request('POST', self.project_url+self.login_path, data={'username':self.user,'password':self.pwd})
        authorization = 'Bearer ' + res.json()['data']['access_token']
        authx = res.json()['data']['b_token']
        headers = 'auth-x:' + authx + '\n' + 'authorization:' + authorization
        return headers

    def run(self):
        #获取数据列表
        total_list = self.interfaceList()
        #获取数据头
        self.header = self.getHeader()  #在此切换是否为固定Token  #3
        # self.header = "S-ORIGIN:xxzx" + '\n' + "S-TOKEN:eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eydzdWInOnh4engsJ2lhdCc6MTU0NTYyMzEwMywnZXhwJzoxNTQ1NjI2NzAzfQ==.fd7ae70bc2f282bc29d3091a607087a2a44da8cd87d30d27021651c6bb341f86"
        for index,value in enumerate(total_list):
            print(index)
            self.writeSolo(value)

def initYApi2Csv(projects,csvname,apipath,api_user,api_pwd,project_url,login_path,user,pwd,tmp):
    api_csv = Api2Csv(projects,csvname,apipath,api_user,api_pwd,project_url,login_path,user,pwd,tmp)
    api_csv.run()