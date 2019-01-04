import time
try:
    import thread
except ImportError:
    import _thread as thread
import json
import websocket

print("### BiLive_Client 服务端连接工具 ###")

print("\n请输入需连接的url（带ws/wss头）：")

url = input()

print("\n请输入该客户端对应protocol：")

protocol = input()

option_tmp = {
    "config": {},
    "users": {},
    "uid": [],
    "info": {}
}

class MyWebSocket():

    def get_ts():
        millis = int(round(time.time() * 1000))
        return str(millis)

    def msg_handler(msg):
        cmd = msg["cmd"]
        if cmd == "delUserData":
            option_tmp["users"].pop(msg["uid"])
            print("已删除用户：" + msg["uid"])
        elif cmd == "getAllUID":
            option_tmp["uid"] = msg["data"]
            order = 0
            while order < len(msg["data"]):
                print(str(order + 1) + ": " + msg["data"][order])
                order += 1
            print("已获取UID列表")
        elif cmd == "getConfig":
            option_tmp["config"] = msg["data"]
            indentData = json.dumps(msg["data"], indent = 4, separators=(', ', ': '))
            print(indentData)
            print("已获取全局设置")
        elif cmd == "getUserData":
            option_tmp["users"][msg["uid"]] = msg["data"]
            indentData = json.dumps(msg["data"], indent = 4, separators=(', ', ': '))
            print(indentData)
            print("已获取" + msg["uid"] + "用户设置")
        elif cmd == "newUserData":
            option_tmp["users"][msg["uid"]] = msg["data"]
            print("已新建用户：" + msg["uid"])
        elif cmd == "setUserData":
            text = json.dumps(msg)
            if text.find("\\u53c2\\u6570\\u9519\\u8bef") == -1:
                print("已更新" + msg["uid"] + "用户设置")
            else:
                print(msg["msg"])
        elif cmd == "setConfig":
            text = json.dumps(msg)
            if text.find("\\u53c2\\u6570\\u9519\\u8bef") == -1:
                print("已更新全局设置")
            else:
                print(msg["msg"])
        elif cmd == "getInfo":
            option_tmp["info"] = msg["data"]
        else: return

    def run_cmd(self, ws, option):
        if option.lower() == "addUser".lower() or option.lower() == "au".lower():
            msg = { "cmd": "newUserData" }
            ws.send(add_ts(msg))
        elif option.lower() == "delUser".lower() or option.lower() == "du".lower():
            print("输入要删除的用户的uid序号：")
            uid = input()
            if (uid[len(uid)-1]) == ".":
                num = uid[0:-1]
                if num.isdecimal() is True:
                    if int(num) <= len(option_tmp["uid"]):
                        uid = option_tmp["uid"][int(num)-1]
                    else:
                        print("无效序号")
                        return
                else:
                    print("无效序号")
                    return
            if option_tmp["users"]. __contains__(uid) is not True:
                print("无效uid")
                return
            msg = { "cmd": "delUserData", "uid": uid }
            ws.send(add_ts(msg))
        elif option.lower() == "getConfig".lower() or option.lower() == "gc".lower():
            msg = { "cmd":"getConfig" }
            ws.send(add_ts(msg))
        elif option.lower() == "getInfo".lower() or option.lower() == "gi".lower():
            msg = { "cmd":"getInfo" }
            ws.send(add_ts(msg))
        elif option.lower() == "getUID".lower() or option.lower() == "gud".lower():
            msg = { "cmd":"getAllUID" }
            ws.send(add_ts(msg))
        elif option.lower() == "getUser".lower() or option.lower() == "gu".lower():
            print("输入要获取的用户的uid序号：")
            uid = input()
            if (uid[len(uid)-1]) == ".":
                num = uid[0:-1]
                if num.isdecimal() is True:
                    if int(num) <= len(option_tmp["uid"]):
                        uid = option_tmp["uid"][int(num)-1]
                    else:
                        print("无效序号")
                        return
                else:
                    print("无效序号")
                    return
            if option_tmp["users"]. __contains__(uid) is not True:
                print("无效uid")
                return
            msg = { "cmd": "getUserData", "uid": uid }
            ws.send(add_ts(msg))
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

    def setUser(self, ws):
        print("输入要设置的用户的uid：")
        uid = input()
        if (uid[len(uid)-1]) == ".":
            num = uid[0:-1]
            if num.isdecimal() is True:
                if int(num) <= len(option_tmp["uid"]):
                    uid = option_tmp["uid"][int(num)-1]
                else:
                    print("无效序号")
                    return
            else:
                print("无效序号")
                return
        if option_tmp["users"]. __contains__(uid) is not True:
            print("无效uid")
            return
        print("输入要设置的用户项目：")
        key = input()
        if option_tmp["users"][uid]. __contains__(key) is not True:
            print("无效key")
            return
        print("输入要设置的用户项目的值：")
        val = input()
        option_tmp["users"][uid][key] = self.decide_type(val)
        msg = { "cmd":"setUserData", "uid": uid, "data": option_tmp["users"][uid] }
        ws.send(add_ts(msg))

    def setConfig(self, ws):
        print("输入要设置的全局项目：")
        key = input()
        print("输入要设置的全局项目的值：")
        val = input()
        option_tmp["config"][key] = self.decide_type(val)
        msg = { "cmd":"setConfig", "data": option_tmp["config"] }
        ws.send(add_ts(msg))

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

def on_message(self, message):
    msg = json.loads(message)
    MyWebSocket.msg_handler(msg)

def on_error(self, error):
    print(error)

def on_close(self):
    print("############### closed ###############")

def add_ts(msg):
    msg["ts"] = MyWebSocket.get_ts()
    message = json.dumps(msg)
    return message

def on_open(ws):
    def run(*args):
        msg = { "cmd":"getConfig" }
        ws.send(add_ts(msg))
        time.sleep(0.5)
        msg = { "cmd":"getAllUID" }
        ws.send(add_ts(msg))
        time.sleep(0.5)
        msg = { "cmd":"getInfo" }
        ws.send(add_ts(msg))
        time.sleep(0.5)
        while len(option_tmp["users"]) < len(option_tmp["uid"]):
            i = 0
            while i < len(option_tmp["uid"]):
                msg = { "cmd": "getUserData", "uid": option_tmp["uid"][i] }
                ws.send(add_ts(msg))
                i += 1
                time.sleep(0.5)
        time.sleep(1)
        cmd = "NOT CLOSE"
        print("options加载完毕")
        while cmd != "close":
            print("输入cmd:")
            cmd = input()
            MyWebSocket.run_cmd(MyWebSocket, ws, cmd)
        ws.close()
    thread.start_new_thread(run, ())

if __name__ == "__main__":
    #websocket.enableTrace(True)
    ws = websocket.WebSocketApp(url, subprotocols=[protocol],
        on_message = on_message,
        on_error = on_error,
        on_close = on_close)
    ws.on_open = on_open
    ws.run_forever()
