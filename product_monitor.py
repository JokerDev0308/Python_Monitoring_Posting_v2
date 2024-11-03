import requests
from PyQt5.QtWidgets import (
    QWidget, QLabel, QVBoxLayout, QPushButton, QTimeEdit,
    QHBoxLayout, QTextEdit, QProgressBar,QCheckBox
)
from PyQt5.QtGui import QPixmap
from monitor_thread import MonitorThread
from utils import load_product_list, is_within_notification_time
from PyQt5.QtCore import Qt , QTime
from datetime import datetime

class ProductMonitorApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("自動検出と投稿")  # Product Monitor
        self.setMinimumSize(800, 600)

        # UI Elements
        self.product_name_label = QLabel()
        self.price_label = QLabel()  # Price
        self.stock_status_label = QLabel()  # Stock Status
        self.image_display = QLabel()
        self.image_display.setMinimumSize(300, 350)
        self.image_display.setMaximumWidth(300)
        self.image_display.setStyleSheet("QLabel { background-color: white; padding: 15px; }")
        
        self.results_display = QTextEdit()
        self.results_display.setReadOnly(True)

        self.start_time = QTimeEdit()
        self.end_time = QTimeEdit()

        # Set default times
        self.start_time.setTime(QTime(0, 0))  # Default start time
        self.end_time.setTime(QTime(23, 59))  # Default end time

        # Set ranges
        self.start_time.setMinimumTime(QTime(0, 0))  # Minimum start time
        self.start_time.setMaximumTime(QTime(23, 58))  # Maximum start time (less than end time)
        self.end_time.setMinimumTime(QTime(0, 1))  # Minimum end time (greater than start time)
        self.end_time.setMaximumTime(QTime(23, 59))  # Maximum end time

        self.start_time_label = QLabel("勤務時間: ")
        self.end_time_label = QLabel(" ~ ")

        self.start_button = QPushButton("開始")  # Start
        self.stop_button = QPushButton("停止")  # Stop
        self.repeat_checkbox = QCheckBox("常に検索")
        self.repeat_checkbox.setChecked(True)
        self.posting_X_checkbox = QCheckBox("「X」に投稿")
        self.posting_X_checkbox.setChecked(True)

        # Button states
        self.stop_button.setEnabled(False)

        # Progress bar
        self.progress = QProgressBar()
        self.progress.setRange(0, 100)

        # Layouts
        text_layout = QVBoxLayout()
        text_layout.addWidget(self.price_label)
        text_layout.addWidget(self.stock_status_label)

        time_layout = QHBoxLayout()
        time_layout.addWidget(self.start_time_label)
        time_layout.addWidget(self.start_time)
        time_layout.addWidget(self.end_time_label)
        time_layout.addWidget(self.end_time)


        product_layout = QVBoxLayout()
        product_layout.addWidget(self.image_display)
        product_layout.addLayout(text_layout)

        body_layout = QHBoxLayout()
        body_layout.addLayout(product_layout)
        body_layout.addWidget(self.results_display)

        self.sapce = QLabel()

        button_layout = QHBoxLayout()
        button_layout.addWidget(self.repeat_checkbox)
        button_layout.addLayout(time_layout)
        button_layout.addWidget(self.sapce)
        button_layout.addWidget(self.posting_X_checkbox)
        button_layout.addWidget(self.start_button)
        button_layout.addWidget(self.stop_button)

        main_layout = QVBoxLayout()
        main_layout.addWidget(self.product_name_label)
        main_layout.addLayout(body_layout)
        main_layout.addWidget(self.progress)
        main_layout.addLayout(button_layout)

        self.setLayout(main_layout)

        # Connect buttons to functions
        self.start_button.clicked.connect(self.start_monitoring)
        self.stop_button.clicked.connect(self.stop_monitoring)

        # Connect time change signals
        self.start_time.timeChanged.connect(self.validate_times)
        self.end_time.timeChanged.connect(self.validate_times)

        self.products = load_product_list()
        self.monitor_thread = None

        self.validate_times()
    
    def validate_times(self):
        start_time_value = self.start_time.time()
        end_time_value = self.end_time.time()

        # Ensure the end time is greater than the start time
        if start_time_value >= end_time_value:
            self.end_time.setEnabled(False)  # Disable end time if invalid
            self.results_display.append("終了時間は開始時間より後でなければなりません。")  # End time must be after start time
        else:
            self.end_time.setEnabled(True)  # Enable end time if valid

    def start_monitoring(self):
        # if is_within_notification_time():
        if self.start_time.time() <= datetime.now().time() <= self.end_time.time():
            # self.results_display.clear()
            self.progress.setValue(0)
            self.monitor_thread = MonitorThread(self.products, self.posting_X_checkbox.isChecked())
            
            # Connect signals to update UI
            self.monitor_thread.update_product_name.connect(self.product_name_label.setText)
            self.monitor_thread.update_sale.connect(lambda sale: self.price_label.setText(f"価格: {sale}"))  # Price
            self.monitor_thread.update_status.connect(self.stock_status_label.setText)
            self.monitor_thread.update_progress.connect(self.progress.setValue)
            self.monitor_thread.update_result.connect(self.update_display)
            self.monitor_thread.update_image.connect(self.load_image)
            self.monitor_thread.finished.connect(self.on_finished)
            
            self.monitor_thread.start()

            # Update button states
            self.start_button.setEnabled(False)
            self.stop_button.setEnabled(True)
        else:
            self.update_display("現在、作業時間外です。設定で時間を編集してください。")  # Now is out of working time; please edit the time in the settings.

    def stop_monitoring(self):
        if self.monitor_thread:
            self.monitor_thread.monitoring = False  # Stop monitoring
            self.monitor_thread.quit()  # Properly stop the thread
            self.monitor_thread.wait()  # Wait for the thread to finish

        # Update button states
        self.start_button.setEnabled(True)
        self.stop_button.setEnabled(False)

    def update_display(self, result):      
        self.results_display.append(result)
        self.results_display.append("")

    def load_image(self, image_url):
        if image_url:
            try:
                response = requests.get(image_url)
                response.raise_for_status()  # Raise an error for bad responses

                pixmap = QPixmap()
                if pixmap.loadFromData(response.content):
                    display_size = self.image_display.size()
                    scaled_pixmap = pixmap.scaled(display_size, Qt.KeepAspectRatio, Qt.SmoothTransformation)
                    self.image_display.setPixmap(scaled_pixmap)
                    self.image_display.setScaledContents(True)
                else:
                    self.image_display.setText("画像データの読み込みに失敗しました")  # Failed to load image data
            except requests.exceptions.RequestException as e:
                print(f"画像の取得エラー: {e}")  # Error fetching image
                self.image_display.setText("画像の読み込みにエラーが発生しました")  # Error loading image
            except Exception as e:
                print(f"画像の読み込み中に予期しないエラーが発生しました: {e}")  # Unexpected error loading image
                self.image_display.setText("画像が利用できません")  # Image not available
        else:
            self.image_display.setText("画像URLが提供されていません")  # No image URL provided

    def on_finished(self):
        if self.repeat_checkbox.isChecked() and self.monitor_thread.monitoring:
            self.start_monitoring()
        else:
            self.start_button.setEnabled(True)
            self.stop_button.setEnabled(False)  # Disable stop button
