import threading,time
def Reslove(fn):
    def mainfn():
        args = None
        params = yield args
        fn(params);
        yield params
    return mainfn;
class ThreadPool:
    poolOnly = False;
    def __init__(self,num):
        if ThreadPool.poolOnly:
            raise Exception("The ThreadPool Has been instantiated!");
        self.__ThreadPoolWorker = [[] for item in range(0,num)];
        self.__Threads = [{"Thread":threading.Thread(target=self.__test,args=(item,)),"Event":threading.Event()} for item in range(0,num)]
        for index in range(0, num):
            self.__Threads[index]["Thread"].start();
        ThreadPool.poolOnly = True;

    def __test(self,num):
        while True:
            if len(self.__ThreadPoolWorker[num]) > 0:
                params = self.__ThreadPoolWorker[num].pop(0)
                params["sendControl"].send(params["args"])
            else:
                self.__Threads[num]["Event"].clear();#如果无任务状态则进入休眠
                self.__Threads[num]["Event"].wait()

    def __WakeUpAllThreads(self):
        for item in self.__Threads:
            item["Event"].set()

    def AddWorker(self,fn,args):
        #计算平均值
        avg = self.__ComputAvg();

        #唤醒线程
        self.__WakeUpAllThreads()

        #生产携程控制器，执行完正函数后进行动态规划
        @Reslove
        def SendController(args):
            fn(args)
            avg = self.__ComputAvg();
            if len(self.__ThreadPoolWorker[curpostion]) > avg:
                for (index, item) in enumerate(self.__ThreadPoolWorker):
                    if len(item) < avg:
                        item.append({"sendControl": _sendController, "args": args})
                        break;

        _sendController = SendController()
        _sendController.send(None)
        #安排到队列
        for (index,item) in enumerate(self.__ThreadPoolWorker):
            if len(item) <= avg:
                item.append({"sendControl":_sendController,"args":args})
                curpostion = index
                break;

    #计算队列平均值函数
    def __ComputAvg(self):
        _sum = 0
        for item in self.__ThreadPoolWorker:
            _sum += len(item)
        return int(_sum / len(self.__ThreadPoolWorker))
