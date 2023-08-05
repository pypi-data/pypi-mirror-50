RAW = "raw"
class MainParam:
    Result_Path = "./result/"
    Press_File = "Press_"
    USETIME = "USETIME"
    RESPONSE_TRUE = "RESPONSE_TRUE"
    RESPONSE_FALSE = "RESPONSE_FALSE"
    RESUALT_CSV = "resualt.csv"
    TIME_CSV = "time.csv"
    RRESS_RESUALT_HEADER = ["时间","成功","失败"]
    PRESS_TIME_HEADER = ["耗时","数量"]
    ERROR_LIST = ["error","Error","失败","错误","异常","禁止"
                 "Max retries exceeded with url",
                  "500 Internal Server Error</title>",
                  "RemoteDisconnected(",
                  "ConnectionAbortedError(",
                  "WinError 10048",
                  "ConnectionResetError(",
                  "0x032000",
                  ]


class PostParm:
    FALSE = False
    TRUE = True
    NULL = "null"
    REQUESTS = "requests"
    REQUEST = "request"
    URL = "url"
    NAME = "name"
    METHOD = "method"
    HEADERS = "headers"
    DATA = "data"
    DATATYPE = "dataMode"
    RAWMODEDATA = "rawModeData"
    # URLPARAMS = ""
    START = "START"
    END ="END"

class csv_parm:
    CHINA_KEY = ["等级","中文名","名称","描述","结果路径","请求类型","地址","头信息","主信息","信息类型","URL参数","压测/基础"]
    KEY = ["Lv","Cname","Name","Describe","ResualPath","Method","Url","Headers","Data","DataType","UrlParams","TestType"]
    LV = "Lv"
    CNAME = "Cname"
    NAME = "Name"
    DESCRIBE = "Describe"
    RESUALPATH = "ResualPath"
    METHOD = "Method"
    URL = "Url"
    HEADERS = "Headers"
    DATA = "Data"
    DATATYPE = "DataType"
    URLPARAMS = "UrlParams"
    TESTTYPE = "TestType"
    RAW = "raw"

class code_parm:
    DATATYPE = 9
    DATA = 8

class ResultError:
    ALL = ['.php','null','发生未知错误','接口异常','未知错误','404 Not Found','Yahoo! Inc.','网络异常','FALSE','api error','接口校验失败','参数','必传','必填','为空']
    OTHER = ['.php','null','发生未知错误','接口异常','未知错误','404 Not Found','Yahoo! Inc.','网络异常','FALSE','api error']  #其他
    UNCERTAIN = ['接口校验失败']   #错误信息不明确
    LESSPARAM = ['参数','必传','必填','为空'] # 缺少参数  或参数不正确
