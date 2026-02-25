from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
    QLabel, QLineEdit, QPushButton, QFrame
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont
from datetime import datetime

class MainWindow(QMainWindow):
    def __init__(self, manager):
        super().__init__()
        self.manager = manager
        
        # Window setup
        self.setWindowTitle("定時關機程式")
        self.setMinimumSize(400, 300)
        
        # Central Widget & Main Layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        main_layout.setSpacing(20)
        main_layout.setContentsMargins(30, 30, 30, 30)

        # --- Section 1: Status Display ---
        self.status_label = QLabel("預計關機時間：")
        self.status_label.setAlignment(Qt.AlignCenter)
        font = QFont()
        font.setPointSize(18)
        font.setBold(True)
        self.status_label.setFont(font)
        main_layout.addWidget(self.status_label)
        
        self.info_label = QLabel("")
        self.info_label.setAlignment(Qt.AlignCenter)
        init_red = "#EF9A9A" if self.is_dark_mode() else "#D32F2F"
        self.info_label.setStyleSheet(f"color: {init_red};")
        main_layout.addWidget(self.info_label)

        # --- Section 2: Input Area ---
        input_frame = QFrame()
        input_layout = QHBoxLayout(input_frame)
        input_layout.setContentsMargins(0, 0, 0, 0)
        
        self.time_input = QLineEdit()
        self.time_input.setPlaceholderText("輸入小時 (例如 1.5)")
        self.time_input.setAlignment(Qt.AlignCenter)
        
        unit_label = QLabel("小時")
        
        set_button = QPushButton("建立定時關機")
        set_button.setCursor(Qt.PointingHandCursor)
        set_button.clicked.connect(self.on_set_clicked)

        input_layout.addWidget(self.time_input)
        input_layout.addWidget(unit_label)
        input_layout.addWidget(set_button)
        
        main_layout.addWidget(input_frame)

        # --- Section 3: Quick Settings ---
        quick_frame = QFrame()
        quick_layout = QHBoxLayout(quick_frame)
        quick_layout.setContentsMargins(0, 0, 0, 0)
        
        quick_label = QLabel("快速設定:")
        quick_layout.addWidget(quick_label)
        
        for hrs in [2, 4, 6, 8]:
            btn = QPushButton(f"{hrs}小時")
            btn.setCursor(Qt.PointingHandCursor)
            # Use closure to capture the specific hour
            btn.clicked.connect(lambda checked=False, h=hrs: self.manager.schedule_shutdown(str(h)))
            quick_layout.addWidget(btn)
            
        main_layout.addWidget(quick_frame)

        # --- Section 4: Cancel Button ---
        cancel_button = QPushButton("取消關機")
        cancel_button.setCursor(Qt.PointingHandCursor)
        cancel_bg = "rgba(239, 154, 154, 0.2)" if self.is_dark_mode() else "#ffcccc"
        cancel_fg = "#EF9A9A" if self.is_dark_mode() else "#cc0000"
        cancel_button.setStyleSheet(f"background-color: {cancel_bg}; color: {cancel_fg}; font-weight: bold;")
        cancel_button.clicked.connect(self.manager.cancel_shutdown)
        main_layout.addWidget(cancel_button)

        # Connect Signals from Manager to UI slots
        self.connect_signals()

    def connect_signals(self):
        self.manager.shutdown_scheduled.connect(self.update_status_scheduled)
        self.manager.shutdown_cancelled.connect(self.update_status_cancelled)
        self.manager.error_occurred.connect(self.show_error)

    def on_set_clicked(self):
        text = self.time_input.text()
        self.manager.schedule_shutdown(text)

    def is_dark_mode(self) -> bool:
        bg = self.palette().color(self.palette().ColorRole.Window)
        return bg.lightness() < 128

    # --- Slots ---
    def update_status_scheduled(self, target_time: datetime):
        time_str = target_time.strftime("%H:%M:%S")
        self.status_label.setText(f"預計關機時間：{time_str}")
        self.status_label.setStyleSheet("")  # 跟隨系統，不強制設色
        self.info_label.setText(f"將於 {time_str} 執行關機")
        green = "#66BB6A" if self.is_dark_mode() else "#2E7D32"  # 淺綠 vs 深綠
        self.info_label.setStyleSheet(f"color: {green};")

    def update_status_cancelled(self):
        self.status_label.setText("預計關機時間：")
        self.info_label.setText("已取消關機")
        blue = "#4FC3F7" if self.is_dark_mode() else "#0277BD"  # 亮水藍 vs 深藍
        self.info_label.setStyleSheet(f"color: {blue};")

    def show_error(self, message: str):
        self.info_label.setText(message)
        red = "#EF9A9A" if self.is_dark_mode() else "#D32F2F"  # 淺紅 vs 深紅
        self.info_label.setStyleSheet(f"color: {red};")
