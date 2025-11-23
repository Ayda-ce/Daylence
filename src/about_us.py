import os
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPalette, QColor, QPixmap
from PyQt5.QtWidgets import QVBoxLayout, QLabel, QHBoxLayout, QDialog, QDesktopWidget

class About_us(QDialog):
    """
    A dialog window that displays information about the Activities Planner application.
    This dialog shows the application's version information, copyright details,
    and a brief description of its purpose. It supports theming and font customization.

    """
    def __init__(self, theme, font_families, settings, parent=None):
        """
        Args:
        theme (dict): Color theme dictionary containing background and text colors
        font_families (dict): Dictionary of font families for different UI elements
        settings (dict): Application settings dictionary
        """
        super().__init__(parent)
        self.theme = theme
        self.font_families = font_families
        self.settings = settings
        # Set window properties
        self.setWindowFlags(Qt.Window | Qt.CustomizeWindowHint | Qt.WindowTitleHint |
                            Qt.WindowSystemMenuHint | Qt.WindowCloseButtonHint)
        self.setWindowTitle("About")
        self.setFixedSize(800, 400)
        self.center()
        # Set background color based on the theme
        palette = self.palette()
        palette.setColor(QPalette.Background, QColor(self.theme['Background']))
        self.setPalette(palette)
        self.init_ui()
        self.apply_styles()

    def center(self):
        """
        Centers the dialog on the screen.
        """
        screen_geometry = QDesktopWidget().screenGeometry()
        x = (screen_geometry.width() - self.width()) // 2
        y = (screen_geometry.height() - self.height()) // 2
        self.move(x, y)

    def init_ui(self):
        """
        Initializes the user interface layout and widgets, including an image and text section.
        """
        layout = QHBoxLayout()

        # Image section
        image_label = QLabel(self)
        pixmap = QPixmap(os.path.join(os.path.dirname(__file__), "Files", "about.png"))
        pixmap = pixmap.scaled(370, 370, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        image_label.setPixmap(pixmap)
        image_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(image_label)

        # Text section
        text_layout = QVBoxLayout()
        text_layout.setContentsMargins(20, 0, 0, 0)
        self.title_label = QLabel("Activities Planner")
        self.version_label = QLabel("Version 1.0.15")
        # self.feedback_label = QLabel("For feedback or suggestions, please contact: daylence2025@gmail.com")
        # self.feedback_label = QLabel("For feedback or suggestions, please contact: <a href=\"daylence2025@gmail.com\">'daylence2025@gmail.com'</a>")
        self.feedback_label = QLabel(f"For feedback or suggestions, please contact: <a href=\"mailto:daylence2025@gmail.com\" style=\"color: {self.theme['Text']};\">daylence2025@gmail.com</a>")
        self.copyright_label = QLabel("Copyright @2025 by Ayda - All Rights Reserved.")
        self.description_label = QLabel(
            "The Activities Planner app is designed to help you manage your time effectively by calculating "
            "the time required for your tasks. It ensures the accuracy of your schedule by taking into account "
            "the duration of your activities and the time needed for rest."
        )
        self.description_label.setWordWrap(True)
        self.feedback_label.setWordWrap(True)
        self.feedback_label.setOpenExternalLinks(True)
        
        # Add widgets to layout with stretch factors
        text_layout.addWidget(self.title_label, stretch=1)
        text_layout.addWidget(self.version_label, stretch=1)
        text_layout.addWidget(self.description_label, stretch=3)
        text_layout.addWidget(self.feedback_label, stretch=1)
        text_layout.addWidget(self.copyright_label, stretch=2)
        layout.addLayout(text_layout)
        self.setLayout(layout)

    def apply_styles(self):
        """
        Applies the current theme and font styles to all widgets in the dialog.
        """
        self.title_label.setStyleSheet(f"""
        color: {self.theme['Text']};
        font-size: 24px;
        font-family: {self.font_families['Main_Font'].family()};
        font-weight: bold;
        """)
        self.version_label.setStyleSheet(f"""
        color: {self.theme['Text']};
        font-size: 22px;
        font-family: {self.font_families['Text'].family()};
        """)
        self.copyright_label.setStyleSheet(f"""
        color: {self.theme['Text']};
        font-size: 14px;
        font-family: {self.font_families['Text'].family()};
        """)
        self.description_label.setStyleSheet(f"""
        color: {self.theme['Text']};
        font-size: 14px;
        font-family: {self.font_families['Text'].family()};
        """)    
        self.feedback_label.setStyleSheet(f"""
        color: {self.theme['Text']};
        font-size: 14px;
        font-family: {self.font_families['Text'].family()};
        """)