import sys
import webbrowser
import csv
import time
from lxml import html
from appJar import gui
import requests

EndOF = 'endoffile'

class DeadAccountRemover():

    def updateProgress(self):
        if(self.accountCountTotal == 0):
            #print("here")
            percentComplete = 0
        else:
            #print("there" + str(100 * self.accountProcessedTotal / self.accountCountTotal))
            percentComplete = 100 * self.accountProcessedTotal / self.accountCountTotal
        #print(str(self.accountCountTotal) + " " + str(self.accountProcessedTotal) + " " +str(percentComplete) + " hey!!")
        self.app.setMeter("progress bar", percentComplete)

    #counts the total number of accounts inputed
    def sumAccounts(self, csvFile):
        sumOfAccounts = 0
        for line in csvFile:
            for account in line:
                sumOfAccounts +=1
        return sumOfAccounts
   
    def findDeadAccounts(self, file):

        #self.app.hideSubWindow("Open File")

        url = "https://www.instagram.com/"
        
    
        ACCOUNTNUMTOSEARCH = int(self.app.getEntry("Number of Accounts to Search Through"))
        #open csv file from first command line arg
        with open(file, 'r') as my_file:
            read = csv.reader(my_file, delimiter=',')
      

            accountProcessedTotal = self.accountProcessedTotal
            
            accountCurrentTotal = 0
            removedCurrentTotal = 0
            #set labels for progress information
            if(self.sumAccountCount == False):
                self.accountCountTotal = self.sumAccounts(read)
                self.app.setLabel("l1", "Total Accounts To Be Processed: " + str(self.accountCountTotal))
                self.sumAccountCount = True

            startAtSpecificAccount = False
            self.app.infoBox('FYI','working on removing accounts')
            
            nextAccount = self.nextAccount
            startAtFirstAccount = self.startAtFirstAccount


            my_file.seek(0,0)
            read = csv.reader(my_file, delimiter=',')
            #read csv by line
            for line in read:
                
                startTime = time.time()
                #Do this if we are starting with the first line
                if(startAtFirstAccount):
                    print("Starting with the first account")
                    for account in line:
                        print("Account #: %d" % accountCurrentTotal)
                        if (accountCurrentTotal == ACCOUNTNUMTOSEARCH):
                            print("Taking a short break...")
                            print(time.time() - startTime)
                            print("1")
                            accountProcessedTotal += accountCurrentTotal
                            self.accountProcessedTotal = accountProcessedTotal
                            accountsKept = accountProcessedTotal - self.removedTotal
                            self.app.setLabel("l2", "Total Accounts Processed: " + str(accountProcessedTotal))
                            self.app.setLabel("l6", "Total Accounts Kept: "+ str(accountsKept))
                            self.app.setSetting("self.accountCountTotal", self.accountCountTotal)
                            return account
                        accountCurrentTotal += 1
                        #attach username to IG url and open that url (2 = new tab)
                        urlWithAccount = url + account
                        #webbrowser.open(urlWithAccount,2)

                        try:
                            page = requests.get(urlWithAccount)
                        except requests.exceptions.RequestException as e:
                            print("2")
                            self.startAtFirstAccount = False
                            accountProcessedTotal += accountCurrentTotal
                            self.accountProcessedTotal = accountProcessedTotal-1
                            accountsKept = accountProcessedTotal - self.removedTotal - 1
                            self.app.setLabel("l2", "Total Accounts Processed: " + str(accountProcessedTotal-1))
                            self.app.setLabel("l6", "Total Accounts Kept: "+ str(accountsKept))
                            self.app.errorBox("Request Exception", str(e) + " \n Will Restart From Failed Account ")
                            self.app.setSetting("self.accountCountTotal", self.accountCountTotal)
                            return account
                            
                        tree = html.fromstring(page.content)
                        title = tree.xpath('//title/text()')
                        # print('working on account number' + str(accountCurrentTotal) + " " + account  )
                        if(title == ['\n                  Page Not Found • Instagram\n                ']):
                                print(title)
                                self.app.setTextArea("IG Users Removed", account+",")
                                removedCurrentTotal += 1
                                self.removedTotal += 1
                                self.app.setLabel("l3", "Total Accounts Removed: " + str(self.removedTotal))
                                self.app.setLabel("l4", "Total Accounts Removed In This Batch: " + str(removedCurrentTotal))
                                time.sleep((accountCurrentTotal+2)%30)
                        else:
                            self.app.setTextArea("IG Users To Keep", account+",")
                            #webbrowser.open(urlWithAccount,2)

                        self.app.setLabel("l5", "Total Accounts Processed In This Batch: " + str(accountCurrentTotal))
                        self.startAtFirstAccount = False
                    accountProcessedTotal += accountCurrentTotal
                    
                    print("53")
                    self.app.setLabel("l2", "Total Accounts Processed: " + str(accountProcessedTotal))

                        
   
                #otherwise do this
                if(startAtFirstAccount == False):
                    self.app.infoBox("Starting at...", "Next account: "+ nextAccount)
                    for account in line:
                        if(account == self.nextAccount):
                            startAtSpecificAccount = True
                        if(startAtSpecificAccount):
                            print("Account #: %d" % accountCurrentTotal)
                            if (accountCurrentTotal == ACCOUNTNUMTOSEARCH) :#accountCurrentTotal != 0 and accountCurrentTotal % 200 == 0):
                                print("Taking a short break...")
                                print(time.time() - startTime)
                                #print("13")
                                #time.sleep(600)
                                accountProcessedTotal += accountCurrentTotal
                                self.accountProcessedTotal = accountProcessedTotal
                                accountsKept = accountProcessedTotal - self.removedTotal 
                                self.app.setLabel("l2", "Total Accounts Processed: " + str(accountProcessedTotal))
                                self.app.setLabel("l6", "Total Accounts Kept: "+ str(accountsKept))
                                self.app.setSetting("self.accountCountTotal", self.accountCountTotal)
                                return account
                            
                            accountCurrentTotal += 1
                            #attach username to IG url and open that url (2 = new tab)
                            urlWithAccount = url + account
                            #webbrowser.open(urlWithAccount,2)
                            try:
                                page = requests.get(urlWithAccount)
                            except requests.exceptions.RequestException as e:
                                #print("14")
                                self.startAtFirstAccount = False
                                accountProcessedTotal += accountCurrentTotal
                                self.accountProcessedTotal = accountProcessedTotal-1
                                accountsKept = accountProcessedTotal - self.removedTotal - 1
                                self.app.setLabel("l2", "Total Accounts Processed: " + str(accountProcessedTotal-1))
                                self.app.setLabel("l6", "Total Accounts Kept: "+ str(accountsKept))
                                self.app.errorBox("Request Exception", str(e) + " \n Will Restart From Failed Account ")
                                self.app.setSetting("self.accountCountTotal", self.accountCountTotal)
                                return account
                            
                            tree = html.fromstring(page.content)
                            title = tree.xpath('//title/text()')
                            # print('working on account number' + str(accountCurrentTotal) + " " + account  )
                            if(title == ['\n                  Page Not Found • Instagram\n                ']):
                                print(title)
                                self.app.setTextArea("IG Users Removed", account+",")
                                removedCurrentTotal += 1
                                self.removedTotal += 1
                                self.app.setLabel("l3", "Total Accounts Removed: " + str(self.removedTotal))
                                self.app.setLabel("l4", "Total Accounts Removed In This Batch: " + str(removedCurrentTotal))
                                time.sleep((accountCurrentTotal+2)%30)
                            else:
                                self.app.setTextArea("IG Users To Keep", account+",")
                                #webbrowser.open(urlWithAccount,2)
                                

                            #print("15")
                            self.app.setLabel("l5", "Total Accounts Processed In This Batch: " + str(accountCurrentTotal))
                            self.startAtFirstAccount = False
                        
 
 
        self.app.setSetting("self.accountCountTotal", self.accountCountTotal)                           
        return EndOF

    #
    #
    def learnMyFriends(self, file):
        self.app.showSubWindow("LMF")
        with open(file, 'r') as my_file:
            read = csv.reader(my_file, delimiter=',')
            for line in read:
                for account in line:
                    
                    if(self.isKnowPlayer):
                        self.app.setTextArea("IG Users To Keep", account+",")
                    else:
                        self.app.setTextArea("IG Users Removed", account+",")
        
            accounts2Save = open(self.newFileName + "LFWL.csv", 'w')
            accounts2Remove = open(self.newFileName + "LFBL.csv", 'w')
            accounts2Save.write(self.app.getTextArea("IG Users To Keep"))
            accounts2Remove.write(self.app.getTextArea("IG Users Removed"))
            accounts2Remove.close()
            accounts2Save.close();
        
            
    def buttonOptions(self, button):
        if(button == "Find"):
            print("accountCountTotal: " + str(self.accountCountTotal))
            #self.app.openSubWindow("Open File")
            file = self.app.openBox(fileTypes=[("Comma Seperated Value","*.csv")])#parent="Open File")
            #self.app.hideSubWindow("Open File")
            #self.app.stopSubWindow()
            self.nextAccount = self.findDeadAccounts(file)
        if(button == "Save"):
            self.app.showSubWindow("Name File")
        if(button == "Quit"):
            self.app.stop()
        if(button == "Submit"):
            self.app.hideSubWindow("Name File")
            self.newFileName = self.app.getEntry("Name File: ")
            accounts2Save = open(self.newFileName + "WL.csv", 'w')
            accounts2Remove = open(self.newFileName + "BL.csv", 'w')
            accounts2Save.write(self.app.getTextArea("IG Users To Keep"))
            accounts2Remove.write(self.app.getTextArea("IG Users Removed"))
            accounts2Remove.close()
            accounts2Save.close();
        if(button == "Learn My Friends"):
            self.app.infoBox("FYI", "1.This feature helps to weed out users you are not friends with \n \
2. This feature does not use the progress bar \n \
3. This feature should be used after finding dead accounts")
            file = self.app.openBox(fileTypes=[("Comma Seperated Value","*.csv")])#parent="Open File")
            self.learnMyFriends(file)

    def LMFButtonOptions(self, button):
        if(button == "Yes"):
            self.isKnownPlayer = True
        if(button == "Pause"):
            self.app.hideSubWindow("LMF")
        if(button == "No"):
            self.isKnownPlayer = False
            
            
            
            
        
            
    def setup(self):
        app = gui(useSettings=True)
        
        app.setTitle("Defunct Instagram Account Remover")

        #file open
        app.startSubWindow("Name File", modal=True, title="Name File")
        app.addLabelEntry("Name File: ")
        app.setResizable(canResize=False)
        app.addButtons(["Submit"],self.buttonOptions)
        app.stopSubWindow()

        #Learn My Friends SubWindow
        app.startSubWindow("LMF", modal=True, title="Learn My Friends")
        app.setResizable(canResize=False)
        app.addLabel("LMFLabel1", "Do you know: ?")
        app.addButtons(["Yes","Pause","No"],self.LMFButtonOptions)
        app.stopSubWindow()

        #text areas
        app.addLabel("IG Users To Keep")
        app.addTextArea("IG Users To Keep")
        app.addLabel("IG Users Removed")
        app.addTextArea("IG Users Removed")

        #accounts to search entry
        app.addLabelNumericEntry("Number of Accounts to Search Through")
        app.setEntry("Number of Accounts to Search Through", "25")

        #count labels
        app.addLabel("l1", "Total Accounts To Be Processed: 0")
        app.addLabel("l5", "Total Accounts Processed In This Batch: 0" )
        app.addLabel("l2", "Total Accounts Processed: 0" )
        app.addLabel("l3", "Total Accounts Removed: 0" )
        app.addLabel("l4", "Total Accounts Removed In This Batch: 0")
        app.addLabel("l6", "Total Accounts Kept: 0")

        #buttons
        app.addButtons(["Find","Learn My Friends","Save","Quit"], self.buttonOptions)

        #progress bar
        app.addMeter("progress bar")
        app.registerEvent(self.updateProgress)


        #global vars
        self.app = app
        self.nextAccount = ''
        self.startAtFirstAccount = True
        self.sumAccountCount = False
        self.removedTotal = 0
        self.accountProcessedTotal = 0
        self.accountCountTotal = 0
        self.newFileName = ''
        self.isKnownUser = False

 
        
        app.go()

if __name__ == '__main__':
    app = DeadAccountRemover()
    app.setup()
    
        
