﻿import re
import sys
import json
import datetime
from datetime import datetime
from datetime import timedelta, date


class WhatsAppChatParser:
    message = ""
    insideMessage = False

    def __init__(self, chatExportFile ):
        self.quoteList = []
        self.ignoredList = []
        self.quoteIndex = 0
        self.deletedPattern()
        self.author = 'All'
        self.SetStartDate('01/01/00')
        self.SetEndDate('01/01/68')
        self.messageDate = '01/01/00'
       
    def SetMessageAuthor(self, author):
        self.author = author

    def SetStartDate(self,startDate):
        self.startDate = startDate
        self.startDateDays = (datetime.strptime(self.startDate,"%d/%m/%y")-datetime(1970,1,1)).days

    def SetEndDate(self,endDate):
        self.endDate = endDate
        self.endDateDays = (datetime.strptime(self.endDate,"%d/%m/%y")-datetime(1970,1,1)).days

    def isStartOfMewMessage(self,line):
        tsPattern = re.compile("[^\d]*(\d+\/\d+\/\d+),.* [Aa|Pp][Mm]")
        m = tsPattern.match(line)
        if ( m ):
            self.messageDate = m.group(1)
            return ( True)
        return (False)

    def isPermissibleAuthor(self,line):
        if ( self.author == 'All' ):
            return ( True)
        authorpatthern = re.compile(".*"+self.author+"\s*: ")
        authormatch = authorpatthern.match(line)
        if( authormatch ):
            return (True)
        return (False)

    def isInAcceptableTimeRange(self):
        # if self.messageDate is in the given date range return true
        self.messageSateDays = (datetime.strptime(self.messageDate,"%d/%m/%y")-datetime(1970,1,1)).days
        if ( (self.messageSateDays >= self.startDateDays) and  (self.messageSateDays  <= self.endDateDays) ):
            return(True)
        return(False)

    def ExtractMessageFromLine(self, line):
        authorpatthern = re.compile(".* [Aa|Pp][Mm][^:]*: (.*)")
        authormatch = authorpatthern.match(line)
        if ( authormatch) :
            return(authormatch.group(1))
        return('')
    
    def deletedPattern(self):
        messageYouDeletedMsgPattern = ".*You deleted this message."
        messageOtherDeletedMsgPattern = ".*This message was deleted."
        messageWebsiteLinkPattern = ".*http"
        messageOmitted = ".Media omitted"
        documentOmitted = ".document omitted"
        imageOmitted = ".‎image omitted"
        videoOmitted = ".‎video omitted"
        audioOmitted = ".‎audio omitted"
        gifOmitted = ".GIF omitted"
        messageEncryption = ".*Messages to this chat"
        messageGroupEncryption = ".*Messages to this group"
        messageGroupSubjectChange = ".*changed the subject to “.*”"
        messageGroupDescriptionChanged = ".*changed the group description"
        messageGroupDescriptionDeleted = ".*deleted the group description"
        self.ignoredList.append(messageYouDeletedMsgPattern)
        self.ignoredList.append(messageOtherDeletedMsgPattern)
        self.ignoredList.append(messageWebsiteLinkPattern)
        self.ignoredList.append(messageOmitted)
        self.ignoredList.append(documentOmitted) 
        self.ignoredList.append(imageOmitted) 
        self.ignoredList.append(videoOmitted) 
        self.ignoredList.append(audioOmitted) 
        self.ignoredList.append(gifOmitted) 
        self.ignoredList.append(messageEncryption)
        self.ignoredList.append(messageGroupEncryption)
        self.ignoredList.append(messageGroupSubjectChange) 
        self.ignoredList.append(messageGroupDescriptionChanged) 
        self.ignoredList.append(messageGroupDescriptionDeleted) 
        
        



    def shouldThisBeIgnored(self, line ):

        gotMatch = False
        for regex in self.ignoredList:
            s = re.search(regex,line)
            if( s ):
                gotMatch = True
                break
        if gotMatch:
            return (True)
        return (False)


    def ExtractQuoteList(self, chatExportFile ):
        fileHandler = open (chatExportFile, "r", encoding="utf8")
        while True:
            
            line = fileHandler.readline()
            if not line :
                break;
            if ( self.shouldThisBeIgnored(line) ):
                continue
            if ( self.isStartOfMewMessage(line)):
                if ( self.insideMessage ) :
                    self.appendMessageToQuoteList()
                    self.insideMessage = False
                    self.message = ''

                if ( self.isPermissibleAuthor(line) ):
                    if ( self.isInAcceptableTimeRange()):
                        self.message = self.ExtractMessageFromLine(line)
                        self.insideMessage = True
            elif ( self.insideMessage ):
                self.message = self.message + line
        # Close Close
        fileHandler.close()
        if ( self.insideMessage ):
            self.appendMessageToQuoteList()
            self.insideMessage = False

    def appendMessageToQuoteList(self):
        if (len(self.message) > 5):
            self.message = re.sub(r'\n+', '\n', self.message).strip()
            self.quoteList.append(self.message)

    	

 
    def getNextQuote(self):
        if ( self.quoteIndex >= len(self.quoteList)):
            raise
        self.message = self.quoteList[self.quoteIndex]
        self.time = self.quoteList[self.quoteIndex]
        self.quoteIndex += 1
        return ( self.message )
