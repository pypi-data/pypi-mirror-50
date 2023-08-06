import urllib;
from urllib import request;
from urllib import parse;
from importlib import reload
import os,json,sys,time,inspect,hashlib,threading,datetime,copy;
from scarf.main.main import main;

class Scarf:
    __Tools__ = {} #工具集合
    @staticmethod
    def __CreateDef(list):
        if len(list) == 0:
            return None
        def Interceptor(params,sqlopt,history = {},respone = False):
            yield params
            for (index,item) in enumerate(list):
                if respone or not isinstance(respone,bool) :
                    result = item.get("method")(params, history, sqlopt, respone)
                    respone = result.get("respone")
                    yield {"result": result, "LAST": index == len(list) - 1, "respone": respone}
                else:
                    result = item.get("method")(params, history, sqlopt)
                    yield {"result": result, "LAST": index == len(list) - 1}
                history[item.get("name")] = result.get("next")

        return Interceptor

    def __init__(self,mainpath,classList=[]):
        if isinstance(classList,tuple):
            self.__classes = []
            self.__JSONParams = None
            self.__params = None
            self.__resultInters = {}#拦截器对象
            for item in classList:
                self.__classes.append(item)
        else:
            self.__classes = classList;
        sys.path.append(os.getcwd())   #将整个项目加入解析器的搜索目录
        self.__rePath = sys.path[0];
        self.__StaticPath = "";
        self.__checkObj={"staticPath":self.__CheckstaticPath,"CROS":self.__CheckCROS,"Page":self.__CheckPage,"StaticVisit":self.__CheckStaticVisit,"ClientParmasRecord":self.__ClientParmasRecord,"Service":self.__CheckService,"port":self.__CheckPort,"SQLOptions":self.__CheckSQLConnction,"env":self.__CheckEnv,"interceptor":self.__CheckInterceptor}
        if os.path.exists(mainpath):
            if os.path.splitext(mainpath)[1].lower() == ".json":
                fs = None;
                InitItems = ("port","staticPath","CROS","Page","StaticVisit","ClientParmasRecord","interceptor","Service","SQLOptions","env");
                AllTimes = len(InitItems);
                try:
                    fs = open(mainpath,"r+");
                    #读取json文件
                    content = fs.read()
                    res = json.loads(content);
                    self.__JSONParams = json.loads(content) #获取JSON文件中的参数
                    fs.close();
                    #检查json
                    for key in res:
                        if key in InitItems or key == "mode" or key == 'OpenHTTPS':
                            continue;
                        else:
                            raise Exception("Unknow Variable name in JSON File with :"+key);
                    for (index,item) in enumerate(InitItems):
                        print("\r")
                        print("Task with Get :  "+item);
                        if res.get(item) is None:
                            self.__progress((index / AllTimes) * 100, 50)
                            continue;
                        itemResult = self.__checkObj[item](res[item])
                        if itemResult["flag"]:
                            if item == "staticPath":
                                self.__StaticPath = res[item];
                            elif itemResult.get("data") is not None:
                                res[item] = itemResult.get("data");
                            elif itemResult.get("ServiceList"):
                                for item in itemResult["ServiceList"]:
                                    res["Service"][item]["fn"] = itemResult["ServiceList"][item]["fn"]
                            self.__progress((index / AllTimes) * 100, 50)
                        else:
                            raise Exception(itemResult["ErrorStr"]);
                    self.__progress((AllTimes / AllTimes) * 100, 50);
                    #挂载拦截器
                    self.__AddInters(res)
                    res["staticPath"] = self.__rePath + res["staticPath"];
                    if res.get("mode") is None:
                        res["mode"] = 10;
                    else:
                        if isinstance(res["mode"],bool):
                            res["mode"] = 10 if res["mode"] == False else 450;
                        else:
                            res["mode"] = int(res["mode"])
                    # 整合工具集
                    Scarf.__Tools__["Request"] = self.Request
                    if res.get("OpenHTTPS"):
                        if not res["OpenHTTPS"].get("crt"):
                            raise Exception("No 'crt' File")
                        elif not res["OpenHTTPS"].get("key"):
                            raise Exception("No 'Key' File")
                        elif not res["OpenHTTPS"].get("password"):
                            raise Exception("No Password")
                    self.__params = res # 参数保存
                    main(res)
                except Exception as e:
                    raise e;
                finally:
                    fs.close();
            else:
                raise Exception("The Entry Is Not a JSON File!")
        else:
            raise Exception("The Entry File Is Not Found!");

    def __progress(self,percent, width=150):
        if percent >= 100:
            percent = 100

        show_str = ('[%%-%ds]' % width) % (int(width * percent / 100) * "#")
        print('\r%s %d%%' % (show_str, percent), end='')

    def __getMD5(self,path):
        if os.path.isfile(path):
            try:
                f = open(path, 'rb')
                hashCode = hashlib.md5(f.read()).hexdigest()
                return hashCode
            except:
                return None
        else:
            return None

    def __AddInters(self,res):
        for Interceptor in self.__resultInters["ReqIters"] if self.__resultInters.get("ReqIters") else []:
            if Interceptor.get("globa") is None and Interceptor.get("include"):
                for item in Interceptor["include"]:
                    # 检查page页面
                    if res.get("Page").get(item):
                        if res["Page"][item].get("Interceptor"):
                            res["Page"][item]["Interceptor"]["req"].append({
                                "name": Interceptor["name"],
                                "method": Interceptor["fn"]
                            })
                        else:
                            res["Page"][item]["Interceptor"] = {
                                "req": [{
                                    "name": Interceptor["name"],
                                    "method": Interceptor["fn"]
                                }],
                                "res": []
                            }
                        continue
                    # 检查service接口层
                    if res.get("Service").get(item):
                        if res["Service"][item].get("Interceptor"):
                            res["Service"][item]["Interceptor"]["req"].append({
                                "name": Interceptor.get("name"),
                                "method": Interceptor["fn"]
                            })
                        else:
                            res["Service"][item]["Interceptor"] = {
                                "req": [{
                                    "name": Interceptor.get("name"),
                                    "method": Interceptor["fn"]
                                }],
                                "res": []
                            }
                        continue
                    else:
                        res["Service"][item] = {
                            'methods': "*",
                            "Interceptor": {
                                "req": [{
                                    "name": Interceptor.get("name"),
                                    "method": Interceptor["fn"]
                                }],
                                "res": []
                            },
                        }

        for Interceptor in self.__resultInters["ResIters"] if self.__resultInters.get("ResIters") else []:
            if Interceptor.get("globa") is None and Interceptor.get("include"):
                for item in Interceptor["include"]:
                    # 检查page页面
                    if res.get("Page").get(item):
                        if res["Page"][item].get("Interceptor"):
                            res["Page"][item]["Interceptor"]["res"].append({
                                "name": Interceptor["name"],
                                "method": Interceptor["fn"]
                            })
                        else:
                            res["Page"][item]["Interceptor"] = {
                                "req": [],
                                "res": [{
                                    "name": Interceptor["name"],
                                    "method": Interceptor["fn"]
                                }]
                            }
                        continue
                    # 检查service接口层
                    if res.get("Service").get(item):
                        if res["Service"][item].get("Interceptor"):
                            res["Service"][item]["Interceptor"]["res"].append({
                                "name": Interceptor.get("name"),
                                "method": Interceptor["fn"]
                            })
                        else:
                            res["Service"][item]["Interceptor"] = {
                                "req": [],
                                "res": [{
                                    "name": Interceptor.get("name"),
                                    "method": Interceptor["fn"]
                                }]
                            }
                        continue
                    else:
                        res["Service"][item] = {
                            'methods': "*",
                            "Interceptor": {
                                "req": [],
                                "res": [{
                                    "name": Interceptor.get("name"),
                                    "method": Interceptor["fn"]
                                }]
                            },
                        }

        #转化为拦截器方法
        for item in res["Service"].values():
            if item.get("Interceptor"):
                item["Interceptor"]["req"] = Scarf.__CreateDef(item["Interceptor"]["req"])
                item["Interceptor"]["res"] = Scarf.__CreateDef(item["Interceptor"]["res"])

        for item in res["Page"].values():
            if item.get("Interceptor"):
                item["Interceptor"]["req"] = Scarf.__CreateDef(item["Interceptor"]["req"])
                item["Interceptor"]["res"] = Scarf.__CreateDef(item["Interceptor"]["res"])

        res["Service"]["Interceptor"] = {
            "req":self.__resultInters.get("ReqMethod"),
            "res":self.__resultInters.get("ResMethod")
        }

        res["Page"]["Interceptor"] = {
            "req": self.__resultInters.get("ReqMethod"),
            "res": self.__resultInters.get("ResMethod")
        }

    def __Update(self,module):
        if main.updateParams is None:
            return
        begin_time = datetime.datetime.now()
        for (index,item) in enumerate(self.__classes):
            if item.__class__.__name__ == module.__class__.__name__:
                try:
                    self.__classes[index] = getattr(reload(sys.modules.get(module.__class__.__module__)),type(module).__name__)()
                except Exception as e:
                    print('\033[31m'+str(e)+'\033[0m')
                    print('\033[31m' + 'Actual consumption time :' + str(
                        (float((datetime.datetime.now() - begin_time).microseconds) / 1000)) + ' ms\033[0m')
                    print('\033[31mUpdate Error!\r\n\033[0m')
                    return
                break
        print('\033[34m' + 'Start Reintegration module...' + '\033[0m')
        _v = copy.deepcopy(self.__JSONParams)
        result = self.__checkObj["Service"](self.__JSONParams["Service"])
        if result["flag"]:
            self.__params["Service"] = result["ServiceList"]
        else:
            print('\033[0;31;0m' + 'Actual consumption time :' + str(
                (float((datetime.datetime.now() - begin_time).microseconds) / 1000)) + ' ms\033[0m')
            print('\033[0;31;0m Update Failed At "Reslove" Module ! \033[0m')
            return
        result = self.__checkObj["Page"](self.__JSONParams["Page"])
        if result["flag"]:
            self.__params["Page"] = result["data"]
        else:
            print('\033[0;31;0m' + 'Actual consumption time :' + str(
                (float((datetime.datetime.now() - begin_time).microseconds) / 1000)) + ' ms\033[0m')
            print('\033[0;31;0m Update Failed At "Reslove" Module ! \033[0m')
            return
        self.__checkObj["interceptor"](self.__JSONParams["interceptor"])
        self.__AddInters(self.__params)
        main.updateParams(self.__params)
        print('\033[34m' + 'Actual consumption time :' +str((float((datetime.datetime.now() - begin_time).microseconds) / 1000))+ ' ms\033[0m')
        print('\033[32mUpdate Successful!\r\n\033[0m')
        self.__JSONParams = _v

    def __FindFun(self,params):
        if type(params).__name__ == "str":
            for (index,item) in enumerate(self.__classes):
                if type(item).__name__ == params.split(".")[0]:
                   return self.__searchMethod(item,".".join(params.split(".")[1:]))
                else:
                   method = self.__searchMethod(item, ".".join(params.split(".")[1:]))
                   if method:
                       if method.__code__.co_argcount > 1:
                           return method
                       else:
                           raise Exception("The Method '" + method.__name__ + "("+params+")' Must Have At Least Two Params")
                   elif index == len(self.__classes) - 1:
                    raise Exception("Can't Find Method '" + params + "'")

        else:
            raise Exception("Error Value With :"+str(params));


    def __CheckstaticPath(self,pathstr):
        return {"flag":os.path.exists(self.__rePath + pathstr),"ErrorStr":"Can't Find StaticPath :"+pathstr};

    def __CheckCROS(self,CROSList):
        return {"flag":True if len(CROSList) == 5 or len(CROSList) == 0 else False,"ErrorStr":"Error CROS Object"}

    def __CheckPage(self,pageList):
        result = {};
        for item in pageList:
           if os.path.exists(self.__rePath + self.__StaticPath + pageList[item]["url"]):
                def Create_Func(pageInfo,render):
                    def give_page(params,sqlopt):
                        return {"type":"file","url": pageInfo,"render":render}
                    return give_page
                if item == "404":
                    result[item] = {"url":pageList[item]["url"]}
                else:
                  result[item] = {"methods":pageList[item].get("methods") if pageList[item].get("methods") else ["GET"],"fn":Create_Func(pageList[item]["url"],self.__FindFun(pageList[item].get("render")) if pageList[item].get("render") else None),"url":pageList[item]["url"]}
                continue;
           else:
               raise Exception("Can Not Found Page : '"+self.__StaticPath + pageList[item]+"'");
        return {"flag":True,"data":result}

    def __CheckStaticVisit(self,sv):
        return {"flag":True if type(sv).__name__ == "bool" or isinstance(sv,list) else False,"ErrorStr":"StaticVisit is Not a Boolean value"};

    def __ClientParmasRecord(self,str):
        return {"flag": True, "ErrorStr": '',"data":self.__FindFun(str)}

    def __CheckService(self,ServiceList):
        for item in ServiceList:
            ServiceList[item]["fn"] = self.__FindFun(ServiceList[item]["fn"]);
        return {"flag":True,"ErrorStr":'',"ServiceList":ServiceList}

    def __CheckPort(self,portnum):
        if isinstance(portnum,int):
            return {"flag":True,"ErrorStr":''}
        else:
            return {"flag":False,"ErrorStr":'The Port is Not Wrongful'};

    def __CheckSQLConnction(self,opt):
        ErrorStr = "";
        if opt == False:
            return {"flag":True,"ErrorStr":''}

        if len(opt.keys()) == 0:
            return {"flag": False, "ErrorStr": 'No SQL Params!'};

        OPtionsList = ["host","port","user","password","database"];
        for item in opt:
            OPtionsList.remove(item)
        for (index,item) in enumerate(OPtionsList):
            ErrorStr += ("'" + str(item) + "',");
        if len(OPtionsList) == 0:
            return {"flag": True, "ErrorStr": ''}
        else:
            return {"flag":False,"ErrorStr":"No Params :"+str(ErrorStr[0:-1])};

    def __CheckInterceptor(self,inses):
        if not inses:
            return
        #第一步创建request的拦截器
        globalReqList = []
        for item in inses.get("request"):
            if item.get("fn") is None:
                return {"flag":False,"ErrorStr":"Interceptor No Has Params 'fn'"}
            item["fn"] = self.__FindFun(item.get("fn"))
            if item["fn"] is None:
                return {"flag": False, "ErrorStr": "Can Not Find '" + item["name"] + "' Method"}
            if item.get("globa"):
                globalReqList.append({
                    "name":item["name"],
                    "method":item["fn"]
                })

        globalResList = []
        for item in inses.get("respone"):
            if item.get("fn") is None:
                return {"flag":False,"ErrorStr":"Interceptor No Has Params 'fn'"}
            item["fn"] = self.__FindFun(item.get("fn"))
            if item["fn"] is None:
                return {"flag": False, "ErrorStr": "Can Not Find '" + item["name"] + "' Method"}
            if item.get("globa"):
                globalResList.append({
                    "name":item["name"],
                    "method":item["fn"]
                })

        self.__resultInters = {
            "ReqIters": inses.get("request"),#url使用的拦截器
            "ReqMethod": Scarf.__CreateDef(globalReqList),#全局请求拦截器
            "ResIters":inses.get("respone"),
            "ResMethod": Scarf.__CreateDef(globalResList)
        }

        return {"flag":True,"ErrorStr":""}





    def __searchMethod(self,obj, str):
        info = str.strip().split(".")
        getTool = {
            "has": dict.get if type(obj).__name__ == "dict" else hasattr,
            "get": dict.get if type(obj).__name__ == "dict" else getattr
        }
        for (index, item) in enumerate(info):
            if getTool["has"](obj, item):
                obj = getTool["get"](obj, item)
            else:
                return None
        return obj

    def Request(**params):
        if params.get("Method") is None:
            raise Exception("Missing params : 'Method'");
        if params.get("url") is None:
            raise Exception("Missing params : 'url'");
        if params.get("timeout") is None:
            params["timeout"] = 5 * 10;
        if params.get("headers") is None:
            params["headers"] = {};
            params["headers"][
                "User-Agent"] = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.109 Safari/537.36";
        else:
            if params.get("headers").get("User-Agent") is None:
                params["headers"][
                    "User-Agent"] = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.109 Safari/537.36";
        if params.get("data") is not None:
            params["data"] = urllib.parse.urlencode(params["data"]);
            params["data"] = params["data"].encode("ascii");

        try:
            if params.get("Method").lower() == "get":
                if params.get("params") is not None and isinstance(params.get("params"), dict):
                    params["url"] += "?"
                    for item in params["params"]:
                        params["url"] += (item + "=" + params["params"][item])
                    params["url"] = params["url"][0, len(params["url"]) - 2];
                req = request.Request(params["url"], None, params["headers"])
            else:
                req = request.Request(params["url"], params.get("data"), params["headers"])
            req.get_method = lambda: params["Method"];
            res = request.urlopen(req);
            return {
                "code": 1,
                "header": res.headers,
                "body": res.read().decode("utf-8")
            };
        except Exception as e:
            return {"code": 0, "ErrorMsg": e};

    def __CheckEnv(self,env):
        if isinstance(env,bool) or isinstance(env,int):
            if env == True:
                MD5List = {}
                for item in self.__classes:
                    if isinstance(item, dict):
                        continue;
                    MD5List[inspect.getsourcefile(item.__class__)] = self.__getMD5(inspect.getsourcefile(item.__class__))
                # 文件监听
                def WatchFile():
                    while True:
                        for item in self.__classes:
                            if isinstance(item, dict):
                                continue;
                            testCode = self.__getMD5(inspect.getsourcefile(item.__class__))
                            if MD5List[inspect.getsourcefile(item.__class__)] != testCode:
                                self.__Update(item)
                            MD5List[inspect.getsourcefile(item.__class__)] = testCode
                        time.sleep(2)

                watchFile = threading.Thread(target=WatchFile)
                watchFile.start()
            return {"flag": True, "ErrorStr": ''}
        else:
            return {"flag": False, "ErrorStr": 'Environment is not Invalid'}
