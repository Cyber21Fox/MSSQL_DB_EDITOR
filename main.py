
import sys
import pyodbc
from design import Ui_MainWindow
from enter import Ui_Enter
from user_panel import Ui_Form
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QMessageBox, QComboBox, QTableWidgetItem
сursor = None

'''Класс соединения и вызова окна входа'''
class Connection(QtWidgets.QWidget):
    def __init__(self):
        super(Connection, self).__init__()
        self.en = Ui_Enter()
        self.en.setupUi(self)
        self.en.lineEdit_4.setEchoMode(QtWidgets.QLineEdit.Password)
        self.en.pushButton.clicked.connect(self.connect)
        self.en.pushButton_2.clicked.connect(self.exit)

    def exit(self):
        self.close()
    def connect(self):
        try:
            global cursor
            self.en.server = self.en.lineEdit.text()
            self.en.database = self.en.lineEdit_2.text()
            self.en.username = self.en.lineEdit_3.text()
            self.en.password = self.en.lineEdit_4.text()
            self.cn = pyodbc.connect(
                "Driver={SQL Server Native Client 11.0};"
                "Server=" + self.en.server +
                ";Database=" + self.en.database +
                ";UID="+self.en.username+
                ";PWD="+self.en.password+";")
            cursor = self.cn.cursor()
            self.Privacy()
        except:
            self.error = QMessageBox.question(
                self, "Message", "Ошибка подключения к базе данных.\nПроверьте корректность введеных данных.",
                QMessageBox.Ok)

    def Privacy(self):
        try:
            self.close()
            cursor.execute("IF IS_MEMBER ('db_owner') = 1 SELECT 'True' AS [Результат] "
                           "ELSE SELECT 'False' AS [Результат]")
            row = cursor.fetchone()
            print(row[0])
            if str(row[0]) == "True":
                self.w1 = Admin_panel()
                self.w1.show()
            else:
                self.w2 = User_panel()
                self.w2.show()
            self.reply = QMessageBox.question(
                self, "Message", "Подключение к базе данных " + self.en.database + " прошло успешно!",
                QMessageBox.Ok)         #Вывод успешного входa
        except:
            self.error = QMessageBox.question(
                self, "Message", "Ошибка подключения к базе данных.\nПроверьте корректность введеных данных.",
                QMessageBox.Ok)
            self.close()
'''Класс отвечающий за окно Администратора'''
class Admin_panel(QtWidgets.QMainWindow):           #Окно администратора
    def __init__(self):
        super(Admin_panel, self).__init__()
        self.ai = Ui_MainWindow()
        self.ai.setupUi(self)
        global cursor
        self.show_database()
        self.ai.pushBut.clicked.connect(self.AddData_Klient)
        self.ai.pushButton_3.clicked.connect(self.AddData_Klient_pokupatel)
        self.ai.pushButton_12.clicked.connect(self.AddData_Klient_prodavec)
        self.ai.pushButton_16.clicked.connect(self.AddData_Object)
        self.ai.pushButton_26.clicked.connect(self.AddData_Kind_Object)
        self.ai.pushButton_30.clicked.connect(self.AddData_Trebovaniya)
        self.ai.pushButton_34.clicked.connect(self.AddData_Place)
        self.ai.pushButton_42.clicked.connect(self.AddData_Agent)
        self.ai.pushButton_38.clicked.connect(self.AddData_Sdelka)
        self.ai.pushButton_46.clicked.connect(self.AddData_Office)

        self.ai.tableWidget_0.cellClicked.connect(self.CellClick_Klient)
        self.ai.tableWidget_1.cellClicked.connect(self.CellClick_Klient_pokupatel)
        self.ai.tableWidget_2.cellClicked.connect(self.CellClick_Klient_prodavec)
        self.ai.tableWidget_3.cellClicked.connect(self.CellClick_Object)
        self.ai.tableWidget_4.cellClicked.connect(self.CellClick_Kind_Object)
        self.ai.tableWidget_5.cellClicked.connect(self.CellClick_Trebovaniya)
        self.ai.tableWidget_6.cellClicked.connect(self.CellClick_Place)
        self.ai.tableWidget_7.cellClicked.connect(self.CellClick_Agent)
        self.ai.tableWidget_8.cellClicked.connect(self.CellClick_Sdelka)
        self.ai.tableWidget_9.cellClicked.connect(self.CellClick_Office)

        self.ai.pushBut2.clicked.connect(self.Update_Klient)
        self.ai.pushButton_5.clicked.connect(self.Update_Klient_pokupatel)
        self.ai.pushButton_14.clicked.connect(self.Update_Klient_prodavec)
        self.ai.pushButton_17.clicked.connect(self.Update_Object)
        self.ai.pushButton_27.clicked.connect(self.Update_Kind_Object)
        self.ai.pushButton_31.clicked.connect(self.Update_Trebovaniya)
        self.ai.pushButton_35.clicked.connect(self.Update_Place)
        self.ai.pushButton_44.clicked.connect(self.Update_Agent)
        self.ai.pushButton_39.clicked.connect(self.Update_Sdelka)
        self.ai.pushButton_47.clicked.connect(self.Update_Office)

        self.ai.pushBut1.clicked.connect(self.Delete_Klient)
        self.ai.pushButton_22.clicked.connect(self.Delete_Klient_pokupatel)
        self.ai.pushButton_23.clicked.connect(self.Delete_Klient_prodavec)
        self.ai.pushButton_24.clicked.connect(self.Delete_Object)
        self.ai.pushButton_25.clicked.connect(self.Delete_Kind_Object)
        self.ai.pushButton_28.clicked.connect(self.Delete_Trebovaniya)
        self.ai.pushButton_32.clicked.connect(self.Delete_Place)
        self.ai.pushButton_45.clicked.connect(self.Delete_Agent)
        self.ai.pushButton_36.clicked.connect(self.Delete_Sdelka)
        self.ai.pushButton_40.clicked.connect(self.Delete_Office)

    def update_database(self):
        try:
            self.create_Klient()
            self.create_Klient_pokupatel()
            self.create_Klient_prodavec()
            self.create_Object()
            self.create_Kind_Object()
            self.create_Trebovaniya()
            self.create_Place()
            self.create_Agent()
            self.create_Sdelka()
            self.create_Office()
        except:
            self.error = QMessageBox.question(
                self, "Message", "Ошибка загрузки базы данных.",
                QMessageBox.Ok)

    def show_database(self):  # вывод базы данных
        try:
            self.count_string = "select count(*) from"
            self.count_column = "select count(*) from information_schema.columns where table_name='"
            self.add_string = "select * from "
            self.name_columns="SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE table_name='"
            self.table = ["КЛИЕНТ","КЛИЕНТ_ПОКУПАТЕЛЬ", "КЛИЕНТ_ПРОДАВЕЦ", "ОБЪЕКТ", "ВИД_ОБЪЕКТА",
                          "ТРЕБОВАНИЯ_К_ОБЪЕКТУ", "РАЙОН","СОТРУДНИК","СДЕЛКА","ОФИС"]
            self.dict_name=[]
            self.update_database()
        except:
            self.error = QMessageBox.question(
                self, "Message", "Ошибка загрузки базы данных.",
                QMessageBox.Ok)

    ''' Заполнение таблиц '''
    def create_Klient(self):

        cursor.execute(self.count_string + " " + self.table[0])  # кол строк
        self.st = cursor.fetchone()
        self.ai.tableWidget_0.setRowCount(self.st[0])

        cursor.execute(self.count_column + self.table[0] + "'")  # кол столбцов
        self.col = cursor.fetchone()
        self.ai.tableWidget_0.setColumnCount(self.col[0])

        cursor.execute(self.name_columns + self.table[0] + "'")
        self.name_col = cursor.fetchone()
        while self.name_col:                                    #названия столбцов
            self.dict_name.append(self.name_col[0])
            self.name_col = cursor.fetchone()
        self.ai.tableWidget_0.setHorizontalHeaderLabels(self.dict_name)
        print(self.table[0])
        print(self.dict_name)
        self.dict_name.clear()
        for j in range(self.col[0]):
            cursor.execute(self.add_string + self.table[0])
            for i in range(self.st[0]):
                self.info_str = cursor.fetchone() # If info_str != NUll: info_str = 0
                self.ai.tableWidget_0.setItem(i, j, QTableWidgetItem(str(self.info_str[j])))
        self.ai.tableWidget_0.resizeColumnsToContents()

    def create_Klient_pokupatel(self):
        cursor.execute(self.count_string + " " + self.table[1])  # кол строк
        self.st = cursor.fetchone()
        self.ai.tableWidget_1.setRowCount(self.st[0])

        cursor.execute(self.count_column + self.table[1] + "'")  # кол столбцов
        self.col = cursor.fetchone()
        self.ai.tableWidget_1.setColumnCount(self.col[0])

        cursor.execute(self.name_columns + self.table[1] + "'")
        self.name_col = cursor.fetchone()
        while self.name_col:
            self.dict_name.append(self.name_col[0])
            self.name_col = cursor.fetchone()
        self.ai.tableWidget_1.setHorizontalHeaderLabels(self.dict_name)
        print(self.table[1])
        print(self.dict_name)
        self.dict_name.clear()
        for j in range(self.col[0]):
            cursor.execute(self.add_string + self.table[1])
            for i in range(self.st[0]):
                self.info_str = cursor.fetchone()
                self.ai.tableWidget_1.setItem(i, j, QTableWidgetItem(str(self.info_str[j])))
        self.ai.tableWidget_1.resizeColumnsToContents()

        self.ai.comboBox.clear()
        cursor.execute("select * from КЛИЕНТ")
        wow = cursor.fetchone()
        while wow:
            self.ai.comboBox.addItem(str(wow[0]))
            wow = cursor.fetchone()

        self.ai.comboBox_12.clear()
        cursor.execute("select * from СОТРУДНИК")
        wow = cursor.fetchone()
        while wow:
            self.ai.comboBox_12.addItem(str(wow[0]))
            wow = cursor.fetchone()

    def create_Klient_prodavec(self):
        cursor.execute(self.count_string + " " + self.table[2])  # кол строк
        self.st = cursor.fetchone()
        self.ai.tableWidget_2.setRowCount(self.st[0])

        cursor.execute(self.count_column + self.table[2] + "'")  # кол столбцов
        self.col = cursor.fetchone()
        self.ai.tableWidget_2.setColumnCount(self.col[0])

        cursor.execute(self.name_columns + self.table[2] + "'")  # названия столбцов
        self.name_col = cursor.fetchone()
        while self.name_col:
            self.dict_name.append(self.name_col[0])
            self.name_col = cursor.fetchone()
        self.ai.tableWidget_2.setHorizontalHeaderLabels(self.dict_name)
        print(self.table[2])
        print(self.dict_name)
        self.dict_name.clear()
        for j in range(self.col[0]):
            cursor.execute(self.add_string + self.table[2])
            for i in range(self.st[0]):
                self.info_str = cursor.fetchone()
                self.ai.tableWidget_2.setItem(i, j, QTableWidgetItem(str(self.info_str[j])))
        self.ai.tableWidget_2.resizeColumnsToContents()

        self.ai.comboBox_2.clear()
        cursor.execute("select * from КЛИЕНТ")
        wow = cursor.fetchone()
        while wow:
            self.ai.comboBox_2.addItem(str(wow[0]))
            wow = cursor.fetchone()

        self.ai.comboBox_11.clear()
        cursor.execute("select * from ОБЪЕКТ")
        wow = cursor.fetchone()
        while wow:
            self.ai.comboBox_11.addItem(str(wow[0]))
            wow = cursor.fetchone()

    def create_Object(self):
        cursor.execute(self.count_string + " " + self.table[3])  # кол строк
        self.st = cursor.fetchone()
        self.ai.tableWidget_3.setRowCount(self.st[0])

        cursor.execute(self.count_column + self.table[3] + "'")  # кол столбцов
        self.col = cursor.fetchone()
        self.ai.tableWidget_3.setColumnCount(self.col[0])

        cursor.execute(self.name_columns + self.table[3] + "'")
        self.name_col = cursor.fetchone()
        while self.name_col:  # названия столбцов
            self.dict_name.append(self.name_col[0])
            self.name_col = cursor.fetchone()
        self.ai.tableWidget_3.setHorizontalHeaderLabels(self.dict_name)
        print(self.table[3])
        print(self.dict_name)
        self.dict_name.clear()
        for j in range(self.col[0]):
            cursor.execute(self.add_string + self.table[3])
            for i in range(self.st[0]):
                self.info_str = cursor.fetchone()
                self.ai.tableWidget_3.setItem(i, j, QTableWidgetItem(str(self.info_str[j])))
        self.ai.tableWidget_3.resizeColumnsToContents()

        self.ai.comboBox_5.clear()
        cursor.execute("select * from СОТРУДНИК")
        wow = cursor.fetchone()
        while wow:
            self.ai.comboBox_5.addItem(str(wow[0]))
            wow = cursor.fetchone()

        self.ai.comboBox_6.clear()
        cursor.execute("select * from РАЙОН")
        wow = cursor.fetchone()
        while wow:
            self.ai.comboBox_6.addItem(str(wow[0]))
            wow = cursor.fetchone()

        self.ai.comboBox_7.clear()
        cursor.execute("select * from ВИД_ОБЪЕКТА")
        wow = cursor.fetchone()
        while wow:
            self.ai.comboBox_7.addItem(str(wow[0]))
            wow = cursor.fetchone()

    def create_Kind_Object(self):
        cursor.execute(self.count_string + " " + self.table[4])  # кол строк
        self.st = cursor.fetchone()
        self.ai.tableWidget_4.setRowCount(self.st[0])

        cursor.execute(self.count_column + self.table[4] + "'")  # кол столбцов
        self.col = cursor.fetchone()
        self.ai.tableWidget_4.setColumnCount(self.col[0])
        cursor.execute(self.name_columns + self.table[4] + "'")
        self.name_col = cursor.fetchone()
        while self.name_col:  # названия столбцов
            self.dict_name.append(self.name_col[0])
            self.name_col = cursor.fetchone()
        self.ai.tableWidget_4.setHorizontalHeaderLabels(self.dict_name)
        print(self.table[4])
        print(self.dict_name)
        self.dict_name.clear()
        for j in range(self.col[0]):
            cursor.execute(self.add_string + self.table[4])
            for i in range(self.st[0]):
                self.info_str = cursor.fetchone()
                self.ai.tableWidget_4.setItem(i, j, QTableWidgetItem(str(self.info_str[j])))
        self.ai.tableWidget_4.resizeColumnsToContents()

    def create_Trebovaniya(self):
        cursor.execute(self.count_string + " " + self.table[5])  # кол строк
        self.st = cursor.fetchone()
        self.ai.tableWidget_5.setRowCount(self.st[0])

        cursor.execute(self.count_column + self.table[5] + "'")  # кол столбцов
        self.col = cursor.fetchone()
        self.ai.tableWidget_5.setColumnCount(self.col[0])

        cursor.execute(self.name_columns + self.table[5] + "'")
        self.name_col = cursor.fetchone()

        while self.name_col:  # названия столбцов
            self.dict_name.append(self.name_col[0])
            self.name_col = cursor.fetchone()
        self.ai.tableWidget_5.setHorizontalHeaderLabels(self.dict_name)
        print(self.table[5])
        print(self.dict_name)
        self.dict_name.clear()

        for j in range(self.col[0]):
            cursor.execute(self.add_string + self.table[5])
            for i in range(self.st[0]):
                self.info_str = cursor.fetchone()
                self.ai.tableWidget_5.setItem(i, j, QTableWidgetItem(str(self.info_str[j])))
        self.ai.tableWidget_5.resizeColumnsToContents()

        self.ai.comboBox_3.clear()
        cursor.execute("select * from ВИД_ОБЪЕКТА")
        wow = cursor.fetchone()
        while wow:
            self.ai.comboBox_3.addItem(str(wow[0]))
            wow = cursor.fetchone()

        self.ai.comboBox_4.clear()
        cursor.execute("select * from РАЙОН")
        wow = cursor.fetchone()
        while wow:
            self.ai.comboBox_4.addItem(str(wow[0]))
            wow = cursor.fetchone()

        self.ai.comboBox_14.clear()
        cursor.execute("select * from КЛИЕНТ_ПОКУПАТЕЛЬ")
        wow = cursor.fetchone()
        while wow:
            self.ai.comboBox_14.addItem(str(wow[0]))
            wow = cursor.fetchone()

    def create_Place(self):
        cursor.execute(self.count_string + " " + self.table[6])  # кол строк
        self.st = cursor.fetchone()
        self.ai.tableWidget_6.setRowCount(self.st[0])

        cursor.execute(self.count_column + self.table[6] + "'")  # кол столбцов
        self.col = cursor.fetchone()
        self.ai.tableWidget_6.setColumnCount(self.col[0])

        cursor.execute(self.name_columns + self.table[6] + "'")
        self.name_col = cursor.fetchone()

        while self.name_col:  # названия столбцов
            self.dict_name.append(self.name_col[0])
            self.name_col = cursor.fetchone()
        self.ai.tableWidget_6.setHorizontalHeaderLabels(self.dict_name)
        print(self.table[6])
        print(self.dict_name)
        self.dict_name.clear()

        for j in range(self.col[0]):
            cursor.execute(self.add_string + self.table[6])
            for i in range(self.st[0]):
                self.info_str = cursor.fetchone()
                self.ai.tableWidget_6.setItem(i, j, QTableWidgetItem(str(self.info_str[j])))
        self.ai.tableWidget_6.resizeColumnsToContents()

    def create_Agent(self):
        cursor.execute(self.count_string + " " + self.table[7])  # кол строк
        self.st = cursor.fetchone()
        self.ai.tableWidget_7.setRowCount(self.st[0])

        cursor.execute(self.count_column + self.table[7] + "'")  # кол столбцов
        self.col = cursor.fetchone()
        self.ai.tableWidget_7.setColumnCount(self.col[0])

        cursor.execute(self.name_columns + self.table[7] + "'")
        self.name_col = cursor.fetchone()

        while self.name_col:  # названия столбцов
            self.dict_name.append(self.name_col[0])
            self.name_col = cursor.fetchone()
        self.ai.tableWidget_7.setHorizontalHeaderLabels(self.dict_name)
        print(self.table[7])
        print(self.dict_name)
        self.dict_name.clear()

        for j in range(self.col[0]):
            cursor.execute(self.add_string + self.table[7])
            for i in range(self.st[0]):
                self.info_str = cursor.fetchone()
                self.ai.tableWidget_7.setItem(i, j, QTableWidgetItem(str(self.info_str[j])))
        self.ai.tableWidget_7.resizeColumnsToContents()

        self.ai.comboBox_13.clear()
        cursor.execute("select * from ОФИС")
        wow = cursor.fetchone()
        while wow:
            self.ai.comboBox_13.addItem(str(wow[0]))
            wow = cursor.fetchone()

    def create_Sdelka(self):
        cursor.execute(self.count_string + " " + self.table[8])  # кол строк
        self.st = cursor.fetchone()
        self.ai.tableWidget_8.setRowCount(self.st[0])

        cursor.execute(self.count_column + self.table[8] + "'")  # кол столбцов
        self.col = cursor.fetchone()
        self.ai.tableWidget_8.setColumnCount(self.col[0])

        cursor.execute(self.name_columns + self.table[8] + "'")
        self.name_col = cursor.fetchone()

        while self.name_col:  # названия столбцов
            self.dict_name.append(self.name_col[0])
            self.name_col = cursor.fetchone()
        self.ai.tableWidget_8.setHorizontalHeaderLabels(self.dict_name)
        print(self.table[8])
        print(self.dict_name)
        self.dict_name.clear()

        for j in range(self.col[0]):
            cursor.execute(self.add_string + self.table[8])
            for i in range(self.st[0]):
                self.info_str = cursor.fetchone()
                self.ai.tableWidget_8.setItem(i, j, QTableWidgetItem(str(self.info_str[j])))
        self.ai.tableWidget_8.resizeColumnsToContents()

        self.ai.comboBox_8.clear()
        cursor.execute("select * from КЛИЕНТ")
        wow = cursor.fetchone()
        while wow:
            self.ai.comboBox_8.addItem(str(wow[0]))
            wow = cursor.fetchone()

        self.ai.comboBox_9.clear()
        cursor.execute("select * from СОТРУДНИК")
        wow = cursor.fetchone()
        while wow:
            self.ai.comboBox_9.addItem(str(wow[0]))
            wow = cursor.fetchone()

        self.ai.comboBox_10.clear()
        cursor.execute("select * from ОБЪЕКТ")
        wow = cursor.fetchone()
        while wow:
            self.ai.comboBox_10.addItem(str(wow[0]))
            wow = cursor.fetchone()

    def create_Office(self):
        cursor.execute(self.count_string + " " + self.table[9])  # кол строк
        self.st = cursor.fetchone()
        self.ai.tableWidget_9.setRowCount(self.st[0])

        cursor.execute(self.count_column + self.table[9] + "'")  # кол столбцов
        self.col = cursor.fetchone()
        self.ai.tableWidget_9.setColumnCount(self.col[0])

        cursor.execute(self.name_columns + self.table[9] + "'")
        self.name_col = cursor.fetchone()

        while self.name_col:  # названия столбцов
            self.dict_name.append(self.name_col[0])
            self.name_col = cursor.fetchone()
        self.ai.tableWidget_9.setHorizontalHeaderLabels(self.dict_name)
        print(self.table[9])
        print(self.dict_name)
        self.dict_name.clear()

        for j in range(self.col[0]):
            cursor.execute(self.add_string + self.table[9])
            for i in range(self.st[0]):
                self.info_str = cursor.fetchone()
                self.ai.tableWidget_9.setItem(i, j, QTableWidgetItem(str(self.info_str[j])))
        self.ai.tableWidget_9.resizeColumnsToContents()

    '''Вывод данных из таблиц в формы заполнения'''
    def CellClick_Klient(self, row):
        cursor.execute("select * from КЛИЕНТ")
        info = cursor.fetchall()
        self.id_klenta=info[row][0]
        self.ai.line2.setText(info[row][1])

    def CellClick_Klient_pokupatel(self, row):
        cursor.execute("select * from КЛИЕНТ_ПОКУПАТЕЛЬ")
        info = cursor.fetchall()
        self.id_pokyp=info[row][0]
        self.ai.line3.setText(info[row][1])
        self.ai.line4.setText(info[row][2])
        self.ai.line6.setText(info[row][3])
        self.ai.line7.setText(info[row][4])
        self.ai.line10.setText(info[row][5])

    def CellClick_Klient_prodavec(self, row):
        cursor.execute("select * from КЛИЕНТ_ПРОДАВЕЦ")
        info = cursor.fetchall()
        self.id_prod = info[row][0]
        self.ai.line11.setText(info[row][1])
        self.ai.line12.setText(info[row][2])
        self.ai.line14.setText(info[row][3])
        self.ai.line15.setText(info[row][4])
        self.ai.line18.setText(info[row][5])
        self.ai.line16.setText(info[row][6])
        self.ai.line19.setText(str(info[row][7]))

    def CellClick_Object(self, row):
        cursor.execute("select * from ОБЪЕКТ")
        info = cursor.fetchall()
        self.id_obj = info[row][0]
        self.ai.line21.setText(info[row][1])
        self.ai.line26.setText(info[row][2])
        self.ai.line23.setText(str(info[row][3]))
        self.ai.line24.setText(str(info[row][4]))
        self.ai.line25.setText(str(info[row][5]))
        self.ai.line22.setText(str(info[row][6]))

    def CellClick_Kind_Object(self, row):
        cursor.execute("select * from ВИД_ОБЪЕКТА")
        info = cursor.fetchall()
        self.id_kind = info[row][0]
        self.ai.line31.setText(info[row][1])

    def CellClick_Trebovaniya(self, row):
        cursor.execute("select * from ТРЕБОВАНИЯ_К_ОБЪЕКТУ")
        info = cursor.fetchall()
        self.id_treb = info[row][0]
        self.ai.line32.setText(info[row][1])
        self.ai.line35.setText(str(info[row][2]))
        self.ai.line36.setText(str(info[row][3]))
        self.ai.line33.setText(str(info[row][4]))
        self.ai.line34.setText(str(info[row][5]))
        self.ai.line37.setText(str(info[row][6]))

    def CellClick_Place(self,row):
        cursor.execute("select * from РАЙОН")
        info = cursor.fetchall()
        self.id_place = info[row][0]
        self.ai.line41.setText(info[row][1])

    def CellClick_Agent(self, row):
        cursor.execute("select * from СОТРУДНИК")
        info = cursor.fetchall()
        self.id_agent = info[row][0]
        self.ai.line42.setText(info[row][1])
        self.ai.line43.setText(info[row][2])
        self.ai.line45.setText(info[row][3])
        self.ai.line48.setText(str(info[row][4]))
        self.ai.line44.setText(info[row][5])
        self.ai.line46.setText(str(info[row][6]))
        self.ai.line49.setText(str(info[row][7]))
        self.ai.line47.setText(str(info[row][8]))
        self.ai.line50.setText(str(info[row][9]))

    def CellClick_Sdelka(self,row):
        cursor.execute("select * from СДЕЛКА")
        info = cursor.fetchall()
        self.id_sdelka = info[row][0]
        self.ai.line53.setText(info[row][1])
        self.ai.line54.setText(str(info[row][2]))
        self.ai.line55.setText(str(info[row][3]))
        self.ai.line56.setText(str(info[row][4]))

    def CellClick_Office(self, row):
        cursor.execute("select * from ОФИС")
        info = cursor.fetchall()
        self.id_office = info[row][0]
        self.ai.line61.setText(info[row][1])
        self.ai.line62.setText(str(info[row][2]))

    '''Добавление записей'''
    def AddData_Klient(self):
        try:
            self.tip_klienta = self.ai.line2.text()
            cursor.execute("INSERT INTO КЛИЕНТ (Тип_клиента) VALUES ('" + self.tip_klienta + "')")
            cursor.commit()
            self.update_database()
        except:
            self.error = QMessageBox.question(
                self, "Message", "Ошибка добавления данных.",
                QMessageBox.Ok)

    def AddData_Klient_pokupatel(self):
        try:
            self.fam = self.ai.line3.text()
            self.imya= self.ai.line4.text()
            self.otch = self.ai.line6.text()
            self.seriya_pass = self.ai.line7.text()
            self.num_pass = self.ai.line10.text()
            self.num_klienta = self.ai.comboBox.currentText()
            self.num_agent = self.ai.comboBox_12.currentText()
            cursor.execute("INSERT INTO КЛИЕНТ_ПОКУПАТЕЛЬ (Код_клиента_покупателя, Фамилия, "
                           "Имя, Отчество, Серия_Паспорта, Номер_Паспорта, Номер_агента) VALUES "
                           "('" + self.num_klienta + "','" + self.fam + "','" + self.imya + "','" + self.otch + "','" + self.seriya_pass + "','" + self.num_pass + "','" + self.num_agent + "')")
            cursor.commit()
            self.update_database()
        except:
            self.error = QMessageBox.question(
                self, "Message", "Ошибка добавления данных.",
                QMessageBox.Ok)

    def AddData_Klient_prodavec(self):
        try:
            self.fam = self.ai.line11.text()
            self.imya = self.ai.line12.text()
            self.otch = self.ai.line14.text()
            self.seriya_pass = self.ai.line15.text()
            self.num_pass = self.ai.line18.text()
            self.ogrn = self.ai.line16.text()
            self.cell = self.ai.line19.text()
            self.num_obj = self.ai.comboBox_11.currentText()
            self.kod_klienta = self.ai.comboBox_2.currentText()
            cursor.execute("INSERT INTO КЛИЕНТ_ПРОДАВЕЦ (Код_клиента_продавца, Фамилия, Имя, Отчество, "
                           "Серия_Паспорта, Номер_Паспорта, Наличие_выписки_из_ЕГРН, Цена_недвижимости, Номер_объекта) VALUES "
                           "('" + self.kod_klienta + "','" + self.fam + "',"
                           "'" + self.imya + "','" + self.otch + "','" + self.seriya_pass + "','" + self.num_pass + "',"
                           "'" + self.ogrn + "','" + self.cell + "','" + self.num_obj+"')")
            cursor.commit()
            self.update_database()
        except:
            self.error = QMessageBox.question(
                self, "Message", "Ошибка добавления данных.",
                QMessageBox.Ok)

    def AddData_Object(self):
        try:
            self.tip_build = self.ai.line21.text()
            self.do_build = self.ai.line26.text()
            self.place = self.ai.line23.text()
            self.room = self.ai.line24.text()
            self.floor = self.ai.line25.text()
            self.cell = self.ai.line22.text()
            self.num_agent = self.ai.comboBox_5.currentText()
            self.num_place = self.ai.comboBox_6.currentText()
            self.num_kind_obj = self.ai.comboBox_7.currentText()
            cursor.execute("INSERT INTO ОБЪЕКТ (Тип_здания, Назначение_здания, Площадь, Количество_комнат,"
                           " Этаж, Выставленная_цена, Номер_сотрудника, Номер_района, Номер_вида_объекта) VALUES "
                           "('" + self.tip_build + "','" + self.do_build + "','" + self.place + "','" + self.room + "','" + self.floor + "',"
                            "'" + self.cell + "','" + self.num_agent + "','" + self.num_place + "','" + self.num_kind_obj + "')")
            cursor.commit()
            self.update_database()
        except:
            self.error = QMessageBox.question(
                self, "Message", "Ошибка добавления данных.",
                QMessageBox.Ok)

    def AddData_Kind_Object(self):
        try:
            self.name_obj = self.ai.line31.text()
            cursor.execute("INSERT INTO ВИД_ОБЪЕКТА (Название_вида) VALUES ('" + self.name_obj + "')")
            cursor.commit()
            self.update_database()
        except:
            self.error = QMessageBox.question(
                self, "Message", "Ошибка добавления данных.",
                QMessageBox.Ok)

    def AddData_Trebovaniya(self):
        try:
            self.tip_build = self.ai.line32.text()
            self.do_build = self.ai.line37.text()
            self.place = self.ai.line33.text()
            self.room = self.ai.line36.text()
            self.floor = self.ai.line34.text()
            self.cell = self.ai.line35.text()
            self.num_place = self.ai.comboBox_4.currentText()
            self.num_kind_obj = self.ai.comboBox_3.currentText()
            self.kod_klienta = self.ai.comboBox_14.currentText()
            cursor.execute("INSERT INTO ТРЕБОВАНИЯ_К_ОБЪЕКТУ (Код_требования, Тип_здания, Цена, Количество_комнат, Площадь, Этаж, Назначение_здания,"
                           " Номер_вида_объекта, Номер_района) VALUES "
                           "('" + self.kod_klienta + "','" + self.tip_build + "','" + self.cell + "','" + self.room + "','" + self.place + "','" + self.floor + "',"
                            "'" + self.do_build + "','" + self.num_kind_obj + "','" + self.num_place + "')")
            cursor.commit()
            self.update_database()
        except:
            self.error = QMessageBox.question(
                self, "Message", "Ошибка добавления данных.",
                QMessageBox.Ok)

    def AddData_Place(self):
        try:
            self.name_place = self.ai.line41.text()
            cursor.execute("INSERT INTO РАЙОН (Название_района) VALUES ('" + self.name_place + "')")
            cursor.commit()
            self.update_database()
        except:
            self.error = QMessageBox.question(
                self, "Message", "Ошибка добавления данных.",
                QMessageBox.Ok)

    def AddData_Agent(self):
        try:
            self.fam = self.ai.line42.text()
            self.imya = self.ai.line43.text()
            self.otch = self.ai.line45.text()
            self.phone = self.ai.line48.text()
            self.seriya_pass = self.ai.line46.text()
            self.num_pass = self.ai.line49.text()
            self.work = self.ai.line44.text()
            self.inn = self.ai.line47.text()
            self.snils = self.ai.line50.text()
            self.num_office = self.ai.comboBox_13.currentText()
            cursor.execute("INSERT INTO СОТРУДНИК (Фамилия, Имя, Отчество, Телефон, Должность, "
                           "Серия_Паспорта, Номер_Паспорта, ИНН, СНИЛС, Номер_офиса) VALUES "
                           "('" +self.fam+ "','" + self.imya + "','" + self.otch + "','" + self.phone + "','" + self.work + "',"
                            "'" + self.seriya_pass + "','" + self.num_pass + "','" + self.inn + "','" + self.snils + "','" + self.num_office +"')")
            cursor.commit()
            self.update_database()
        except:
            self.error = QMessageBox.question(
                self, "Message", "Ошибка добавления данных.",
                QMessageBox.Ok)

    def AddData_Sdelka(self):
        try:
            self.tip_sdelki = self.ai.line53.text()
            self.full_cell = self.ai.line54.text()
            self.agent_cell = self.ai.line55.text()
            self.klient_cell = self.ai.line56.text()
            self.kod = self.ai.line57.text()
            self.num_agent = self.ai.comboBox_9.currentText()
            self.num_obj = self.ai.comboBox_10.currentText()
            self.num_klienta = self.ai.comboBox_8.currentText()
            cursor.execute("INSERT INTO СДЕЛКА (Код_сделки, Тип_сделки, Итоговая_сумма_для_покупателя, Выплата_сотруднику, Выплата_продавцу, "
                           "Номер_сотрудника, Номер_объекта, Номер_клиента) VALUES "
                           "('" + str(self.kod) + "','" + str(self.tip_sdelki) + "','" + str(self.full_cell) + "','" + str(self.agent_cell) + "','" + str(self.klient_cell) + "','" + str(self.num_agent) + "',"
                            "'" + str(self.num_obj) + "','" + str(self.num_klienta) + "')")
            cursor.commit()
            self.update_database()
        except:
            self.error = QMessageBox.question(
                self, "Message", "Ошибка добавления данных.",
                QMessageBox.Ok)

    def AddData_Office(self):
        try:
            self.name_office = self.ai.line61.text()
            self.number_office = self.ai.line62.text()
            cursor.execute("INSERT INTO ОФИС (Название_офиса, Номер_телефона) VALUES ('" + self.name_office + "','" + self.number_office + "')")
            cursor.commit()
            self.update_database()
        except:
            self.error = QMessageBox.question(
                self, "Message", "Ошибка добавления данных.",
                QMessageBox.Ok)

    '''Обновление записей'''
    def Update_Klient(self):
        try:
            self.tip_klienta = self.ai.line2.text()
            cursor.execute("UPDATE КЛИЕНТ SET Тип_клиента ='" + self.tip_klienta + "' WHERE Код_клиента="+str(self.id_klenta))
            cursor.commit()
            self.update_database()
        except:
            self.error = QMessageBox.question(
                self, "Message", "Ошибка обновления данных. Выберите строку из таблицы!",
                QMessageBox.Ok)

    def Update_Klient_pokupatel(self):
        try:
            self.fam = self.ai.line3.text()
            self.imya= self.ai.line4.text()
            self.otch = self.ai.line6.text()
            self.seriya_pass = self.ai.line7.text()
            self.num_pass = self.ai.line10.text()
            self.num_klienta = self.ai.comboBox.currentText()
            self.num_agent = self.ai.comboBox_12.currentText()
            cursor.execute("UPDATE КЛИЕНТ_ПОКУПАТЕЛЬ SET Код_клиента_покупателя='" + self.num_klienta + "', Фамилия='" + self.fam + "', "
                           "Имя='" + self.imya + "', Отчество='" + self.otch + "', Серия_Паспорта='" + str(self.seriya_pass) + "'"
                            ", Номер_Паспорта='" + str(self.num_pass) + "', Номер_агента='" + str(self.num_agent) + "' WHERE Код_клиента_покупателя="+ str(self.id_pokyp))
            cursor.commit()
            self.update_database()
        except:
            self.error = QMessageBox.question(
                self, "Message", "Ошибка обновления данных. Выберите строку из таблицы!",
                QMessageBox.Ok)

    def Update_Klient_prodavec(self):
        try:
            self.fam = self.ai.line11.text()
            self.imya = self.ai.line12.text()
            self.otch = self.ai.line14.text()
            self.seriya_pass = self.ai.line15.text()
            self.num_pass = self.ai.line18.text()
            self.ogrn = self.ai.line16.text()
            self.cell = self.ai.line19.text()
            self.num_obj = self.ai.comboBox_11.currentText()
            self.kod_klienta = self.ai.comboBox_2.currentText()
            cursor.execute("UPDATE КЛИЕНТ_ПРОДАВЕЦ SET Код_клиента_продавца='" + str(self.kod_klienta) + "', Фамилия='" + self.fam + "', Имя='" + self.imya + "', Отчество='" + self.otch + "', "
                           "Серия_Паспорта='" + str(self.seriya_pass) + "', Номер_Паспорта='" + str(self.num_pass) + "'"
                            ", Наличие_выписки_из_ЕГРН='" + str(self.ogrn) + "', Цена_недвижимости='" + str(self.cell) + "', Номер_объекта='" + str(self.num_obj)+"' WHERE Код_клиента_продавца="+str(self.id_prod))
            cursor.commit()
            self.update_database()
        except:
            self.error = QMessageBox.question(
                self, "Message", "Ошибка обновления данных. Выберите строку из таблицы!",
                QMessageBox.Ok)

    def Update_Object(self):
        try:
            self.tip_build = self.ai.line21.text()
            self.do_build = self.ai.line26.text()
            self.place = self.ai.line23.text()
            self.room = self.ai.line24.text()
            self.floor = self.ai.line25.text()
            self.cell = self.ai.line22.text()
            self.num_agent = self.ai.comboBox_5.currentText()
            self.num_place = self.ai.comboBox_6.currentText()
            self.num_kind_obj = self.ai.comboBox_7.currentText()
            cursor.execute("UPDATE ОБЪЕКТ SET Тип_здания='" + self.tip_build + "', Назначение_здания='" + self.do_build + "', Площадь='" + str(self.place)+ "', Количество_комнат='" + str(self.room) + "',"
                           " Этаж='" + str(self.floor) + "', Выставленная_цена='" + str(self.cell) + "', Номер_сотрудника='" +str( self.num_agent) + "', Номер_района='" + str(self.num_place) + "', Номер_вида_объекта='" + str(self.num_kind_obj) + "' WHERE Код_объекта="+str(self.id_obj))
            cursor.commit()
            self.update_database()
        except:
            self.error = QMessageBox.question(
                self, "Message", "Ошибка обновления данных. Выберите строку из таблицы!",
                QMessageBox.Ok)

    def Update_Kind_Object(self):
        try:
            self.name_obj = self.ai.line31.text()
            cursor.execute("UPDATE ВИД_ОБЪЕКТА SET Название_вида='" + self.name_obj + "' WHERE Код_вида_объекта="+str(self.id_kind))
            cursor.commit()
            self.update_database()
        except:
            self.error = QMessageBox.question(
                self, "Message", "Ошибка обновления данных. Выберите строку из таблицы!",
                QMessageBox.Ok)

    def Update_Trebovaniya(self):
        try:
            self.tip_build = self.ai.line32.text()
            self.do_build = self.ai.line37.text()
            self.place = self.ai.line33.text()
            self.room = self.ai.line36.text()
            self.floor = self.ai.line34.text()
            self.cell = self.ai.line35.text()
            self.num_place = self.ai.comboBox_4.currentText()
            self.num_kind_obj = self.ai.comboBox_3.currentText()
            self.kod_klienta = self.ai.comboBox_14.currentText()
            cursor.execute("UPDATE ТРЕБОВАНИЯ_К_ОБЪЕКТУ SET Код_требования='" + str(self.kod_klienta) + "', Тип_здания='" + self.tip_build + "', Цена='" + str(self.cell) + "'"
                            ", Количество_комнат='" + str(self.room) + "', Площадь='" + str(self.place) + "', Этаж='" + str(self.floor) + "', Назначение_здания='" + self.do_build + "',"
                           " Номер_вида_объекта='" + str(self.num_kind_obj) + "', Номер_района='" + str(self.num_place) + "' WHERE Код_требования="+str(self.id_treb))

            cursor.commit()
            self.update_database()
        except:
            self.error = QMessageBox.question(
                self, "Message", "Ошибка обновления данных. Выберите строку из таблицы!",
                QMessageBox.Ok)

    def Update_Place(self):
        try:
            self.name_place = self.ai.line41.text()
            cursor.execute("UPDATE РАЙОН SET Название_района='" + self.name_place + "' WHERE Код_района="+str(self.id_place))
            cursor.commit()
            self.update_database()
        except:
            self.error = QMessageBox.question(
                self, "Message", "Ошибка обновления данных. Выберите строку из таблицы!",
                QMessageBox.Ok)

    def Update_Agent(self):
        try:
            self.fam = self.ai.line42.text()
            self.imya = self.ai.line43.text()
            self.otch = self.ai.line45.text()
            self.phone = self.ai.line48.text()
            self.seriya_pass = self.ai.line46.text()
            self.num_pass = self.ai.line49.text()
            self.work = self.ai.line44.text()
            self.inn = self.ai.line47.text()
            self.snils = self.ai.line50.text()
            self.num_office = self.ai.comboBox_13.currentText()
            cursor.execute("UPDATE СОТРУДНИК SET Фамилия='" +self.fam+ "', Имя='" + self.imya + "', Отчество='" + self.otch + "', "
                           "Телефон='" + str(self.phone) + "', Должность='" + self.work + "', "
                           "Серия_Паспорта='" + str(self.seriya_pass) + "', Номер_Паспорта='" + str(self.num_pass) + "', "
                           "ИНН='" + str(self.inn) + "', СНИЛС='" + str(self.snils) + "', Номер_офиса='" + str(self.num_office) +"' WHERE Код_сотрудника="+str(self.id_agent))
            cursor.commit()
            self.update_database()
        except:
            self.error = QMessageBox.question(
                self, "Message", "Ошибка обновления данных. Выберите строку из таблицы!",
                QMessageBox.Ok)

    def Update_Sdelka(self):
        try:
            self.tip_sdelki = self.ai.line53.text()
            self.full_cell = self.ai.line54.text()
            self.agent_cell = self.ai.line55.text()
            self.klient_cell = self.ai.line56.text()
            self.num_agent = self.ai.comboBox_9.currentText()
            self.num_obj = self.ai.comboBox_10.currentText()
            self.num_klienta = self.ai.comboBox_8.currentText()
            cursor.execute("UPDATE СДЕЛКА SET Тип_сделки='" + self.tip_sdelki + "', Итоговая_сумма_для_покупателя='" + str(self.full_cell) + "', Выплата_сотруднику='" + str(self.agent_cell) + "', Выплата_продавцу='" + str(self.klient_cell) + "', "
                           "Номер_сотрудника='" + str(self.num_agent) + "', Номер_объекта='" + str(self.num_obj) + "', Номер_клиента='" + str(self.num_klienta) + "' WHERE Код_сделки="+str(self.id_sdelka))
            cursor.commit()
            self.update_database()
        except:
            self.error = QMessageBox.question(
                self, "Message", "Ошибка обновления данных. Выберите строку из таблицы!",
                QMessageBox.Ok)

    def Update_Office(self):
        try:
            self.name_office = self.ai.line61.text()
            self.number_office = self.ai.line62.text()
            cursor.execute("UPDATE ОФИС SET Название_офиса='" + self.name_office + "', Номер_телефона='" + str(self.number_office) + "' WHERE Код_офиса="+str(self.id_office))
            cursor.commit()

            self.update_database()
        except:
            self.error = QMessageBox.question(
                self, "Message", "Ошибка обновления данных. Выберите строку из таблицы!",
                QMessageBox.Ok)

    '''Удаление записей'''
    def Delete_Klient(self):
        try:
            cursor.execute("DELETE FROM КЛИЕНТ WHERE Код_клиента="+str(self.id_klenta))
            cursor.commit()
            self.update_database()
        except:
            self.error = QMessageBox.question(
                self, "Message", "Ошибка удаления данных.\nВозможно имеются зависимости от этих данных!",
                QMessageBox.Ok)

    def Delete_Klient_pokupatel(self):
        try:
            cursor.execute("DELETE FROM КЛИЕНТ_ПОКУПАТЕЛЬ WHERE Код_клиента_покупателя="+ str(self.id_pokyp))
            cursor.commit()
            self.update_database()
        except:
            self.error = QMessageBox.question(
                self, "Message", "Ошибка удаления данных.\nВозможно имеются зависимости от этих данных!",
                QMessageBox.Ok)

    def Delete_Klient_prodavec(self):
        try:
            cursor.execute("DELETE FROM КЛИЕНТ_ПРОДАВЕЦ WHERE Код_клиента_продавца="+str(self.id_prod))
            cursor.commit()
            self.update_database()
        except:
            self.error = QMessageBox.question(
                self, "Message", "Ошибка удаления данных.\nВозможно имеются зависимости от этих данных!",
                QMessageBox.Ok)

    def Delete_Object(self):
        try:
            cursor.execute("DELETE FROM ОБЪЕКТ WHERE Код_объекта="+str(self.id_obj))
            cursor.commit()
            self.update_database()
        except:
            self.error = QMessageBox.question(
                self, "Message", "Ошибка удаления данных.\nВозможно имеются зависимости от этих данных!",
                QMessageBox.Ok)

    def Delete_Kind_Object(self):
        try:
            cursor.execute("DELETE FROM ВИД_ОБЪЕКТА WHERE Код_вида_объекта="+str(self.id_kind))
            cursor.commit()
            self.update_database()
        except:
            self.error = QMessageBox.question(
                self, "Message", "Ошибка удаления данных.\nВозможно имеются зависимости от этих данных!",
                QMessageBox.Ok)

    def Delete_Trebovaniya(self):
        try:
            cursor.execute("DELETE FROM ТРЕБОВАНИЯ_К_ОБЪЕКТУ WHERE Код_требования="+str(self.id_treb))
            cursor.commit()
            self.update_database()
        except:
            self.error = QMessageBox.question(
                self, "Message", "Ошибка удаления данных.\nВозможно имеются зависимости от этих данных!",
                QMessageBox.Ok)

    def Delete_Place(self):
        try:
            self.name_place = self.ai.line41.text()
            cursor.execute("DELETE FROM РАЙОН WHERE Код_района="+str(self.id_place))
            cursor.commit()
            self.update_database()
        except:
            self.error = QMessageBox.question(
                self, "Message", "Ошибка удаления данных.\nВозможно имеются зависимости от этих данных!",
                QMessageBox.Ok)

    def Delete_Agent(self):
        try:
            cursor.execute("DELETE FROM СОТРУДНИК WHERE Код_сотрудника="+str(self.id_agent))

            cursor.commit()
            self.update_database()
        except:
            self.error = QMessageBox.question(
                self, "Message", "Ошибка удаления данных.\nВозможно имеются зависимости от этих данных!",
                QMessageBox.Ok)

    def Delete_Sdelka(self):
        try:
            self.name_office = self.ai.line61.text()
            self.number_office = self.ai.line62.text()
            cursor.execute("DELETE FROM СДЕЛКА WHERE Код_сделки="+str(self.id_sdelka))
            cursor.commit()
            self.update_database()
        except:
            self.error = QMessageBox.question(
                self, "Message", "Ошибка удаления данных.\nВозможно имеются зависимости от этих данных!",
                QMessageBox.Ok)

    def Delete_Office(self):
        try:
            print(self.id_office)
            cursor.execute("DELETE FROM ОФИС WHERE Код_офиса="+str(self.id_office))
            cursor.commit()
            self.update_database()
        except:
            self.error = QMessageBox.question(
                self, "Message", "Ошибка удаления данных.\nВозможно имеются зависимости от этих данных!",
                QMessageBox.Ok)
'''Класс отвечающий за окно Сотрудник агентства'''
class User_panel(QtWidgets.QWidget):
    def __init__(self):
        super(User_panel, self).__init__()
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        global cursor
        self.show_database()
        self.ui.pushBut.clicked.connect(self.AddData_Klient)
        self.ui.pushButton_3.clicked.connect(self.AddData_Klient_pokupatel)
        self.ui.pushButton_12.clicked.connect(self.AddData_Klient_prodavec)
        self.ui.pushButton_16.clicked.connect(self.AddData_Object)
        self.ui.pushButton_30.clicked.connect(self.AddData_Trebovaniya)
        self.ui.pushButton_38.clicked.connect(self.AddData_Sdelka)

        self.ui.tableWidget_0.cellClicked.connect(self.CellClick_Klient)
        self.ui.tableWidget_1.cellClicked.connect(self.CellClick_Klient_pokupatel)
        self.ui.tableWidget_2.cellClicked.connect(self.CellClick_Klient_prodavec)
        self.ui.tableWidget_3.cellClicked.connect(self.CellClick_Object)
        self.ui.tableWidget_5.cellClicked.connect(self.CellClick_Trebovaniya)
        self.ui.tableWidget_8.cellClicked.connect(self.CellClick_Sdelka)

        self.ui.pushBut2.clicked.connect(self.Update_Klient)
        self.ui.pushButton_5.clicked.connect(self.Update_Klient_pokupatel)
        self.ui.pushButton_14.clicked.connect(self.Update_Klient_prodavec)
        self.ui.pushButton_17.clicked.connect(self.Update_Object)
        self.ui.pushButton_31.clicked.connect(self.Update_Trebovaniya)
        self.ui.pushButton_39.clicked.connect(self.Update_Sdelka)

    def update_database(self):
        try:
            self.create_Klient()
            self.create_Klient_pokupatel()
            self.create_Klient_prodavec()
            self.create_Object()
            self.create_Kind_Object()
            self.create_Trebovaniya()
            self.create_Place()
            self.create_Agent()
            self.create_Sdelka()
            self.create_Office()
        except:
            self.error = QMessageBox.question(
                self, "Message", "Ошибка загрузки базы данных.",
                QMessageBox.Ok)

    def show_database(self):  # вывод базы данных
        try:
            self.count_string = "select count(*) from"
            self.count_column = "select count(*) from information_schema.columns where table_name='"
            self.add_string = "select * from "
            self.name_columns = "SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE table_name='"
            self.table = ["КЛИЕНТ", "КЛИЕНТ_ПОКУПАТЕЛЬ", "КЛИЕНТ_ПРОДАВЕЦ", "ОБЪЕКТ", "ВИД_ОБЪЕКТА",
                          "ТРЕБОВАНИЯ_К_ОБЪЕКТУ", "РАЙОН", "СОТРУДНИК", "СДЕЛКА", "ОФИС"]
            self.dict_name = []
            self.update_database()
        except:
            self.error = QMessageBox.question(
                self, "Message", "Ошибка загрузки базы данных.",
                QMessageBox.Ok)

    ''' Заполнение таблиц '''

    def create_Klient(self):

        cursor.execute(self.count_string + " " + self.table[0])  # кол строк
        self.st = cursor.fetchone()
        self.ui.tableWidget_0.setRowCount(self.st[0])

        cursor.execute(self.count_column + self.table[0] + "'")  # кол столбцов
        self.col = cursor.fetchone()
        self.ui.tableWidget_0.setColumnCount(self.col[0])

        cursor.execute(self.name_columns + self.table[0] + "'")
        self.name_col = cursor.fetchone()
        while self.name_col:  # названия столбцов
            self.dict_name.append(self.name_col[0])
            self.name_col = cursor.fetchone()
        self.ui.tableWidget_0.setHorizontalHeaderLabels(self.dict_name)
        print(self.table[0])
        print(self.dict_name)
        self.dict_name.clear()
        for j in range(self.col[0]):
            cursor.execute(self.add_string + self.table[0])
            for i in range(self.st[0]):
                self.info_str = cursor.fetchone()
                self.ui.tableWidget_0.setItem(i, j, QTableWidgetItem(str(self.info_str[j])))
        self.ui.tableWidget_0.resizeColumnsToContents()

    def create_Klient_pokupatel(self):
        cursor.execute(self.count_string + " " + self.table[1])  # кол строк
        self.st = cursor.fetchone()
        self.ui.tableWidget_1.setRowCount(self.st[0])

        cursor.execute(self.count_column + self.table[1] + "'")  # кол столбцов
        self.col = cursor.fetchone()
        self.ui.tableWidget_1.setColumnCount(self.col[0])

        cursor.execute(self.name_columns + self.table[1] + "'")
        self.name_col = cursor.fetchone()
        while self.name_col:
            self.dict_name.append(self.name_col[0])
            self.name_col = cursor.fetchone()
        self.ui.tableWidget_1.setHorizontalHeaderLabels(self.dict_name)
        print(self.table[1])
        print(self.dict_name)
        self.dict_name.clear()
        for j in range(self.col[0]):
            cursor.execute(self.add_string + self.table[1])
            for i in range(self.st[0]):
                self.info_str = cursor.fetchone()
                self.ui.tableWidget_1.setItem(i, j, QTableWidgetItem(str(self.info_str[j])))
        self.ui.tableWidget_1.resizeColumnsToContents()

        self.ui.comboBox.clear()
        cursor.execute("select * from КЛИЕНТ")
        wow = cursor.fetchone()
        while wow:
            self.ui.comboBox.addItem(str(wow[0]))
            wow = cursor.fetchone()

        self.ui.comboBox_12.clear()
        cursor.execute("select * from СОТРУДНИК")
        wow = cursor.fetchone()
        while wow:
            self.ui.comboBox_12.addItem(str(wow[0]))
            wow = cursor.fetchone()

    def create_Klient_prodavec(self):
        cursor.execute(self.count_string + " " + self.table[2])  # кол строк
        self.st = cursor.fetchone()
        self.ui.tableWidget_2.setRowCount(self.st[0])

        cursor.execute(self.count_column + self.table[2] + "'")  # кол столбцов
        self.col = cursor.fetchone()
        self.ui.tableWidget_2.setColumnCount(self.col[0])

        cursor.execute(self.name_columns + self.table[2] + "'")  # названия столбцов
        self.name_col = cursor.fetchone()
        while self.name_col:
            self.dict_name.append(self.name_col[0])
            self.name_col = cursor.fetchone()
        self.ui.tableWidget_2.setHorizontalHeaderLabels(self.dict_name)
        print(self.table[2])
        print(self.dict_name)
        self.dict_name.clear()
        for j in range(self.col[0]):
            cursor.execute(self.add_string + self.table[2])
            for i in range(self.st[0]):
                self.info_str = cursor.fetchone()
                self.ui.tableWidget_2.setItem(i, j, QTableWidgetItem(str(self.info_str[j])))
        self.ui.tableWidget_2.resizeColumnsToContents()

        self.ui.comboBox_2.clear()
        cursor.execute("select * from КЛИЕНТ")
        wow = cursor.fetchone()
        while wow:
            self.ui.comboBox_2.addItem(str(wow[0]))
            wow = cursor.fetchone()

        self.ui.comboBox_11.clear()
        cursor.execute("select * from ОБЪЕКТ")
        wow = cursor.fetchone()
        while wow:
            self.ui.comboBox_11.addItem(str(wow[0]))
            wow = cursor.fetchone()

    def create_Object(self):
        cursor.execute(self.count_string + " " + self.table[3])  # кол строк
        self.st = cursor.fetchone()
        self.ui.tableWidget_3.setRowCount(self.st[0])

        cursor.execute(self.count_column + self.table[3] + "'")  # кол столбцов
        self.col = cursor.fetchone()
        self.ui.tableWidget_3.setColumnCount(self.col[0])

        cursor.execute(self.name_columns + self.table[3] + "'")
        self.name_col = cursor.fetchone()
        while self.name_col:  # названия столбцов
            self.dict_name.append(self.name_col[0])
            self.name_col = cursor.fetchone()
        self.ui.tableWidget_3.setHorizontalHeaderLabels(self.dict_name)
        print(self.table[3])
        print(self.dict_name)
        self.dict_name.clear()
        for j in range(self.col[0]):
            cursor.execute(self.add_string + self.table[3])
            for i in range(self.st[0]):
                self.info_str = cursor.fetchone()
                self.ui.tableWidget_3.setItem(i, j, QTableWidgetItem(str(self.info_str[j])))
        self.ui.tableWidget_3.resizeColumnsToContents()

        self.ui.comboBox_5.clear()
        cursor.execute("select * from СОТРУДНИК")
        wow = cursor.fetchone()
        while wow:
            self.ui.comboBox_5.addItem(str(wow[0]))
            wow = cursor.fetchone()

        self.ui.comboBox_6.clear()
        cursor.execute("select * from РАЙОН")
        wow = cursor.fetchone()
        while wow:
            self.ui.comboBox_6.addItem(str(wow[0]))
            wow = cursor.fetchone()

        self.ui.comboBox_7.clear()
        cursor.execute("select * from ВИД_ОБЪЕКТА")
        wow = cursor.fetchone()
        while wow:
            self.ui.comboBox_7.addItem(str(wow[0]))
            wow = cursor.fetchone()

    def create_Kind_Object(self):
        cursor.execute(self.count_string + " " + self.table[4])  # кол строк
        self.st = cursor.fetchone()
        self.ui.tableWidget_4.setRowCount(self.st[0])

        cursor.execute(self.count_column + self.table[4] + "'")  # кол столбцов
        self.col = cursor.fetchone()
        self.ui.tableWidget_4.setColumnCount(self.col[0])
        cursor.execute(self.name_columns + self.table[4] + "'")
        self.name_col = cursor.fetchone()
        while self.name_col:  # названия столбцов
            self.dict_name.append(self.name_col[0])
            self.name_col = cursor.fetchone()
        self.ui.tableWidget_4.setHorizontalHeaderLabels(self.dict_name)
        print(self.table[4])
        print(self.dict_name)
        self.dict_name.clear()
        for j in range(self.col[0]):
            cursor.execute(self.add_string + self.table[4])
            for i in range(self.st[0]):
                self.info_str = cursor.fetchone()
                self.ui.tableWidget_4.setItem(i, j, QTableWidgetItem(str(self.info_str[j])))
        self.ui.tableWidget_4.resizeColumnsToContents()

    def create_Trebovaniya(self):
        cursor.execute(self.count_string + " " + self.table[5])  # кол строк
        self.st = cursor.fetchone()
        self.ui.tableWidget_5.setRowCount(self.st[0])

        cursor.execute(self.count_column + self.table[5] + "'")  # кол столбцов
        self.col = cursor.fetchone()
        self.ui.tableWidget_5.setColumnCount(self.col[0])

        cursor.execute(self.name_columns + self.table[5] + "'")
        self.name_col = cursor.fetchone()

        while self.name_col:  # названия столбцов
            self.dict_name.append(self.name_col[0])
            self.name_col = cursor.fetchone()
        self.ui.tableWidget_5.setHorizontalHeaderLabels(self.dict_name)
        print(self.table[5])
        print(self.dict_name)
        self.dict_name.clear()

        for j in range(self.col[0]):
            cursor.execute(self.add_string + self.table[5])
            for i in range(self.st[0]):
                self.info_str = cursor.fetchone()
                self.ui.tableWidget_5.setItem(i, j, QTableWidgetItem(str(self.info_str[j])))
        self.ui.tableWidget_5.resizeColumnsToContents()

        self.ui.comboBox_3.clear()
        cursor.execute("select * from ВИД_ОБЪЕКТА")
        wow = cursor.fetchone()
        while wow:
            self.ui.comboBox_3.addItem(str(wow[0]))
            wow = cursor.fetchone()

        self.ui.comboBox_4.clear()
        cursor.execute("select * from РАЙОН")
        wow = cursor.fetchone()
        while wow:
            self.ui.comboBox_4.addItem(str(wow[0]))
            wow = cursor.fetchone()

        self.ui.comboBox_14.clear()
        cursor.execute("select * from КЛИЕНТ_ПОКУПАТЕЛЬ")
        wow = cursor.fetchone()
        while wow:
            self.ui.comboBox_14.addItem(str(wow[0]))
            wow = cursor.fetchone()

    def create_Place(self):
        cursor.execute(self.count_string + " " + self.table[6])  # кол строк
        self.st = cursor.fetchone()
        self.ui.tableWidget_6.setRowCount(self.st[0])

        cursor.execute(self.count_column + self.table[6] + "'")  # кол столбцов
        self.col = cursor.fetchone()
        self.ui.tableWidget_6.setColumnCount(self.col[0])

        cursor.execute(self.name_columns + self.table[6] + "'")
        self.name_col = cursor.fetchone()

        while self.name_col:  # названия столбцов
            self.dict_name.append(self.name_col[0])
            self.name_col = cursor.fetchone()
        self.ui.tableWidget_6.setHorizontalHeaderLabels(self.dict_name)
        print(self.table[6])
        print(self.dict_name)
        self.dict_name.clear()

        for j in range(self.col[0]):
            cursor.execute(self.add_string + self.table[6])
            for i in range(self.st[0]):
                self.info_str = cursor.fetchone()
                self.ui.tableWidget_6.setItem(i, j, QTableWidgetItem(str(self.info_str[j])))
        self.ui.tableWidget_6.resizeColumnsToContents()

    def create_Agent(self):
        cursor.execute(self.count_string + " " + self.table[7])  # кол строк
        self.st = cursor.fetchone()
        self.ui.tableWidget_7.setRowCount(self.st[0])

        cursor.execute(self.count_column + self.table[7] + "'")  # кол столбцов
        self.col = cursor.fetchone()
        self.ui.tableWidget_7.setColumnCount(self.col[0])

        cursor.execute(self.name_columns + self.table[7] + "'")
        self.name_col = cursor.fetchone()

        while self.name_col:  # названия столбцов
            self.dict_name.append(self.name_col[0])
            self.name_col = cursor.fetchone()
        self.ui.tableWidget_7.setHorizontalHeaderLabels(self.dict_name)
        print(self.table[7])
        print(self.dict_name)
        self.dict_name.clear()

        for j in range(self.col[0]):
            cursor.execute(self.add_string + self.table[7])
            for i in range(self.st[0]):
                self.info_str = cursor.fetchone()
                self.ui.tableWidget_7.setItem(i, j, QTableWidgetItem(str(self.info_str[j])))
        self.ui.tableWidget_7.resizeColumnsToContents()

    def create_Sdelka(self):
        cursor.execute(self.count_string + " " + self.table[8])  # кол строк
        self.st = cursor.fetchone()
        self.ui.tableWidget_8.setRowCount(self.st[0])

        cursor.execute(self.count_column + self.table[8] + "'")  # кол столбцов
        self.col = cursor.fetchone()
        self.ui.tableWidget_8.setColumnCount(self.col[0])

        cursor.execute(self.name_columns + self.table[8] + "'")
        self.name_col = cursor.fetchone()

        while self.name_col:  # названия столбцов
            self.dict_name.append(self.name_col[0])
            self.name_col = cursor.fetchone()
        self.ui.tableWidget_8.setHorizontalHeaderLabels(self.dict_name)
        print(self.table[8])
        print(self.dict_name)
        self.dict_name.clear()

        for j in range(self.col[0]):
            cursor.execute(self.add_string + self.table[8])
            for i in range(self.st[0]):
                self.info_str = cursor.fetchone()
                self.ui.tableWidget_8.setItem(i, j, QTableWidgetItem(str(self.info_str[j])))
        self.ui.tableWidget_8.resizeColumnsToContents()

        self.ui.comboBox_8.clear()
        cursor.execute("select * from КЛИЕНТ")
        wow = cursor.fetchone()
        while wow:
            self.ui.comboBox_8.addItem(str(wow[0]))
            wow = cursor.fetchone()

        self.ui.comboBox_9.clear()
        cursor.execute("select * from СОТРУДНИК")
        wow = cursor.fetchone()
        while wow:
            self.ui.comboBox_9.addItem(str(wow[0]))
            wow = cursor.fetchone()

        self.ui.comboBox_10.clear()
        cursor.execute("select * from ОБЪЕКТ")
        wow = cursor.fetchone()
        while wow:
            self.ui.comboBox_10.addItem(str(wow[0]))
            wow = cursor.fetchone()

    def create_Office(self):
        cursor.execute(self.count_string + " " + self.table[9])  # кол строк
        self.st = cursor.fetchone()
        self.ui.tableWidget_9.setRowCount(self.st[0])

        cursor.execute(self.count_column + self.table[9] + "'")  # кол столбцов
        self.col = cursor.fetchone()
        self.ui.tableWidget_9.setColumnCount(self.col[0])

        cursor.execute(self.name_columns + self.table[9] + "'")
        self.name_col = cursor.fetchone()

        while self.name_col:  # названия столбцов
            self.dict_name.append(self.name_col[0])
            self.name_col = cursor.fetchone()
        self.ui.tableWidget_9.setHorizontalHeaderLabels(self.dict_name)
        print(self.table[9])
        print(self.dict_name)
        self.dict_name.clear()

        for j in range(self.col[0]):
            cursor.execute(self.add_string + self.table[9])
            for i in range(self.st[0]):
                self.info_str = cursor.fetchone()
                self.ui.tableWidget_9.setItem(i, j, QTableWidgetItem(str(self.info_str[j])))
        self.ui.tableWidget_9.resizeColumnsToContents()

    '''Вывод данных из таблиц в формы заполнения'''

    def CellClick_Klient(self, row):
        cursor.execute("select * from КЛИЕНТ")
        info = cursor.fetchall()
        self.id_klenta = info[row][0]
        self.ui.line2.setText(info[row][1])

    def CellClick_Klient_pokupatel(self, row):
        cursor.execute("select * from КЛИЕНТ_ПОКУПАТЕЛЬ")
        info = cursor.fetchall()
        self.id_pokyp = info[row][0]
        self.ui.line3.setText(info[row][1])
        self.ui.line4.setText(info[row][2])
        self.ui.line6.setText(info[row][3])
        self.ui.line7.setText(info[row][4])
        self.ui.line10.setText(info[row][5])

    def CellClick_Klient_prodavec(self, row):
        cursor.execute("select * from КЛИЕНТ_ПРОДАВЕЦ")
        info = cursor.fetchall()
        self.id_prod = info[row][0]
        self.ui.line11.setText(info[row][1])
        self.ui.line12.setText(info[row][2])
        self.ui.line14.setText(info[row][3])
        self.ui.line15.setText(info[row][4])
        self.ui.line18.setText(info[row][5])
        self.ui.line16.setText(info[row][6])
        self.ui.line19.setText(str(info[row][7]))

    def CellClick_Object(self, row):
        cursor.execute("select * from ОБЪЕКТ")
        info = cursor.fetchall()
        self.id_obj = info[row][0]
        self.ui.line21.setText(info[row][1])
        self.ui.line26.setText(info[row][2])
        self.ui.line23.setText(str(info[row][3]))
        self.ui.line24.setText(str(info[row][4]))
        self.ui.line25.setText(str(info[row][5]))
        self.ui.line22.setText(str(info[row][6]))

    def CellClick_Trebovaniya(self, row):
        cursor.execute("select * from ТРЕБОВАНИЯ_К_ОБЪЕКТУ")
        info = cursor.fetchall()
        self.id_treb = info[row][0]
        self.ui.line32.setText(info[row][1])
        self.ui.line35.setText(str(info[row][2]))
        self.ui.line36.setText(str(info[row][3]))
        self.ui.line33.setText(str(info[row][4]))
        self.ui.line34.setText(str(info[row][5]))
        self.ui.line37.setText(str(info[row][6]))

    def CellClick_Sdelka(self, row):
        cursor.execute("select * from СДЕЛКА")
        info = cursor.fetchall()
        self.id_sdelka = info[row][0]
        self.ui.line53.setText(info[row][1])
        self.ui.line54.setText(str(info[row][2]))
        self.ui.line55.setText(str(info[row][3]))
        self.ui.line56.setText(str(info[row][4]))

    '''Добавление записей'''

    def AddData_Klient(self):
        try:
            self.tip_klienta = self.ui.line2.text()
            cursor.execute("INSERT INTO КЛИЕНТ (Тип_клиента) VALUES ('" + self.tip_klienta + "')")
            cursor.commit()
            self.update_database()
        except:
            self.error = QMessageBox.question(
                self, "Message", "Ошибка добавления данных.",
                QMessageBox.Ok)

    def AddData_Klient_pokupatel(self):
        try:
            self.fam = self.ui.line3.text()
            self.imya = self.ui.line4.text()
            self.otch = self.ui.line6.text()
            self.seriya_pass = self.ui.line7.text()
            self.num_pass = self.ui.line10.text()
            self.num_klienta = self.ui.comboBox.currentText()
            self.num_agent = self.ui.comboBox_12.currentText()
            cursor.execute("INSERT INTO КЛИЕНТ_ПОКУПАТЕЛЬ (Код_клиента_покупателя, Фамилия, "
                           "Имя, Отчество, Серия_Паспорта, Номер_Паспорта, Номер_агента) VALUES "
                           "('" + self.num_klienta + "','" + self.fam + "','" + self.imya + "','" + self.otch + "','" + self.seriya_pass + "','" + self.num_pass + "','" + self.num_agent + "')")
            cursor.commit()
            self.update_database()
        except:
            self.error = QMessageBox.question(
                self, "Message", "Ошибка добавления данных.",
                QMessageBox.Ok)

    def AddData_Klient_prodavec(self):
        try:
            self.fam = self.ui.line11.text()
            self.imya = self.ui.line12.text()
            self.otch = self.ui.line14.text()
            self.seriya_pass = self.ui.line15.text()
            self.num_pass = self.ui.line18.text()
            self.ogrn = self.ui.line16.text()
            self.cell = self.ui.line19.text()
            self.num_obj = self.ui.comboBox_11.currentText()
            self.kod_klienta = self.ui.comboBox_2.currentText()
            cursor.execute("INSERT INTO КЛИЕНТ_ПРОДАВЕЦ (Код_клиента_продавца, Фамилия, Имя, Отчество, "
                           "Серия_Паспорта, Номер_Паспорта, Наличие_выписки_из_ЕГРН, Цена_недвижимости, Номер_объекта) VALUES "
                           "('" + self.kod_klienta + "','" + self.fam + "',"
                                                                        "'" + self.imya + "','" + self.otch + "','" + self.seriya_pass + "','" + self.num_pass + "',"
                                                                                                                                                                 "'" + self.ogrn + "','" + self.cell + "','" + self.num_obj + "')")
            cursor.commit()
            self.update_database()
        except:
            self.error = QMessageBox.question(
                self, "Message", "Ошибка добавления данных.",
                QMessageBox.Ok)

    def AddData_Object(self):
        try:
            self.tip_build = self.ui.line21.text()
            self.do_build = self.ui.line26.text()
            self.place = self.ui.line23.text()
            self.room = self.ui.line24.text()
            self.floor = self.ui.line25.text()
            self.cell = self.ui.line22.text()
            self.num_agent = self.ui.comboBox_5.currentText()
            self.num_place = self.ui.comboBox_6.currentText()
            self.num_kind_obj = self.ui.comboBox_7.currentText()
            cursor.execute("INSERT INTO ОБЪЕКТ (Тип_здания, Назначение_здания, Площадь, Количество_комнат,"
                           " Этаж, Выставленная_цена, Номер_сотрудника, Номер_района, Номер_вида_объекта) VALUES "
                           "('" + self.tip_build + "','" + self.do_build + "','" + self.place + "','" + self.room + "','" + self.floor + "',"
                                                                                                                                         "'" + self.cell + "','" + self.num_agent + "','" + self.num_place + "','" + self.num_kind_obj + "')")
            cursor.commit()
            self.update_database()
        except:
            self.error = QMessageBox.question(
                self, "Message", "Ошибка добавления данных.",
                QMessageBox.Ok)

    def AddData_Trebovaniya(self):
        try:
            self.tip_build = self.ui.line32.text()
            self.do_build = self.ui.line37.text()
            self.place = self.ui.line33.text()
            self.room = self.ui.line36.text()
            self.floor = self.ui.line34.text()
            self.cell = self.ui.line35.text()
            self.num_place = self.ui.comboBox_4.currentText()
            self.num_kind_obj = self.ui.comboBox_3.currentText()
            self.kod_klienta = self.ui.comboBox_14.currentText()
            cursor.execute(
                "INSERT INTO ТРЕБОВАНИЯ_К_ОБЪЕКТУ (Код_требования, Тип_здания, Цена, Количество_комнат, Площадь, Этаж, Назначение_здания,"
                " Номер_вида_объекта, Номер_района) VALUES "
                "('" + self.kod_klienta + "','" + self.tip_build + "','" + self.cell + "','" + self.room + "','" + self.place + "','" + self.floor + "',"
                                                                                                                                                     "'" + self.do_build + "','" + self.num_kind_obj + "','" + self.num_place + "')")
            cursor.commit()
            self.update_database()
        except:
            self.error = QMessageBox.question(
                self, "Message", "Ошибка добавления данных.",
                QMessageBox.Ok)

    def AddData_Sdelka(self):
        try:
            self.tip_sdelki = self.ui.line53.text()
            self.full_cell = self.ui.line54.text()
            self.agent_cell = self.ui.line55.text()
            self.klient_cell = self.ui.line56.text()
            self.kod = self.ui.line57.text()
            self.num_agent = self.ui.comboBox_9.currentText()
            self.num_obj = self.ui.comboBox_10.currentText()
            self.num_klienta = self.ui.comboBox_8.currentText()
            cursor.execute(
                "INSERT INTO СДЕЛКА (Код_сделки, Тип_сделки, Итоговая_сумма_для_покупателя, Выплата_сотруднику, Выплата_продавцу, "
                "Номер_сотрудника, Номер_объекта, Номер_клиента) VALUES "
                "('" + str(self.kod) + "','" + str(self.tip_sdelki) + "','" + str(self.full_cell) + "','" + str(
                    self.agent_cell) + "','" + str(self.klient_cell) + "','" + str(self.num_agent) + "',"
                                                                                                     "'" + str(
                    self.num_obj) + "','" + str(self.num_klienta) + "')")
            cursor.commit()
            self.update_database()
        except:
            self.error = QMessageBox.question(
                self, "Message", "Ошибка добавления данных.",
                QMessageBox.Ok)

    '''Обновление записей'''

    def Update_Klient(self):
        try:
            self.tip_klienta = self.ui.line2.text()
            cursor.execute(
                "UPDATE КЛИЕНТ SET Тип_клиента ='" + self.tip_klienta + "' WHERE Код_клиента=" + str(self.id_klenta))
            cursor.commit()
            self.update_database()
        except:
            self.error = QMessageBox.question(
                self, "Message", "Ошибка обновления данных. Выберите строку из таблицы!",
                QMessageBox.Ok)

    def Update_Klient_pokupatel(self):
        try:
            self.fam = self.ui.line3.text()
            self.imya = self.ui.line4.text()
            self.otch = self.ui.line6.text()
            self.seriya_pass = self.ui.line7.text()
            self.num_pass = self.ui.line10.text()
            self.num_klienta = self.ui.comboBox.currentText()
            self.num_agent = self.ui.comboBox_12.currentText()
            cursor.execute(
                "UPDATE КЛИЕНТ_ПОКУПАТЕЛЬ SET Код_клиента_покупателя='" + self.num_klienta + "', Фамилия='" + self.fam + "', "
                                                                                                                         "Имя='" + self.imya + "', Отчество='" + self.otch + "', Серия_Паспорта='" + str(
                    self.seriya_pass) + "'"
                                        ", Номер_Паспорта='" + str(self.num_pass) + "', Номер_агента='" + str(
                    self.num_agent) + "' WHERE Код_клиента_покупателя=" + str(self.id_pokyp))
            cursor.commit()
            self.update_database()
        except:
            self.error = QMessageBox.question(
                self, "Message", "Ошибка обновления данных. Выберите строку из таблицы!",
                QMessageBox.Ok)

    def Update_Klient_prodavec(self):
        try:
            self.fam = self.ui.line11.text()
            self.imya = self.ui.line12.text()
            self.otch = self.ui.line14.text()
            self.seriya_pass = self.ui.line15.text()
            self.num_pass = self.ui.line18.text()
            self.ogrn = self.ui.line16.text()
            self.cell = self.ui.line19.text()
            self.num_obj = self.ui.comboBox_11.currentText()
            self.kod_klienta = self.ui.comboBox_2.currentText()
            cursor.execute("UPDATE КЛИЕНТ_ПРОДАВЕЦ SET Код_клиента_продавца='" + str(
                self.kod_klienta) + "', Фамилия='" + self.fam + "', Имя='" + self.imya + "', Отчество='" + self.otch + "', "
                                                                                                                       "Серия_Паспорта='" + str(
                self.seriya_pass) + "', Номер_Паспорта='" + str(self.num_pass) + "'"
                                                                                 ", Наличие_выписки_из_ЕГРН='" + str(
                self.ogrn) + "', Цена_недвижимости='" + str(self.cell) + "', Номер_объекта='" + str(
                self.num_obj) + "' WHERE Код_клиента_продавца=" + str(self.id_prod))
            cursor.commit()
            self.update_database()
        except:
            self.error = QMessageBox.question(
                self, "Message", "Ошибка обновления данных. Выберите строку из таблицы!",
                QMessageBox.Ok)

    def Update_Object(self):
        try:
            self.tip_build = self.ui.line21.text()
            self.do_build = self.ui.line26.text()
            self.place = self.ui.line23.text()
            self.room = self.ui.line24.text()
            self.floor = self.ui.line25.text()
            self.cell = self.ui.line22.text()
            self.num_agent = self.ui.comboBox_5.currentText()
            self.num_place = self.ui.comboBox_6.currentText()
            self.num_kind_obj = self.ui.comboBox_7.currentText()
            cursor.execute(
                "UPDATE ОБЪЕКТ SET Тип_здания='" + self.tip_build + "', Назначение_здания='" + self.do_build + "', Площадь='" + str(
                    self.place) + "', Количество_комнат='" + str(self.room) + "',"
                                                                              " Этаж='" + str(
                    self.floor) + "', Выставленная_цена='" + str(self.cell) + "', Номер_сотрудника='" + str(
                    self.num_agent) + "', Номер_района='" + str(self.num_place) + "', Номер_вида_объекта='" + str(
                    self.num_kind_obj) + "' WHERE Код_объекта=" + str(self.id_obj))
            cursor.commit()
            self.update_database()
        except:
            self.error = QMessageBox.question(
                self, "Message", "Ошибка обновления данных. Выберите строку из таблицы!",
                QMessageBox.Ok)

    def Update_Trebovaniya(self):
        try:
            self.tip_build = self.ui.line32.text()
            self.do_build = self.ui.line37.text()
            self.place = self.ui.line33.text()
            self.room = self.ui.line36.text()
            self.floor = self.ui.line34.text()
            self.cell = self.ui.line35.text()
            self.num_place = self.ui.comboBox_4.currentText()
            self.num_kind_obj = self.ui.comboBox_3.currentText()
            self.kod_klienta = self.ui.comboBox_14.currentText()
            cursor.execute("UPDATE ТРЕБОВАНИЯ_К_ОБЪЕКТУ SET Код_требования='" + str(
                self.kod_klienta) + "', Тип_здания='" + self.tip_build + "', Цена='" + str(self.cell) + "'"
                                                                                                        ", Количество_комнат='" + str(
                self.room) + "', Площадь='" + str(self.place) + "', Этаж='" + str(
                self.floor) + "', Назначение_здания='" + self.do_build + "',"
                                                                         " Номер_вида_объекта='" + str(
                self.num_kind_obj) + "', Номер_района='" + str(self.num_place) + "' WHERE Код_требования=" + str(
                self.id_treb))

            cursor.commit()
            self.update_database()
        except:
            self.error = QMessageBox.question(
                self, "Message", "Ошибка обновления данных. Выберите строку из таблицы!",
                QMessageBox.Ok)

    def Update_Sdelka(self):
        try:
            self.tip_sdelki = self.ui.line53.text()
            self.full_cell = self.ui.line54.text()
            self.agent_cell = self.ui.line55.text()
            self.klient_cell = self.ui.line56.text()
            self.num_agent = self.ui.comboBox_9.currentText()
            self.num_obj = self.ui.comboBox_10.currentText()
            self.num_klienta = self.ui.comboBox_8.currentText()
            cursor.execute(
                "UPDATE СДЕЛКА SET Тип_сделки='" + self.tip_sdelki + "', Итоговая_сумма_для_покупателя='" + str(
                    self.full_cell) + "', Выплата_сотруднику='" + str(self.agent_cell) + "', Выплата_продавцу='" + str(
                    self.klient_cell) + "', "
                                        "Номер_сотрудника='" + str(self.num_agent) + "', Номер_объекта='" + str(
                    self.num_obj) + "', Номер_клиента='" + str(self.num_klienta) + "' WHERE Код_сделки=" + str(
                    self.id_sdelka))
            cursor.commit()
            self.update_database()
        except:
            self.error = QMessageBox.question(
                self, "Message", "Ошибка обновления данных. Выберите строку из таблицы!",
                QMessageBox.Ok)

app = QtWidgets.QApplication([])
application = Connection()
application.show()
sys.exit(app.exec())