import sys
import csv
import json
from PyQt5.QtWidgets import (QApplication, QMainWindow, QListWidget, QListWidgetItem, QHBoxLayout, QPushButton, QVBoxLayout, QWidget, 
                             QFileDialog, QDialog, QFormLayout, QLineEdit, QTextEdit, QDialogButtonBox, QMessageBox, QMenu, QCheckBox)
from PyQt5.QtGui import QPalette, QColor
from PyQt5.QtCore import Qt


class EditDialog(QDialog):
    def __init__(self, name='', prompt='', negative_prompt='', parent=None, font_size=14):
        super().__init__(parent)
        self.setWindowTitle('Edit Entry')

        self.layout = QFormLayout(self)

        self.name_edit = QLineEdit(name)
        self.prompt_edit = QTextEdit(prompt)
        self.negative_prompt_edit = QTextEdit(negative_prompt)

        self.layout.addRow('Name:', self.name_edit)
        self.layout.addRow('Prompt:', self.prompt_edit)
        self.layout.addRow('Negative Prompt:', self.negative_prompt_edit)

        self.button_box = QDialogButtonBox(QDialogButtonBox.Save | QDialogButtonBox.Cancel)
        self.button_box.accepted.connect(self.accept)
        self.button_box.rejected.connect(self.reject)

        self.layout.addWidget(self.button_box)

        self.apply_styles(font_size)

    def apply_styles(self, font_size=14):
        self.setStyleSheet(f"""
        QDialog {{
            background-color: #353535;
            color: white;
            font-size: {font_size}px;
        }}
        QLabel {{
            color: white;
            font-size: {font_size}px;
        }}
        QLineEdit {{
            background-color: #3A3A3A;
            color: white;
            border: 1px solid #555;
            border-radius: 5px;
            padding: 5px;
            font-size: {font_size}px;
        }}
        QCheckBox {{
            color: white;
            font-size: {font_size}px;
        }}
        QDialogButtonBox QPushButton {{
            background-color: #3A3A3A;
            color: white;
            border: 1px solid #555;
            border-radius: 5px;
            padding: 5px;
            font-size: {font_size}px;
        }}
        QDialogButtonBox QPushButton::hover {{
            background-color: #4A4A4A;
        }}
        QDialogButtonBox QPushButton::pressed {{
            background-color: #2A2A2A;
        }}
        QFormLayout {{
            font-size: {font_size}px;
        }}
        """)


    def get_data(self):
        return self.name_edit.text(), self.prompt_edit.toPlainText(), self.negative_prompt_edit.toPlainText()


class SettingsDialog(QDialog):
    def __init__(self, settings, parent=None):
        super().__init__(parent)
        self.setWindowTitle('Settings')

        self.layout = QFormLayout(self)

        self.toggle_visibility_checkbox = QCheckBox('Show Full Prompt Info')
        self.toggle_visibility_checkbox.setChecked(settings.get('show_full_prompt_info', True))

        self.font_size_edit = QLineEdit()
        self.font_size_edit.setText(str(settings.get('font_size', 14)))

        self.layout.addRow(self.toggle_visibility_checkbox)
        self.layout.addRow('Font Size:', self.font_size_edit)

        self.button_box = QDialogButtonBox(QDialogButtonBox.Save | QDialogButtonBox.Cancel)
        self.button_box.accepted.connect(self.save_settings)
        self.button_box.rejected.connect(self.reject)

        self.layout.addWidget(self.button_box)

        self.settings = settings

        self.apply_styles(settings.get('font_size', 14))

    def apply_styles(self, font_size=14):
        self.setStyleSheet(f"""
        QDialog {{
            background-color: #353535;
            color: white;
            font-size: {font_size}px;
        }}
        QLabel {{
            color: white;
        }}
        QLineEdit {{
            background-color: #3A3A3A;
            color: white;
            border: 1px solid #555;
            border-radius: 5px;
            padding: 5px;
            font-size: {font_size}px;
        }}
        QCheckBox {{
            color: white;
            font-size: {font_size}px;
        }}
        QDialogButtonBox QPushButton {{
            background-color: #3A3A3A;
            color: white;
            border: 1px solid #555;
            border-radius: 5px;
            padding: 5px;
            font-size: {font_size}px;
        }}
        QDialogButtonBox QPushButton::hover {{
            background-color: #4A4A4A;
        }}
        QDialogButtonBox QPushButton::pressed {{
            background-color: #2A2A2A;
        }}
        """)

    def save_settings(self):
        self.settings['show_full_prompt_info'] = self.toggle_visibility_checkbox.isChecked()
        self.settings['font_size'] = int(self.font_size_edit.text())
        with open('settings.json', 'w') as file:
            json.dump(self.settings, file)
        self.accept()


class StyleOrganizer(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('Stable Diffusion Style Organizer')
        self.setGeometry(100, 100, 600, 400)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout(self.central_widget)

        self.list_widget = QListWidget()
        self.list_widget.setDragDropMode(QListWidget.InternalMove)
        self.list_widget.itemDoubleClicked.connect(self.edit_item)
        self.list_widget.setContextMenuPolicy(Qt.CustomContextMenu)
        self.list_widget.customContextMenuRequested.connect(self.show_context_menu)

        self.load_button = QPushButton('Load CSV')
        self.load_button.clicked.connect(self.load_csv)

        self.save_button = QPushButton('Save CSV')
        self.save_button.clicked.connect(self.save_csv)

        self.add_button = QPushButton('Add Style')
        self.add_button.clicked.connect(self.add_item)

        self.delete_button = QPushButton('Delete Style')
        self.delete_button.clicked.connect(self.delete_item)

        self.settings_button = QPushButton('Settings')
        self.settings_button.clicked.connect(self.open_settings_dialog)

        # Create a horizontal layout for the add, delete, and settings buttons
        self.button_layout = QHBoxLayout()
        self.button_layout.addWidget(self.add_button)
        self.button_layout.addWidget(self.delete_button)
        self.button_layout.addWidget(self.settings_button)

        self.layout.addWidget(self.list_widget)
        self.layout.addLayout(self.button_layout)  # Add the horizontal layout to the main layout
        self.layout.addWidget(self.load_button)
        self.layout.addWidget(self.save_button)

        self.load_settings()
        self.apply_dark_theme(self.settings.get('font_size', 14))

    def apply_dark_theme(self, font_size=14):
        dark_palette = QPalette()
        dark_palette.setColor(QPalette.Window, QColor(53, 53, 53))
        dark_palette.setColor(QPalette.WindowText, Qt.white)
        dark_palette.setColor(QPalette.Base, QColor(35, 35, 35))
        dark_palette.setColor(QPalette.AlternateBase, QColor(53, 53, 53))
        dark_palette.setColor(QPalette.ToolTipBase, Qt.white)
        dark_palette.setColor(QPalette.ToolTipText, Qt.white)
        dark_palette.setColor(QPalette.Text, Qt.white)
        dark_palette.setColor(QPalette.Button, QColor(53, 53, 53))
        dark_palette.setColor(QPalette.ButtonText, Qt.white)
        dark_palette.setColor(QPalette.BrightText, Qt.red)
        dark_palette.setColor(QPalette.Link, QColor(42, 130, 218))
        dark_palette.setColor(QPalette.Highlight, QColor(42, 130, 218))
        dark_palette.setColor(QPalette.HighlightedText, Qt.black)

        QApplication.setPalette(dark_palette)

        # Apply styles to buttons for a better look
        button_style = f"""
        QPushButton {{
            background-color: #3A3A3A;
            color: white;
            border: 1px solid #555;
            border-radius: 5px;
            padding: 5px;
            font-size: {font_size}px;
        }}
        QPushButton::hover {{
            background-color: #4A4A4A;
        }}
        QPushButton::pressed {{
            background-color: #2A2A2A;
        }}
        """

        self.load_button.setStyleSheet(button_style)
        self.save_button.setStyleSheet(button_style)
        self.add_button.setStyleSheet(button_style)
        self.delete_button.setStyleSheet(button_style)
        self.settings_button.setStyleSheet(button_style)

        # Apply styles to the edit dialog buttons and main dialog
        dialog_button_style = f"""
        QDialogButtonBox QPushButton {{
            background-color: #3A3A3A;
            color: white;
            border: 1px solid #555;
            border-radius: 5px;
            padding: 5px;
            font-size: {font_size}px;
        }}
        QDialogButtonBox QPushButton::hover {{
            background-color: #4A4A4A;
        }}
        QDialogButtonBox QPushButton::pressed {{
            background-color: #2A2A2A;
        }}
        """
        dialog_style = f"""
        QDialog {{
            background-color: #353535;
            color: white;
            font-size: {font_size}px;
        }}
        QLabel {{
            color: white;
        }}
        QLineEdit, QTextEdit {{
            background-color: #3A3A3A;
            color: white;
            border: 1px solid #555;
            border-radius: 5px;
            padding: 5px;
            font-size: {font_size}px;
        }}
        """
        self.central_widget.setStyleSheet(f"font-size: {font_size}px;")

        for button in self.findChildren(QPushButton):
            button.setStyleSheet(button_style)

        for dialog in self.findChildren(QDialog):
            dialog.setStyleSheet(dialog_style)
            dialog.findChild(QDialogButtonBox).setStyleSheet(dialog_button_style)

    def load_settings(self):
        try:
            with open('settings.json', 'r') as file:
                self.settings = json.load(file)
        except FileNotFoundError:
            self.settings = {'show_full_prompt_info': True, 'font_size': 14}

        self.toggle_visibility()

    def load_csv(self):
        file_name, _ = QFileDialog.getOpenFileName(self, 'Open CSV File', '', 'CSV Files (*.csv)')
        if file_name:
            with open(file_name, newline='') as csvfile:
                csvreader = csv.reader(csvfile)
                next(csvreader)  # Skip the header line
                self.list_widget.clear()
                for row in csvreader:
                    item = QListWidgetItem(f'{row[0]}: {row[1]} | Negative Prompt: {row[2]}' if self.settings.get('show_full_prompt_info', True) else row[0])
                    item.setData(32, row)
                    self.list_widget.addItem(item)

    def save_csv(self):
        file_name, _ = QFileDialog.getSaveFileName(self, 'Save CSV File', '', 'CSV Files (*.csv)')
        if file_name:
            with open(file_name, 'w', newline='') as csvfile:
                csvwriter = csv.writer(csvfile)
                csvwriter.writerow(['name', 'prompt', 'negative_prompt'])  # Write the header line
                for index in range(self.list_widget.count()):
                    item = self.list_widget.item(index)
                    csvwriter.writerow(item.data(32))

    def edit_item(self, item):
        data = item.data(32)
        dialog = EditDialog(data[0], data[1], data[2], self, self.settings.get('font_size', 14))
        if dialog.exec_():
            name, prompt, negative_prompt = dialog.get_data()
            item.setText(f'{name}: {prompt} | Negative Prompt: {negative_prompt}' if self.settings.get('show_full_prompt_info', True) else name)
            item.setData(32, [name, prompt, negative_prompt])

    def add_item(self):
        dialog = EditDialog(parent=self, font_size=self.settings.get('font_size', 14))
        if dialog.exec_():
            name, prompt, negative_prompt = dialog.get_data()
            item = QListWidgetItem(f'{name}: {prompt} | Negative Prompt: {negative_prompt}' if self.settings.get('show_full_prompt_info', True) else name)
            item.setData(32, [name, prompt, negative_prompt])
            self.list_widget.addItem(item)

    def show_message_box(self, title, text, buttons=QMessageBox.Yes | QMessageBox.No):
        message_box = QMessageBox(self)
        message_box.setWindowTitle(title)
        message_box.setText(text)
        message_box.setStandardButtons(buttons)
        message_box.setStyleSheet(f"""
        QMessageBox {{
            background-color: #353535;
            color: white;
            font-size: {self.settings.get('font_size', 14)}px;
        }}
        QMessageBox QPushButton {{
            background-color: #3A3A3A;
            color: white;
            border: 1px solid #555;
            border-radius: 5px;
            padding: 5px;
        }}
        QMessageBox QPushButton::hover {{
            background-color: #4A4A4A;
        }}
        QMessageBox QPushButton::pressed {{
            background-color: #2A2A2A;
        }}
        """)
        return message_box.exec_()

    def delete_item(self):
        selected_item = self.list_widget.currentItem()
        if selected_item:
            reply = self.show_message_box('Delete Style', 'Are you sure you want to delete this style?', QMessageBox.Yes | QMessageBox.No)
            if reply == QMessageBox.Yes:
                self.list_widget.takeItem(self.list_widget.row(selected_item))

    def show_context_menu(self, position):
        context_menu = QMenu(self)

        add_above_action = context_menu.addAction("Add New Style Above")
        add_below_action = context_menu.addAction("Add New Style Below")
        add_spacer_above_action = context_menu.addAction("Add Spacer Above")
        add_spacer_below_action = context_menu.addAction("Add Spacer Below")
        edit_action = context_menu.addAction("Edit")
        delete_action = context_menu.addAction("Delete")

        action = context_menu.exec_(self.list_widget.mapToGlobal(position))

        selected_item = self.list_widget.itemAt(position)

        if action == add_above_action:
            self.add_item_at(selected_item, above=True)
        elif action == add_below_action:
            self.add_item_at(selected_item, above=False)
        elif action == add_spacer_above_action:
            self.add_spacer_at(selected_item, above=True)
        elif action == add_spacer_below_action:
            self.add_spacer_at(selected_item, above=False)
        elif action == edit_action:
            if selected_item:
                self.edit_item(selected_item)
        elif action == delete_action:
            if selected_item:
                self.delete_item_at(selected_item)

    def add_item_at(self, selected_item, above):
        dialog = EditDialog(parent=self, font_size=self.settings.get('font_size', 14))
        if dialog.exec_():
            name, prompt, negative_prompt = dialog.get_data()
            item = QListWidgetItem(f'{name}: {prompt} | Negative Prompt: {negative_prompt}' if self.settings.get('show_full_prompt_info', True) else name)
            item.setData(32, [name, prompt, negative_prompt])
            if selected_item:
                row = self.list_widget.row(selected_item)
                if above:
                    self.list_widget.insertItem(row, item)
                else:
                    self.list_widget.insertItem(row + 1, item)
            else:
                self.list_widget.addItem(item)

    def add_spacer_at(self, selected_item, above):
        item = QListWidgetItem('----------')
        item.setData(32, ['----------', '', ''])
        if selected_item:
            row = self.list_widget.row(selected_item)
            if above:
                self.list_widget.insertItem(row, item)
            else:
                self.list_widget.insertItem(row + 1, item)
        else:
            self.list_widget.addItem(item)

    def delete_item_at(self, selected_item):
        reply = self.show_message_box('Delete Style', 'Are you sure you want to delete this style?', QMessageBox.Yes | QMessageBox.No)
        if reply == QMessageBox.Yes:
            self.list_widget.takeItem(self.list_widget.row(selected_item))

    def open_settings_dialog(self):
        dialog = SettingsDialog(self.settings, self)
        dialog.apply_styles(self.settings.get('font_size', 14))
        if dialog.exec_():
            self.toggle_visibility()
            self.apply_dark_theme(self.settings.get('font_size', 14))

    def toggle_visibility(self):
        for index in range(self.list_widget.count()):
            item = self.list_widget.item(index)
            data = item.data(32)
            if self.settings.get('show_full_prompt_info', True):
                item.setText(f'{data[0]}: {data[1]} | Negative Prompt: {data[2]}')
            else:
                item.setText(data[0])

if __name__ == '__main__':
    app = QApplication(sys.argv)
    try:
        with open('settings.json', 'r') as file:
            settings = json.load(file)
    except FileNotFoundError:
        settings = {'show_full_prompt_info': True, 'font_size': 14}
    font_size = settings.get('font_size', 14)
    app.setStyleSheet(f"""
        * {{
            font-size: {font_size}px;
        }}
    """)
    window = StyleOrganizer()
    window.show()
    sys.exit(app.exec_())
