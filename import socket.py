import socket
import pyautogui
import threading
SERVER = "irc.twitch.tv"
PORT = 6667
PASS = ""
BOT = "TwitchBot"
CHANNEL = "duckyz11"
OWNER = "duckyz11"
message = ""
irc = socket.socket()
irc.connect((SERVER, PORT))
irc.send("PASS {} \r\n".format(PASS).encode("utf-8"))
irc.send("NICK {} \r\n".format(BOT).encode("utf-8"))
irc.send("JOIN {} \r\n".format(CHANNEL).encode("utf-8"))

def gamecontrol():
    global message
    while True:
        if "go" in message.lower():
            pyautogui.keyDown(' w ')
            message = ""
            pyautogui.keyUp(' w ')
        elif "back" in message.lower():
            pyautogui.keyDown(' s ')
            message = ""
            pyautogui.keyUp(' s ')
        elif "right" in message.lower():
            pyautogui.keyDown(' d ')
            message = ""
            pyautogui.keyUp(' d ')
        elif "left" in message.lower():
            pyautogui.keyDown(' a ')
            message = ""
            pyautogui.keyUp(' a ')
        elif "jump" in message.lower():
            pyautogui.keyDown(' space ')
            message = ""
            pyautogui.keyUp(' space ')
        elif "flash" in message.lower():
            pyautogui.keyDown(' q ')
            message = ""
            pyautogui.keyUp('q')
        elif "dismiss" in message.lower():
            pyautogui.keyDown('k')
            message = ""
            pyautogui.keyUp('k')
        elif "heal" in message.lower():
            pyautogui.keyDown(' l')
            message = ""
            pyautogui.keyUp('l')
        elif "Ult" in message.lower():
            pyautogui.keyDown(' b ')
            message = ""
            pyautogui.keyUp('b')
        else:
            pass
def twitch():
    def joinchat():
        Loading = True
        while Loading:
            readbuffer_join = irc.recv(1024)
            readbuffer_join = readbuffer_join.decode()
            for line in readbuffer_join.split("\n")[0:-1]:
                print(line)
                Loading = loadingComplete(line)



    def loadingComplete(line):
        if ("End of /NAMES list" in line):
            print("Bot has joined " + CHANNEL + "'s Channel!")
            sendMessage(irc, "Chat Room Joined")
            return False
        else:
            return True
    def sendMessage(irc, message):
        messageTemp = "PRIVMSG #" + CHANNEL +" :" + message
        irc.send((messageTemp + "\n").encode())

    def getUser(line):
        separate = line.split(":", 2)
        user = separate[1].split("!", 1)[0]
        return user

    def getMessage(line):
        global message
        try:
            message = (line.split(" :",2))[2]
        except:
            message =""
        return message
    def Console(line):
        if "PRIVMSG" in line:
            return False
        else:
            return True

    joinchat()

    while True:
        try:
            readbuffer = irc.recv(1024).decode()
        except:
            readbuffer =""
        for line in readbuffer.split("\r\n"):
            if line == "":
                continue
            if "PING" in line and Console(line):
                    msgg = "PONG tmi.Twitch.tv/r/n".encode()
                    irc.send(msgg)
                    print(msgg)
                    continue
            else:
                user = getUser(line)
                message = getMessage(line)
                print(user + ":" + message)
if __name__ =='__main__':
    t1 = threading.Thread(target = twitch)
    t1. start()
    t2 = threading.Thread(target = gamecontrol)
    t2. start()