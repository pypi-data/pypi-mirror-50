import struct
class ws:
    __BaseClientsList = [None]
    def __init__(self,client,fn):
        self.__client__ = client
        self.__client__.setblocking(False);
        self.Allowed = True
        for (index,item) in enumerate(ws.__BaseClientsList):
            if item is None:
                ws.__BaseClientsList[index] = self;
                fn(self,None,2,index)
                break;
            if index == len(ws.__BaseClientsList) - 1:
                fn(self, None, 2, len(ws.__BaseClientsList))
                ws.__BaseClientsList.append(self)

    def ReciveMsg(self,params):
        if self.Allowed:
            fn = params["fn"]
            AddWorkerYd = params["AddWorkerYd"]
            try:
                msg = self.__client__.recv(1024);
                if struct.pack("B", msg[0]) == b'\x88':
                    num = self.__remove()
                    fn(self, None, 0, num)
                    return
                _req_result = self.__decode__(msg)
            except Exception as e:
                AddWorkerYd.AddWorker(self.ReciveMsg, {"fn": fn, "AddWorkerYd": AddWorkerYd})
                return
            try:
                fn(self, _req_result, 1, None)
            except Exception as e:
                print(e)
            AddWorkerYd.AddWorker(self.ReciveMsg,{"fn":fn,"AddWorkerYd":AddWorkerYd})
        else:
            self.__client__.close()

    def __remove(self):
        for (index, item) in enumerate(ws.__BaseClientsList):
            if item == self:
                self.close(None)
                ws.__BaseClientsList[index] = None
                return index

    def close(self,index):
        if index:
            ws.__BaseClientsList[index].close()
            ws.__BaseClientsList.pop(index)
            return
        self.__client__.close();
        self.Allowed = False

    def __decode__(self,data):
        code_len = data[1] & 0x7f
        if code_len == 0x7e:
            mask = data[4:8]
            decoded = data[8:]
        elif code_len == 0x7f:
            mask = data[10:14]
            decoded = data[14:]
        else:
            mask = data[2:6]
            decoded = data[6:]
        bytes_list = bytearray()
        for i in range(len(decoded)):
            chunk = decoded[i] ^ mask[i % 4]
            bytes_list.append(chunk)
        data = str(bytes_list, encoding="utf-8")
        return data

    def emit(self,message):
        token = b'\x81'
        length = len(message.encode())
        if length <= 125:
            token += struct.pack('B', length)
        elif length <= 0xFFFF:
            token += struct.pack('!BH', 126, length)
        else:
            token += struct.pack('!BQ', 127, length)
        data = token + message.encode()
        self.__client__.send(data);
