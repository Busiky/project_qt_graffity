# -*- coding: utf-8 -*-

import shutil
import sqlite3
import sys
import random

from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, \
    QMainWindow, qApp, QTableWidgetItem, QDialog, QFileDialog, QInputDialog, QCheckBox
from PyQt5.QtGui import QFont, QPixmap
from ui_table_window import Ui_TableWindow
from ui_form_window import Ui_FormWindow
from ui_dialog import Ui_Dialog
from ui_add_picture import Ui_AddPic
from ui_select_dialog import Ui_SelectDialog
from ui_update_dialog import Ui_UpDialog


class Window(QWidget):
    def __init__(self):
        super().__init__()
        self.setup_ui()

    def setup_ui(self):
        self.setGeometry(500, 200, 800, 600)
        self.setWindowTitle('Street Art')

        layout = QVBoxLayout()
        hlayout = QHBoxLayout()

        label = QLabel()
        font = QFont()
        font.setPointSize(24)
        label.setFont(font)
        label.setText('Modern Street Art')
        label.setAlignment(Qt.AlignHCenter)

        with sqlite3.connect('graffity.db') as con:
            pictures = con.execute('SELECT filename FROM files').fetchall()

        label_1 = QLabel()
        pic = random.choice(pictures)[0]
        pixmap = QPixmap(f'data\{pic}')
        label_1.setAlignment(Qt.AlignTop)
        label_1.setAlignment(Qt.AlignHCenter)
        label_1.setPixmap(pixmap)

        layout.addWidget(label)
        layout.addWidget(label_1)

        btn = QPushButton('Form')
        font_1 = QFont()
        font_1.setPointSize(14)
        btn.setFont(font_1)
        btn.clicked.connect(self.con_form)
        hlayout.addWidget(btn)
        btn_1 = QPushButton('Table')
        btn_1.setFont(font_1)
        btn_1.clicked.connect(self.con_table)
        hlayout.addWidget(btn_1)

        layout.addLayout(hlayout)

        self.setLayout(layout)

    def con_form(self):
        form_view = Form_Window(self)
        form_view.show()
        self.hide()

    def con_table(self):
        table_view = Table_Window(self)
        table_view.show()
        self.hide()


class Table_Window(QMainWindow, Ui_TableWindow):
    def __init__(self, *args):
        super().__init__(*args)
        self.setupUi(self)

        self.table = self.tableWidget

        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels([
            'id', 'author', 'work_name', 'city', 'year'
        ])

        con = sqlite3.connect('graffity.db')

        for row_number, row in enumerate(con.execute('SELECT * FROM main_table').fetchall()):
            self.table.insertRow(row_number)
            for col_number, col in enumerate(row):
                self.table.setItem(row_number, col_number, QTableWidgetItem(str(col)))

        con.close()

        self.gridLayout_2.addWidget(self.table, 0, 0, 1, 3)

        self.actionGo_to_Form.triggered.connect(self.go_to_form)
        self.pushButton.clicked.connect(self.go_to_form)

        self.actionAdd_Item.triggered.connect(self.add_item)
        self.pushButton_2.clicked.connect(self.add_item)

        self.actionRemove_Item.triggered.connect(self.remove_item)
        self.pushButton_3.clicked.connect(self.remove_item)

        self.actionSelect_Items.triggered.connect(self.select_items)
        self.pushButton_4.clicked.connect(self.select_items)

        self.actionUpdate_Item.triggered.connect(self.update_item)
        self.pushButton_5.clicked.connect(self.update_item)

        self.pushButton_6.clicked.connect(self.add_picture)

        self.actionExit.triggered.connect(qApp.quit)

    def go_to_form(self):
        form_view = Form_Window(self)
        form_view.show()
        self.hide()

    def add_item(self):
        dialog = Dialog(self)
        if dialog.exec():
            with sqlite3.connect('graffity.db') as con:
                cur = con.cursor()
                data = [
                    dialog.lineEdit.text(),
                    dialog.lineEdit_2.text(),
                    dialog.lineEdit_3.text(),
                    str(dialog.spinBox.value())
                ]

                cur.execute(f'INSERT INTO main_table VALUES (NULL, ?, ?, ?, ?)', data)

                con.commit()
            self.update_table()

            with sqlite3.connect('graffity.db') as con:
                cur = con.cursor()
                pic_id = max([x[0] for x in cur.execute('SELECT id FROM main_table').fetchall()])
                count_pictures = len(
                    cur.execute(f'SELECT picture_id FROM files WHERE picture_id = {pic_id}').fetchall())

                filename = dialog.file
                format = filename.split('.')[-1]
                myfilename = f'{pic_id}_{count_pictures}.{format}'
                shutil.copyfile(filename, f'data\{myfilename}')

                cur.execute(f'INSERT INTO files VALUES (NULL, "{myfilename}", {pic_id})')
                comment = dialog.textEdit.toPlainText()
                if comment:
                    cur.execute(f'INSERT INTO comments VALUES (NULL, "{comment}", {pic_id})')

                con.commit()

    def add_picture(self):
        AddPictureDialog().exec()

    def update_table(self):
        self.table.clear()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels([
            'id', 'author', 'work_name', 'city', 'year'
        ])

        with sqlite3.connect('graffity.db') as con:
            for row_number, row in enumerate(con.execute('SELECT * FROM main_table').fetchall()):
                self.table.insertRow(row_number)
                for col_number, col in enumerate(row):
                    self.table.setItem(row_number, col_number, QTableWidgetItem(str(col)))

    def remove_item(self):
        pic_id, ok = QInputDialog.getInt(self, 'Введите id картинки', 'Выбор id:', 1)
        if ok:
            with sqlite3.connect('graffity.db') as con:
                con.execute(f'DELETE FROM main_table WHERE id = {pic_id}')
                con.execute(f'DELETE FROM files WHERE picture_id = {pic_id}')
                con.execute(f'DELETE FROM comments WHERE picture_id = {pic_id}')

        self.update_table()

    def select_items(self):
        SelectionDialog(self).exec()

    def update_item(self):
        UpdateDialog(self).exec()


class UpdateDialog(QDialog, Ui_UpDialog):
    def __init__(self, *args):
        super().__init__(*args)
        self.setupUi(self)

        self.buttonBox.button(QtWidgets.QDialogButtonBox.Ok).clicked.connect(self.run_update)
        self.buttonBox.button(QtWidgets.QDialogButtonBox.Cancel).clicked.connect(self.close)

        self.pic_id, ok = QInputDialog.getInt(self, 'Введите id картинки', 'Выбор id:', 1)

        if ok:
            with sqlite3.connect('graffity.db') as con:
                cur = con.cursor()
                id, author, work_name, city, year = cur.execute(
                    f'SELECT * FROM main_table WHERE id = {self.pic_id}').fetchall()[0]
                filename = cur.execute(f'SELECT filename FROM files WHERE picture_id = {self.pic_id}').fetchall()[0][0]
                list_comment = cur.execute(f'SELECT comment FROM comments WHERE picture_id = {self.pic_id}').fetchall()
                if list_comment:
                    comment = list_comment[0][0]
                else:
                    comment = ''

                self.lcdNumber.display(id)
                self.lineEdit.setText(author)
                self.lineEdit_2.setText(work_name)
                self.lineEdit_3.setText(city)
                self.spinBox.setValue(year)
                self.lineEdit_4.setText(filename)
                self.textEdit.setText(comment)

    def run_update(self):
        with sqlite3.connect('graffity.db') as con:
            cur = con.cursor()
            cur.execute(f'UPDATE main_table SET author = "{self.lineEdit.text()}" WHERE id = {self.pic_id}')
            cur.execute(f'UPDATE main_table SET work_name = "{self.lineEdit_2.text()}" WHERE id = {self.pic_id}')
            cur.execute(f'UPDATE main_table SET city = "{self.lineEdit_3.text()}" WHERE id = {self.pic_id}')
            cur.execute(f'UPDATE main_table SET year = "{self.spinBox.value()}" WHERE id = {self.pic_id}')
            file_number = min([
                int(x[0]) for x in cur.execute(f'SELECT * FROM files WHERE picture_id = {self.pic_id}').fetchall()
            ])
            cur.execute(
                f'UPDATE files SET filename = "{self.lineEdit_4.text()}" WHERE picture_id = {self.pic_id} and id = {file_number}'
            )
            cur.execute(
                f'UPDATE comments SET comment = "{self.textEdit.toPlainText()}" WHERE picture_id = {self.pic_id}')
            self.accept()


class Form_Window(QMainWindow, Ui_FormWindow):
    def __init__(self, *args):
        super().__init__(*args)
        self.setupUi(self)

        self.i = 0
        with sqlite3.connect('graffity.db') as con:
            self.list_of_id = sorted([x[0] for x in con.execute(f'SELECT id FROM files').fetchall()])
            self.id = self.list_of_id[self.i]

        self.pushButton.clicked.connect(self.previous)
        self.pushButton_2.clicked.connect(self.next)

        self.actionGo_to_Table.triggered.connect(self.go_to_table)
        self.actionExit.triggered.connect(qApp.quit)

        self.form_update()

    def form_update(self):
        with sqlite3.connect('graffity.db') as con:
            cur = con.cursor()
            pictures = cur.execute(f'SELECT filename, picture_id FROM files').fetchall()
            id_from_main_table = pictures[self.i][1]
            data = cur.execute(f'SELECT * FROM main_table WHERE id = {id_from_main_table}').fetchall()

        self.lcdNumber.display(str(id_from_main_table))
        pixmap = QPixmap(f'data\{pictures[self.i][0]}')
        self.label_11.setAlignment(Qt.AlignHCenter)
        self.label_11.setPixmap(pixmap)

        self.label_10.setText(data[0][1])
        self.label_2.setText(data[0][2])
        self.label_6.setText(data[0][3])
        self.label_4.setText(str(data[0][4]))

    def go_to_table(self):
        table_view = Table_Window(self)
        table_view.show()
        self.hide()

    def previous(self):
        self.i -= 1
        if self.i < 0:
            self.i = len(self.list_of_id) - 1
        self.form_update()

    def next(self):
        self.i += 1
        if self.i >= len(self.list_of_id):
            self.i = 0
        self.form_update()


class Dialog(QDialog, Ui_Dialog):
    def __init__(self, *args):
        super().__init__(*args)
        self.setupUi(self)

        self.buttonBox.button(QtWidgets.QDialogButtonBox.Ok).clicked.connect(self.accept)
        self.buttonBox.button(QtWidgets.QDialogButtonBox.Cancel).clicked.connect(self.close)

        self.pushButton.clicked.connect(self.upload_file)

    def upload_file(self):
        self.file = QFileDialog.getOpenFileName(self, 'Загрузка картинки')[0]


class AddPictureDialog(QDialog, Ui_AddPic):
    def __init__(self, *args):
        super().__init__(*args)
        self.setupUi(self)

        self.pushButton.clicked.connect(self.upload_file)
        self.buttonBox.button(QtWidgets.QDialogButtonBox.Ok).clicked.connect(self.accept)
        self.buttonBox.button(QtWidgets.QDialogButtonBox.Cancel).clicked.connect(self.close)

        self.pic_id, ok = QInputDialog.getInt(self, 'Введите id картинки', 'Выбор id:', 1)
        if ok:
            with sqlite3.connect('graffity.db') as con:
                cur = con.cursor()

                comment = self.textEdit.toPlainText()
                if comment != 'Введите комментарий здесь' and comment != '':
                    cur.execute(f'INSERT INTO comments VALUES (NULL, "{comment}", {self.pic_id})')

                con.commit()

                self.label_9.setText(str(self.pic_id))
                n, author, work, *rest = cur.execute(f'SELECT * FROM main_table WHERE id = {self.pic_id}').fetchall()[0]
                self.label_3.setText(author)
                self.label_5.setText(work)
                pic = sorted(
                    cur.execute(f'SELECT filename FROM files WHERE picture_id = {self.pic_id}').fetchall()
                )[0][0]
                pixmap = QPixmap(f'data\{pic}')
                self.label_7.setPixmap(pixmap)

    def upload_file(self):
        self.filename = QFileDialog.getOpenFileName(self, 'Загрузка картинки')[0]
        if self.filename:
            self.label_8.setText(self.filename)

        with sqlite3.connect('graffity.db') as con:
            cur = con.cursor()
            count_pictures = len(
                cur.execute(f'SELECT picture_id FROM files WHERE picture_id = {self.pic_id}').fetchall()
            )

            format = self.filename.split('.')[-1]
            myfilename = f'{self.pic_id}_{count_pictures}.{format}'
            shutil.copyfile(self.filename, f'data\{myfilename}')

            cur.execute(f'INSERT INTO files VALUES (NULL, "{myfilename}", {self.pic_id})')


class SelectionDialog(QDialog, Ui_SelectDialog):
    def __init__(self, *args):
        super().__init__(*args)
        self.setupUi(self)

        self.pushButton.clicked.connect(self.run)
        self.pushButton_2.clicked.connect(self.clean)
        self.pushButton_3.clicked.connect(self.close)

    def run(self):
        buttons = {
            self.checkBox: 'id', self.checkBox_2: 'author',
            self.checkBox_3: 'work_name', self.checkBox_4: 'city',
            self.checkBox_5: 'year'
        }

        checked_buttons = filter(QCheckBox.isChecked, buttons.keys())

        self.list_to_show = [buttons[button] for button in checked_buttons]

        radio_buttons = {
            self.radioButton: 'id', self.radioButton_2: 'author',
            self.radioButton_3: 'work_name', self.radioButton_5: 'city',
            self.radioButton_6: 'year'
        }

        checked_radio = list(filter(lambda x: x.isChecked(), radio_buttons.keys()))

        self.order = radio_buttons[checked_radio[0]]

        layout = self.formLayout
        table = self.tableWidget

        col = len(self.list_to_show)
        table.setColumnCount(col)
        table.setHorizontalHeaderLabels(self.list_to_show)

        with sqlite3.connect('graffity.db') as con:
            selection_fields = ', '.join(self.list_to_show)

            for row_number, row in enumerate(
                    con.execute(
                        f'SELECT {selection_fields} FROM main_table ORDER by {self.order}').fetchall()
            ):
                table.insertRow(row_number)
                for col_number, col in enumerate(row):
                    table.setItem(row_number, col_number, QTableWidgetItem(str(col)))

        layout.addWidget(table)
        self.setLayout(layout)

    def clean(self):
        layout = self.formLayout
        table = self.tableWidget
        table.clear()

        layout.addWidget(table)
        self.setLayout(layout)

        self.checkBox.setChecked(True)
        self.checkBox_2.setChecked(False)
        self.checkBox_3.setChecked(False)
        self.checkBox_5.setChecked(False)
        self.checkBox_4.setChecked(False)

        self.radioButton.setChecked(True)
        self.radioButton_2.setChecked(False)
        self.radioButton_3.setChecked(False)
        self.radioButton_5.setChecked(False)
        self.radioButton_6.setChecked(False)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    wnd = Window()
    wnd.show()
    exit(app.exec())
