from websocket import create_connection
import time
import json

print("### BiLive_Client 服务端连接工具 ###")

print("\n请输入需连接的url（带ws/wss头）：")

url = input()

print("\n请输入该客户端对应protocol：")

protocol = input()

option = "NOT CLOSE"

class wsSend():

    def run_options(self, ws, option):
        if option.lower() == "addUser".lower() or option.lower() == "au".lower():
            self.addUser(self, ws)
        elif option.lower() == "delUser".lower() or option.lower() == "du".lower():
            self.delUser(self, ws)
        elif option.lower() == "getConfig".lower() or option.lower() == "gc".lower():
            self.getConfig(self, ws)
        elif option.lower() == "getInfo".lower() or option.lower() == "gi".lower():
            self.getInfo(self, ws)
        elif option.lower() == "getUID".lower() or option.lower() == "gud".lower():
            self.getUID(self, ws)
        elif option.lower() == "getUser".lower() or option.lower() == "gu".lower():
            self.getUser(self, ws)
        elif option.lower() == "help".lower() or option.lower() == "h".lower():
            self.getHelp(self)
        elif option.lower() == "setConfig".lower() or option.lower() == "sc".lower():
            self.setConfig(self, ws)
        elif option.lower() == "setUser".lower() or option.lower() == "su".lower():
            self.setUser(self, ws)
        elif option.lower() == "close".lower():
            print("关闭连接")
        else:
            print("参数错误，请输入help查看帮助")
            return

    def decide_type(data):
        arr = data.split("#")
        if arr[1].lower() == "bool".lower():
            if arr[0] == "0":
                return False
            elif arr[0] == "1":
                return True
            else:
                print("输入格式错误，请查阅帮助")
                return
        elif arr[1].lower() == "str".lower():
            return arr[0]
        elif arr[1].lower() == "int".lower():
            return int(arr[0])
        elif arr[1].lower() == "list".lower():
            strArr = arr[0].split(",")
            numArr = strArr
            i = 0
            while i < len(strArr):
                numArr[i] = int(strArr[i])
                i += 1
            return numArr
        else:
            print("输入格式错误，请查阅帮助")
            return

    def get_ts():
        millis = int(round(time.time() * 1000))
        return str(millis)

    def addUser(self, ws):
        data = "{\"cmd\":\"newUserData\",\"ts\":" + self.get_ts() + "}"
        ws.send(data)
        res = json.loads(ws.recv())
        if res["cmd"] == "newUserData":
            print("已新建用户：" + res["uid"] + "\n")
        else:
            print("未收到后端确认，请稍后重试或手动查阅用户信息以确认")
            return

    def delUser(self, ws):
        data = "{\"cmd\":\"getAllUID\",\"ts\":" + self.get_ts() + "}"
        ws.send(data)
        listRes = json.loads(ws.recv())
        if listRes["cmd"] == "getAllUID":
            order = 0
            while order < len(listRes["data"]):
                print(str(order + 1) + ": " + listRes["data"][order])
                order += 1
            print("输入要删除的用户的uid序号：")
            uid = input()
            data = "{\"cmd\":\"delUserData\",\"uid\":\"" + listRes["data"][int(uid)-1] + "\",\"ts\":" + self.get_ts() + "}"
            ws.send(data)
            delRes = json.loads(ws.recv())
            if delRes["cmd"] == "delUserData":
                print("已删除用户：" + listRes["data"][int(uid)-1] + "\n")
            else:
                print("未收到后端确认，请稍后重试或手动查阅用户信息以确认")
                return
        else:
            print("未获取到UID列表，请稍后再试")
            return

    def getUID(self, ws):
        data = "{\"cmd\":\"getAllUID\",\"ts\":" + self.get_ts() + "}"
        ws.send(data)
        res = json.loads(ws.recv())
        if res["cmd"] == "getAllUID":
            order = 0
            while order < len(res["data"]):
                print(str(order + 1) + ": " + res["data"][order])
                order += 1
            print("已获取UID列表\n")
        else:
            print("未获取到UID列表，请稍后再试")
            return

    def getUser(self, ws):
        data = "{\"cmd\":\"getAllUID\",\"ts\":" + self.get_ts() + "}"
        ws.send(data)
        listRes = json.loads(ws.recv())
        if listRes["cmd"] == "getAllUID":
            order = 0
            while order < len(listRes["data"]):
                print(str(order + 1) + ": " + listRes["data"][order])
                order += 1
            print("输入要获取的用户的uid序号：")
            uid = input()
            data = "{\"cmd\":\"getUserData\",\"uid\":\"" + listRes["data"][int(uid)-1] + "\",\"ts\":" + self.get_ts() + "}"
            ws.send(data)
            userRes = json.loads(ws.recv())
            if userRes["cmd"] == "getUserData":
                indentData = json.dumps(userRes["data"], indent = 4, separators=(', ', ': '))
                print(indentData)
                print("已获取" + listRes["data"][int(uid)-1] + "用户设置\n")
            else:
                print("未获取到有关用户信息，请稍后再试")
                return
        else:
            print("未获取到UID列表，请稍后再试")
            return

    def setUser(self, ws):
        data = "{\"cmd\":\"getAllUID\",\"ts\":" + self.get_ts() + "}"
        ws.send(data)
        listRes = json.loads(ws.recv())
        if listRes["cmd"] == "getAllUID":
            order = 0
            while order < len(listRes["data"]):
                print(str(order + 1) + ": " + listRes["data"][order])
                order += 1
            print("输入要设置的用户的uid序号：")
            uid = input()
            data = "{\"cmd\":\"getUserData\",\"uid\":\"" + listRes["data"][int(uid)-1] + "\",\"ts\":" + self.get_ts() + "}"
            ws.send(data)
            userRes = json.loads(ws.recv())
            if userRes["cmd"] == "getUserData":
                configData = userRes["data"]
            else:
                print("未获取到有关用户信息，请稍后再试")
                return
            print("输入要设置的用户项目：")
            key = input()
            print("输入要设置的用户项目的值：")
            val = input()
            configData[key] = self.decide_type(val)
            dataText = json.dumps(configData)
            sendUserData = "{\"cmd\":\"setUserData\",\"uid\":\"" + listRes["data"][int(uid)-1] + "\",\"data\":" + dataText + ",\"ts\":" + self.get_ts() + "}"
            ws.send(sendUserData)
            res = json.loads(ws.recv())
            if res["cmd"] == "setUserData":
                print("已更新用户设置\n")
            else:
                print("未收到后端确认，请稍后重试或手动查阅用户信息以确认")
                return
        else:
            print("未获取到UID列表，请稍后再试")
            return

    def getConfig(self, ws):
        data = "{\"cmd\":\"getConfig\",\"ts\":" + self.get_ts() + "}"
        ws.send(data)
        res = json.loads(ws.recv())
        if res["cmd"] == "getConfig":
            indentData = json.dumps(res["data"], indent=4, separators=(', ', ': '))
            print(indentData)
            print("已获取全局设置\n")
        else:
            print("未获取到全局设置，请稍后再试")
            return

    def setConfig(self, ws):
        data = "{\"cmd\":\"getConfig\",\"ts\":" + self.get_ts() + "}"
        ws.send(data)
        res = json.loads(ws.recv())
        if res["cmd"] == "getConfig":
            configData = res["data"]
        else:
            print("未获取到全局设置，请稍后再试")
            return
        print("输入要设置的全局项目：")
        key = input()
        print("输入要设置的全局项目的值：")
        val = input()
        configData[key] = self.decide_type(val)
        dataText = json.dumps(configData)
        sendUserData = "{\"cmd\":\"setConfig\",\"data\":" + dataText + ",\"ts\":" + self.get_ts() + "}"
        ws.send(sendUserData)
        if res["cmd"] == "setConfig":
            print("已更新全局设置\n")
        else:
            print("未收到后端确认，请稍后重试或手动查阅全局设置以确认")
            return

    def getInfo(self, ws):
        data = "{\"cmd\":\"getInfo\",\"ts\":" + self.get_ts() + "}"
        ws.send(data)
        res = json.loads(ws.recv())
        if res["cmd"] == "getInfo":
            indentData = json.dumps(res["data"], indent=4, separators=(', ', ': '))
            print(indentData)
            print("已获取参数描述\n")
        else:
            print("未获取到参数描述，请稍后再试")
            return

    def getHelp(self):
        print("帮助：")
        print("这是一个用于bilive_client的options设置工具，适用于部署于服务器等无GUI场景时的应用设置\n")
        print("支持的参数有：addUser(添加用户), close(关闭连接), delUser(删除用户), getConfig(获取全局设置), getInfo(获取参数描述)")
        print("getUID(获取全部UID), getUser(获取用户), help(帮助), setConfig(调整全局设置), setUser(设置用户)")
        print("还可使用参数的缩写来使用命令，如: au(addUser), gud(getUID), gu(getUser), h(help)，但close不可缩写，参数不分大小写\n")
        print("使用 addUser, getConfig, getInfo, getUID, help 参数时，不需进行二次操作")
        print("使用 delUser, getUser 参数时，需进行二次操作，输入所需删除/获取的用户的唯一的应用自动生成uid，可通过getUID命令查看")
        print("使用 setConfig 参数时，需进行“选择”和“赋值”的操作，具体可查看下部分")
        print("使用 setUser 参数时，需同 delUser 等命令一般，先指定uid，再进行“选择”和“赋值”的操作，具体可查看下部分\n")
        print("选择与赋值过程，需先指定设置的key名称(区分大小写)，再设置其值")
        print("赋值时，根据赋值类型不同，使用#分隔值与类型描述符，如：233#int(数值), wTFisThis#str(字符串)。描述符不分大小写")
        print("对于布尔型和js数组，设置有所不同：")
        print("对于布尔型，其描述符为bool，用0代表false，1代表true。如：0#bool(false)")
        print("对于数组，其描述符为list，用,分割数组项目。如：3,9#list([3,9])")


if __name__ == "__main__":
    ws = create_connection(url, subprotocols=[protocol])
    print("Connected to " + url + "\n")
    while option != "close" :
        option = input()
        wsSend.run_options(wsSend, ws, option)
    ws.close()
