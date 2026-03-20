from transformers import ViTImageProcessor, ViTForImageClassification
from PIL import Image
import torch
import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout,
                             QPushButton, QLabel, QFileDialog)
from PyQt5.QtGui import QPixmap, QPainter, QFont, QColor
from PyQt5.QtCore import Qt

class VITClassifierGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.image = None
        self.image_path = None
        self.result_text = ""

        # 모델 초기화
        self.processor = ViTImageProcessor.from_pretrained("google/vit-base-patch16-224")
        self.model = ViTForImageClassification.from_pretrained("google/vit-base-patch16-224")

        self.initUI()

    def initUI(self):
        self.setWindowTitle('VIT Image Classifier')
        self.setGeometry(100, 100, 800, 700)

        # 중앙 위젯 설정
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout()

        # 이미지 표시 레이블
        self.image_label = QLabel("이미지를 불러오세요")
        self.image_label.setAlignment(Qt.AlignCenter)
        self.image_label.setMinimumSize(600, 500)
        layout.addWidget(self.image_label)

        # 이미지 불러오기 버튼
        self.load_button = QPushButton('이미지 불러오기')
        self.load_button.clicked.connect(self.load_image)
        layout.addWidget(self.load_button)

        # 모델 추론 버튼
        self.predict_button = QPushButton('모델 추론')
        self.predict_button.setEnabled(False)
        self.predict_button.clicked.connect(self.predict_image)
        layout.addWidget(self.predict_button)

        central_widget.setLayout(layout)

    def load_image(self):
        file_name, _ = QFileDialog.getOpenFileName(
            self,
            "이미지 선택",
            "",
            "Image Files (*.png *.jpg *.jpeg *.bmp)"
        )

        if file_name:
            self.image_path = file_name
            self.image = Image.open(file_name)
            self.result_text = ""
            self.display_image()
            self.predict_button.setEnabled(True)

    def display_image(self):
        if self.image:
            pixmap = QPixmap(self.image_path)

            # 결과 텍스트가 있으면 이미지 위에 그리기
            if self.result_text:
                painter = QPainter(pixmap)
                painter.setFont(QFont('Arial', 16, QFont.Bold))
                painter.fillRect(10, 10, 400, 80, QColor(0, 0, 0, 180))
                painter.setPen(QColor(255, 255, 255))
                painter.drawText(20, 35, self.result_text.split('\n')[0])
                painter.drawText(20, 60, self.result_text.split('\n')[1])
                painter.end()

            scaled_pixmap = pixmap.scaled(
                self.image_label.width() - 10,
                self.image_label.height() - 10,
                Qt.KeepAspectRatio,
                Qt.SmoothTransformation
            )
            self.image_label.setPixmap(scaled_pixmap)

    def predict_image(self):
        if self.image:
            image_rgb = self.image.convert('RGB')
            inputs = self.processor(images=image_rgb, return_tensors="pt")

            with torch.no_grad():
                outputs = self.model(**inputs)
                logits = outputs.logits
                probs = logits.softmax(dim=-1)

            pred_idx = int(torch.argmax(probs[0]))
            pred_label = self.model.config.id2label[pred_idx]
            pred_prob = float(probs[0][pred_idx] * 100)

            self.result_text = f"클래스: {pred_label}\n확률: {pred_prob:.2f}%"
            self.display_image()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    gui = VITClassifierGUI()
    gui.show()
    sys.exit(app.exec_())
