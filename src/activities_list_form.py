from PyQt5.QtCore import Qt
from PyQt5 import QtWidgets
from utils import load_activity_names
from Custom_TableView import CustomView
from PyQt5.QtGui import QPalette, QColor
from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout, QPushButton, QDialog, QMessageBox


class ActivitiesListForm(QDialog):
    def __init__(self, theme, font_family, file_path, vcf, editable=True, parent=None):
        """
        Initialize the Activities List dialog.

        Args:
            theme (dict): A dictionary containing theme-related colors (e.g., Background, Header, Text, Hover).
            font_family (str): The font family to use in the form.
            file_path (str): The file path to load and save activities.
            vcf (str): The vertical format preference for the activity list (e.g., "compact" or "expanded").
            editable (bool): Whether the activity list should be editable. Default is True.
            parent (QWidget, optional): The parent widget. Defaults to None.
        """
        super().__init__(parent)
        self.theme = theme
        self.font_family = font_family
        self.file_path = file_path
        self.editable = editable
        self.vertival_format = vcf.lower()
        self.setWindowTitle("Activity List")
        self.resize(500, 400)
        self.setAutoFillBackground(True)
        
        # Set background color based on the selected theme
        palette = self.palette()
        palette.setColor(QPalette.Window, QColor(self.theme['Background']))
        self.setPalette(palette)

        layout = QVBoxLayout()

        # Load and sort activities, then add an empty item at the end for new activities
        self.activities = load_activity_names(self.file_path)
        self.activities.sort()
        self.activities += ['']

        # Create table widget to display activities
        self.table_widget = CustomView(
            theme=self.theme,
            font_family=self.font_family,
            data=[[activity] for activity in self.activities],
            column_names=["Activity"],
            vc_format=self.vertival_format,
            is_editable=self.editable,
            parent=self
        )
        self.table_widget.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
        layout.addWidget(self.table_widget)

        # Buttons layout
        buttons_layout = QHBoxLayout()

        # OK button
        ok_button = QPushButton("OK")
        ok_button.setFixedSize(100, 50)
        ok_button.setStyleSheet(f"""
            QPushButton {{
                background-color: {self.theme['Header']};
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
        ok_button.clicked.connect(self.on_ok_clicked)
        buttons_layout.addWidget(ok_button)
        layout.addLayout(buttons_layout)
        self.setLayout(layout)

    def on_ok_clicked(self):
        """
        Handle the OK button click event.

        Prompts the user whether they want to save any changes made to the activity list.
        If they choose 'Yes', it saves the activities; if 'No', it discards changes.
        If 'Cancel' is selected, no action is taken.
        """
        # Get activities from the table
        activities = self.get_activities()

        # Ask the user whether they want to save changes
        reply = QMessageBox.question(self, 'Save Changes', 'Do you want to save changes?',
                                        QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel)
        
        if reply == QMessageBox.Yes:
            self.save_activities(activities)
            self.accept()
        elif reply == QMessageBox.No:
            self.reject()
        else:
            pass  # Cancel, do nothing

    def get_activities(self):
        """
        Get all activities from the table widget.

        Returns:
            list: A list of activities currently displayed in the table.
        """
        activities = []
        for row in range(self.table_widget.model.rowCount(None)):
            activity = self.table_widget.model.data(self.table_widget.model.index(row, 0), Qt.DisplayRole)
            if activity:
                activities.append(activity)
        return activities

    def save_activities(self, activities):
        """
        Save the list of activities to the specified file.

        Args:
            activities (list): A list of activities to be saved.
        """
        with open(self.file_path, "w", encoding="utf-8") as file:
            for activity in list(set(activities)):  # Remove duplicates before saving
                file.write(activity + '\n')
