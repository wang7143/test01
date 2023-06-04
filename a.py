import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QGridLayout, QHBoxLayout, QVBoxLayout, QTableWidget, QTableWidgetItem ,QComboBox,QDialog
import sqlite3
from PyQt5.QtCore import pyqtSignal
# 在文件开头
from PyQt5.QtWidgets import QInputDialog
# 统计功能部分代码
from PyQt5.QtCore import QDateTime
from PyQt5.QtWidgets import QFileDialog, QMessageBox

class Card:
    def __init__(self, num, balance):
        self.num = num
        self.balance = balance
        self.is_lost = False

class Machine:
    def __init__(self, id, type, price):
        self.id = id
        self.type = type
        self.price = price
        self.card_num = None
        self.start_time = None
        self.end_time = None
        


# 在Machine类中添加一个end_time属性
class Machine:
    def __init__(self, id, type, price):
        self.id = id
        self.type = type
        self.price = price
        self.card_num = None
        self.start_time = None
        self.end_time = None

    

# 创建一个配置窗口类，继承自QDialog
class ConfigDialog(QDialog):
    config_changed = pyqtSignal(str, float, str)    
    
    def __init__(self):
        super().__init__()
        self.initUI()
        

    def initUI(self):
        # 创建一些控件，用于选择或输入配置信息
        machine_type_label = QLabel('机器类型：')
        self.machine_type_combo = QComboBox()
        self.machine_type_combo.addItems(['1', '2', '3'])
        price_label = QLabel('价格：')
        self.price_edit = QLineEdit()
        date_label = QLabel('日期：')
        self.date_combo = QComboBox()
        self.date_combo.addItems(['工作日', '周末', '节假日'])
        confirm_button = QPushButton('确定')
        cancel_button = QPushButton('取消')

        # 布局控件
        grid = QGridLayout()
        grid.addWidget(machine_type_label, 0, 0)
        grid.addWidget(self.machine_type_combo, 0, 1)
        grid.addWidget(price_label, 1, 0)
        grid.addWidget(self.price_edit, 1, 1)
        grid.addWidget(date_label, 2, 0)
        grid.addWidget(self.date_combo, 2, 1)
        grid.addWidget(confirm_button, 3, 0)
        grid.addWidget(cancel_button, 3, 1)
        self.setLayout(grid)

        # 连接信号槽
        confirm_button.clicked.connect(self.confirm)
        cancel_button.clicked.connect(self.cancel)

    def confirm(self):
        machine_type = self.machine_type_combo.currentText() # 获取当前选择的机器类型
        price = float(self.price_edit.text()) # 获取输入的价格，并转换成浮点数
        date = self.date_combo.currentText() # 获取当前选择的日期
        # 获取配置信息，并更新相应的机器价格
        self.config_changed.emit(machine_type, price, date) # 发射信号，并传递参数
        self.close() # 关闭窗口
        
        # 省略具体的更新逻辑，可以用一个字典来存储不同类型和日期的价格
        

    def cancel(self):
        # 关闭窗口
        self.close()

    


class ManagementSystem(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.cards = [] # 存储卡号信息
        self.machines = [] # 存储机器信息
        self.config_dialog = None
        self.machines = [] # 初始化列表
        machine1 = Machine(1, '1', 1) # 创建一个类型为1，价格为1的Machine对象
        machine2 = Machine(2, '2', 2) # 创建一个类型为2，价格为2的Machine对象
        machine3 = Machine(3, '3', 3) # 创建一个类型为3，价格为3的Machine对象
        self.machines.append(machine1) # 把Machine对象添加到列表中
        self.machines.append(machine2) # 把Machine对象添加到列表中
        self.machines.append(machine3) # 把Machine对象添加到列表中

    def initUI(self):
        # 卡号管理部分UI
        card_num_label = QLabel('卡号：')
        self.card_num_edit = QLineEdit()
        balance_label = QLabel('余额：')
        self.balance_edit = QLineEdit()
        self.balance_edit.setReadOnly(True)

        new_card_button = QPushButton('新建卡号')
        delete_card_button = QPushButton('删除卡号')
        query_button = QPushButton('查询卡号')
        recharge_button = QPushButton('充值')
        lost_button = QPushButton('挂失')
        unlost_button = QPushButton('解挂')
        unlost_button1 = QPushButton('设置')
        
        

        card_vbox = QVBoxLayout()
        card_vbox.addWidget(card_num_label)
        card_vbox.addWidget(self.card_num_edit)
        card_vbox.addWidget(balance_label)
        card_vbox.addWidget(self.balance_edit)

        card_hbox = QHBoxLayout()
        card_hbox.addLayout(card_vbox)
        card_hbox.addWidget(new_card_button)
        card_hbox.addWidget(delete_card_button)
        card_hbox.addWidget(query_button)
        card_hbox.addWidget(recharge_button)
        card_hbox.addStretch()
        card_hbox.addWidget(lost_button)
        card_hbox.addWidget(unlost_button)
        card_hbox.addWidget(unlost_button1)

        # 上级管理部分UI
        machine1_label = QLabel('机器1')
        machine2_label = QLabel('机器2')
        machine3_label = QLabel('机器3')
        status_label = QLabel('状态')
        price_label = QLabel('价格')
        card_num_label1 = QLabel('卡号')
        card_num_label2 = QLabel('卡号')
        card_num_label3 = QLabel('卡号')

        self.machine1_price_label = QLabel('1')
        self.machine2_price_label = QLabel('2')
        self.machine3_price_label = QLabel('3')

        self.machine1_card_num_edit = QLineEdit()
        self.machine2_card_num_edit = QLineEdit()
        self.machine3_card_num_edit = QLineEdit()

        self.machine1_status_label = QLabel('空闲')
        self.machine2_status_label = QLabel('空闲')
        self.machine3_status_label = QLabel('空闲')

        self.start_button1 = QPushButton('上机')
        self.end_button1 = QPushButton('下机')
        self.start_button2 = QPushButton('上机')
        self.end_button2 = QPushButton('下机')
        self.start_button3 = QPushButton('上机')
        self.end_button3 = QPushButton('下机')
        
        


        machine_grid = QGridLayout()
        machine_grid.addWidget(machine1_label, 0, 0)
        machine_grid.addWidget(status_label, 1, 0)
        machine_grid.addWidget(self.machine1_status_label, 1, 1)
        machine_grid.addWidget(price_label, 2, 0)
        machine_grid.addWidget(self.machine1_price_label, 2, 1)
        machine_grid.addWidget(card_num_label1, 3, 0)
        machine_grid.addWidget(self.machine1_card_num_edit, 3, 1)
        machine_grid.addWidget(self.start_button1, 4, 0)
        machine_grid.addWidget(self.end_button1, 4, 1)

        machine_grid.addWidget(machine2_label, 0, 2)
        new_status_label = QLabel(status_label.text())
        machine_grid.addWidget(new_status_label, 1, 2)

        machine_grid.addWidget(self.machine2_status_label, 1, 3)
        new_price_label = QLabel(price_label.text())
        machine_grid.addWidget(new_price_label, 2, 2)

        machine_grid.addWidget(self.machine2_price_label, 2, 3)
        machine_grid.addWidget(card_num_label2, 3, 2)
        machine_grid.addWidget(self.machine2_card_num_edit, 3, 3)
        machine_grid.addWidget(self.start_button2, 4, 2)
        machine_grid.addWidget(self.end_button2, 4, 3)

        machine_grid.addWidget(machine3_label, 0, 4)
        new_status_label = QLabel(status_label.text())
        machine_grid.addWidget(new_status_label, 1, 4)

        machine_grid.addWidget(self.machine3_status_label, 1, 5)
        new_price_label = QLabel(price_label.text())
        machine_grid.addWidget(new_price_label, 2, 4)

        machine_grid.addWidget(self.machine3_price_label, 2, 5)
        machine_grid.addWidget(card_num_label3, 3, 4)
        machine_grid.addWidget(self.machine3_card_num_edit, 3, 5)
        machine_grid.addWidget(self.start_button3, 4, 4)
        machine_grid.addWidget(self.end_button3, 4, 5)

        # 统计功能部分UI
        self.stat_table = QTableWidget()
        self.stat_table.setColumnCount(3)
        self.stat_table.setHorizontalHeaderLabels(['机器号', '卡号', '开始时间'])
        vbox = QVBoxLayout()
        vbox.addWidget(self.stat_table)

        # 整体布局
        main_vbox = QVBoxLayout()
        main_vbox.addLayout(card_hbox)
        main_vbox.addLayout(machine_grid)
        main_vbox.addLayout(vbox)
        self.setLayout(main_vbox)

        # 信号槽连接
        new_card_button.clicked.connect(self.new_card)
        delete_card_button.clicked.connect(self.delete_card)
        query_button.clicked.connect(self.query_card)
        recharge_button.clicked.connect(self.recharge)
        lost_button.clicked.connect(self.card_lost)
        unlost_button.clicked.connect(self.card_unlost)
        unlost_button1.clicked.connect(self.open_config)
        self.start_button1.clicked.connect(lambda : self.start_machine(1))
        self.end_button1.clicked.connect(lambda : self.end_machine(1))
        self.start_button2.clicked.connect(lambda : self.start_machine(2))
        self.end_button2.clicked.connect(lambda : self.end_machine(2))
        self.start_button3.clicked.connect(lambda : self.start_machine(3))
        self.end_button3.clicked.connect(lambda : self.end_machine(3))

    def update_price(self, machine_type, price, date):
        # 根据机器类型，更新相应的价格标签
        if machine_type == '1':
            self.machine1_price_label.setText(str(price))
        elif machine_type == '2':
            self.machine2_price_label.setText(str(price))
        elif machine_type == '3':
            self.machine3_price_label.setText(str(price))

    # 在ManagementSystem类中添加一个打开配置窗口的方法
    def open_config(self):
        self.config_dialog = ConfigDialog()
        self.config_dialog.config_changed.connect(self.update_price) # 连接信号和槽函数
        self.config_dialog.exec_()
        
    # 卡号管理部分函数

    def new_card(self):
        # 新建卡号函数，生成一个随机的卡号和初始余额，并添加到self.cards列表中
        import random
        num = random.randint(100000, 999999) # 生成一个6位数的卡号
        balance = random.randint(10, 100) # 生成一个10到100之间的初始余额
        card = Card(num, balance) # 创建一个Card对象
        self.cards.append(card) # 添加到self.cards列表中
        self.card_num_edit.setText(str(num)) # 显示卡号
        self.balance_edit.setText(str(balance)) # 显示余额

    def delete_card(self):
        # 删除卡号函数，根据输入的卡号，从self.cards列表中删除对应的Card对象
        num = int(self.card_num_edit.text()) # 获取输入的卡号
        for card in self.cards: # 遍历self.cards列表
            if card.num == num: # 如果找到匹配的卡号
                self.cards.remove(card) # 删除该Card对象
                break # 跳出循环
        self.card_num_edit.clear() # 清空卡号输入框
        self.balance_edit.clear() # 清空余额显示框

    def recharge(self):
        # 充值函数，根据输入的卡号和金额，给对应的Card对象增加余额
        num = int(self.card_num_edit.text()) # 获取输入的卡号
        amount = int(self.balance_edit.text()) # 获取输入的金额
        for card in self.cards: # 遍历self.cards列表
            if card.num == num: # 如果找到匹配的卡号
                card.balance += amount # 增加余额
                break # 跳出循环
        self.balance_edit.setText(str(card.balance)) # 显示更新后的余额

    def card_lost(self):
        # 挂失函数，根据输入的卡号，将对应的Card对象的is_lost属性设为True
        num = int(self.card_num_edit.text()) # 获取输入的卡号
        for card in self.cards: # 遍历self.cards列表
            if card.num == num: # 如果找到匹配的卡号
                card.is_lost = True # 设为挂失状态
                break # 跳出循环

    def card_unlost(self):
        # 解挂函数，根据输入的卡号，将对应的Card对象的is_lost属性设为False
        num = int(self.card_num_edit.text()) # 获取输入的卡号
        for card in self.cards: # 遍历self.cards列表
            if card.num == num: # 如果找到匹配的卡号
                card.is_lost = False # 设为正常状态
                break # 跳出循环

    # 上机管理部分函数

    def start_machine(self, machine_id):
        machine = self.machines[machine_id - 1] # 从列表中找到对应的Machine对象
        machine.start_time = QDateTime.currentDateTime()
        machine.card_num = int(self.card_num_edit.text())
        # 上机函数，根据输入的卡号和机器id，验证是否可以上机，并记录上机时间和消费金额等信息
        import time
        num = int(getattr(self, f"machine{machine_id}_card_num_edit").text())  # 获取输入的卡号，根据id动态获取控件属性
        for card in self.cards: # 遍历self.cards列表
            if card.num == num: # 如果找到匹配的卡号
                if card.is_lost: # 如果是挂失状态，提示无法上机，并返回
                    print("该卡已挂失，无法上机")
                    return 
                if card.balance < int(getattr(self, f"machine{machine_id}_price_label").text()): # 将价格转换为浮点数
                    print("该卡余额不足，无法上机")
                    return 
                machine = Machine(machine_id, "普通", getattr(self, f"machine{machine_id}_price_label").text()) # 创建一个Machine对象，根据id动态获取控件属性
                machine.card_num = num # 记录卡号
                machine.start_time = time.time() # 记录上机时间
                self.machines.append(machine) # 添加到self.machines列表中
                getattr(self, f"machine{machine_id}_status_label").setText("使用中") # 更新机器状态，根据id动态获取控件属性
                break # 跳出循环


    def update_stat_table(self, id, num, start_time, end_time, cost):
        # 更新统计表格的函数，根据输入的参数，在表格中添加一行记录，并更新数据库中的数据
        import datetime
        row = self.stat_table.rowCount() # 获取当前表格的行数
        self.stat_table.insertRow(row) # 在表格中插入一行
        self.stat_table.setItem(row, 0, QTableWidgetItem(str(id))) # 设置第一列为机器号
        self.stat_table.setItem(row, 1, QTableWidgetItem(str(num))) # 设置第二列为卡号
        start_time_str = datetime.datetime.fromtimestamp(start_time).strftime("%Y-%m-%d %H:%M:%S") # 将上机时间转换为字符串格式
        self.stat_table.setItem(row, 2, QTableWidgetItem(start_time_str)) # 设置第三列为上机时间
        end_time_str = datetime.datetime.fromtimestamp(end_time).strftime("%Y-%m-%d %H:%M:%S") # 将下机时间转换为字符串格式
        self.stat_table.setItem(row, 3, QTableWidgetItem(end_time_str)) # 设置第四列为下机时间
        self.stat_table.setItem(row, 4, QTableWidgetItem(str(cost))) # 设置第五列为消费金额

        # 费用设置配置功能部分函数

    def set_price(self):
        # 设置价格的函数，根据输入的价格和类型，更新界面和数据库中的价格信息
        price = float(self.price_edit.text()) # 获取输入的价格，转换为浮点数
        _type = self.type_combo.currentText() # 获取选择的类型，普通或者高级
        if _type == "普通": # 如果是普通类型，更新所有普通机器的价格显示和数据库信息
            for id in range(1, 4): 
                getattr(self, f"machine{id}_price_label").setText(str(price)) 
                self.update_price_in_db(id, price)
        else: # 如果是高级类型，更新所有高级机器的价格显示和数据库信息
            for id in range(4, 7):
                getattr(self, f"machine{id}_price_label").setText(str(price))
                self.update_price_in_db(id, price)

    def update_price_in_db(self, id, price):
    # 更新数据库
        conn = sqlite3.connect("machine.db") # 连接到数据库文件
        cursor = conn.cursor() # 创建一个游标对象
        sql = f"UPDATE machine SET price = {price} WHERE id = {id}" # 构造一个更新语句
        cursor.execute(sql) # 执行更新语句
        conn.commit() # 提交更改
        cursor.close() # 关闭游标
        conn.close() # 关闭连接

   
    def end_machine(self, machine_id):
        # 省略其他代码
        machine = self.machines[machine_id - 1]
        machine.end_time = QDateTime.currentDateTime() # 记录当前时间
        row_count = self.stat_table.rowCount()
        self.stat_table.insertRow(row_count)
        self.stat_table.setItem(row_count, 0, QTableWidgetItem(str(machine.id)))
        self.stat_table.setItem(row_count, 1, QTableWidgetItem(str(machine.card_num)))
        self.stat_table.setItem(row_count, 2, QTableWidgetItem(machine.start_time.toString('yyyy-MM-dd hh:mm:ss')))
        self.stat_table.setItem(row_count, 3, QTableWidgetItem(machine.end_time.toString('yyyy-MM-dd hh:mm:ss')))
        seconds = machine.start_time.secsTo(machine.end_time) # 计算使用机器的秒数
        cost = seconds * machine.price / 60 # 计算使用机器的费用，假设是按分钟收费
        cost = int(cost) + int(machine.price)
        # num = int(getattr(self, f"machine{id}_card_num_edit").text()) # 获取输入的卡号，根据id动态获取控件属性
        for card in self.cards: # 从卡列表中找到对应的卡对象
            if card.num == machine.card_num:
                card.balance -= cost # 从卡的余额中扣除费用
                if card.num == int(self.card_num_edit.text()): # 如果当前显示的是这张卡的信息，就更新余额显示
                    self.balance_edit.setText(str(card.balance))
                break
        # 在end_machine方法中
        if machine_id == 1: # 根据机器号，更新相应的状态标签和卡号输入框
            self.machine1_status_label.setText('空闲')
            self.machine1_card_num_edit.clear()
        elif machine_id == 2:
            self.machine2_status_label.setText('空闲')
            self.machine2_card_num_edit.clear()
        elif machine_id == 3:
            self.machine3_status_label.setText('空闲')
            self.machine3_card_num_edit.clear()
        row_count = self.stat_table.rowCount()
        # self.stat_table.insertRow(row_count)
        self.stat_table.setItem(row_count, 0, QTableWidgetItem(str(machine.id)))
        self.stat_table.setItem(row_count, 1, QTableWidgetItem(str(machine.card_num)))
        self.stat_table.setItem(row_count, 2, QTableWidgetItem(machine.start_time.toString('yyyy-MM-dd hh:mm:ss')))
        self.stat_table.setItem(row_count, 3, QTableWidgetItem(machine.end_time.toString('yyyy-MM-dd hh:mm:ss')))
        self.stat_table.insertRow(row_count)
    # 添加一个保存报表的方法，可以选择保存为csv或txt格式
    def save_report(self):
        file_name, file_type = QFileDialog.getSaveFileName(self, '保存报表', '', 'CSV files (*.csv);;Text files (*.txt)')
        if file_name:
            with open(file_name, 'w') as f:
                if file_type == 'CSV files (*.csv)':
                    f.write('机器号,卡号,开始时间,结束时间\n')
                    for i in range(self.stat_table.rowCount()):
                        f.write(','.join([self.stat_table.item(i,j).text() for j in range(4)]) + '\n')
                elif file_type == 'Text files (*.txt)':
                    f.write('机器号\t卡号\t开始时间\t结束时间\n')
                    for i in range(self.stat_table.rowCount()):
                        f.write('\t'.join([self.stat_table.item(i,j).text() for j in range(4)]) + '\n')
            QMessageBox.information(self, '提示', '报表已保存')

    # 添加一个查询卡号的方法，可以输入卡号，显示其上机情况
    def query_card(self):
        card_num = QInputDialog.getInt(self, '查询卡号', '请输入卡号：')
        if card_num[1]:
            result = []
            for i in range(self.stat_table.rowCount()):
                if self.stat_table.item(i, 1).text() == str(card_num[0]):
                    result.append([self.stat_table.item(i,j).text() for j in range(4)])
            if result:
                QMessageBox.information(self, '查询结果', '\n'.join(['\t'.join(r) for r in result]))
            else:
                QMessageBox.warning(self, '查询结果', '没有找到该卡号的上机记录')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ms = ManagementSystem()
    ms.show()
    sys.exit(app.exec_())
