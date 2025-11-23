from PyQt5.QtCore import Qt
from PyQt5 import QtCore, QtGui
from utils import number2roman_numerals, number2alphabetic
from PyQt5.QtWidgets import QHeaderView, QTableView, QStyledItemDelegate

class MyDelegate(QStyledItemDelegate):
    """
    A custom delegate to style editable cells in the QTableView.
    """

    def __init__(self, theme, parent=None):
        """
        Initialize the delegate with a theme dictionary for styling.

        :param theme: Dictionary of color and style values.
        :param parent: Parent widget (optional).
        """
        super().__init__(parent)
        self.theme = theme

    def createEditor(self, parent, option, index):
        """
        Create an editor for the cell.
        """
        return super().createEditor(parent, option, index)

    def setEditorData(self, editor, index):
        """
        Set editor content and apply theme-based style.
        """
        text = index.data(Qt.EditRole) or index.data(Qt.DisplayRole)
        editor.setText(str(text))
        editor.setStyleSheet(f"""
            QLineEdit {{
                background-color: {self.theme['Table']};
                color: {self.theme['HeaderText']};
                border: none;
                outline: none;
            }}
        """)

class CustomView(QTableView):
    """
    A themed QTableView widget with customizable headers, row indexing, edit/delete functionality,
    and vertical index formatting options.
    """

    def __init__(self, theme, font_family, data, column_names,
                 vc_format='number', is_editable=False, row_limit=None, parent=None):
        """
        Initialize the custom table view.

        :param theme: Color palette dictionary.
        :param font_family: Dictionary of font objects.
        :param data: Table data as a list of lists.
        :param column_names: List of column header names.
        :param vc_format: Vertical header format: 'number', 'roman_numerals', 'alphabetic', or 'NoVC'.
        :param is_editable: If True, table rows can be edited.
        :param row_limit: Maximum number of rows to show (optional).
        :param parent: Parent widget (optional).
        """
        super().__init__(parent)
        self.theme = theme
        self.fontFamilies = font_family
        self.data = data[:row_limit] if row_limit else data
        self.column_names = column_names
        self.vc_format = vc_format
        self.is_editable = is_editable

        # Set custom delegate for styling editors
        delegate = MyDelegate(self.theme)
        self.setItemDelegate(delegate)

        if not self.is_editable:
            self.setEditTriggers(QTableView.NoEditTriggers)
            self.setSelectionMode(QTableView.NoSelection)

        # Header fonts and styles
        self.horizontalHeader().setFont(self.fontFamilies['Table_View_Header'])
        self.set_style()

        self.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.verticalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        self.horizontalHeader().setSectionsMovable(False)
        self.verticalHeader().setSectionsMovable(False)

        # Handle vertical header visibility and formatting
        if self.vc_format == 'NoVC':
            self.verticalHeader().setVisible(False)
        else:
            self.verticalHeader().setVisible(True)
        self.verticalHeader().setDefaultAlignment(Qt.AlignCenter)

        self.verticalHeader().setStyleSheet(f"""
            QHeaderView::section {{
                background-color: {self.theme['Table']};
                border-right: 1px solid {self.theme['Header']};
                border-bottom: 1px solid {self.theme['Header']};
                border-left: 1px solid {self.theme['Header']};
            }}
            QHeaderView {{
                background-color: {self.theme['Table']};
                border-radius: 4px;
            }}
            QHeaderView::section:last {{
                border-top-right-radius: 0px;
            }}
        """)

        self.setShowGrid(True)

        # Assign data model
        self.model = TableModel(self.data, self.column_names, vertical_count_format=self.vc_format, row_limit=row_limit)
        self.setModel(self.model)

        self.setSelectionMode(QTableView.SingleSelection)
        self.setSelectionBehavior(QTableView.SelectRows)
        self.setFont(self.fontFamilies['Table_View_Header'])

        if row_limit:
            # Auto-fit height based on row count
            self.setFixedHeight(5 * self.horizontalHeader().height() + 2 + self.horizontalHeader().height())  # +2 for border

    def set_style(self):
        """
        Apply custom stylesheet based on the theme to table, headers, scrollbars, etc.
        """
        self.setStyleSheet(f"""
            QHeaderView::section:last {{
                border-top-right-radius: 4px;
            }}
            QTableView {{
                background-color: {self.theme['Table']};
                color: {self.theme['HeaderText']};
                border: 1px solid {self.theme['Header']};
                border-radius: 4px;
                gridline-color: {self.theme['Header']};
            }}
            QHeaderView::section {{
                background-color: {self.theme['Header']};
                color: {self.theme['HeaderText']};
                padding: 5px;
                border: none;
            }}
            QHeaderView {{
                background-color: {self.theme['Table']};
                border-radius: 4px;
            }}
            QTableView::item {{
                padding: 5px;
                background-color: {self.theme['Table']};
            }}
            QTableCornerButton::section {{
                background-color: {self.theme['Header']};
                border-top-left-radius: 4px;
            }}
            QTableView::item:selected {{
                background-color: {self.theme['Table']};
                color: {self.theme['HeaderText']};
            }}
            QTableView QScrollBar {{
                background: {self.theme['Table']};
            }}
            QTableView QScrollBar:vertical {{
                background-color: {self.theme['Table']};
                width: 15px;
                margin: 15px 3px 15px 3px;
                border: 1px transparent {self.theme['Table']};
                border-radius: 4px;
            }}
            QTableView QScrollBar::handle:vertical {{
                background-color: {self.theme['Header']};
                min-height: 5px;
                border-radius: 4px;
            }}
            QTableView QScrollBar::sub-line:vertical {{
                margin: 3px 0px 3px 0px;
                border-image: url(:/qss_icons/rc/up_arrow_disabled.png);
                height: 10px;
                width: 10px;
            }}
            QTableView QScrollBar::add-line:vertical {{
                margin: 3px 0px 3px 0px;
                border-image: url(:/qss_icons/rc/down_arrow_disabled.png);
                height: 10px;
                width: 10px;
            }}
            QTableView QScrollBar::sub-line:vertical:hover,QScrollBar::sub-line:vertical:on {{
                border-image: url(:/qss_icons/rc/up_arrow.png);
            }}
            QTableView QScrollBar::add-line:vertical:hover,QScrollBar::add-line:vertical:on {{
                border-image: url(:/qss_icons/rc/down_arrow.png);
            }}
            QTableView QScrollBar::up-arrow:vertical, QScrollBar::down-arrow:vertical,
            QTableView QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {{
                background: none;
            }}
        """)

    def keyPressEvent(self, event):
        """
        Handle key presses for delete and enter actions when editable mode is enabled.
        """
        if self.is_editable:
            if event.key() == Qt.Key_Delete:
                selected_indexes = self.selectedIndexes()
                if selected_indexes:
                    row = selected_indexes[0].row()
                    self.model.removeRow(row)
            elif event.key() == Qt.Key_Return:
                self.model.insertRow(self.model.rowCount(None))
            else:
                super().keyPressEvent(event)

class TableModel(QtCore.QAbstractTableModel):
    """
    A custom table model that handles display, formatting, editing, and row manipulation.
    """

    def __init__(self, data, headers_name, vertical_count_format='number', row_limit=None):
        """
        Initialize the model with data and header names.

        :param data: 2D list representing rows and columns.
        :param headers_name: List of header titles.
        :param vertical_count_format: Format for vertical headers ('number', 'roman_numerals', 'alphabetic').
        :param row_limit: Optional row limit for custom formatting.
        """
        super().__init__()
        self._data = data
        self._headernames = headers_name
        self.vc_format = vertical_count_format
        self.row_limit = row_limit

    def data(self, index, role):
        """
        Return cell data for display and formatting.
        """
        if role == Qt.DisplayRole:
            if 0 <= index.row() < len(self._data) and 0 <= index.column() < len(self._headernames):
                return self._data[index.row()][index.column()]
            return '-'
        elif role == QtCore.Qt.TextAlignmentRole:
            return QtCore.Qt.AlignCenter
        elif role == Qt.ForegroundRole and self.row_limit:
            value = self._data[index.row()][index.column()]
            if value == "No":
                return QtGui.QBrush(QtCore.Qt.red)
            if value == "Yes":
                return QtGui.QBrush(QtCore.Qt.green)
        return None

    def rowCount(self, index):
        """Return number of rows in the table."""
        return len(self._data)

    def columnCount(self, index):
        """Return number of columns in the table."""
        return len(self._headernames)

    def flags(self, index):
        """Set editability flags for each cell."""
        if not index.isValid():
            return Qt.ItemIsEnabled
        return super().flags(index) | Qt.ItemIsEditable

    def headerData(self, section, orientation, role):
        """
        Return header label for given section based on format.
        """
        if role == Qt.DisplayRole:
            if orientation == Qt.Horizontal:
                return str(self._headernames[section])
            if orientation == Qt.Vertical:
                if self.vc_format == 'roman_numerals':
                    return number2roman_numerals(section + 1)
                elif self.vc_format == 'alphabetic':
                    return number2alphabetic(section + 1)
                else:
                    return str(section + 1)
        return None

    def setData(self, index, value, role):
        """
        Set value of a cell during editing.
        """
        if role == Qt.EditRole:
            if 0 <= index.row() < len(self._data) and 0 <= index.column() < len(self._headernames):
                self._data[index.row()][index.column()] = value
                self.dataChanged.emit(index, index)
                return True
        return False

    def removeRow(self, row, parent=QtCore.QModelIndex()):
        """
        Remove a row from the model.
        """
        if 0 <= row < len(self._data):
            self.beginRemoveRows(parent, row, row)
            del self._data[row]
            self.endRemoveRows()
            return True
        return False

    def insertRow(self, row, parent=QtCore.QModelIndex()):
        """
        Insert a new blank row at the specified position.
        """
        if 0 <= row <= len(self._data):
            self.beginInsertRows(parent, row, row)
            self._data.insert(row, [""] * len(self._headernames))
            self.endInsertRows()
            return True
        return False