from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

class MainWindow(QWidget):

    class Button(QWidget):
        def __init__(self, row, column):
            super().__init__()
            self.b_list = [''] * row * column
        
        def create(self, index, text, function):
            btn = QPushButton(text, clicked = lambda:function)
            self.b_list[index] = btn

    def __init__(self):
        super().__init__()
        self.setWindowTitle('Calculator')
        self.setLayout(QVBoxLayout())
        self.number = '0123456789'
        self.operator = ['+','-','\u00D7','÷']
        self.point = '.'
        self.power = '\u00D710\u02E3'
        self.answer = 'Ans'
        self.equal = '='
        self.delete = 'DEL'
        self.all_clear = 'AC'
        self.font_size = 0
        self.font_type = ''
        self.display_size = 0
        self.temp_entry = ''
        self.text_button = [['7','8','9',self.delete,self.all_clear],['4','5','6',self.operator[2],self.operator[3]],['1','2','3',self.operator[0],self.operator[1]],['0',self.point,self.power,self.answer,self.equal]]
        self.button_key = self.Button(len(self.text_button), len(self.text_button[0]))

    def keypad(self):
        box = QWidget()
        box.setLayout(QGridLayout())
        self.display_box =  QLineEdit()
        self.display_box.setMaxLength(self.display_size)
        self.display_box.setAlignment(Qt.AlignRight)
        box.layout().addWidget(self.display_box, 0, 0, 1, 5)
        button_index = 0
        for i in range(len(self.text_button), 0, -1):
            
            for j in range(len(self.text_button[0])):
                text = self.text_button[i-1][j]
                self.button_key.create(button_index, text, self.press(text))
                #button = QPushButton(text, clicked = lambda:self.press(text))
                box.layout().addWidget(self.button_key.b_list[button_index], i, j)

        self.layout().addWidget(box)

    def display_update(self):
        self.display_box.setMaxLength(self.display_size)

    def press(self,text):
        if text in self.number:
            self.temp_entry += text
            self.display_size += 1
            self.display_update()
            self.display_box.setText(self.temp_entry) 
application = QApplication([])
window = MainWindow()
window.keypad()
window.show()
application.exec_()