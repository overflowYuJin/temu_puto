# 24, 10.13.....

from PyQt5.QtWidgets import QWidget, QPushButton, QApplication, QFileDialog, QLabel, QHBoxLayout, QDialog, QVBoxLayout, QMessageBox
import sys
import subprocess
import json
import os
import time

main_py_path = False

class make_window(QWidget):
    def __init__(self, width, height, title):
        super().__init__()
        self.width = width
        self.height = height
        self.title = title

        # 만듬
        self.setFixedSize(self.width , self.height)
        self.setWindowTitle(self.title)


class make_button(QWidget):
    def __init__(self, width, height, name, parent):
        super().__init__(parent)
        self.width = width
        self.height = height
        self.name = name

        # 만듬
        self.button = QPushButton(self.name, self)
        self.button.setFixedSize(self.width, self.height)

def find_main_path():
    
    dialog = QDialog()
    dialog.setWindowTitle("경고")
    dialog.setFixedSize(300,150)

    dialog.setStyleSheet("background-color : #e7e7e7;")

    layout = QHBoxLayout()
    layout2 = QVBoxLayout()

    label = QLabel("실행을 위하여 main.py를 찾아주세요.", dialog)
    label.setStyleSheet("background-color : #e7e7e7; color : black;")


    layout2.addWidget(label)

    yes_button = QPushButton("찾기", dialog)
    no_button = QPushButton("취소", dialog)

    yes_button.setStyleSheet("""
    QPushButton {
        background-color: #3b8e3b;
        color : white;
        border-radius : 10px;
        padding : 5px 10px;
    }
    QPushButton:hover {
       background-color : #369036;                      
    }
    

    """)

    no_button.setStyleSheet("""
    QPushButton {
        background-color : #a0a0a0;
        color : black;
        border-radius : 10px;
        padding : 5px 10px;
    }    
    QPushButton:hover {
        background-color: 8a8a8a;
    }
    """)

    yes_button.clicked.connect(dialog.accept)
    no_button.clicked.connect(dialog.reject)

    layout.addWidget(yes_button)
    layout.addWidget(no_button)

    layout2.addLayout(layout)

    dialog.setLayout(layout2)

    result = dialog.exec_()

    try:
        if result == QDialog.Accepted:
            options = QFileDialog.Options()
            file_name, _ = QFileDialog.getOpenFileName(None, "파일 열기", "", "파이썬 파일 (*.py)", options=options)
            if file_name: # 파일을 찾음
                base_name = os.path.basename(file_name) # << 경로에서 파일 이름과 확장자를 추출한다함.
                name, ext = os.path.splitext(base_name)
                if name == "main.py":
                    print("done")
    except Exception as E:
        print(f"{E}, exit")
        sys.exit()

def show_warning():

    msg_box = QMessageBox()
    
    # 메시지 박스 설정
    msg_box.setIcon(QMessageBox.Warning)
    msg_box.setWindowTitle("경고")
    msg_box.setText("가능한 확장자 : png, jpg")
    msg_box.setInformativeText("닫기 버튼을 눌러야 창이 닫힙니다.")
    msg_box.setStandardButtons(QMessageBox.Close)

    msg_box.exec_()

    time.sleep(1)

def OpenFile_ForImage():

    show_warning()

    dialog = QDialog()
    dialog.setWindowTitle("안내")
    dialog.setFixedSize(300,150)

    dialog.setStyleSheet("background-color : #e7e7e7;")

    layout = QHBoxLayout()
    layout2 = QVBoxLayout()

    label = QLabel("열기를 눌러 편집하고 싶은 사진을 선택합니다.", dialog)
    label.setStyleSheet("background-color : #e7e7e7; color : black;")

    layout2.addWidget(label)

    yes_button = QPushButton("열기", dialog)
    no_button = QPushButton("취소", dialog)

    yes_button.setStyleSheet("""
    QPushButton {
        background-color: #3b8e3b;
        color : white;
        border-radius : 10px;
        padding : 5px 10px;
    }
    QPushButton:hover {
       background-color : #369036;                      
    }
    

    """)

    no_button.setStyleSheet("""
    QPushButton {
        background-color : #a0a0a0;
        color : black;
        border-radius : 10px;
        padding : 5px 10px;
    }    
    QPushButton:hover {
        background-color: 8a8a8a;
    }
    """)

    yes_button.clicked.connect(dialog.accept)
    no_button.clicked.connect(dialog.reject)

    layout.addWidget(yes_button)
    layout.addWidget(no_button)

    layout2.addLayout(layout)

    dialog.setLayout(layout2)

    result = dialog.exec_()

    time.sleep(0.5)

    try:
        if result == QDialog.Accepted:
            options = QFileDialog.Options()
            file_name, _ = QFileDialog.getOpenFileName(None, "파일 열기", "", "이미지 파일 (*.png *.jpg)", options=options)
            if file_name: # 파일을 선택함
                with open("path.json", 'w') as f:
                    json.dump({"path": file_name}, f)
                if main_py_path: # 경로가 있음
                    subprocess.Popen(["python3", main_py_path])
                    sys.exit()
                else: # 경로가 없음
                    find_main_path()
            else: # 닫기를 누름
                print("취소")
                return False
            
    except Exception as E:
        print(f"{E}, exit")
        sys.exit()
    

app = QApplication(sys.argv)

lobby_width = 600
lobby_height = 400

bring_button_width = 100
bring_button_height = 30

bring_button_X = int(lobby_width/2 - bring_button_width/2)
bring_button_Y = int(lobby_height/2 - bring_button_height/2)

lobby = make_window(lobby_width, lobby_height,"main")
lobby.setStyleSheet("background-color : #e7e7e7;")

lobby_label = QLabel("Temu_photoshop", lobby)
lobby_label.setStyleSheet("background-color : #e7e7e7; color : black;")
lobby_label.move(bring_button_X - 5, bring_button_Y - 25)

bring_photo_button = make_button(bring_button_width, bring_button_height, "here", lobby)
bring_photo_button.move(bring_button_X, bring_button_Y)

bring_photo_button.setStyleSheet("""
    QPushButton {                   
        background-color : blue;  
        color : white;
        border-radius : 15px;  
             
                                 }
    """)

bring_photo_button.button.clicked.connect(OpenFile_ForImage)

lobby.show()


sys.exit(app.exec_())
