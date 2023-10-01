import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QTextEdit, QPushButton
from PyQt5.QtWebEngineWidgets import QWebEngineView
import markdown

class MarkdownEditor(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        self.editor = QTextEdit()
        self.viewer = QWebEngineView()

        btn = QPushButton('Render')
        btn.clicked.connect(self.renderMarkdown)

        layout.addWidget(self.editor)
        layout.addWidget(btn)
        layout.addWidget(self.viewer)

        self.setLayout(layout)

    def renderMarkdown(self):
        md_text = self.editor.toPlainText()
        html = markdown.markdown(md_text)
        self.viewer.setHtml(html)

app = QApplication(sys.argv)
ex = MarkdownEditor()
ex.show()
sys.exit(app.exec_())
