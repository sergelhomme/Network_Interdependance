#---------------------------------------------------------------------
#
# Copyright Serge Lhomme
# EMAIL: serge.lhomme (at) u-pec.fr
# WEB  : http://serge.lhomme.pagesperso-orange.fr/deven.html
#
# Outil pour analyser des AMDE
#
#---------------------------------------------------------------------
#
# licensed under the terms of GNU GPL 2
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
#---------------------------------------------------------------------

from PyQt4 import QtCore, QtGui
from matplotlib import pyplot as plt
import matplotlib.patches as patches
import numpy as np
import networkx as nx
import sys
import os
import csv
from ui_textedit import  Ui_MainWindow
from bardialog import UiBar

class MyForm(QtGui.QMainWindow):
     def __init__(self, parent=None):
         QtGui.QMainWindow.__init__(self, parent)
         self.ui = Ui_MainWindow()
         self.ui.setupUi(self)
         QtCore.QObject.connect(self.ui.pushButton, QtCore.SIGNAL("clicked()"),self.message)
         QtCore.QObject.connect(self.ui.pushButton_2, QtCore.SIGNAL("clicked()"),self.testText)
         QtCore.QObject.connect(self.ui.actionEffet, QtCore.SIGNAL("triggered()"),self.message)
         QtCore.QObject.connect(self.ui.actionCause, QtCore.SIGNAL("triggered()"),self.message_inv)
         QtCore.QObject.connect(self.ui.actionScenario, QtCore.SIGNAL("triggered()"),self.testText)
         QtCore.QObject.connect(self.ui.actionPdf, QtCore.SIGNAL("triggered()"),self.print_)
         QtCore.QObject.connect(self.ui.actionHtml, QtCore.SIGNAL("triggered()"),self.save)
         QtCore.QObject.connect(self.ui.actionVisualisation, QtCore.SIGNAL("triggered()"),self.amde)
         QtCore.QObject.connect(self.ui.actionModification, QtCore.SIGNAL("triggered()"),self.modifier_amde)
         QtCore.QObject.connect(self.ui.actionStatistique, QtCore.SIGNAL("triggered()"),self.stat)
         QtCore.QObject.connect(self.ui.actionHistogramme, QtCore.SIGNAL("triggered()"),self.hist)
         QtCore.QObject.connect(self.ui.actionGraph, QtCore.SIGNAL("triggered()"),self.gr)
         QtCore.QObject.connect(self.ui.actionExport, QtCore.SIGNAL("triggered()"),self.export)
         QtCore.QObject.connect(self.ui.actionExport2, QtCore.SIGNAL("triggered()"),self.relation)
         QtCore.QObject.connect(self.ui.actionAppli, QtCore.SIGNAL("triggered()"),self.appli) 
         global am
         global net
         global filepath
         p = os.path.abspath(__file__)
         (filepath, filename) = os.path.split(p)
         phr = 'Bienvenue dans la nouvelle application spéciale AMDE. <br> <br> Attention, vous travaillez dans le dossier : ' + str(filepath) + ' . L\'outil se permettra de modifier ce dossier, en y sauvegardant par exemple les fichiers nécessaires à son fonctionnement. Assurez vous d\'avoir une copie de votre fichier amde.csv ailleurs.'
         adresse = os.path.join(filepath, "amde.csv")
         am = []
         test = 0
         try :
              f = open(adresse, "rt")
              reader = csv.reader(f)
              for row in reader :
                   if len(row) == 6 :
                        am = am + [row]
              f.close()
         except :
              phr = phr + "<br><br> Il n'y a pas de fichier amde.csv dans le dossier "+ str(filepath) +", vous n'allez pas pouvoir faire grand chose."
              test = 1
         if test == 0 :
                   net = []
                   for i in range(len(am)):
                        effet2 = am[i][3].split(';')
                        for j in range(len(effet2)):
                             for k in range(len(am)):
                                  cause2 = am[k][2].split(';')
                                  for l in range(len(cause2)):
                                       if cause2[l]==effet2[j]:
                                            net = net + [[i+1,k+1]]
         self.ui.textEdit.setText(phr)

     def print_(self):
        document = self.ui.textEdit.document()
        printer = QtGui.QPrinter()
        dlg = QtGui.QPrintDialog(printer, self)
        if dlg.exec_() != QtGui.QDialog.Accepted:
            return
        document.print_(printer)
        self.statusBar().showMessage("Ready", 2000)
        
     def save(self):
        filename = QtGui.QFileDialog.getSaveFileName(self,
                "Choose a file name", '.', "HTML (*.html *.htm)")
        if not filename:
            return
        file = QtCore.QFile(filename)
        if not file.open(QtCore.QFile.WriteOnly | QtCore.QFile.Text):
            QtGui.QMessageBox.warning(self, "Dock Widgets",
                    "Cannot write file %s:\n%s." % (filename, file.errorString()))
            return
        out = QtCore.QTextStream(file)
        QtGui.QApplication.setOverrideCursor(QtCore.Qt.WaitCursor)
        out << self.ui.textEdit.toHtml()
        QtGui.QApplication.restoreOverrideCursor()
        self.statusBar().showMessage("Saved '%s'" % filename, 2000)
          
     def saveFile(self, fileName):
        file = QtCore.QFile(fileName)
        if not file.open(QtCore.QFile.WriteOnly | QtCore.QFile.Text):
            QtGui.QMessageBox.warning(self, "Application",
                    "Cannot write file %s:\n%s." % (fileName, file.errorString()))
            return False
        outf = QtCore.QTextStream(file)
        QtGui.QApplication.setOverrideCursor(QtCore.Qt.WaitCursor)
        outf << self.ui.textEdit.toPlainText()
        QtGui.QApplication.restoreOverrideCursor()
        self.setCurrentFile(fileName);
        self.statusBar().showMessage("File saved", 2000)
        return True
         
     def testText(self):
        text, ok = QtGui.QInputDialog.getText(self, "QInputDialog.getText()",
                "Numero fonction perturbe:", QtGui.QLineEdit.Normal,
                "")
        if ok and text != '':
            text2, ok = QtGui.QInputDialog.getText(self, "QInputDialog.getText()",
                "Numero fonction autre:", QtGui.QLineEdit.Normal,
                "")
            if ok and text2 != '':
                 adressefleche = os.path.join(filepath, "fleche.jpg")
                 dep=int(text)
                 arr=int(text2)
                 G = nx.DiGraph()
                 G.add_edges_from(net)
                 fin='<table width=100% border=0><tr bgcolor="#a2c511"><td width=20%><b>Nom</b></td><td><b>Effet</b></td></tr>'
                 try :
                    chemin = nx.shortest_path(G,dep,arr)
                    for i in range (len(chemin)):
                      if i<len(chemin)-1 :
                       numcomposant = chemin[i]
                       nomcomposant = am[numcomposant-1][0]
                       fin=fin+"<tr><td>"+str(nomcomposant)+"</td><td>"+str(am[numcomposant-1][3])+'</td></tr>'+"<tr><td colspan=2><img src='"+str(adressefleche)+"'></td></tr>"
                      if i==len(chemin)-1 :
                       numcomposant = chemin[i]
                       nomcomposant=am[numcomposant-1][0]
                       fin=fin+"<tr><td>"+str(nomcomposant)+"</td><td>"+str(am[numcomposant-1][3])+'</td></tr></table>'
                 except :
                      t = 'Do Nothing'
                 self.ui.textEdit.setText(fin)

     def modifier_amde(self):
        text, ok = QtGui.QInputDialog.getText(self, "Numero",
                "Numéro fonction :", QtGui.QLineEdit.Normal,
                "")
        if ok and text != '':
            text2, ok = QtGui.QInputDialog.getText(self, "Colonne",
                "Numéro de la colonne a modifier :", QtGui.QLineEdit.Normal,
                "")
            if ok and text2 != '':
                 text3, ok = QtGui.QInputDialog.getText(self, "texte",
                   "Texte a mofifier:", QtGui.QLineEdit.Normal,
                   "")
                 if ok and text3 != '':
                      am[int(text)-1][int(text2)-1] = text3
                      adresse = os.path.join(filepath, "amde.csv")
                      f = open(adresse, "wt")
                      w = csv.writer(f,lineterminator='\n')
                      for row in am :
                           w.writerow(row)
                      f.close()

     def amde(self):
         m = len(am)
         final2 = '<table width=100% border=0><tr height=100 bgcolor="#a2c511"><td><b><center>Numero</center></b></td><td><b><center>Reseau</center></b></td><td><b><center>Nom</center></b></td><td><b><center>Fonction</center></b></td><td><b><center>Causes</center></b></td><td><b><center>Effets</center></b></td></tr>'
         for i in range(m):
              final2 = final2+"<tr><td>"+str(i+1)+"</td>"+"<td>"+str(am[i][4])+"</td>"+"<td>"+str(am[i][0])+"</td><td>"+str(am[i][1])+"</td><td>"+str(am[i][2])+"</td><td>"+str(am[i][3])+"</td></tr>"
         final2 = final2+'</table>'
         self.ui.textEdit.setText(str(final2))
                   
     def message(self):
         G = nx.DiGraph()
         G.add_edges_from(net)
         m = len(am)
         final = '<table width=100% border=0><tr height=100 bgcolor="#a2c511"><td><b><center>Numero</center></b></td><td><b><center>Composant</center></b></td><td><b><center>Fonction</center></b></td><td><b><center>Numero pert</center></b></td><td><b><center>Composant Perturbe</center></b></td><td><b><center>Fonction Perturbee</center></b></td></tr>'
         self.dlg5 = UiBar(self)
         self.dlg5.ui.progressBar.setProperty("value", 0)
         self.dlg5.show()
         for i in range(m):
              valbar=int(i/float(m)*100)
              self.dlg5.ui.progressBar.setProperty("value", valbar)
              final=final+"<tr><td>"+str(i+1)+"</td>"+"<td>"+str(am[i][0])+"</td>"+"<td>"+str(am[i][1])+"</td><td></td><td></td><td></td></tr>"
              for j in range(m):
                 if j != i:
                     try :
                          spl = nx.shortest_path_length(G,i+1,j+1)
                          final = final+"<tr><td colspan=3><td>"+str(j+1)+"</td>"+"<td>"+str(am[j][0])+"</td>"+"<td>"+str(am[j][1])+"</td>"
                     except :
                          t = "Do Nothing"
         final=final+'</table>'
         self.dlg5.close()
         self.ui.textEdit.setText(str(final))
     
     def message_inv(self):
         G = nx.DiGraph()
         G.add_edges_from(net)
         m = len(am)
         final = '<table width=100% border=0><tr height=100 bgcolor="#a2c511"><td><b><center>Numero</center></b></td><td><b><center>Composant perturbe</center></b></td><td><b><center>Fonction perturbee</center></b></td><td><b><center>Numero pert</center></b></td><td><b><center>Composant</center></b></td><td><b><center>Fonction</center></b></td></tr>'
         self.dlg5 = UiBar(self)
         self.dlg5.ui.progressBar.setProperty("value", 0)
         self.dlg5.show()
         for i in range(m):
              valbar=int(i/float(m)*100)
              self.dlg5.ui.progressBar.setProperty("value", valbar)
              final=final+"<tr><td>"+str(i+1)+"</td>"+"<td>"+str(am[i][0])+"</td>"+"<td>"+str(am[i][1])+"</td><td></td><td></td><td></td></tr>"
              for j in range(m):
                   if j != i:
                        try :
                             spl = nx.shortest_path_length(G,j+1,i+1)
                             final = final+"<tr><td colspan=3><td>"+str(j+1)+"</td>"+"<td>"+str(am[j][0])+"</td>"+"<td>"+str(am[j][1])+"</td>"
                        except :
                             t = "Do Nothing"
         final=final+'</table>'
         self.dlg5.close()
         self.ui.textEdit.setText(str(final))
     	 
     def stat(self):
         G = nx.DiGraph()
         G.add_edges_from(net)
         m = len(am)
         final = '<table width=100% border=0><tr height=100 bgcolor="#a2c511"><td><b><center>Numero</center></b></td><td><b><center>Composant</center></b></td><td><b><center>Fonction</center></b></td><td><b><center>Nombre Effet</center></b></td><td><b><center>Nombre cause</center></b></td></tr>'
         self.dlg5 = UiBar(self)
         self.dlg5.ui.progressBar.setProperty("value", 0)
         self.dlg5.show()
         for i in range(m):
              ct1 = 0
              ct2 = 0
              valbar=int(i/float(m)*100)
              self.dlg5.ui.progressBar.setProperty("value", valbar)
              final=final+"<tr><td>"+str(i+1)+"</td>"+"<td>"+str(am[i][0])+"</td>"+"<td>"+str(am[i][1])+"</td><td></td><td></td></tr>"
              for j in range(m):
                 if j != i:
                     try :
                          spl = nx.shortest_path_length(G,i+1,j+1)
                          ct1 = ct1 + 1
                     except :
                          t = "Do Nothing"
                     try :
                          spl = nx.shortest_path_length(G,j+1,i+1)
                          ct2 = ct2 + 1
                     except :
                          t = "Do Nothing"
              final = final+"<tr><td colspan=3><td>"+str(ct1)+"</td>"+"<td>"+str(ct2)+"</td></tr>"
         self.dlg5.close()
         self.ui.textEdit.setText(str(final))
         
     def hist(self):
         G = nx.DiGraph()
         G.add_edges_from(net)
         m = len(am)
         self.dlg5 = UiBar(self)
         self.dlg5.ui.progressBar.setProperty("value", 0)
         self.dlg5.show()
         res1 = []
         res2 = []
         for i in range(m):
              ct1 = 0
              ct2 = 0
              valbar=int(i/float(m)*100)
              self.dlg5.ui.progressBar.setProperty("value", valbar)
              for j in range(m):
                 if j != i:
                     try :
                          spl = nx.shortest_path_length(G,i+1,j+1)
                          ct1 = ct1 + 1
                     except :
                          t = "Do Nothing"
                     try :
                          spl = nx.shortest_path_length(G,j+1,i+1)
                          ct2 = ct2 + 1
                     except :
                          t = "Do Nothing"
              res1 = res1 + [[i+1,ct1]]
              res2 = res2 + [[i+1,ct2]]
         self.dlg5.close()
         ares1 = np.array(res1)
         fig1 = plt.figure()
         ax1 = fig1.add_subplot(111)
         for i in range(m) :
              x = i + 0.6
              h = res1[i][1]
              ax1.add_patch( patches.Rectangle(
                   (x, 0),   # (x,y)
                   0.8,          # width
                   h,          # height
                   ))
         plt.ylim((0,max(ares1[:,1]+2)))
         plt.xlim((0,m + 2))
         plt.ylabel('Nombre Effets')
         plt.xlabel('Identifiant')
         plt.show()
         ares2 = np.array(res2)
         fig1 = plt.figure()
         ax1 = fig1.add_subplot(111)
         for i in range(m) :
              x = i + 0.6
              h = res2[i][1]
              ax1.add_patch( patches.Rectangle(
                   (x, 0),   # (x,y)
                   0.8,          # width
                   h,          # height
                   ))
         plt.ylim((0,max(ares2[:,1]+2)))
         plt.xlim((0,m + 2))
         plt.ylabel('Nombre Causes')
         plt.xlabel('Identifiant')
         plt.show()

     def gr(self):
         G = nx.DiGraph()
         G.add_edges_from(net)
         positi = nx.spring_layout(G)
         plt.plot(nx.draw(G,pos = positi,node_size=300,with_labels = True))
         plt.show()

     def export(self):
         G = nx.DiGraph()
         G.add_edges_from(net)
         m = len(am)
         self.dlg5 = UiBar(self)
         self.dlg5.ui.progressBar.setProperty("value", 0)
         self.dlg5.show()
         res = [["Numero","Composant","Fonction","Nombre Effet","Nombre cause"]]
         for i in range(m):
              ct1 = 0
              ct2 = 0
              valbar=int(i/float(m)*100)
              self.dlg5.ui.progressBar.setProperty("value", valbar)
              for j in range(m):
                 if j != i:
                     try :
                          spl = nx.shortest_path_length(G,i+1,j+1)
                          ct1 = ct1 + 1
                     except :
                          t = "Do Nothing"
                     try :
                          spl = nx.shortest_path_length(G,j+1,i+1)
                          ct2 = ct2 + 1
                     except :
                          t = "Do Nothing"
              res = res + [[i+1,am[i][0],am[i][1],ct1,ct2]]
         self.dlg5.close()
         adresse = os.path.join(filepath, "stat.csv")
         f = open(adresse, "wt")
         w = csv.writer(f,lineterminator='\n')
         for row in res :
              w.writerow(row)
         f.close()
         self.ui.textEdit.setText("Un fichier stat.csv a été créé dans le dossier "+str(filepath)+" .")

     def relation(self):
         adresse = os.path.join(filepath, "relation.csv")
         f = open(adresse, "wt")
         w = csv.writer(f,lineterminator='\n')
         for row in net :
              w.writerow(row)
         f.close()
         self.ui.textEdit.setText("Un fichier relation.csv a été créé dans le dossier "+str(filepath)+" .")

     def appli(self):
          adresse = os.path.join(filepath, "README.MD")
          fichier = open(adresse, "r")
          w = fichier.read()
          fichier.close()
          self.ui.textEdit.setText(str(w))

if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    myapp = MyForm()    
    myapp.show()
    sys.exit(app.exec_())
