import re
from PyQt5 import QtCore
from PyQt5.QtCore import Qt, QRegExp
from PyQt5.QtGui import QValidator
from PyQt5.QtWidgets import QComboBox
from PyQt5.QtGui import QRegExpValidator
from PyQt5.QtWidgets import (QTableWidget, QStyledItemDelegate, QMenu, QLineEdit, QCompleter, 
                             QAbstractItemView, QHeaderView, QSizePolicy, QTableWidgetItem, QTimeEdit)

class CustomTable(QTableWidget):
    """
    A custom table widget that extends QTableWidget. It allows editable cells,
    row creation, row deletion, and input validation for time duration. It also
    provides an autocompletion feature for the input fields.
    
    Attributes:
        theme (dict): A dictionary of colors for styling the table.
        font_families (dict): A dictionary containing font settings for the table and headers.
        data (dict): A dictionary containing data to be used for autocompletion.
    """
    def __init__(self, theme, font_family, data):
        """
        Initializes the custom table with specified theme, font family, and data.
        
        Args:
            theme (dict): Dictionary containing color themes for table styling.
            font_family (dict): Dictionary containing font settings for the table.
            data (dict): Dictionary of data to be used for autocompletion.
        """
        super().__init__()
        self.data = data
        self.theme = theme
        self.font_families = font_family
        self.setColumnCount(2)
        self.setHorizontalHeaderLabels(["Activity Name", "Duration"])
        self.setSelectionMode(QTableWidget.SingleSelection)
        self.setSelectionBehavior(QTableWidget.SelectRows)
        self.setRowHeight(0, 60)
        self.setFont(self.font_families['Table'])
        self.horizontalHeader().setFont(self.font_families['Table_Header'])
        self.horizontalHeader().setDefaultAlignment(Qt.AlignCenter)
        self.gridStyle = Qt.NoPen
        self.showGrid = False
        self.set_style()
        self.horizontalHeader().setHighlightSections(False)
        self.verticalHeader().hide()
        self.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)
        self.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.sizePolicy().hasHeightForWidth())
        self.setSizePolicy(sizePolicy)
        self.viewport().installEventFilter(self)
        self.setContextMenuPolicy(QtCore.Qt.NoContextMenu)
        self.Create_new_row()
        self.setEditTriggers(QAbstractItemView.EditKeyPressed | QAbstractItemView.AnyKeyPressed)
        self.setItemDelegate(TableItemCompleter(self.data, self))

    def refresh_data(self, data):
        """
        Refreshes the table's data and updates the autocompleter.

        Args:
            data (dict): Dictionary containing new data for autocompletion.
        """
        self.data = data
        self.setItemDelegate(TableItemCompleter(self.data, self))
        
    def eventFilter(self, editor, event):
        if event.type() == QtCore.QEvent.FocusOut:
            # Commit the change when focus is lost
            self.commitData.emit(editor)
        return super().eventFilter(editor, event)

    # def keyPressEvent(self, event):
    #     """
    #     Handles key press events for row deletion and creation.
        
    #     Args:
    #         event (QKeyEvent): The key press event.
    #     """
    #     if event.key() == Qt.Key_Delete:
    #         current_row = self.currentRow()
    #         if current_row >= 0:
    #             self.removeRow(current_row)
    #     elif event.key() == Qt.Key_Return or event.key() == Qt.Key_Enter:
    #         self.Create_new_row()
    #     elif event.key() not in (Qt.Key_Return, Qt.Key_Enter, Qt.Key_Tab, Qt.Key_Delete, Qt.Key_Escape, 
    #                        Qt.Key_Shift, Qt.Key_Control, Qt.Key_Alt, Qt.Key_Meta, Qt.Key_End, Qt.Key_PageUp, 
    #                        Qt.Key_PageDown, Qt.Key_Home, Qt.Key_Left, Qt.Key_Up, Qt.Key_Right, Qt.Key_Down):
    #         current_item = self.currentItem()
    #         if current_item:
    #             self.editItem(current_item)
    #             typed_text = event.text()
    #             if current_item.column() == 0:
    #                 self.item(current_item.row(), current_item.column()).setText(event.text())
    #             elif current_item.column() == 1:
    #                 # reg_ex = QRegExp("([0-9]|[0-1][0-9]|2[0-3]):[0-5][0-9]")
    #                 # time_validator = QRegExpValidator(reg_ex)
    #                 # if time_validator.validate(typed_text, 0)[0] == 1:
    #                 self.item(current_item.row(), current_item.column()).setText(typed_text)
    #                 # else:
    #                     # return
    #             editor = self.indexWidget(self.currentIndex())
    #             if editor and isinstance(editor, QLineEdit):
    #                 completer = editor.completer()
    #                 if completer:
    #                     completer.setCompletionPrefix(typed_text)
    #                     completer.complete()
    #     else:
    #         super().keyPressEvent(event)


    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Delete:
            current_row = self.currentRow()
            if current_row >= 0:
                self.removeRow(current_row)
            if current_row == 0:
                self.Create_new_row()

        elif event.key() in (Qt.Key_Return, Qt.Key_Enter):
            self.Create_new_row()

        elif event.key() not in (
            Qt.Key_Return, Qt.Key_Enter, Qt.Key_Tab, Qt.Key_Delete, Qt.Key_Escape,
            Qt.Key_Shift, Qt.Key_Control, Qt.Key_Alt, Qt.Key_Meta, Qt.Key_End,
            Qt.Key_PageUp, Qt.Key_PageDown, Qt.Key_Home, Qt.Key_Left,
            Qt.Key_Up, Qt.Key_Right, Qt.Key_Down
        ):
            current_item = self.currentItem()
            if current_item:
                self.editItem(current_item)
        

        else:
            super().keyPressEvent(event)


    def Create_new_row(self):
        """
        Creates a new row at the bottom of the table.
        """
        row = self.rowCount()
        self.insertRow(row)
        self.setCurrentCell(row, 0)
        for column in range(self.columnCount()):
            item = QTableWidgetItem("")
            item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled | Qt.ItemIsEditable)
            self.setItem(row, column, item)

    def set_style(self):
        """
        Applies the style to the table based on the provided theme.
        """
        self.setStyleSheet(f"""
            QHeaderView::section:first {{
                border-top-left-radius: 4px;
            }}

            QHeaderView::section:last {{
                border-top-right-radius: 4px;
            }}

            QHeaderView::section {{
                background-color: {self.theme['Header']};
                border: 0px solid {self.theme['Header']};
                color: {self.theme['HeaderText']};
                padding: 3px;
            }}

            QTableWidget {{
                background-color: {self.theme['Table']};
                gridline-color: {self.theme['Header']};
                color: {self.theme['HeaderText']};
                border-radius: 5px;
                border: 1px solid {self.theme['Header']};
                selection-background-color: #000000;
            }}

            QTableWidget:first {{
                border-right: 0px solid {self.theme['Header']};
                color: {self.theme['HeaderText']};
                gridline-color: transparent;
            }}

            QTableWidget:last {{
                border-left: 0px solid {self.theme['Header']};
                color: {self.theme['HeaderText']};
                gridline-color: transparent;
            }}

            QTableWidget QScrollBar {{
                background: {self.theme['Table']};
            }}

            QTableCornerButton::section {{
                background-color: {self.theme['Table']};
            }}

            QHeaderView {{
                background-color: {self.theme['Table']};
                border-radius: 5px;
            }}

            QTableWidget::item {{
                border-bottom: 1px solid {self.theme['Header']};
                color: {self.theme['HeaderText']};
            }}

            QTableWidget QScrollBar:vertical
            {{
                background-color: {self.theme['Table']};
                width: 15px;
                margin: 15px 3px 15px 3px;
                border: 1px transparent {self.theme['Table']};
                border-radius: 4px;
            }}
            QTableWidget QScrollBar::handle:vertical
            {{
                background-color: {self.theme['Header']};
                min-height: 5px;
                border-radius: 4px;
            }}
            QTableWidget QScrollBar::sub-line:vertical
            {{
                margin: 3px 0px 3px 0px;
                border-image: url(:/qss_icons/rc/up_arrow_disabled.png);
                height: 10px;
                width: 10px;
                subcontrol-position: top;
                subcontrol-origin: margin;
            }}
            QTableWidget QScrollBar::add-line:vertical
            {{
                margin: 3px 0px 3px 0px;
                border-image: url(:/qss_icons/rc/down_arrow_disabled.png);
                height: 10px;
                width: 10px;
                subcontrol-position: bottom;
                subcontrol-origin: margin;
            }}
            QTableWidget QScrollBar::sub-line:vertical:hover,QScrollBar::sub-line:vertical:on
            {{
                border-image: url(:/qss_icons/rc/up_arrow.png);
                height: 10px;
                width: 10px;
                subcontrol-position: top;
                subcontrol-origin: margin;
            }}
            QTableWidget QScrollBar::add-line:vertical:hover, QScrollBar::add-line:vertical:on
            {{
                border-image: url(:/qss_icons/rc/down_arrow.png);
                height: 10px;
                width: 10px;
                subcontrol-position: bottom;
                subcontrol-origin: margin;
            }}
            QTableWidget QScrollBar::up-arrow:vertical, QScrollBar::down-arrow:vertical
            {{
                background: none;
            }}
            QTableWidget QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical
            {{
                background: none;
            }}
        """)


    def set_theme(self, theme):
        """
        Sets a new theme for the table and applies the style.

        Args:
            theme (dict): A dictionary containing new theme colors for the table.
        """
        self.theme = theme
        self.set_style()

    def set_font_family(self, font_family):
        """
        Sets the font family for the table and header.

        Args:
            font_family (dict): A dictionary containing the font settings.
        """
        self.font_families = font_family
        self.setFont(self.font_families['Table'])
        self.horizontalHeader().setFont(self.font_families['Table_Header'])

    def get_data(self):
        """
        Retrieves the data from the table (name and duration).

        Returns:
            list: A list of lists containing the name and duration from each row.
        """
        data = []
        for row in range(self.rowCount()):
            name_item = self.item(row, 0)
            duration_item = self.item(row, 1)
            
            if not name_item or not duration_item:
                continue
                
            name = name_item.text().strip()
            duration = duration_item.text().strip()
            
            if not name and not duration:
                continue
                
            if duration:  
                time_parts = duration.split(':')
                if len(time_parts) != 2 or not all(part.isdigit() for part in time_parts):
                    continue  
                    
                hours, minutes = map(int, time_parts)
                if hours < 0 or hours > 23 or minutes < 0 or minutes > 59:
                    continue  
                    
            if name and duration:
                data.append([name, duration])
                
        return data


    def add_row(self, name, duration):
        if name.strip() == "" and duration.strip() == "":
            return  
            
        row = self.rowCount()
        self.insertRow(row)
        item_name = QTableWidgetItem(name.strip())
        item_duration = QTableWidgetItem(duration.strip())
        item_name.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled | Qt.ItemIsEditable)
        item_duration.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled | Qt.ItemIsEditable)
        self.setItem(row, 0, item_name)
        self.setItem(row, 1, item_duration)


class TableItemCompleter(QStyledItemDelegate):
    """
    A delegate that provides autocompletion for table items based on a provided data dictionary.
    
    Attributes:
        data (dict): A dictionary containing data for autocompletion.
        parent (QWidget): The parent widget for this delegate.
    """
    def __init__(self, completionMap, parent=None):
        """
        Initializes the completer with the provided data.

        Args:
            data (dict): Dictionary containing autocompletion data.
            parent (QWidget): The parent widget for the delegate.
        """
        super().__init__(parent)
        self.completers = {}
        for i, (column, completionList) in enumerate(completionMap.items()):
            completer = QCompleter(completionList, self)
            completer.setCaseSensitivity(Qt.CaseInsensitive)
            popup = completer.popup()
            popup.setStyleSheet("""
                QListView {
                    background-color: #4A4A4A;
                    color: #FFFFFF;
                    border: 0px solid #444444;
                }
                QListView::item {
                    padding: 5px;
                }
                QListView::item:selected {
                    background-color: #640408;
                    color: #B53534;
                }
                QListView::item:hover {
                    background-color: #640408;
                    color: #B53534;
                }
            """)
            self.completers[i] = completer
            completer.setFilterMode(Qt.MatchStartsWith)
            self.editor = None
        
    # def createEditor(self, parent, option, index):
    #     """
    #     Creates the editor (QLineEdit) for the item at the specified index.

    #     Args:
    #         parent (QWidget): The parent widget for the editor.
    #         option (QStyleOptionViewItem): Style options for the item.
    #         index (QModelIndex): The index of the item to edit.

    #     Returns:
    #         QLineEdit: The editor widget (a QLineEdit with autocompletion).
    #     """
    #     editor = QLineEdit(parent)
    #     editor.setContextMenuPolicy(Qt.NoContextMenu)
    #     if index.column() in self.completers:
    #         if index.column() == 1:
    #             reg_ex = QRegExp("([0-9]|[0-1][0-9]|2[0-3]):[0-5][0-9]")
    #             input_validator = QRegExpValidator(reg_ex, editor)
    #             editor.setValidator(input_validator)
    #             editor.setText('')
    #         editor.setCompleter(self.completers[index.column()])
    #     return editor

    def createEditor(self, parent, option, index):
        if index.column() == 1:  # Duration column
            editor = QTimeEdit(parent)
            editor.setDisplayFormat("HH:mm")
            editor.setTime(QtCore.QTime(0, 0))
            return editor
        else:
            editor = QLineEdit(parent)
            editor.setContextMenuPolicy(Qt.NoContextMenu)
            if index.column() in self.completers:
                editor.setCompleter(self.completers[index.column()])
            return editor
    #========================================================
    # def createEditor(self, parent, option, index):
    #     editor = QLineEdit(parent)
    #     editor.setContextMenuPolicy(Qt.NoContextMenu)
        
    #     if index.column() == 0 and 0 in self.completers:
    #         editor.setCompleter(self.completers[0])
            
    #     return editor  
    #========================================================
    # def setModelData(self, editor, model, index):
    #     model.setData(index, editor.text().strip())

    def setModelData(self, editor, model, index):
        if isinstance(editor, QTimeEdit):
            time = editor.time()
            model.setData(index, time.toString("HH:mm"))
        else:
            model.setData(index, editor.text().strip())