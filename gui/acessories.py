from PySide6.QtGui import QPalette, QFont, QColor

class BasicColors(QPalette):
    def __init__(self):
        QPalette.__init__(self)
        self.setColor(QPalette.Active, QPalette.Window,
                      QColor(255, 255, 255, 255))
        self.setColor(QPalette.Active, QPalette.WindowText,
                      QColor(0, 0, 0, 255))

class BasicFont(QFont):
    def __init__(self):
        QFont.__init__(self)
        self.setPointSize(12)

class DetailsFont(QFont):
    def __init__(self):
        QFont.__init__(self)
        self.setPointSize(10)

class TitleFont(QFont):
    def __init__(self):
        QFont.__init__(self)
        self.setCapitalization(QFont.AllUppercase)
        self.setBold(True)
        self.setPointSize(14)

class EmphasisFont(BasicFont):
    def __init__(self):
        BasicFont.__init__(self)
        self.setItalic(True)
        self.setBold(True)