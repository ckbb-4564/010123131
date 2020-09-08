from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

class MainWindow(QWidget):

    class Button(QWidget):
        def __init__(self, row, column):
            super().__init__()
            self.b_list = [''] * row * column
        
        def create(self, index, text, function):
            btn = QPushButton(text, clicked = lambda:function(text))
            self.b_list[index] = btn

    def __init__(self):
        super().__init__()
        self.setWindowTitle('Calculator')
        self.setLayout(QVBoxLayout())
        self.number = '0123456789'
        self.number_super = ['\u2070', '\u00B9', '\u00B2', '\u00B3', '\u2074', '\u2075', '\u2076', '\u2077', '\u2078', '\u2079']
        self.operator = ['+','-','\u00D7','÷']
        self.operator_super = []
        self.point = '.'
        self.power = '\u00D710\u02E3'
        self.mode_power = False
        self.answer = 'Ans'
        self.equal = '='
        self.delete = 'DEL'
        self.all_clear = 'AC'
        self.font_size = 0
        self.font_type = ''
        self.display_size = 0
        self.display_entry = ''
        self.eval_entry = ''
        self.old_answer = 0
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
                self.button_key.create(button_index, text, self.press)
                #button = QPushButton(text, clicked = lambda:self.press(text))
                box.layout().addWidget(self.button_key.b_list[button_index], i, j)

        self.layout().addWidget(box)

    def display_update(self):
        self.display_box.setMaxLength(self.display_size)

    def press(self,text):
        if text in self.number:
            if self.display_entry == '0':
                if text == '0':
                    pass
                else:
                    self.display_entry += text
                    self.eval_entry += text
                    self.display_size += 1
            else:
                if self.mode_power:
                    if self.display_entry[-2:] == '0'+self.number_super[0]:
                        pass
                    else:
                        self.display_entry += self.number_super[int(text)]
                        self.eval_entry += text
                        self.display_size += 1
                else:
                    self.display_entry += text
                    self.eval_entry += text
                    self.display_size += 1
        
        elif text in self.operator:
            if text == self.operator[1]:
                if self.display_entry == '' or self.display_entry[-1] == '(' or self.display_entry[-1] in self.number:
                    self.display_entry += text
                    self.eval_entry += text
                    self.display_size += 1
            elif self.display_entry[-1] in self.number:
                if text == self.operator[0]:
                    self.display_entry += text
                    self.eval_entry += text
                    self.display_size += 1
                elif text == self.operator[2]:
                    self.display_entry += text
                    self.eval_entry += '*'
                    self.display_size += 1
                elif text == self.operator[3]:
                    self.display_entry += text
                    self.eval_entry += '/'
                    self.display_size += 1
        
        elif text == self.delete:
            if self.display_size > 0:
                self.display_entry = self.display_entry[:-1]
                self.eval_entry = self.eval_entry[:-1]
                self.display_size -= 1
        
        elif text == self.all_clear:
            self.display_entry = ''
            self.eval_entry = ''
            self.display_size = 0
        
        elif text == self.point:
            if self.mode_power:
                pass
            else:
                if self.display_size == 0:
                    self.display_entry += '0.'
                    self.eval_entry += '0.'
                    self.display_size += 2
                else:
                    self.display_entry += '.'
                    self.eval_entry += '.'
                    self.display_size += 1
        
        elif text == self.power:
            if self.display_size > 0 and self.mode_power == False:
                self.mode_power = not self.mode_power 
                self.display_entry += '\u00D710'
                self.eval_entry += '*10**'
                self.display_size += 3
            elif self.display_size > 0 and self.mode_power == True:
                self.mode_power = not self.mode_powera
        
        elif text == self.answer:
            if self.display_entry[-1] in self.number or self.display_entry[-1] == 's':
                pass
            else:
                self.display_entry += self.answer
                self.eval_entry += self.old_answer
                print(self.eval_entry)
                self.display_size += 3
        
        elif text == self.equal:
            if self.display_size > 0:
                if self.display_entry[-1] in self.number or self.display_entry[-1] == 's' or self.display_entry[-1] in self.number_super:
                    try:
                        result = str(eval(self.eval_entry))
                        self.eval_entry = result
                        self.old_answer = result
                    except ZeroDivisionError:
                        result = 'ERROR: Division by zero'
                        self.display_state = 'ERROR'
                        self.old_answer = 0
                    except SyntaxError:
                        result = 'ERROR: SyntaxError'
                        self.display_state = 'ERROR'
                        self.old_answer = 0
                self.display_entry = result
                self.display_size = len(result)
        
        self.display_update()
        self.display_box.setText(self.display_entry)

application = QApplication([])
window = MainWindow()
window.keypad()
window.show()
application.exec_()