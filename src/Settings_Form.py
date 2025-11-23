import os
from PyQt5.QtCore import QEvent
from styles import color_palette
from PyQt5 import QtWidgets, QtCore
from utils import change_image_color
from PyQt5.QtGui import QPalette, QColor
from PyQt5.QtWidgets import QVBoxLayout, QLabel, QHBoxLayout, QDialog, QComboBox, QFormLayout, QPushButton

class SettingsForm(QDialog):
    """
    A dialog window for application settings configuration.
    
    This form allows users to modify theme, font, and number display settings.
    Changes can be saved or canceled.
    
    Attributes:
        theme (dict): Current color theme dictionary
        font_family (str): Current font family
        settings (dict): Application settings dictionary
        dir_path (str): Directory path of the current file
        hover_icon_path (str): Path to hover state icon
        default_icon_path (str): Path to default state icon
        old_hover (str): Previous hover color
        old_default (str): Previous default color
        started_hover (str): Initial hover color
        started_default (str): Initial default color
    """
    
    def __init__(self, theme, font_family, settings, parent=None):
        """
        Initialize the settings form.
        
        Args:
            theme (dict): Current color theme
            font_family (str): Current font family
            settings (dict): Application settings
            parent (QWidget, optional): Parent widget. Defaults to None.
        """
        super().__init__(parent)
        self.theme = theme
        self.font_family = font_family
        self.settings = settings
        self.dir_path = os.path.dirname(os.path.realpath(__file__))
        
        # Set icon paths
        self.hover_icon_path = self.dir_path + '\\Files\\arrow_down_hover.png'
        self.default_icon_path = self.dir_path + '\\Files\\arrow_down_default.png'
        self.default_icon_path = self.default_icon_path.replace("\\", "/")
        self.hover_icon_path = self.hover_icon_path.replace("\\", "/")
        
        # Store color states for icon management
        self.old_hover = "" + self.theme['HeaderText']
        self.old_default = "" + self.theme['Header']
        self.started_hover = "" + self.theme['HeaderText']
        self.started_default = "" + self.theme['Header']
        
        # Window setup
        self.setWindowTitle("Settings")
        self.resize(400, 300)
        self.setModal(True)
        self.setAutoFillBackground(True)
        
        # Apply theme to window
        palette = self.palette()
        palette.setColor(QPalette.Window, QColor(self.theme['Background']))
        self.setPalette(palette)
        
        # Window flags to remove help and maximize buttons
        self.setWindowFlags(self.windowFlags() & ~QtCore.Qt.WindowContextHelpButtonHint)
        self.setWindowFlags(self.windowFlags() & ~QtCore.Qt.WindowMaximizeButtonHint)
        self.setFixedSize(self.size())
        
        self.init_ui()

    def apply_theme(self):
        """
        Apply the current theme to all UI elements.
        
        Updates colors for labels, combo boxes, and buttons according to the current theme.
        """
        palette = self.palette()
        palette.setColor(QPalette.Window, QColor(self.theme['Background']))
        self.setPalette(palette)
        
        # Theme label styling
        self.theme_label.setStyleSheet(f"color: {self.theme['Text']}; font-size: 14px;")
        
        # Theme combo box styling
        self.theme_combo.setStyleSheet(f"""
            QComboBox {{
                background-color: {self.theme['Button']};
                color: {self.theme['Text']};
                border: 2px solid {self.theme['Header']};
                padding: 5px;
                font-size: 14px;
                border-radius: 6px;
                font-weight: bold;
            }}
            QComboBox:hover {{
                background-color: {self.theme['Hover']};
                border: 2px solid {self.theme['Hover']};
                color: white;
            }}
            QComboBox::drop-down{{
                border: none;
            }}
            QComboBox::down-arrow{{
                image: url({self.default_icon_path});
                padding-right: 10px;
                width: 10px;
                height: 10px;
            }}
        """)

        # Font label styling
        self.font_label.setStyleSheet(f"color: {self.theme['Text']}; font-size: 14px;")
        
        # Font combo box styling
        self.font_combo.setStyleSheet(f"""
            QComboBox {{
                background-color: {self.theme['Button']};
                color: {self.theme['Text']};
                border: 2px solid {self.theme['Header']};
                padding: 5px;
                font-size: 14px;
                border-radius: 6px;
                font-weight: bold;
            }}
            QComboBox:hover {{
                background-color: {self.theme['Hover']};
                border: 2px solid {self.theme['Hover']};
                color: white;
            }}
            QComboBox::drop-down{{
                border: none;
            }}
            QComboBox::down-arrow{{
                image: url({self.default_icon_path});
                padding-right: 10px;
                width: 10px;
                height: 10px;
            }}
        """)

        # Number display label styling
        self.number_display_label.setStyleSheet(f"color: {self.theme['Text']}; font-size: 14px;")
        
        # Number display combo box styling
        self.number_display_combo.setStyleSheet(f"""
            QComboBox {{
                background-color: {self.theme['Button']};
                color: {self.theme['Text']};
                border: 2px solid {self.theme['Header']};
                padding: 5px;
                font-size: 14px;
                border-radius: 6px;
                font-weight: bold;
            }}
            QComboBox:hover {{
                background-color: {self.theme['Hover']};
                border: 2px solid {self.theme['Hover']};
                color: white;
            }}
            QComboBox::drop-down{{
                border: none;
            }}
            QComboBox::down-arrow{{
                image: url({self.default_icon_path});
                padding-right: 10px;
                width: 10px;
                height: 10px;
            }}
        """)

        # OK button styling
        self.ok_button.setStyleSheet(f"""
            QPushButton {{
                background-color: {self.theme['Header']};
                color: {self.theme['Text']};
                border: 2px solid {self.theme['Header']};
                padding: 5px;
                font-size: 14px;
                border-radius: 6px;
                font-weight: bold;
            }}
            QPushButton:hover {{
                background-color: {self.theme['Hover']};
                border: 2px solid {self.theme['Hover']};
                color: white;
            }}
        """)

        # Cancel button styling
        self.cancel_button.setStyleSheet(f"""
            QPushButton {{
                background-color: {self.theme['Button']};
                color: {self.theme['Text']};
                border: 2px solid {self.theme['Header']};
                padding: 5px;
                font-size: 14px;
                border-radius: 6px;
                font-weight: bold;
            }}
            QPushButton:hover {{
                background-color: {self.theme['Hover']};
                border: 2px solid {self.theme['Hover']};
                color: white;
            }}
        """)

    def init_ui(self):
        """Initialize the user interface components."""
        self.layout = QVBoxLayout()
        self.form_layout = QFormLayout()
        
        # Theme selection
        self.theme_label = QLabel("Theme:")
        self.theme_label.setStyleSheet(f"color: {self.theme['Text']}; font-size: 14px;")
        self.theme_combo = QComboBox()
        self.theme_combo.addItems(["dark_red", "dark_green", "dark_blue", "light", 
                                  "dark_mode", "dark_pink", "the_best_theme", 
                                  "optimal_theme", "dark_optimal_theme"])
        self.theme_combo.setCurrentText(self.settings['Theme'])
        self.theme_combo.setStyleSheet(f"""
            QComboBox {{
                background-color: {self.theme['Button']};
                color: {self.theme['Text']};
                border: 2px solid {self.theme['Header']};
                padding: 5px;
                font-size: 14px;
                border-radius: 6px;
                font-weight: bold;
            }}
            QComboBox:hover {{
                background-color: {self.theme['Hover']};
                border: 2px solid {self.theme['Hover']};
                color: white;
            }}
            QComboBox::drop-down{{
                border: none;
            }}
            QComboBox::down-arrow{{
                image: url({self.default_icon_path});
                padding-right: 10px;
                width: 10px;
                height: 10px;
            }}
        """)
        self.theme_combo.currentTextChanged.connect(self.on_theme_changed)
        self.theme_combo.installEventFilter(self)
        self.form_layout.addRow(self.theme_label, self.theme_combo)

        # Font selection
        self.font_label = QLabel("Font:")
        self.font_label.setStyleSheet(f"color: {self.theme['Text']}; font-size: 14px;")
        self.font_combo = QComboBox()
        self.font_combo.addItems(["First", "Second", "Third"])
        self.font_combo.setCurrentText(self.settings['Font'])
        self.font_combo.setStyleSheet(f"""
            QComboBox {{
                background-color: {self.theme['Button']};
                color: {self.theme['Text']};
                border: 2px solid {self.theme['Header']};
                padding: 5px;
                font-size: 14px;
                border-radius: 6px;
                font-weight: bold;
            }}
            QComboBox:hover {{
                background-color: {self.theme['Hover']};
                border: 2px solid {self.theme['Hover']};
                color: white;
            }}
            QComboBox::drop-down{{
                border: none;
            }}
            QComboBox::down-arrow{{
                image: url({self.default_icon_path});
                padding-right: 10px;
                width: 10px;
                height: 10px;
            }}
        """)
        self.font_combo.installEventFilter(self)
        self.form_layout.addRow(self.font_label, self.font_combo)

        # Number display format selection
        self.number_display_label = QLabel("Number Display:")
        self.number_display_label.setStyleSheet(f"color: {self.theme['Text']}; font-size: 14px;")
        self.number_display_combo = QComboBox()
        self.number_display_combo.addItems(["Numbers", "Roman_Numerals", "Alphabetic"])
        self.number_display_combo.setCurrentText(self.settings['Number_Format'])
        self.number_display_combo.setStyleSheet(f"""
            QComboBox {{
                background-color: {self.theme['Button']};
                color: {self.theme['Text']};
                border: 2px solid {self.theme['Header']};
                padding: 5px;
                font-size: 14px;
                border-radius: 6px;
                font-weight: bold;
            }}
            QComboBox:hover {{
                background-color: {self.theme['Hover']};
                border: 2px solid {self.theme['Hover']};
                color: white;
            }}
            QComboBox::drop-down{{
                border: none;
            }}
            QComboBox::down-arrow{{
                image: url({self.default_icon_path});
                padding-right: 10px;
                width: 10px;
                height: 10px;
            }}
        """)
        self.number_display_combo.installEventFilter(self)
        self.form_layout.addRow(self.number_display_label, self.number_display_combo)

        self.layout.addLayout(self.form_layout)
        self.layout.addSpacerItem(QtWidgets.QSpacerItem(20, 20, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding))

        # Buttons layout
        buttons_layout = QHBoxLayout()

        # OK button
        self.ok_button = QPushButton("OK")
        self.ok_button.setFixedSize(100, 40)
        self.ok_button.setStyleSheet(f"""
            QPushButton {{
                background-color: {self.theme['Header']};
                color: {self.theme['Text']};
                border: 2px solid {self.theme['Header']};
                padding: 5px;
                font-size: 14px;
                border-radius: 6px;
                font-weight: bold;
            }}
            QPushButton:hover {{
                background-color: {self.theme['Hover']};
                border: 2px solid {self.theme['Hover']};
                color: white;
            }}
        """)
        self.ok_button.clicked.connect(self.on_ok_clicked)

        # Cancel button
        self.cancel_button = QPushButton("Cancel")
        self.cancel_button.setFixedSize(100, 40)
        self.cancel_button.setStyleSheet(f"""
            QPushButton {{
                background-color: {self.theme['Button']};
                color: {self.theme['Text']};
                border: 2px solid {self.theme['Header']};
                padding: 5px;
                font-size: 14px;
                border-radius: 6px;
                font-weight: bold;
            }}
            QPushButton:hover {{
                background-color: {self.theme['Hover']};
                border: 2px solid {self.theme['Hover']};
                color: white;
            }}
        """)
        self.cancel_button.clicked.connect(self.cancel_button_clicked)

        buttons_layout.addWidget(self.ok_button)
        buttons_layout.addWidget(self.cancel_button)
        self.layout.addLayout(buttons_layout)

        self.setLayout(self.layout)

    def eventFilter(self, obj, event):
        """
        Handle hover events for combo boxes.
        
        Args:
            obj (QObject): The object that generated the event
            event (QEvent): The event that occurred
            
        Returns:
            bool: True if the event was handled, False otherwise
        """
        if obj == self.theme_combo or obj == self.font_combo or obj == self.number_display_combo:
            if event.type() == QEvent.Enter:
                # Hover state styling
                obj.setStyleSheet(f"""
                    QComboBox {{
                        background-color: {self.theme['Button']};
                        color: {self.theme['Text']};
                        border: 2px solid {self.theme['Header']};
                        padding: 5px;
                        font-size: 14px;
                        border-radius: 6px;
                        font-weight: bold;
                    }}
                    QComboBox:hover {{
                        background-color: {self.theme['Hover']};
                        border: 2px solid {self.theme['Hover']};
                        color: white;
                    }}
                    QComboBox::drop-down{{
                        border: none;
                    }}
                    QComboBox::down-arrow{{
                        image: url({self.hover_icon_path});
                        padding-right: 10px;
                        width: 10px;
                        height: 10px;
                    }}
                """)
            elif event.type() == QEvent.Leave:
                # Normal state styling
                obj.setStyleSheet(f"""
                    QComboBox {{
                        background-color: {self.theme['Button']};
                        color: {self.theme['Text']};
                        border: 2px solid {self.theme['Header']};
                        padding: 5px;
                        font-size: 14px;
                        border-radius: 6px;
                        font-weight: bold;
                    }}
                    QComboBox:hover {{
                        background-color: {self.theme['Hover']};
                        border: 2px solid {self.theme['Hover']};
                        color: white;
                    }}
                    QComboBox::drop-down{{
                        border: none;
                    }}
                    QComboBox::down-arrow{{
                        image: url({self.default_icon_path});
                        padding-right: 10px;
                        width: 10px;
                        height: 10px;
                    }}
                """)
        return super().eventFilter(obj, event)

    def cancel_button_clicked(self):
        """Handle cancel button click - revert icon colors and reject dialog."""
        self.modify_icons_color(self.theme['HeaderText'], self.theme['Header'], self.started_hover, self.started_default)
        self.reject()

    def on_theme_changed(self):
        """Handle theme change - update colors and icons."""
        self.theme = color_palette(self.theme_combo.currentText().lower())
        self.modify_icons_color(self.old_hover, self.old_default, self.theme['HeaderText'], self.theme['Header'])
        self.old_hover = "" + self.theme['HeaderText']
        self.old_default = "" + self.theme['Header']
        self.apply_theme()

    def modify_icons_color(self, old_hover, old_default, new_hover, new_default):
        """
        Change the color of icons based on theme changes.
        
        Args:
            old_hover (str): Previous hover color
            old_default (str): Previous default color
            new_hover (str): New hover color
            new_default (str): New default color
        """
        hover_icon_path = self.dir_path + '\\Files\\arrow_down_hover.png'
        default_icon_path = self.dir_path + '\\Files\\arrow_down_default.png'
        change_image_color(hover_icon_path, hover_icon_path, old_hover, new_hover)
        change_image_color(default_icon_path, default_icon_path, old_default, new_default)

    def on_ok_clicked(self):
        """
        Handle OK button click - save settings to file and accept dialog.
        
        Saves the current theme, font, and number format settings to a file.
        """
        selected_font = self.font_combo.currentText()
        selected_number_display = self.number_display_combo.currentText()
        selected_theme = self.theme_combo.currentText().lower()

        self.settings['Theme'] = selected_theme
        self.settings['Font'] = selected_font
        self.settings['Number_Format'] = selected_number_display

        # Save settings to file
        with open(self.parent().dir_path + "\\Files\\settings.dat", "w") as file:
            for key, value in self.settings.items():
                file.write(f"{key}:{value}\n")

        self.accept()