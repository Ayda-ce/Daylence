import os
from PyQt5 import QtCore
from PyQt5 import QtWidgets
from PyQt5.QtGui import QPalette, QColor
from PyQt5.QtCore import Qt, QCoreApplication
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QGridLayout, QLabel, QPushButton, QHBoxLayout, QDesktopWidget, QGroupBox

from about_us import About_us
from Custom_Table import CustomTable
from Settings_Form import SettingsForm
from Calculation_Page import CalculatePage
from styles import color_palette, font_families
from activities_list_form import ActivitiesListForm
from utils import read_settings, load_activity_names, create_day_times_list

def create_groupbox(title, table, font_family, theme):
    """Create styled group box with table"""
    groupBox = QGroupBox()
    groupBox.setObjectName("groupBox")
    groupBox.setFont(font_family)
    groupBox.setStyleSheet(f"""border:0;
                            color:{theme['HeaderText']};
                            background-color: {theme['Table']};
                            border-radius: 6px;
                            """)
    groupBox.setAlignment(QtCore.Qt.AlignCenter)
    groupBox.setFlat(True)
    groupBox.setTitle(QCoreApplication.translate("MainWindow", title, None))
    layout = QVBoxLayout()
    layout.addWidget(table)
    layout.setContentsMargins(10, 30, 10, 10)
    groupBox.setLayout(layout)
    return groupBox

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        # Initialize paths and settings
        self.dir_path = os.path.dirname(os.path.realpath(__file__))
        self.settings = read_settings(self.dir_path + "\\Files\\settings.dat")
        self.theme = color_palette(self.settings['Theme'])
        self.font_families = font_families(self.settings['Font'])
        self.number_format = self.settings['Number_Format']
        self.setWindowTitle("Main Page")
        self.resize(1680, 900)
        self.setMinimumSize(1000, 400)
        self.center()
        self.setAutoFillBackground(True)
        palette = self.palette()
        palette.setColor(QPalette.Window, QColor(self.theme['Background']))
        self.setPalette(palette)
        self.setContextMenuPolicy(Qt.NoContextMenu)
        self.about_window = None
        self.settings_window = None
        
        # Load data
        self.timelist = create_day_times_list(23)
        self.activity_names = load_activity_names(self.dir_path + "\\Files\\Activity Names.txt")
        self.suggest_lists = {'Activity Name': self.activity_names, 'Duration': self.timelist}
        
        # Setup UI
        self.init_ui()
        self.load_last_info()

    def init_ui(self):
        main_layout = QVBoxLayout()
        tables_layout = QGridLayout()
        
        # Create tables
        self.activities_with_breaks = CustomTable(self.theme, self.font_families, self.suggest_lists)
        self.activities_without_breaks = CustomTable(self.theme, self.font_families, self.suggest_lists)
        self.daily_joint_activities = CustomTable(self.theme, self.font_families, self.suggest_lists)
        
        # Create group boxes
        self.activities_with_breaks_group = create_groupbox("Activities with breaks", self.activities_with_breaks, self.font_families['Group_Box'], self.theme)
        self.activities_without_breaks_group = create_groupbox("Activities without breaks", self.activities_without_breaks, self.font_families['Group_Box'], self.theme)
        self.daily_joint_activities_group = create_groupbox("Daily joint activities", self.daily_joint_activities, self.font_families['Group_Box'], self.theme)
        
        # Layout setup
        tables_layout.setContentsMargins(10, 10, 10, 10)
        tables_layout.setSpacing(30)
        tables_layout.addWidget(self.activities_with_breaks_group, 0,0)
        tables_layout.addWidget(self.activities_without_breaks_group, 0, 1)
        tables_layout.addWidget(self.daily_joint_activities_group, 0, 2)
        main_layout.addLayout(tables_layout)
        
        buttons_layout = QHBoxLayout()
        
        # Show activities button
        show_activities_button = QPushButton("Show Activities")
        show_activities_button.setFixedSize(200, 50)
        show_activities_button_style = f"""
            QPushButton {{
                background-color: {self.theme['Button']};
                color: {self.theme['Text']};
                border: 2px solid {self.theme['Header']};
                padding: 10px 25px;
                font-size: 18px;
                border-radius: 6px;
                font-weight: bold;
            }}
            QPushButton:hover {{
                background-color: {self.theme['Hover']};
                border: 2px solid {self.theme['Hover']};
                color: white;
            }}
        """
        show_activities_button.setStyleSheet(show_activities_button_style)
        show_activities_button.clicked.connect(self.show_activity_list)
        
        # Calculate button
        calculate_button = QPushButton("Calculate")
        calculate_button.setFixedSize(200, 50)
        calculate_button_style = f"""
            QPushButton {{
                background-color: {self.theme['Button']};
                color: {self.theme['Text']};
                border: 2px solid {self.theme['Header']};
                padding: 10px 25px;
                font-size: 18px;
                border-radius: 6px;
                font-weight: bold;
            }}
            QPushButton:hover {{
                background-color: {self.theme['Hover']};
                border: 2px solid {self.theme['Hover']};
                color: white;
            }}
        """
        calculate_button.setStyleSheet(calculate_button_style)
        calculate_button.clicked.connect(self.calculate_button)
        
        # About label
        about_label = QLabel("About", self)
        about_label.setStyleSheet(f"""
            QLabel {{
                color: {self.theme['Text']};
                font-size: 19px;
                font-weight: bold;
                text-decoration: underline;
            }}
            QLabel:hover {{
                color: {self.theme['Hover']};
            }}
        """)
        about_label.setAlignment(Qt.AlignLeft | Qt.AlignCenter)
        about_label.mousePressEvent = self.open_about_window
        
        # Settings label
        settings_label = QLabel("Settings", self)
        settings_label.setStyleSheet(f"""
            QLabel {{
                color: {self.theme['Text']};
                font-size: 19px;
                font-weight: bold;
                text-decoration: underline;
            }}
            QLabel:hover {{
                color: {self.theme['Hover']};
            }}
        """)
        settings_label.setAlignment(Qt.AlignLeft | Qt.AlignCenter)
        settings_label.mousePressEvent = self.open_settings_window
        
        # Add widgets to layout
        buttons_layout.addWidget(about_label, alignment=Qt.AlignLeft)
        buttons_layout.addWidget(settings_label, alignment=Qt.AlignLeft)
        buttons_layout.addStretch()
        buttons_layout.addWidget(show_activities_button)
        buttons_layout.addWidget(calculate_button)
        buttons_layout.setSpacing(10)
        
        main_layout.addLayout(buttons_layout)
        main_layout.setStretch(0, 7)
        main_layout.setStretch(1, 0)
        self.setLayout(main_layout)


    def center(self):
        """Center window on screen"""
        screen_geometry = QDesktopWidget().screenGeometry()
        x = (screen_geometry.width() - self.width()) // 2
        y = (screen_geometry.height() - self.height()) // 2
        self.move(x, y)


    def save_last_info(self):
        """Save table data to file"""
        files_dir = os.path.join(self.dir_path, "Files")
        if not os.path.exists(files_dir):
            os.makedirs(files_dir)
        file_path = os.path.join(files_dir, "last_info.dat")
        try:
            with open(file_path, "w", encoding='utf-8') as f:
                f.write("[Activities with breaks]\n")
                for row in self.activities_with_breaks.get_data():
                    f.write(f"{row[0]}|{row[1]}\n")
                f.write("\n")
                
                f.write("\n[Activities without breaks]\n")
                for row in self.activities_without_breaks.get_data():
                    f.write(f"{row[0]}|{row[1]}\n")
                
                f.write("\n[Daily joint activities]\n")
                for row in self.daily_joint_activities.get_data():
                    f.write(f"{row[0]}|{row[1]}\n")
        except Exception as e:
            print(f"Error saving data: {e}")


    def load_last_info(self):
        """Load saved table data from file"""
        file_path = os.path.join(self.dir_path, "Files", "last_info.dat")
        if not os.path.exists(file_path):
            return

        try:
           
            for table in [
                self.activities_with_breaks,
                self.activities_without_breaks,
                self.daily_joint_activities
            ]:
                table.setRowCount(0)

            current_section = None
            with open(file_path, "r", encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    if not line:
                        continue

                    if line == "[Activities with breaks]":
                        current_section = "with_breaks"
                    elif line == "[Activities without breaks]":
                        current_section = "without_breaks"
                    elif line == "[Daily joint activities]":
                        current_section = "joint_activities"
                    else:
                        parts = line.split("|")
                        if len(parts) == 2:
                            if current_section == "with_breaks":
                                self.activities_with_breaks.add_row(parts[0], parts[1])
                            elif current_section == "without_breaks":
                                self.activities_without_breaks.add_row(parts[0], parts[1])
                            elif current_section == "joint_activities":
                                self.daily_joint_activities.add_row(parts[0], parts[1])

            # Clean empty rows  
            for table in [
                self.activities_with_breaks,
                self.activities_without_breaks,
                self.daily_joint_activities
            ]:
                rows_to_remove = []
                for row in range(table.rowCount() - 1, -1, -1):
                    if not table.item(row, 0) or not table.item(row, 1) or \
                    (table.item(row, 0).text().strip() == "" and table.item(row, 1).text().strip() == ""):
                        rows_to_remove.append(row)
                for row in rows_to_remove:
                    table.removeRow(row)
                table.Create_new_row()
        except Exception as e:
            print(f"Error Loading data: {e}")

    def closeEvent(self, event):
        """Handle window close event"""
        self.save_last_info()
        event.accept()


    def show_activity_list(self):
        """Show activity list dialog"""
        activities_file_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "Files", "Activity Names.txt")
        dialog = ActivitiesListForm(self.theme, self.font_families, activities_file_path, self.number_format, self)
        dialog.exec_()
        self.activity_names = load_activity_names(activities_file_path)
        self.suggest_lists = {'Activity Name': self.activity_names, 'Duration': self.timelist}
        self.activities_with_breaks.refresh_data(self.suggest_lists)
        self.activities_without_breaks.refresh_data(self.suggest_lists)
        self.daily_joint_activities.refresh_data(self.suggest_lists)


    def open_about_window(self, event):
        """Open about window"""
        if self.about_window is None or not self.about_window.isVisible():
            self.about_window = About_us(
                theme=self.theme,
                font_families=self.font_families,
                settings=self.settings,
                parent=self
            )
            self.about_window.show()
            self.about_window.finished.connect(self.on_about_window_closed)


    def open_settings_window(self, event):
        """Open settings window"""
        if self.settings_window is None or not self.settings_window.isVisible():
            self.settings_window = SettingsForm(self.theme, self.font_families, self.settings, self)
            self.settings_window.theme_combo.currentTextChanged.connect(self.apply_theme_immediately)
            self.settings_window.show()
            self.settings_window.finished.connect(self.on_settings_window_closed)


    def apply_theme_immediately(self, theme_name):
        """Apply theme changes immediately"""
        self.theme = color_palette(theme_name.lower())
        self.update_ui()


    def on_about_window_closed(self):
        """Handle about window close"""
        self.about_window = None


    def on_settings_window_closed(self):
        """Handle settings window close"""
        self.settings_window = None
        self.settings = read_settings(self.dir_path + "\\Files\\settings.dat")
        self.theme = color_palette(self.settings['Theme'])
        self.font_families = font_families(self.settings['Font'])
        self.number_format = self.settings['Number_Format']
        self.update_ui()


    def update_ui(self):
        """Update UI elements with current theme"""
        palette = self.palette()
        palette.setColor(QPalette.Window, QColor(self.theme['Background']))
        self.setPalette(palette)
        
        for button in self.findChildren(QPushButton):
            if button.text() == "Show Activities":
                button.setStyleSheet(f"""
                    QPushButton {{
                        background-color: {self.theme['Button']};
                        color: {self.theme['Text']};
                        border: 2px solid {self.theme['Header']};
                        padding: 10px 25px;
                        font-size: 18px;
                        border-radius: 6px;
                        font-weight: bold;
                    }}
                    QPushButton:hover {{
                        background-color: {self.theme['Hover']};
                        border: 2px solid {self.theme['Hover']};
                        color: white;
                    }}
                """)
            elif button.text() == "Calculate":
                button.setStyleSheet(f"""
                    QPushButton {{
                        background-color: {self.theme['Button']};
                        color: {self.theme['Text']};
                        border: 2px solid {self.theme['Header']};
                        padding: 10px 25px;
                        font-size: 18px;
                        border-radius: 6px;
                        font-weight: bold;
                    }}
                    QPushButton:hover {{
                        background-color: {self.theme['Hover']};
                        border: 2px solid {self.theme['Hover']};
                        color: white;
                    }}
                """)
                
        for label in self.findChildren(QLabel):
            if label.text() in ["About", "Settings"]:
                label.setStyleSheet(f"""
                    QLabel {{
                        color: {self.theme['Text']};
                        font-size: 19px;
                        font-weight: bold;
                        text-decoration: underline;
                    }}
                    QLabel:hover {{
                        color: {self.theme['Hover']};
                    }}
                """)
                
        for table in self.findChildren(CustomTable):
            table.set_theme(self.theme)
            table.set_font_family(self.font_families)
            
        self.daily_joint_activities_group.setStyleSheet(f"""border:0;
                            color:{self.theme['HeaderText']};
                            background-color: {self.theme['Table']};
                            border-radius: 6px;
                            """)
        self.activities_without_breaks_group.setStyleSheet(f"""border:0;
                            color:{self.theme['HeaderText']};
                            background-color: {self.theme['Table']};
                            border-radius: 6px;
                            """)
        self.activities_with_breaks_group.setStyleSheet(f"""border:0;
                            color:{self.theme['HeaderText']};
                            background-color: {self.theme['Table']};
                            border-radius: 6px;
                            """)


    def calculate_button(self):
        """Handle calculate button click"""
        rest_list = [row for row in self.activities_with_breaks.get_data() if row[0].strip() and row[1].strip()]
        no_rest_list = [row for row in self.activities_without_breaks.get_data() if row[0].strip() and row[1].strip()]
        joint_activities = [row for row in self.daily_joint_activities.get_data() if row[0].strip() and row[1].strip()]
        
        no_rest_list += joint_activities
        
        if not rest_list and not no_rest_list:
            QtWidgets.QMessageBox.warning(self, "Error", "Please enter at least one activity in the tables.")
            return
        
        try:
            self.calculate_page = CalculatePage(self.theme, self.font_families, rest_list, no_rest_list, self.settings)
            self.calculate_page.show()
        except Exception as e:
            QtWidgets.QMessageBox.critical(self, "Error", f"An error occurred during calculation:\n{str(e)}")
            