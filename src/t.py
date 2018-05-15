from PyQt5.QtCore import pyqtSlot
from PyQt5.QtGui import *
from PyQt5 import QtCore




app = QApplication(sys.argv)
w = QWidget()
w.setWindowTitle('Projet Optimisation')
 
# Create textbox
t_text = QPlainTextEdit(w)
t_text.move(0, 0)
t_text.resize(300,200)



t_key = QLineEdit(w)
t_key.move(575, 100)
t_key.resize(150,50)

QLabel('          Enter Key :', t_key)

t_crypted = QPlainTextEdit(w)
t_crypted.move(1000, 0)
t_crypted.resize(300,200)

t_decrypted = QPlainTextEdit(w)
t_decrypted.move(1000,300)
t_decrypted.resize(300,300)


t_key_found = QLineEdit(w)
t_key_found.move(575, 400)
t_key_found.resize(150,50)

QLabel('          Key Found :', t_key_found)

t_iteration = QLineEdit(w)
t_iteration.move(600, 650)
t_iteration.resize(130,50)

QLabel('          Iterations :', t_iteration)

t_time = QLineEdit(w)
t_time.move(300, 650)
t_time.resize(100,50)

QLabel('          Time :', t_time)

listWidget = QListWidget(w)
listWidget.move(0, 350)
listWidget.resize(125,175)
listWidget.addItem("recherche local")
listWidget.addItem("tabou")
listWidget.addItem("genetique")


gui_tabou = QListWidget(w)
gui_tabou.move(200, 350)
gui_tabou.resize(175,250)
gui_tabou.hide()



# Set window size.
w.resize(1366, 768)
 
# Create a button in the window
b_go = QPushButton('Go', w)
b_go.move(550,200)
b_go.resize(200,100)


# Create the actions
@pyqtSlot()
def on_click():
	pass
    

# connect the signals to the slots
b_go.clicked.connect(on_click)
 
# Show the window and run the app
w.show()
app.exec_()