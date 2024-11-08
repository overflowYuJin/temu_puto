# 24 10.26
# 안내창 취소 버튼 누르면 오류 뜸 [10.27 완료]
# 창 닫기 버튼 (빨간버튼)을 눌러도 창 진행이 계속 됌, 즉 중단 시켜야함. [11.8 완료]
# 선택한 사진 확인 할 때 닫기버튼을 누르면 표시된 사진도 함께 꺼져야함. [11.8 완료]

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
    def __init__(self, title, yes_callback, no_callback, yes_button, no_button, contents, handle_close=None, associated_window = None, parent=None):
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
        self.handle_close = handle_close
        self.associated_window = associated_window

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
            """no_callback이 None일 때 if문이 없으면 오류뜸"""
            if no_callback is None: 
                self.no_button.clicked.connect(self.reject)
            else:
                self.no_button.clicked.connect(lambda : [no_callback(), self.reject()])
            self.no_button.setObjectName("NoButton")

            button_layout.addWidget(self.yes_button)
            button_layout.addWidget(self.no_button)

        layout.addLayout(button_layout)
        self.setLayout(layout)

    def closeEvent(self, event):
        """닫기버튼에 관함"""
        if self.handle_close:
            if self.associated_window:
                self.associated_window.close()
            return
        else:
            event.accept()

        print("was closed")
                

class ShowImage(QMainWindow):
    def __init__(self, image_path):
        super().__init__()

        pixmap = QPixmap(image_path)
        width, height = pixmap.width(), pixmap.height()

        self.setWindowTitle("주목..!")
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
Setting = 0
#-----------------------------------


def wirteImagePath(imagePath, json_path=None):
    print(imagePath) 
    

# --- 사진이 적정크기인지  확인 함수 ---
def CheckTheImageSize(path):
    with Image.open(path) as img:
        width, height = img.size

    # --- 사진 크기 확인 ---
    # 700x700가 최대임
    if width > 700 or height > 700:
        warning_dialog = make_dialog("경고", None, None, "확인", None, f"편집이 불가능한 크기입니다 \n 선택한 사진의 크기 : {width}x{height}")
        warning_dialog.exec_()

    else: 
        # 사진이 적정 크기임
        ImageCheckDialog(path)

# --- 선택한 사진 맞는지 확인하는 함수 ---
def ImageCheckDialog(path):
    global ImageWindow

    # 선택한 이미지를 보여줌
    ImageWindow = ShowImage(path)
    ImageWindow.show()

    # 이미지 확인 창
    check_dialog = make_dialog("", lambda: [ImageWindow.close(),wirteImagePath(path)], lambda: [check_dialog.reject(),ImageWindow.close(), handle_main_flow(1)], "예", "다시 선택", "선택한 사진이 맞습니까?", True, ImageWindow)
    QTimer.singleShot(1500, check_dialog.exec_)

# --- 사진을 위해 파일을 여는 함수 ----
def LoadImage(action=1):
    options = QFileDialog.Options()
    if action == 1:
        file_name, _ = QFileDialog.getOpenFileName(None, "파일 열기", "", "이미지 파일 (*.png *.jpg)", options=options)
        if file_name:
            print("파일 선택 완료:", file_name, "\n")
            return file_name
        else:
            print("파일 선택 취소")
    elif action ==2:
        file_name, _ = QFileDialog.getOpenFileName(None, "파일 열기", "", "json 파일 (*json)", options=options)
        if file_name: # 파일을 찾음
            print(f"json 파일 선택함..{file_name}")
            return file_name
    else:
        print("?")
        sys.exit()

# --- 이미지 선택 안내 창 ---
def display_image_select_guide():
    open_dialog = make_dialog("안내", lambda : [open_dialog.accept(), handle_main_flow(1)], None, "열기" , "취소", "열기 를 눌러 편집하고 싶은 사진을 선택합니다.", True)
    open_dialog.exec_()


def handle_main_flow(action):
    try:
        # --- 사진 크기 안내창 ---
        if action == 0:
            warning_dialog = make_dialog("경고", None, None, "확인", None, "jpg, png 확장자 이미지만 가능합니다. \n 또, 이미지는 700x700 이하의 크기여야 합니다.")
            warning_dialog.exec_()

            QTimer.singleShot(500, display_image_select_guide)

        # --- 이미지 선택 창 ---
        elif action == 1:
            Image = LoadImage()
            if Image: # Image가 선택됌
                CheckTheImageSize(Image)
            
            else:
                print("close")

        # --- 에딧 창 실행 ---
        elif action == 2:
            # 절대경로를 검색했는데 만약에 겹치는게 있다면, 반드시 전에 작업한 적이 있다고 창을 띄어야함.
            # 사용자가 새로 작업하겠다고 하면 전에 있던 수를 지우고 새로운 수를 씀
            # 그러니까 순서가 == 경로를 통해 전에 작업했나 확인을 함 > 했었음(마저 하겠냐고 물어봄) > 아님(맞다면 바로 딸려있는 고유번호로 마져)
            # > 전에 있던 고유번호를 새로운 번호로 바꿈
            pass
                
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
StartButton.clicked.connect(lambda : handle_main_flow(0))

main_window.show()

sys.exit(app.exec_())