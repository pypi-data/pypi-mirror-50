import socket,mimetypes,os,json,sys,hashlib,time,base64,copy,ssl
from scarf.main.Reslove_Request import Reslove_Request
from scarf.ThreadManager.pool import ThreadPool
from scarf.main.ws import ws

class main(Reslove_Request,ThreadPool):
    updateParams = None
    def __init__(self,params):
        self.__params = params
        self.__CROS = {}
        self.__context = None
        CROS = ("Access-Control-Allow-Origin", "Access-Control-Max-Age", "Access-Control-Allow-Headers",
                "Access-Control-Expose-Headers", "Access-Control-Allow-Credentials",)
        for (index,item) in enumerate(params.get("CROS")):
            self.__CROS[CROS[index]] = item
        self.__PoolNumber = params["env"]
        if isinstance(params["env"],bool):
            self.__PoolNumber = 5 if params["env"] else 400
        #服务套接字
        self.__Server = None
        #获取端口号
        self.Port = params.get("port") if params.get("port") else 8080
        # 获取本地IP
        if params.get("Host"):
            self.Host = params.get("Host")
        else:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            try:
                s.connect(('8.8.8.8', 80))
                self.Host = s.getsockname()[0]
            except:
                self.Host = "127.0.0.1"
        if params.get("OpenHTTPS"):
            # 加载ssl证书
            self.__context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
            # 加载服务器所用证书和私钥
            self.__context.load_cert_chain(params.get("OpenHTTPS")["crt"],keyfile=params.get("OpenHTTPS")["key"],password=params.get("OpenHTTPS")["password"])
        def Updating(_params):
            self.__globareqInter = _params["Service"].get("Interceptor").get("req")
            self.__globaresInter = _params["Service"].get("Interceptor").get("res")
            router_list = _params["Service"]
            router_list.update(_params["Page"])
            for item in router_list:
                value = router_list[item]
                del router_list[item]
                if item != "/":
                    item = item[0:-1] if item[-1] == "/" else item
                router_list[item] = value
            router_list["StaticVisit"] = _params.get("StaticVisit")
            router_list["staticPath"] = _params.get("staticPath")
            router_list["allowed"] = []
            router_list["not_allowed"] = []
            if isinstance(self.__params["StaticVisit"], list):
                for item in self.__params["StaticVisit"]:
                    if item.find("-") > -1:
                        router_list["not_allowed"].append(item[item.find("-") + 1:])
                    else:
                        router_list["allowed"].append(item)
            Reslove_Request.routerlist = router_list
        main.updateParams = Updating
        #更新
        Updating(params)
        self.__startService__()
        print('\033[36m' + '\r\n\r\nThe Start is Running...' + '\033[0m')
        IP = str(self.Host) + ("" if params["port"] == 80 else (":" + str(params["port"])));
        self.__StartWaitRequest(IP)

    def __del__(self):
        if self.__Server :
            self.__Server.close()
        print("The Server Has Finished !")

    def __startService__(self):
        self.__Request = Reslove_Request
        self.__Server = socket.socket()
        self.__Server.bind((self.Host, self.Port))
        self.__Server.listen(-1)
        self.__Server.setsockopt(socket.SOL_SOCKET,socket.TCP_NODELAY,1)
        if self.__context:
            self.__Server = self.__context.wrap_socket(self.__Server, server_side=True)
        self.__WorkerManger = ThreadPool(self.__PoolNumber)
        if self.__params["SQLOptions"] == False:
            print("\r\n");
            print("\033[1;33m" + "Do not use Scarf's SQLManager!" + '\033[0m');
            self.__SQLTaskManger = None
        else:
            #创建SQL连接池
            from scarf.main.dbPool import ConnectionPool;
            self.__SQLTaskManger = ConnectionPool(100, self.__params["SQLOptions"])

    def __StartWaitRequest(self,IP):
        print("\r\n" + '\033[1;32m' + "The Server is Open at : " + '\033[0m' + "http://" + IP);
        while True:
            try:
                client, con = self.__Server.accept();
                code = client.recv(1024);
                if len(code) == 0:
                    client.close();
                    continue;
                self.__WorkerManger.AddWorker(self.__ResloveCode, {"code": code, "client": client});
            except Exception as e:
                print(e);


    def __ResloveCode(self,params):
        client = params["client"]
        result = False
        try:
            req = self.__Request(params["code"]).Request
            if req.headers.get("Content-Length"):
                if len(str(req.body)) < float(req.headers["Content-Length"]):
                    length = float(req.bodylength)
                    times = int(float(req.headers["Content-Length"]) / 1024)
                    client.setblocking(False)
                    while times > 0 or length < float(req.headers["Content-Length"]):
                            code = client.recv(1024)
                            params["code"] += code
                            times -= 1
                            length += len(code)
                    del req
                    client.setblocking(True)
                    req = self.__Request(params["code"]).Request
            if req.headers.get("Content-Type"):
                if req.headers.get("Content-Type").find("multipart/form-data") > -1:
                    if req.url_params.get("outputpath") is None:
                        if not os.path.exists(sys.path[0] + "\\output"):
                            os.mkdir(sys.path[0] + "\\output")
                        outputpath = sys.path[0] + "\\output"
                    else:
                        if not os.path.exists(sys.path[0]+"\\"+req.url_params.get("outputpath")):
                            os.mkdir(sys.path[0]+"\\"+req.url_params.get("outputpath"))
                        outputpath = sys.path[0]+"\\"+req.url_params.get("outputpath")
                    _FileKeyNames = req.url_params.get("FilesKeyName") if req.url_params.get("FilesKeyName") else [];
                    for item in _FileKeyNames:
                        for (index,itemval) in enumerate(req.body):
                            if itemval.get("name") == '"'+item+'"':
                                filename = itemval["filename"][1:]
                                filename = filename[0:filename.find('"')]
                                stream = open(outputpath+"\\"+filename, "w");
                                stream.close();
                                file = open(outputpath+"\\"+filename, "wb+");
                                file.write(itemval["body"]);
                                file.close();
                                _currentFileNumber = 0
                                for item in os.listdir():
                                    if os.path.isfile(outputpath+item):
                                        _currentFileNumber += 1
                                md5 = hashlib.md5()
                                _new_filename = str(_currentFileNumber) + filename + str(time.time())
                                md5.update(_new_filename.encode("utf-8"))
                                _new_filename = md5.hexdigest() + os.path.splitext(filename)[1]
                                os.rename(outputpath+"\\"+filename,outputpath+"\\"+_new_filename)
                                req.body[index]["filename"] = filename
                                req.body[index]["body"] = outputpath+"\\"+_new_filename
                                break
            result = self.__Ana_Request(req, client)
        except Exception as  e:
            print(e)
            self.__ErrorReslove__(client, str(e),req.url)
        finally:
            if not result:
                client.close()

    def __matchingRender(self,path):
        path = path[len('' if self.__params.get('staticPath') is None else self.__params.get('staticPath')):]
        for item in self.__params.get("Page"):
            pageUrl = self.__params.get("Page")[item].get("url")
            if pageUrl == path.replace("\\","/"):
                return self.__params.get("Page")[item].get("fn")(None,None).get("render")
        return None

    def __ReadToClientStream__(self,req,client):
        try:
            header = {
                "Content-Type": mimetypes.guess_type(req.filepath)[0],
                "Content-Length": os.path.getsize(req.filepath)
            }
            if req.render is None:
                render = self.__matchingRender(req.filepath)
                if render:
                    req.render = render
                    self.__ReadToClientStream__(req,client)
                    return
                fs = open(req.filepath, "rb+");
                content = fs.read()
            else:
                fs = open(req.filepath, "r+",encoding="utf-8");
                content = fs.read()
                result = req.render()
                index = 0
                fh = "|--"
                value = ""
                record = False
                arr = [""]
                num = 0
                while index < len(content):
                    if content[index:index+3] == fh:
                        if fh == "|--":
                            record = True
                            fh = "--|"
                            index += 3
                        elif fh == "--|":
                            record = False
                            fh = "|--"
                            index += 3
                            arr.append(str(result.get(value.strip())))
                            arr.append("")
                            value = ""
                            num += 2
                    if record:
                        value += content[index]
                    else:
                        arr[num] += content[index]
                    index += 1
                content = "".join(arr)
                header["Content-Length"] = len(content.encode("utf-8"))
            #处理响应头
            header.update(self.__CROS)
            header = self.__CreateResponeHeader(header, "HTTP/1.1 404 Not Found" if req.no_found else True, req.url)
            client.send(header.encode("utf-8"))
            #发送实体内容
            if len(content) < 1024:
                client.send(content if isinstance(content,bytes) else content.encode("utf-8"))
            else:
                i = 0
                while i < len(content):
                    client.send(content[i:i + 1024 if len(content) - i > 1024 else len(content)] if isinstance(content,bytes) else content[i:i + 1024 if len(content) - i > 1024 else len(content)].encode("utf-8"))
                    i += 1024
            fs.close();
        except Exception as e:
            print("读取错误"+str(e))
            client.close()

    def __ErrorReslove__(self,client,message,url):
        Type = "application/json;" if isinstance(message,dict) else "text/plain;"
        headers = {
                "Content-Type":Type,
                "Content-Length":len(message)
        }
        headers.update(self.__CROS)
        client.send(self.__CreateResponeHeader(headers,"HTTP/1.1 500 Server Error",url).encode("utf-8"))
        client.send(message.encode("utf-8"))

    def __Inters_Control(self,Inter,req,client,history = {},respone = False):
            globalReqSend = Inter(req,self.__SQLTaskManger,history,respone)
            globalReqSend.send(None)
            req = copy.deepcopy(req)
            while True:
                result = globalReqSend.send(req)
                if result["result"].get("client"):
                    self.__ConcatParams(result["result"].get("client"),req,client,True)
                    return {"flag": True}
                if result["LAST"]:
                    return {"flag": False, "history":result["result"].get("history") if result["result"].get("history") else {}, "respone": result["result"].get("respone")}

    def __Ana_Request(self,req,client,flag = False):
        #拦截器部分
        if not flag and self.__globareqInter:
            history = self.__Inters_Control(self.__globareqInter, req, client)
            if history.get("flag"):
                return
            history = history.get("history")
        #接口单独拦截器
        if req.url_params:
            if req.url_params.get("Interceptor") and not flag:
                if req.url_params.get("Interceptor").get("req"):
                    if self.__Inters_Control(req.url_params.get("Interceptor").get("req"),req,client,history).get("flag"):
                       return
        # 请求分析阶段
        if req.type == 2:
            self.__ReadToClientStream__(req, client)
            return
        elif req.type == 3:
            header = self.__CreateResponeHeader({
                "Content-Type":"text/plain",
                "Content-Length":len("Not Found!!!")
            },"HTTP/1.1 404 Not Found",req.url)
            header += "Not Found!!!"
            client.send(header.encode("utf-8"))
            return
        elif req.type == 4:#过滤WebSocket
            if req.headers["method"] not in req.url_params["methods"]:
                self.__ErrorReslove__(client, "The Method is Not Allowed",req.url)
                return
            if str(req.headers.get("Upgrade")).lower() == "websocket" and req.headers.get("Sec-Websocket-Version"):
                AcceptKey = req.headers["Sec-Websocket-Key"] + "258EAFA5-E914-47DA-95CA-C5AB0DC85B11";
                sha1 = hashlib.sha1();
                sha1.update(AcceptKey.encode("utf-8"))
                res = self.__CreateResponeHeader({"Upgrade":"websocket","Connection":"Upgrade","Sec-WebSocket-Accept":str(base64.b64encode(sha1.digest()),"utf-8"),"Sec-WebSocket-Version":req.headers["Sec-WebSocket-Version"] if req.headers.get("Sec-WebSocket-Version") else 13},"HTTP/1.1 101 Switching Protocols",req.url)
                client.send(res.encode("utf-8"))
                client = ws(client,req.url_params["fn"])
                client.ReciveMsg({"fn":req.url_params["fn"],"AddWorkerYd":self.__WorkerManger})
                return True
            else:
                self.__ErrorReslove__(client,"Error Request",req.url)
            return
        elif req.type == 1:
            if req.headers["method"].upper() == "OPTIONS":
                client.send(self.__CreateResponeHeader(self.__CROS,True,req.url).encode("utf-8"))
                return
            if req.headers["method"] not in req.url_params["methods"] and req.url_params["methods"] != "*":
                self.__ErrorReslove__(client, "The Method is Not Allowed",req.url)
                return
            result = req.url_params["fn"]({
                "headers": req.headers,
                "body": req.body,
                "params": req.params,
                "query": req.query,
            }, {
                "SQLManager": self.__SQLTaskManger,
                "sqls": req.url_params.get("sqls")
            })
            if result is None:
                raise Exception("No Result")
            self.__ConcatParams(result,req,client)

    def __ConcatParams(self,result,req,client,flag = False):
        history = {}
        if req.url_params:
            if req.url_params.get("Interceptor") and not flag:
                if req.url_params.get("Interceptor").get("res"):
                    history = self.__Inters_Control(req.url_params.get("Interceptor").get("res"), req, client, history,
                                                    result)
                    if history.get("flag"):
                        return
                    result = history.get("respone")
                    history = history['history']
        if not flag and self.__globaresInter:
            result = self.__Inters_Control(self.__globaresInter, req, client, history, result)
            if result.get("flag"):
                return
            result = result.get("respone")
            if result is None:
                raise Exception("No Result")

        res_headers = {}
        for item in self.__CROS:
            res_headers[item] = self.__CROS[item]
        if isinstance(result.get("data"), dict) or isinstance(result.get("data"), tuple) or isinstance(
                result.get("data"), list):
            res_data = json.dumps(result["data"])
            res_headers["Content-Type"] = "application/json;charset=utf-8";
            res_headers["Content-Length"] = len(res_data)
        else:
            # 过滤文件可能
            if result.get("type") == "file":
                req.type = 2
                req.filepath = (self.__params["staticPath"] + result["url"]).replace("/","\\")
                self.__Ana_Request(req, client, True)
                return
            res_data = result["data"]
            res_headers["Content-Type"] = "text/plain;charset=utf-8";
            res_headers["Content-Length"] = len(res_data)
        if isinstance(result.get("headers"), dict):
            for item in result.get("headers"):
                res_headers[item] = result.get("headers")[item]
        respone = self.__CreateResponeHeader(res_headers, "HTTP/1.1 404 Not Found" if req.no_found else (
            "HTTP/1.1 " + str(result.get("code")) if result.get("code") else True), req.url)
        respone += res_data
        client.send(respone.encode("utf-8"))

    def __CreateResponeHeader(self,params_with_headers,stateline,matchurl="/"):
        if stateline == True:
            print(matchurl + "\t\t", "HTTP/1.1 200 OK")
            header = "HTTP/1.1 200 OK \r\n"
        else:
            print(matchurl + "\t\t", stateline)
            header = stateline +"\r\n"
        params_with_headers["Server"] = "Scarf/1.0.8"
        for item in params_with_headers:
            header += (str(item)+": "+str(params_with_headers[item])+"\r\n")
        header += "\r\n"
        return header