import json,urllib.parse,os
class Reslove_Request:

    routerlist = None

    def __init__(self,code):
        self.__Request = {}
        self.__Body = None;
        self.__query = {}
        self.__regurl = ""
        self.__type = -1
        self.__urlparams = None
        self.__params = {}
        self.__filepath = ""
        self.__No_Found = False
        self.__render = None
        self.__bodyLength = 0
        #获取状态行
        self.__GetStateLine__(code)
        #获取请求头
        self.__GetRequestHeaders__(code)
        #获取请求体
        self.__GetRequestBody__(code)

    def __GetStateLine__(self,code):
        code = str(code)
        # 过滤类型字符
        code = code[2:-1]
        self.__Request["method"] = code[0:code.find("\\r\\n")].split(" ")[0]
        self.__Request["url"] = urllib.parse.unquote(code[0:code.find("\\r\\n")].split(" ")[1])
        #检查有否query
        if self.__Request["url"].find("?")>-1:
            query_code = self.__Request["url"][self.__Request["url"].find("?")+1:]
            if query_code.find("&") > -1:
                for item in query_code.split("&"):
                    self.__query[urllib.parse.unquote(item.split("=")[0])] = urllib.parse.unquote(item.split("=")[1])
            else:
                self.__query[urllib.parse.unquote(query_code.split("=")[0])] = urllib.parse.unquote(query_code.split("=")[1])
            self.__Request["url"] = self.__Request["url"][0:self.__Request["url"].find("?")]
        #进行路由匹配
        self.__matchingurl(self.__Request["url"])
        self.__Request["version"] = code[0:code.find("\\r\\n")].split(" ")[2]

    def __GetRequestHeaders__(self,code):
        code = str(code)
        # 过滤类型字符
        code = code[2:-1]
        #获取请求头部分
        headers = code[code.find("\\r\\n")+4:code.find("\\r\\n\\r\\n")]
        for item in headers.split("\\r\\n"):
            key = item.split(": ")[0].lower()
            keyval = key[0].upper()
            index = 0
            while index < len(key[1:]):
                if key[1:][index] == "-" and index < len(key) - 1:
                    keyval += ("-"+key[1:][index + 1].upper())
                    index+=1
                else:
                    keyval += key[1:][index]
                index+=1
            self.__Request[keyval] = item.split(": ")[1]

    def __GetRequestBody__(self,code):
        str_code = str(code)
        body = code[str_code.find("\\r\\n\\r\\n") - (len(self.__Request.keys()) - 3) * 2 + 2:]
        if len(body) == 0:
            self.__Body = "";
            return
        try:
            self.__bodyLength = len(body)
            if self.__Request["Content-Type"].find("application/json") > -1:
                try:
                    self.__Body = json.loads(body);
                except Exception as e:
                    self.__Body = str(body)
            elif self.__Request["Content-Type"].find("x-www-form-urlencoded") > -1:
                try:
                    self.__Body = json.loads(body);
                except Exception as e:
                    body = body.decode("utf-8");
                    if body.find("=") > -1:
                        self.__Body = {}
                        if body.find("&") > -1:
                            for item in body.split("&"):
                                self.__Body[item.split("=")[0]] = item.split("=")[1]
                        else:
                            self.__Body[body.split("=")[0]] = body.split("=")[1]
                    else:
                        raise Exception()
            elif self.__Request["Content-Type"].find("multipart/form-data") > -1:
                boundry = self.__Request.get("Content-Type");
                boundry = "--" + boundry[boundry.find("boundary=") + len("boundary="):];
                length = len(boundry);
                paramsList = [];
                index = length;
                start = length;
                while index < len(body) - length:
                    if body[index:index + length] == boundry.encode("utf-8"):
                        paramsList.append(body[start:index]);
                        start = index + length;
                    index += 1;
                resultdict = [];
                for (index, item) in enumerate(paramsList):
                    index = len(b'/r/n/r/n');
                    bodyStart = 0;
                    bodyEnd = 0;
                    while index < len(item) - len(b'\r\n\r\n'):
                        if item[index:index + len(b'\r\n\r\n')] == b'\r\n\r\n':
                            bodyStart = index + len(b'\r\n\r\n');
                            break;
                        index += 1;
                    index = len(item);
                    while index > -1 + len(b'\r\n'):
                        if item[index - len(b'\r\n'):index] == b'\r\n':
                            bodyEnd = index - len(b'\r\n');
                            break;
                        index -= 1;
                    res = item[0:bodyStart].decode("utf-8").split(";")
                    res.pop(0)
                    params = {"body": item[bodyStart:bodyEnd]};
                    for _item_ in res:
                        if _item_.find("=") > -1:
                            params[_item_.split("=")[0].strip()] = _item_.split("=")[1]
                    resultdict.append(params)
                self.__Body = resultdict
            else:
                raise Exception();
        except:
            try:
                self.__Body = body.decode("utf-8")
            except Exception as e:
                self.__Body = str(body)

    def __matchingurl(self,url):
        #文件匹配阶段
        if Reslove_Request.routerlist["StaticVisit"]:
            staticPath = Reslove_Request.routerlist["staticPath"]
            if os.path.splitext(staticPath + url[1:].replace("/","\\"))[1][1:] not in Reslove_Request.routerlist["not_allowed"] or os.path.splitext(staticPath + url[1:].replace("/","\\"))[1][1:] in Reslove_Request.routerlist["allowed"]:
                if os.path.exists(staticPath + url[1:].replace("/","\\")) and len(os.path.splitext(staticPath + url[1:].replace("/","\\"))[1]) > 0:
                    self.__filepath = staticPath + url[1:]
                    self.__type = 2
                    return
        if url != "/":
            url_items = url.split("/")
            url_items.pop(0)
        else:
            url_items = "/"
        for (index,item) in enumerate(Reslove_Request.routerlist):
            if len(item.split("/")) - 1 > 0 and len(item.split("/")) - 1 == len(url_items):
                if item != "/":
                    test_url = item.split("/")
                    test_url.pop(0)
                else:
                    test_url = "/"
                for (_index,_item) in enumerate(url_items):
                    if _item != test_url[_index] and test_url[_index][0] != ":":
                            break;
                    elif test_url[_index][0] == ":":
                        self.__params[test_url[_index][1:]] = _item
                    if _index == len(url_items) - 1:
                        self.__regurl = item
                        self.__urlparams = Reslove_Request.routerlist[item]
                        self.__type = 4 if Reslove_Request.routerlist[item].get("WebSocket") == True else 1
                        return

            if index == len(Reslove_Request.routerlist) - 1:
                if Reslove_Request.routerlist.get("404"):
                    if isinstance(Reslove_Request.routerlist.get("404"),dict) and Reslove_Request.routerlist.get("404").get("url") is None:
                        self.__urlparams = Reslove_Request.routerlist["404"]
                        self.__type = 1
                    else:
                        self.__filepath = staticPath + Reslove_Request.routerlist.get("404")["url"]
                        self.__type = 2
                else:
                    self.__type = 3
                self.__No_Found = True
                return;


    @property
    def Request(self):
        result = type("RequestParams",(),{
            "headers":self.__Request,   #请求头
            "body":self.__Body, #请求体
            "bodylength":self.__bodyLength,#请求体长度
            "query":self.__query if len(self.__query.keys()) > 0 else None, #query参数
            "type":self.__type, #请求类型
            "matching_url":self.__regurl,   #匹配路由
            "url":self.__Request["url"], #原来路由
            "url_params":self.__urlparams,  #匹配到的路由参数
            "params":self.__params,  #url中的路由参数
            "filepath":self.__filepath, #匹配到的文件路径
            "no_found":self.__No_Found,#是否是404
            "render":self.__render#渲染方法
        })
        return result