# 24 10.26
# 안내창 취소 버튼 누르면 오류 뜸 [10.27 완료]
# 창 닫기 버튼 (빨간버튼)을 눌러도 창 진행이 계속 됌, 즉 중단 시켜야함. [11.8 완료]
# 선택한 사진 확인 할 때 닫기버튼을 누르면 표시된 사진도 함께 꺼져야함. [11.8 완료]
# 부족한 부분들은 거의 다 조정함, Write~Path 함수를 쓰면 될거 같음 [11.14 작성]


"""아 개발 안할거임."""

import subprocess
import sys

# --  여기 아래 모듈들은 별도의 설치가 필요함 -- 

def install_module(package_name):
    # -- 모듈 설치 함수 --
    subprocess.check_call([sys.executable, "-m", "pip", "install", package_name])

#____________________PyQt5_______________________


try:
    from PyQt5.QtWidgets import QWidget, QPushButton, QApplication, QFileDialog, QLabel, QHBoxLayout, QDialog, QVBoxLayout, QMainWindow
    from PyQt5.QtCore import Qt, QTimer
    from PyQt5.QtGui import QPixmap
    print("PyQt5-")
except ImportError:
    # 모듈이 안불러 와짐
    print("PyQt5가 없습니다. \n 설치를 진행합니다.")
    install_module("PyQt5")

#___________________Pillow_______________________

try:
    from PIL import Image
    print("PIL-")  
except ImportError:
    # 모듈이 안불러 와짐
    print("Pillow가 없습니다. \n 설치를 진행합니다.")
    install_module("Pillow")
    
#---------------------------------------------------------------------

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
    def __init__(self, title, accept_function, reject_function, button_label_accept, button_label_rejcet, dialog_message, terminate_if_closed=False, close_together_window = None, just_one_button= False, parent=None):
        super().__init__(parent)


        self.setStyleSheet("""
        QDialog {background-color : #e7e7e7;}
        QLabel {background-color : #e7e7e7; color : black;}
        QPushButton {border-radius : 10px; padding : 5px 10px;}
        #acceptButton {background-color : #3b8e3b; color : white;}
        #acceptButton:hover {background-color : #369036;}
        #rejectButton {background-color : #a0a0a0; color : black;}
        #rejectButton:hover {background-color : #8a8a8a;}
        #checkButton {background-color : #ff4500; color : white; padding : 8px 16px; font-weight : bold; border-radius : 15px;}
        #checkButton:hover {background-color: #ff6347;}
        """)

        def connectButtonEvent(button, button_event, normal_event):
        # --- 버튼에 함수 연결해 주는 함수 ---
        # 각 조건에 대하여 설명을 하자면
        #   - 첫번째, 할당된 이벤트가 없는 경우 
        #   - 두번째, 아닌 경우로 나뉨
            if button_event is None:
                button.clicked.connect(normal_event)
            else:
                button.clicked.connect(lambda : [button_event(), normal_event()])
#---------------------------------------------------------------------

        self.title = title
        self.on_accept = accept_function
        self.on_rejcet = reject_function
        self.accept_label = button_label_accept
        self.reject_label = button_label_rejcet
        self.message = dialog_message
        self.action_closed = terminate_if_closed # 얘는 항상 꺼져 있음 (False)
        self.together_closed = close_together_window # 애는 항상 값이 없음 (None)
        self.check_button = just_one_button # 얘는 항상 꺼져 있음 (False)

        # -- 기본 창 --
        self.setWindowTitle(title)
        self.setFixedSize(300,150)

        # -- 레이아웃 선언 --
        layout = QVBoxLayout()
        button_layout = QHBoxLayout()

        self.label = QLabel(self.message)
        layout.addWidget(self.label)

        if self.check_button:
            # 버튼 하나만 있는 다이로그를 생성함.
            self.checkButton = QPushButton(self.accept_label)
            self.checkButton.clicked.connect(self.accept)
            self.checkButton.setObjectName("checkButton")
            self.checkButton.setFixedSize(100,30)
            button_layout.addWidget(self.checkButton)
        else:
            # 버튼이 두개인 다이로그를 생성함

            self.acceptButton = QPushButton(self.accept_label)
            self.acceptButton.setObjectName("acceptButton")

            self.rejectButton = QPushButton(self.reject_label)
            self.rejectButton.setObjectName("rejectButton")

            # -- 함수 이벤트 연결 --
            connectButtonEvent(self.acceptButton,accept_function,self.accept)
            connectButtonEvent(self.rejectButton,reject_function,self.reject)

            # -- 버튼들 레이아웃 설정 --    
            button_layout.addWidget(self.acceptButton)
            button_layout.addWidget(self.rejectButton)

        layout.addLayout(button_layout)
        self.setLayout(layout)

    def closeEvent(self, event):
        if self.action_closed:
            # 이 다이로그는 닫기 버튼을 무시할 수 없음
            if self.together_closed:
                # 같이 닫혀야할 창들이 있음
                self.together_closed.close()
            return
            # 코드 종료
        else:
            # 이 다이로그는 닫기 버튼을 무시해도 됌
            event.accept()


        print("was closed")

class ShowImage(QMainWindow):
    def __init__(self, image_path):
        super().__init__()

        pixmap = QPixmap(image_path)
        width, height = pixmap.width(), pixmap.height()

        self.setWindowTitle("")
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
image_window = None
setting = 0
#-----------------------------------


def CheckTheImageSize(path):
# --- 사진이 적정크기인지  확인 함수 ---
    with Image.open(path) as img:
        width, height = img.size

    if width > 700 or height > 700:
        # 사진이 적정 크기가 아님
        invalid_size_dialog = make_dialog("안내", None, lambda : [invalid_size_dialog.reject(), CoreLogic("selectImage")], "확인", "다시 선택", f"편집이 불가능한 크기입니다 \n 선택한 사진의 크기 : {width}x{height}")
        invalid_size_dialog.exec_()

    else: 
        # 사진이 적정 크기임
        ImageCheckDialog(path)

def ImageCheckDialog(path):
# --- 선택한 사진 맞는지 확인하는 함수 ---
    global image_window

    image_window = ShowImage(path)
    image_window.show()

    # 이미지 확인 창
    check_the_image_dialog = make_dialog("", lambda : [image_window.close(),CoreLogic(2, path)], lambda: [check_the_image_dialog.reject(), image_window.close(),CoreLogic("selectImage")], "예", "다시 선택", "선택한 사진이 맞습니까?", True, image_window)
    QTimer.singleShot(1500, check_the_image_dialog.exec_)

def LoadImage(action=1):
# --- 사진을 위해 파일을 여는 함수 ----
    options = QFileDialog.Options()
    if action == 1:
        # 이미지 파일을 선택
        file_name, _ = QFileDialog.getOpenFileName(None, "파일 열기", "", "이미지 파일 (*.png *.jpg)", options=options)
        if file_name:
            print("파일 선택 완료:", file_name, "\n")
            return file_name
        else:
            print("파일 선택 취소")
    else:
        print("?")
        sys.exit()

# --- 이미지 선택 안내 창 ---
def ImageSelectGuide():
    file_open_guide_dialog = make_dialog("안내", lambda : [file_open_guide_dialog.accept(), CoreLogic("selectImage")], None, "열기", "취소", "<열기> 를 눌러 편집하고 싶은 사진을 선택합니다.", True)
    file_open_guide_dialog.exec_()


def EditWindow(path):
    # 여기부터 -----------------------------------------------------------------------------
    pass

def CoreLogic(action, path=None):
    try:
        if action == "showGuide":
        # --- 사진 크기 안내창 ---
            image_guide_dialog = make_dialog("경고", None, None, "확인", None, "jpg, png 확장자 이미지만 가능합니다. \n 또, 이미지는 700x700 이하의 크기여야 합니다.", False,False,True)
            image_guide_dialog.exec_()

            QTimer.singleShot(500, ImageSelectGuide)

        elif action == "selectImage":
        # --- 이미지 선택 창 ---
            image = LoadImage()
            if image: # Image가 선택됌
                CheckTheImageSize(image)
            
            else:
                print("close")

        # --- 에딧 창 실행 ---
        elif action == 2:
            EditWindow(path)
                
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
StartButton.clicked.connect(lambda : CoreLogic("showGuide"))

main_window.show()

sys.exit(app.exec_())