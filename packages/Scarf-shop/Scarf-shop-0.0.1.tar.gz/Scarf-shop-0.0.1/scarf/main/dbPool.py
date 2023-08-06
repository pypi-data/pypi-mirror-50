import os;
try:
    import mysql.connector as mysql
except Exception as e:
    print("Can't Found Module 'mysql-connector' for Python");
    res  = input("Do You Need Scarf To Install Module 'mysql-connector-python' Or Use Other db ?");
    if res.lower() == 'yes' or res.lower() == 'y' or len(res.lower()) == 0:
        os.system("pip install mysql-connector-python");
    else:
        print("\033[1;33m"+'Warming: Scarf Has No SQL Chaneel !'+'\033[0m');

class ConnectionPool:
        def __init__(self,Max,keyParams):
            self.__keyParams = keyParams;
            self.__MaxCount = Max;
            self.__resultArray = [];
            self.__CanUseIndex = [];
            self.__fetchArray = [];
            self.__awaitArray = [];
            self.__ConnectionPool = [];
            for item in range(0, self.__MaxCount):
                __db__ = self.__crateConnection();
                self.__CanUseIndex.append(item)
                self.__ConnectionPool.append(__db__);
                self.__resultArray.append(None);

        def __crateConnection(self):
            try:
                __db__ = mysql.connect(host=self.__keyParams["host"], port=self.__keyParams["port"],
                                     user=self.__keyParams["user"], password=self.__keyParams["password"],
                                     database=self.__keyParams["database"]);
                return __db__;
            except Exception as e:
                raise Exception("Error Connection :"+str(e))

        def resloveSQL(self,sql,con,index):
            cursor = con.cursor(dictionary=True);
            try:
                cursor.execute(sql["sql"]);
                if sql.get("search") == True:
                    self.__resultArray[index]["result"] = {"type":1,"result":cursor.fetchall()};
                else:
                    con.commit();
                    self.__resultArray[index]["result"] = {"type": 1};
            except Exception as e:
                if not sql.get("search"):
                    con.rollback();
                self.__resultArray[index]["result"] = {"type": 0, "result": str(e)};
            finally:
                cursor.close();

        def __leave_params(self,sql,opt):
            if sql["sql"].find("#") == -1:
                return sql
            else:
                start = sql["sql"].find("#")
                end = start
                end += 1
                while end < len(sql["sql"]):
                    if sql["sql"][end] == "#":
                        break;
                    end += 1
                param = sql['sql'][start+1:end]
                if opt.get(param):
                    sql["sql"] = sql["sql"].replace("#" + param + "#", str(opt[param]))
                else:
                    sql["sql"] = sql["sql"].replace("#"+param+"#","''")
                return self.__leave_params(sql,opt)

        def excuteSQL(self,sql):
            ResultSeek = None;
            sqls = self.__leave_params(sql,sql.get("params") if sql.get("params") else {})
            for (index,item) in enumerate(self.__resultArray):
                if item is None:
                    ResultSeek = index;
                    self.__resultArray[index] = {"sql":sql,"result":None};
                    con = self.__ConnectionPool.pop(0);
                    self.resloveSQL(sql,con,index);
                    res = self.__resultArray[index]["result"];
                    self.__resultArray[index] = None;
                    self.__ConnectionPool.append(con);
                    return res;
                if index == len(self.__resultArray) - 1:
                   while len(self.__ConnectionPool) < 0:
                       continue;
                   self.excuteSQL(sql);











