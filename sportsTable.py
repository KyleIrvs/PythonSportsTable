
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import *
import ctypes
from SportsUi import Ui_Dialog
import os.path
import json

class team:
    def __init__(self, tName, played , won, lost, drawn, points):
        self.Name = tName
        self.played = played
        self.won = won
        self.lost = lost
        self.drawn = drawn
        self.points = points

class logTeams(object):

    def __init__(self):
        self.teamCount = 0
        self.totalT = 1
        self.teams = self.make_array(self.totalT)

    def getTeamAtPos(self,k):
        if not 0 <= k < self.teamCount:
            return IndexError("This number is out of bounds")

        return self.teams[k]

    def getTeamFromName(self, teamName, arr):
        found = False
        for i in range(len(arr)):
            if teamName == arr[i].Name:
                return arr[i]
        if not found:
            print("team not found")
        pass

    def addTeam(self, teamName,points,played,won,lost,drawn):

        newTeam = team(teamName,points,played,won,lost,drawn)

        if self.teamCount == self.totalT:
            self.resizeTotals(self.totalT + 1)

        self.teams[self.teamCount] = newTeam
        self.teamCount += 1

    def resizeTotals(self, newTotal):
        tmp = self.make_array(newTotal)

        for i in range(self.teamCount):
            tmp[i] = self.teams[i]

        self.teams = tmp
        self.totalT = newTotal

    def make_array(self, newTotal):
        return (newTotal * ctypes.py_object)()

    #Simple prints out entire array to console
    def printArr(self, arr):
        for x in range(len(arr)):
            print(arr[x].Name +" "+  str(arr[x].points))

    #Sorts all teams by score using bubble sort (others aren't needed as it is a small array)
    def Sort(self, arr):
        tempArr = arr
        n = len(arr)
        for i in range(len(arr)-1,0,-1):
            for j in range(i):
                if int(arr[j].points) > int(arr[j+1].points):
                    temp = arr[j]
                    arr[j] = arr[j+1]
                    arr[j+1] = temp
        #self.printArr(arr)

    def updatePoints(self,team1, team2):
        pass



class mainForm(QtWidgets.QMainWindow, Ui_Dialog):
    def __init__(self, parent=None):
        super(mainForm, self).__init__(parent)
        self.data = {}
        self.data['teams'] = []
        self.setupUi(self)
        self.currentLog = logTeams()
        self.initLog()
        #Calls function when button is clicked
        self.btnAddResult.clicked.connect(self.addResult)
        self.btnAddTeam.clicked.connect(self.addNewTeam)

    #Loads all data from json file into data array with all team information
    def initLog(self):
        self.cmbTeam1.addItem("Select Team 1")
        self.cmbTeam2.addItem("Select Team 2")
        if os.path.isfile('teamData.txt') and not os.stat("teamData.txt").st_size == 0:
            print("FileExists, listing all current teams")
            with open('teamData.txt') as teamJson:
                teamData = json.load(teamJson)
                for tD in teamData['teams']:
                    self.currentLog.addTeam(tD['name'], int(tD['played']),int(tD['won']),int(tD['lost']),int(tD['drawn']),int(tD['points']),)
                    self.cmbTeam1.addItem(tD['name'])
                    self.cmbTeam2.addItem(tD['name'])
                    self.data['teams'].append({
                        'name' : tD['name'],
                        'played' : str(tD['played']),
                        'won' : str(tD['won']),
                        'lost' : str(tD['lost']),
                        'drawn' : str(tD['drawn']),
                        'points' : str(tD['points'])

                    })
            self.updateTable()
        else:
            f = open("teamData.txt", "w+")
            f.close()

            #TODO get the json file to save all points data by having it update the dump data after before updateTable


    def updateTable(self):
        self.currentLog.Sort(self.currentLog.teams)
        self.tblLog.setRowCount(self.currentLog.teamCount)
        for i in  range(self.currentLog.teamCount):
            self.tblLog.setItem(i,0, QTableWidgetItem(self.currentLog.teams[i].Name))
            self.tblLog.setItem(i,1, QTableWidgetItem(str(self.currentLog.teams[i].played)))
            self.tblLog.setItem(i,2, QTableWidgetItem(str(self.currentLog.teams[i].won)))
            self.tblLog.setItem(i,3, QTableWidgetItem(str(self.currentLog.teams[i].drawn)))
            self.tblLog.setItem(i,4, QTableWidgetItem(str(self.currentLog.teams[i].lost)))
            self.tblLog.setItem(i,5, QTableWidgetItem(str(self.currentLog.teams[i].points)))
        self.dump()

    #Function to add team to the log and all lists
    def addNewTeam(self):
        if  self.lineEdit.text():
            temp = team(self.lineEdit.text(),0,0,0,0,0)
            self.currentLog.addTeam(temp.Name,0,0,0,0,0)

        #Will add all to file but only after array is updated
            self.data['teams'].append({
                'name' : temp.Name,
                'played' : str(temp.played),
                'won' : str(temp.won),
                'lost' : str(temp.lost),
                'drawn' : str(temp.drawn),
                'points' : str(temp.points)

            })
            self.cmbTeam1.addItem(temp.Name)
            self.cmbTeam2.addItem(temp.Name)
            self.dump()
            self.updateTable()
            self.lineEdit.clear()

    def dump(self):
        with open('teamData.txt', 'w') as outfile:
            json.dump(self.data, outfile)


    #Function to add result to respective teams and update log
    def addResult(self):
        team1Name = self.cmbTeam1.currentText()
        team2Name = self.cmbTeam2.currentText()
        team1 = self.currentLog.getTeamFromName(team1Name,self.currentLog.teams)
        team2 = self.currentLog.getTeamFromName(team2Name,self.currentLog.teams)

        team1.played += 1
        team2.played += 1

        if self.spinBox.value() > self.spinBox_2.value():
            team1.won += 1
            team2.lost += 1
            team1.points+= 4
        else:
            team2.won += 1
            team1.lost += 1
            team2.points+= 4

        self.updateTable()



if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    sportsUi = mainForm()
    sportsUi.show()
    sys.exit(app.exec_())
