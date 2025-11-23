import os
from PyQt5.QtCore import Qt
from create_excel import ExcelTable
from Custom_TableView import CustomView
from PyQt5.QtGui import QPalette, QColor
from calculate_times import CalculateTimes
from PyQt5.QtWidgets import QMainWindow, QVBoxLayout, QHBoxLayout, QPushButton, QGroupBox, QTableView, QWidget, QFileDialog


class CalculatePage(QMainWindow):
    def __init__(self, theme, font_family, list_rest_data, list_no_rest_data, settings):
        super().__init__()
        self.theme = theme
        self.fontFamilies = font_family
        self.settings = settings
        self.list_rest_data = list_rest_data
        self.list_no_rest_data = list_no_rest_data
        settings=self.settings 

        # Table headers
        self.table_headers = [
            ("Initial Activity Times", ["Activity", "Duration"]),
            ("Activity Times", ["Activity", "Subduration", "Duration"]),
            ("Daily Schedule Times", ["Activity", "Duration"])
        ]

        # Window setup
        self.setWindowTitle("Calculation Page")
        self.resize(1680, 900)
        self.setMinimumSize(1000, 400)

        # Set background
        self.setAutoFillBackground(True)
        palette = self.palette()
        palette.setColor(QPalette.Window, QColor(self.theme["Background"]))
        self.setPalette(palette)

        
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        main_layout = QVBoxLayout(central_widget)

        table_layout = QHBoxLayout()
        table_layout.setContentsMargins(10, 10, 10, 10)


        # Calculate times
        calc = CalculateTimes(self.list_rest_data, self.list_no_rest_data)
        rest_data, no_rest_data= calc.calcualte_rest_times()

        total_with_rest, total_without_rest = calc.calculate_total_times()

        total_time_sec = total_with_rest + total_without_rest
        reminder_time = (24*3600) - total_time_sec


        # Format time strings
        total_with_rest_str = f"{total_with_rest // 3600:02}:{(total_with_rest % 3600) // 60:02}"
        total_without_rest_str = f"{total_without_rest // 3600:02}:{(total_without_rest % 3600) // 60:02}"
        total_time_str = f"{total_time_sec // 3600:02}:{(total_time_sec % 3600) // 60:02}"
        reminder_time_str = f"{reminder_time // 3600:02}:{(reminder_time % 3600) // 60:02}"

        

        for header, column_names in self.table_headers:
            group_box = self.create_group_box(header)
            vbox = QVBoxLayout()

            # Prepare table data
            if header == "Daily Schedule Times":

                status_text = "Yes" if total_time_sec <= (24*3600) else "No"

                table_data = [
                    ['Time With Rest',total_with_rest_str],# ':'.join(str(total_time_with_rest_times).split(':')[:2])],
                    ['Total Time Without Rest', total_without_rest_str],
                    ['Total Time', total_time_str],
                    ['Reminder Time', reminder_time_str],
                    ['Status', status_text]
                ]

            elif header == "Initial Activity Times":
                table_data = self.list_rest_data + self.list_no_rest_data
            elif header == "Activity Times":
                table_data = rest_data + no_rest_data


            row_limit = 5 if header == "Daily Schedule Times" else None
            vcf = self.settings['Number_Format'].lower() if header != "Daily Schedule Times" else "NoVC"
            table = CustomView(self.theme, self.fontFamilies, table_data, column_names, vc_format=vcf, row_limit=row_limit)

            # Disable editing for schedule table
            if header == "Daily Schedule Times":
                table.setEditTriggers(QTableView.NoEditTriggers)
                table.setSelectionMode(QTableView.NoSelection)
                table.setFocusPolicy(Qt.NoFocus)

            # Add table to layout
            vbox.addWidget(table)
            vbox.setAlignment(Qt.AlignTop)
            vbox.setContentsMargins(10, 30, 10, 10)
            group_box.setLayout(vbox)
            table_layout.addWidget(group_box)

        main_layout.addLayout(table_layout)

        # Create buttons
        self.export_excel_button = QPushButton("Export Excel")
        self.export_excel_button.setFixedSize(200, 50)
        self.export_excel_button.setStyleSheet(f"""
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
        self.export_excel_button.clicked.connect(self.export_to_excel)

        self.ok_button = QPushButton("OK")
        self.ok_button.setFixedSize(200, 50)
        self.ok_button.setStyleSheet(f"""
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
        self.ok_button.clicked.connect(self.close)

        button_layout = QHBoxLayout()
        button_layout.addStretch()
        button_layout.addWidget(self.export_excel_button, alignment=Qt.AlignRight)
        button_layout.addWidget(self.ok_button, alignment=Qt.AlignRight)
        button_layout.setContentsMargins(0, 0, 10, 10)

        main_layout.addLayout(button_layout)

    def create_group_box(self, header):
        """Create styled group box"""
        group_box = QGroupBox()
        group_box.setFlat(True)
        group_box.setTitle(header)
        group_box.setFont(self.fontFamilies['Group_Box'])
        group_box.setAlignment(Qt.AlignCenter)
        group_box.setStyleSheet(f"""
            QGroupBox {{
                background-color: {self.theme['Table']};
                border: 0px;
                color: {self.theme['HeaderText']};
                border-radius: 6px;
                margin: 5px;
            }}
        """)
        return group_box
    

    def export_to_excel(self):
        """Export data to Excel"""
        all_activities_list = self.list_rest_data + self.list_no_rest_data
        all_activities_list = [activity for activity in all_activities_list if activity[0] != 'Sleep']
        file = str(QFileDialog.getExistingDirectory(self, "Select Directory", os.path.realpath(os.path.dirname(__file__)) ))
        ExcelTable(all_activities_list,"Fa", file).create_excel()
        ExcelTable(all_activities_list,"En", file).create_excel()