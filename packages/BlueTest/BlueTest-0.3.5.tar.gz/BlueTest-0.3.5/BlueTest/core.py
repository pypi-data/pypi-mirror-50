from toolbox import *


from logInit import *
null="null"
import requests,re,time,random

class apiTest(object):
    def __init__(self,data,encode=""):
        self.data = data
        self.min = 5
        self.max = 10000
        self.headers = self.data[csv_parm.HEADERS]

        self.url = self.data[csv_parm.URL]
        self.method = self.data[csv_parm.METHOD]
        self.name = self.data[csv_parm.NAME]
        self.error_list = MainParam.ERROR_LIST
        self.encode=encode

    def writError(self,data,check_type):
        path = "./result/result_error.txt"
        with open(path,"a",encoding='utf8') as file:
            url = re.findall("urlparams:(.*?) response", data)[0]
            all_message = eval(re.findall("response:(.*) c", data)[0].replace("response:", ""))
            data_message = all_message[1]
            message = data_message
            http_code = data.split(" ")[-1].split(":")[-1]
            code = ""
            check = ""

            if message == '' and int(http_code)< 500:
                message_type = '错误信息不明确'
            elif message == '' and int(http_code)>=500:
                message_type = '服务不存在'
            else:
                message_type = '业务性问题'
            for a in ResultError.OTHER:
                if a in message:
                    message_type = '其他'
            for a in ResultError.UNCERTAIN:
                if a in message:
                    message_type = '错误信息不明确'
            for a in ResultError.LESSPARAM:
                if a in message:
                    message_type = '缺少参数或参数不正确'

            if check_type == 'normal':
                if message_type == '业务性问题':
                    check = True
                else:
                    check = False
            if check_type == 'other':
                if message_type == '错误信息不明确' or message_type == '其他':
                    check = False
                else:
                    check = True

            try:
                dict_message = eval(data_message)
                code = str(dict_message["code"])
                message = str(dict_message["message"])
                message_type = message_type

            except:
                pass

            finally:
                file.write(url + "\t" + code+"\t"+http_code + "\t" + message + "\t" + message_type + "\t" + str(check) + "\n")

            pass
    def recordResults(self,data,check_type):
        mkdir("./result/")
        with open("./result/data.txt","a",encoding='utf8') as file:
            file.write("%s \n"%(data)+"\n")
        log.logger.info("%s \n"%(data))
        if not self.responseAssert(data):
            # errorlog.logger.error("%s \n"%(data))
            self.writError(data,check_type)
        # errorlog


    def responseAssert(self,data,error_list=False):
        if "0x000000" in str(data):
            return True
        else:
            return False

    def soloRequest(self,body=False,urlparams=False):
        error_list = self.error_list
        time.sleep(1)
        self.status_code = 0

        querystring = False
        payload = False

        if self.data[csv_parm.URLPARAMS]:
            querystring = self.data[csv_parm.URLPARAMS]
        if urlparams:
            querystring = urlparams
        if self.data[csv_parm.DATA] != "null":
            payload = self.data[csv_parm.DATA]
        if body:
            payload = body
        if self.data[csv_parm.DATATYPE] == csv_parm.RAW: #处理raw格式数据
            payload = str(payload)
            payload = payload.replace(" '", "\"").replace("' ", "\"").replace("'", "\"")

        # with requests.request(method=self.method, url=self.url, params=body) as response:
        if self.encode:
            if type(querystring) == str:
                querystring = querystring.encode(self.encode)
            if type(payload) == str :
                payload = payload.encode(self.encode)
        with requests.request(method=self.method,url=self.url, params=querystring,data=payload,headers =self.headers) as response :
            print(response.status_code)
            self.status_code = response.status_code
            state = False
            for error in error_list:
                if error in response.text:
                        return False,response.text
            return True,response.text
    def specifyLength(self,spec_num=False):
        if not spec_num:
            low = self.min
            height = self.max
            mid =  int((low + height) / 2)
            # str(random.randint(10 ** mid, 10 ** (mid + 1)))
            # return int((low + height) / 2)
            return str(random.randint(10 ** mid, 10 ** (mid + 1)))
        else:
            return str(random.randint(10 ** spec_num, 10 ** (spec_num + 1)))

    def deepTemp(self,temp,value,key):
        str_temp = "temp"
        for index, ddd in enumerate(key):  # 置空
            str_temp += "[key[%d]]" % index
        str_temp += "=%s"%(str(value))
        exec(str_temp)

    def limitCheck(self,body,key,urlparams=False):
        temp = copy.deepcopy(body)
        self.deepTemp(temp,self.specifyLength(spec_num=100000),key)
        if urlparams:
            spec_response = self.soloRequest(urlparams = temp)
        else:
            spec_response = self.soloRequest(body=temp)


        self.deepTemp(temp, self.specifyLength(spec_num=1), key)
        if urlparams:
            spec_response_2 = self.soloRequest(urlparams = temp)
        else:
            spec_response_2 = self.soloRequest(body=temp)

        if spec_response_2 == spec_response:
            if urlparams:
                self.recordResults("%s urlparams %s:limit error >:%s " % (self.name, str(key), str(100000)),check_type="")
                self.recordResults("%s \n"%str(spec_response_2[1]),check_type="")
            else:
                self.recordResults("%s urlparams %s:limit error >:%s " % (self.name, str(key), str(100000)),check_type="")
                self.recordResults("%s \n"%str(spec_response_2[1]),check_type="")
            return True
        self.min = 1
        self.max = 100000
        while abs(self.min - self.max) > 1:
            temp_len = int((self.min + self.max) / 2)
            self.deepTemp(temp, self.specifyLength(), key)
            if urlparams:
                response = self.soloRequest(urlparams = temp)
            else:
                response = self.soloRequest(body=temp)

            log.logger.debug("key:%s max:%s min:%s cur:%s response:%s"%(key,str(self.max),str(self.min),str(temp_len),response))
            if response == spec_response:
                self.max = temp_len
            else:
                self.min = temp_len
        for i in range(self.max + 1, self.min - 2, -1):
            self.deepTemp(temp, self.specifyLength(spec_num=i), key)
            if urlparams:
                response = self.soloRequest(urlparams=temp)
            else:
                response = self.soloRequest(body = temp)
            log.logger.debug("finish check:%s response:%s"%(str(i+1),response))
            if response != spec_response:
                if urlparams:
                    self.recordResults("%s urlparams %s:limit:%s \n" % (self.name, str(key), str(i+1)),check_type="")
                    self.recordResults("%s \n" % str(spec_response[1]),check_type="")
                else:
                    self.recordResults("%s  %s:limit:%s \n" % (self.name, str(key), str(i+1)),check_type="")
                    self.recordResults("%s \n" % str(spec_response[1]),check_type="")
                return i
        return False

    def extrasCheck(self,body,key,urlparams=False):

        temp = copy.deepcopy(body) # temp = {key1:[value1,value2]}      [["key1",0],["key1",1],["key1",2]]
        str_temp="temp"   #["key1",0]     temp["key1"][1111]=123213
        for index in range(len(key)-1):
            str_temp += "[key[%d]]" % index
        str_temp +='["test"]="test"'
        # for index,value in enumerate(key): #置空
        #     str_temp+="[key[%d]]"%index
        # str_temp += "=\"\""
        exec(str_temp)
        if urlparams:
            spec_response = self.soloRequest(urlparams = temp)
        else:
            spec_response = self.soloRequest(temp)
        log.logger.debug(temp)
        self.recordResults("%s extrasCheck: %s 额外参数校验 urlparams:%s response:%s code:%s" % (self.name, key,str_temp+'额外参数校验', spec_response,self.status_code),check_type='other')
        # str_temp = "temp"

    def nomalCheck(self,body,urlparams=False):
        if urlparams:
            spec_response = self.soloRequest(urlparams=body)
        else:
            spec_response = self.soloRequest(body)

        log.logger.debug(body)
        self.recordResults("%s exceptionCheck: 普通请求 urlparams:%s response:%s code:%s" % (self.name, str(self.url), spec_response,self.status_code),check_type="normal")

    def heartBeatTest(self):
        self.headers = self.data[csv_parm.HEADERS]
        self.url = self.data[csv_parm.URL]
        self.method = self.data[csv_parm.METHOD]
        self.name = self.data[csv_parm.NAME]
        d = Base()
        if self.data[csv_parm.DATA] != "null" and self.data[csv_parm.METHOD] == "POST":
            body = self.data[csv_parm.DATA]
            try:
                body = eval(body)
            except:
                pass
            keys, values = d.dataGetKeyAndValue(body)
            if not keys:
                self.exceptionCheck2(body, "")
            for key in keys:
                self.exceptionCheck2(body, key)
                break
        if self.data[csv_parm.METHOD] == "GET":
            body = self.data[csv_parm.URLPARAMS]
            keys, values = d.dataGetKeyAndValue(self.data[csv_parm.URLPARAMS])
            if not keys:
                self.exceptionCheck2(body, "")
            for key in keys:
                self.exceptionCheck2(body, key)
                break

    def dataReduction(self,data,limitcheck=True,extras_check=True):
        self.headers = self.data[csv_parm.HEADERS]
        # print(self.headers)
        self.url = self.data[csv_parm.URL]
        self.method = self.data[csv_parm.METHOD]
        self.name = self.data[csv_parm.NAME]
        d = Base()
        temp_len = 0
        if self.data[csv_parm.DATA] != "null" and self.data[csv_parm.METHOD] == "POST":
            body = self.data[csv_parm.DATA]
            try:
                body = eval(body)
            except:
                pass

            keys,values = d.dataGetKeyAndValue(body)
            temp_len = 0
            self.nomalCheck(body, urlparams=True)
            if not keys:
                self.exceptionCheck(body, "")
            for key in keys:
                self.exceptionCheck(body, key)
                if limitcheck:
                    for solo in range(3):
                        limit = self.limitCheck(body, key)
                        if limit:
                            break
                if extras_check :
                    if temp_len != len(key):
                        temp_len = len(key)
                        self.extrasCheck(body,key)

            temp_len = 0
        if self.data[csv_parm.METHOD] == "GET":
            body = self.data[csv_parm.URLPARAMS]
            keys, values = d.dataGetKeyAndValue(self.data[csv_parm.URLPARAMS])
            self.nomalCheck(body, urlparams=True)
            if not keys:
                self.exceptionCheck(body, "")
            for key in keys:
                self.exceptionCheck(body, key,urlparams=True)
                if limitcheck:
                    for solo in range(3):
                        limit = self.limitCheck(body, key,urlparams=True)
                        if limit:
                            break
                if extras_check :
                    if temp_len != len(key):
                        temp_len = len(key)
                        self.extrasCheck(body,key)
    def exceptionCheck2(self, body, urlparams=False):
        if urlparams:
            spec_response = self.soloRequest(urlparams=body)
        else:
            spec_response = self.soloRequest(body)
        self.recordResults("%s exceptionCheck: 普通请求 urlparams:%s response:%s code:%s" % (self.name, str(self.url), spec_response,self.status_code),check_type="normal")

    def exceptionCheck(self, body, key, urlparams=False):
        temp = copy.deepcopy(body)
        str_temp = "temp"
        for index, value in enumerate(key):  # 置空
            str_temp += "[key[%d]]" % index
        str_temp += "=\"\""

        exec(str_temp)
        if urlparams:
            spec_response = self.soloRequest(urlparams=temp)
        else:
            spec_response = self.soloRequest(temp)
        log.logger.debug(temp)
        if key:
            self.recordResults("%s exceptionCheck: %s为空 urlparams:%s response:%s code:%s" % (self.name, key, key[0]+'为空', spec_response,self.status_code),check_type="other")
            if "type" in key[-1].lower():
                str_temp = "temp"
                for index, value in enumerate(key):  # 置空
                    str_temp += "[key[%d]]" % index
                str_temp += "=\"999999\""
                exec(str_temp)
                if urlparams:
                    spec_response = self.soloRequest(urlparams=temp)
                else:
                    spec_response = self.soloRequest(temp)
                log.logger.debug(temp)
                self.recordResults("%s exceptionCheck: %sType校验 urlparams:%s response:%s code:%s" % (self.name, key, key[0]+'Type校验', spec_response,self.status_code),check_type="other")

            str_temp = "temp"
            for index in range(len(key) - 1):
                str_temp += "[key[%d]]" % index
            str_temp += ".pop(key[-1])"
            exec(str_temp)
            if urlparams:
                spec_response = self.soloRequest(urlparams=temp)
            else:
                spec_response = self.soloRequest(temp)
            log.logger.debug(temp)
            self.recordResults(
                "%s exceptionCheck: %s不传 urlparams:%s response:%s code:%s" % (self.name, key, key[0]+'不传', spec_response,self.status_code),check_type="other")


def initPostMan(name, result_path="", encode=""):
    path = ""
    result_name = ""
    if "\\" in name or "/" in name or "//" in name:
        path = name
    if not result_path:
        if path:
            result_name = name.split("\\")[-1].split("//")[-1].split("/")[-1].split(".")[0]
        else:
            result_name = name.split(".")[0]
        result_path = "./srcdata/%s.csv" % result_name
    if not path:
        test = Postman2Csv("./srcdata/%s.json.postman_collection" % name, resultpath=result_path, encode=encode)
    else:
        test = Postman2Csv(path, resultpath=result_path, encode=encode)

    test.run()


def testByCsvData(name,normal_test=True,mkpy=False,limit_check = False,extras_check=True,encode="",case_type="",counter=True,need=0):
    """test API by csv data

        :param name: csv name or csv path.
        :param normal_test: Test open main switch.LV > mkpy,limit_check,extras_check
        :param mkpy: creat .py file(Support 3.X py) . like postman Generate Code .type Bool
        :param limit_check:  Check the length of parameters.Length range 1-100000. It's a waste of time. Close it if it's not necessary. type Bool
        :param extras_check: Adding non-agreed additional parameters for request validation. type Bool

        Usage::

        """
    path = ""
    if "\\" in name or "/" in name or "//" in name:
        path = name
    if not path:
        test = Csv2Dict("./srcdata/%s.csv"%name)
    else:
        test = Csv2Dict(path)
    d = test.run()
    if not d:
        log.logger.error("CSV serialize False.")
        return False
    start = 0
    if normal_test:
        for i in d:
            if counter:
                print(start,i["Url"],i["Method"])
                if start< need:
                    start += 1
                    continue
            start += 1
            test = apiTest(i,encode=encode)
            if case_type == "HeartTest":
                test.heartBeatTest()
            else:
                test.dataReduction(1,limitcheck=limit_check,extras_check=extras_check)