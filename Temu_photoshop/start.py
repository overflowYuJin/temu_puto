# 24 10.26
# 안내창 취소 버튼 누르면 오류 뜸, Wit~Startedit 함수 안만듬

import subprocess
import sys
import json

def install_module(package_name):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package_name])
try:
    from PyQt5.QtWidgets import QWidget, QPushButton, QApplication, QFileDialog, QLabel, QHBoxLayout, QDialog, QVBoxLayout, QMainWindow
    from PyQt5.QtCore import Qt, QTimer
    from PyQt5.QtGui import QPixmap
    print("PyQt5-")
except ImportError:
    print("PyQt5가 없습니다. \n 설치를 진행합니다.")
    install_module("PyQt5")

try:
    from PIL import Image
    print("PIL-")  
except ImportError:
    print("Pillow가 없습니다. \n 설치를 진행합니다.")
    install_module("Pillow")
    

class make_window(QWidget):
    def __init__(self, width, height, title):
        super().__init__()
        self.width = width
        self.height = height
        self.title = title

        self.setFixedSize(self.width , self.height)
        self.setWindowTitle(self.title)

class make_button(QPushButton):
    def __init__(self, name, width, height, parent=None):
        super().__init__(name, parent)
        self.setFixedSize(width, height)

class make_dialog(QDialog):
    def __init__(self, title, yes_callback, no_callback, yes_button, no_button, contents, parent=None):
        super().__init__(parent)

        self.setStyleSheet("""
        QDialog {background-color : #e7e7e7;}
        QLabel {background-color : #e7e7e7; color : black;}
        QPushButton {border-radius : 10px; padding : 5px 10px;}
        #YesButton {background-color : #3b8e3b; color : white;}
        #YesButton:hover {background-color : #369036;}
        #NoButton {background-color : #a0a0a0; color : black;}
        #NoButton:hover {background-color : #8a8a8a;}
        #CheckButton {background-color : #ff4500; color : white; padding : 8px 16px; font-weight : bold; border-radius : 15px;}
        #CheckButton:hover {background-color: #ff6347;}
        """)

        self.title = title
        self.yes_callback = yes_callback
        self.no_callback = no_callback
        self.yes_button = yes_button
        self.no_button = no_button
        self.contents = contents

        self.setWindowTitle(title)
        self.setFixedSize(300,150)

        layout = QVBoxLayout()
        button_layout = QHBoxLayout()

        self.label = QLabel(contents)
        layout.addWidget(self.label)

        if yes_callback is None:
            self.check_button = QPushButton(yes_button)
            self.check_button.clicked.connect(self.accept)
            self.check_button.setObjectName("CheckButton")
            self.check_button.setFixedSize(100,30)
            button_layout.addWidget(self.check_button)

        else:
            self.yes_button = QPushButton(yes_button)
            self.yes_button.clicked.connect(lambda: [yes_callback(), self.accept()])
            self.yes_button.setObjectName("YesButton")

            self.no_button = QPushButton(no_button)
            self.no_button.clicked.connect(lambda : [no_callback(), self.reject()])
            self.no_button.setObjectName("NoButton")

            button_layout.addWidget(self.yes_button)
            button_layout.addWidget(self.no_button)

        layout.addLayout(button_layout)
        self.setLayout(layout)

class ShowImage(QMainWindow):
    def __init__(self, image_path):
        super().__init__()

        pixmap = QPixmap(image_path)
        width, height = pixmap.width(), pixmap.height()

        self.setWindowTitle("사진을 주목하시오.")
        self.setFixedSize(width+100, height+100)
        
        self.label = QLabel()
        self.label.setPixmap(pixmap)
        self.label.setAlignment(Qt.AlignCenter)

        layout = QVBoxLayout()
        layout.addWidget(self.label)
        layout.setAlignment(Qt.AlignCenter)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

#-----------------------------------
ImageWindow = None
#-----------------------------------

def WirteImagePath_StartEditWindow(imagePath, json_path="path.json"):
    try:
        with open(json_path, "r") as file:
            data = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        data = {}

    data["path"] = imagePath

    with open(json_path, "w") as file:
        json.dump(data, file, indent=4)
    print("done")
    

def CheckTheImageSize(path):
    with Image.open(path) as img:
        width, height = img.size
    if width > 700 or height > 700:
        warning_dialog = make_dialog("경고", None, None, "확인", None, f"편집이 불가능한 크기입니다 \n 선택한 사진의 크기 : {width}x{height}")
        warning_dialog.exec_()
    else:
        ImageCheckDialog(path)

def ImageCheckDialog(path):
    global ImageWindow
    ImageWindow = ShowImage(path)
    ImageWindow.show()

    image_window_x = ImageWindow.geometry().x()
    image_window_y = ImageWindow.geometry().y()
    image_window_height = ImageWindow.geometry().height()

    check_dialog = make_dialog("확인 절차", lambda: [ImageWindow.close(),WirteImagePath_StartEditWindow(path)], lambda: [ImageWindow.close(), selectImageFile(1)], "예", "다시 선택", "선택한 사진이 맞습니까?")
    QTimer.singleShot(500, lambda: check_dialog.move(image_window_x, image_window_y + image_window_height))
    check_dialog.exec_()

def LoadImage():
    options = QFileDialog.Options()
    file_name, _ = QFileDialog.getOpenFileName(None, "파일 열기", "", "이미지 파일 (*.png *.jpg)", options=options)
    if file_name:
        print("파일 선택 완료:", file_name)
        return file_name
    else:
        print("파일 선택 취소")

def show_main_dialog():
    open_dialog = make_dialog("안내", lambda : [open_dialog.accept(), selectImageFile(1)], None, "열기" , "취소", "열기 를 눌러 편집하고 싶은 사진을 선택합니다.")
    open_dialog.exec_()

def selectImageFile(action):
    """0의 경우 메인 버튼을 눌렀을 때, 1의 경우 열기를 눌렀을 때"""
    try:
        if action == 0:
            warning_dialog = make_dialog("경고", None, None, "확인", None, "jpg, png 확장자 이미지만 가능합니다. \n 또, 이미지는 700x700 이하의 크기여야 합니다.")
            warning_dialog.exec_()

            QTimer.singleShot(500, show_main_dialog)

        elif action == 1:
            Image = LoadImage()
            if Image: # Image가 선택됌
                CheckTheImageSize(Image)
            
            else:
                print("close")
                
        else:
            print(f"{Exception}, 종료합니다")
            sys.exit()    

    except Exception as e:
        print(f"{e}, 종료합니다.")
        sys.exit()

app = QApplication(sys.argv)
#--------------------------------------
MainWindowWidth = 600
MainWindowHeight = 400
MainWindowTitle = "main"
#--------------------------------------
MainButtonWidht = 100
MainButtonHeight = 30
MainButtonName = "here"

MainButton_X = int(MainWindowWidth/2 - MainButtonWidht/2)
MainButton_Y = int(MainWindowHeight/2 - MainButtonHeight/2)
#--------------------------------------

main_window = make_window(MainWindowWidth,MainWindowHeight,MainWindowTitle)
main_window.setStyleSheet("background-color : #e7e7e7")

MainWindowLabel = QLabel("Temu_Photoshop", main_window)
MainWindowLabel.setStyleSheet("background-color : #e7e7e7; color : black;")
MainWindowLabel.move(MainButton_X - 5, MainButton_Y - 25)

StartButton = make_button(MainButtonName, MainButtonWidht, MainButtonHeight, main_window)
StartButton.move(MainButton_X,MainButton_Y)
StartButton.setStyleSheet("background-color : blue; color: white; border-radius : 15px;")
StartButton.clicked.connect(lambda : selectImageFile(0))

main_window.show()

sys.exit(app.exec_())