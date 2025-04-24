import sys
import io
import sqlite3
import folium
from PyQt6 import uic
from PyQt6.QtWebEngineWidgets import QWebEngineView
from PyQt6.QtWidgets import QApplication, QMainWindow, QTableWidgetItem, QInputDialog, QMessageBox, QPlainTextEdit

DATABASE = "ProjDb.db"

MOS_COORDS = [([55.749853, 37.537020], 'Москва-Сити', 8, 8), ([55.713126, 37.541422], 'Воробьевы Горы', 5.9, 4.1),
              ([55.628241, 37.563677], 'Битца', 2.3, 1.1), ([55.763637, 37.445481], 'Строгино', 4.5, 3),
              ([55.816686, 37.611600], 'ВДНХ', 7, 7), ([55.627512, 37.694004], 'Царицыно', 6.9, 7),
              ([55.848843, 37.728767], 'Лосиный Остров', 1.2, 1), ([55.659942, 37.662291], 'Коломенское', 7.4, 6),
              ([55.731220, 37.600704], 'Парк Горького', 6.8, 7),
              ([55.698837, 37.707587], 'Нагатинский Затон', 6.9, 6.9),
              ([55.751169, 37.612464], 'Красная Площадь', 7.7, 8), ([55.844008, 37.468894], 'Речной вокзал', 6.9, 6),
              ([55.775228, 37.763203], 'Измайлово', 2.1, 1.7), ([55.656637, 37.467807], 'Тропарево', 5, 4),
              ([55.814904, 37.551343], 'Тимирязевский район', 6.9, 7),
              ([55.691032, 37.589121], 'Академический район', 7.4, 6.4),
              ([55.675603, 37.756233], 'Люблино', 6.8, 6), ([55.656017, 37.835771], 'Котельники', 7.2, 7),
              ([55.698872, 37.480085], 'Кинематографический квартал', 7, 7.4),
              ([55.715932, 37.412900], 'Можайский район', 7.4, 7.4),
              ([55.883797, 37.552636], 'Дегунино', 6.9, 6.2), ([55.876011, 37.617004], 'Медведково', 7, 5.9),
              ([55.805857, 37.661461], 'Сокольники', 3, 1.9), ([55.767516, 37.689812], 'Лефортово', 6.1, 7.2),
              ([55.730777, 37.815186], 'Вешняки', 6, 6.5), ([55.730777, 37.815186], 'Бирюлёво', 7, 6.7)]


class MoscowMap:
    def __init__(self):
        self.map = folium.Map(location=[55.751783, 37.623642], zoom_start=10)
        self.loc = [55.751783, 37.623642]
        self.markers = []
        self.top_air = sorted(MOS_COORDS, key=lambda x: x[2])[:5]
        self.top_noise = sorted(MOS_COORDS, key=lambda x: x[3])[:5]
        for elem in MOS_COORDS:
            air, noise = elem[2], elem[3]
            popup = f'{elem[1]}.\n воздух-{air} шум-{noise}'
            color = None
            if (air + noise) / 2 <= 3:
                color = '#7cfc00'
            elif 3 < (air + noise) / 2 <= 6:
                color = '#f7e00a'
            elif 6 < (air + noise) / 2 <= 8:
                color = '#f7980a'
            else:
                color = '#ff4500'
            folium.Marker(elem[0], popup=popup, icon=folium.Icon(icon='cloud', color='white',
                                                                 icon_color=color, prefix='fa')).add_to(self.map)

    def show(self):
        self.map.show_in_browser()


SPB_COORDS = [([59.941081, 30.317631], 'Центр', 8.2, 7.7), ([59.972888, 30.224723], 'Зенит арена', 7.1, 5.4),
              ([59.927249, 30.236472], 'Севкабель порт', 6.8, 5), ([59.962177, 30.299465], 'Петроградскй остров', 8, 6.9),
              ([59.942524, 30.186356], 'Морской Порт', 5.9, 4.6), ([59.939838, 30.260718], 'Васильевский остров', 7.7, 6.8),
              ([59.921963, 30.315275], 'Река Фонтанка', 8, 7.2), ([59.869476, 30.328729], 'Парк Победы', 6, 4),
              ([59.923274, 30.385698], 'Александро-Невская Лавра', 7, 6), ([60.021637, 30.352435], 'Парк Сосновка', 3.7, 2),
              ([59.914400, 30.467052], 'Невский район', 7.1, 5.9),
              ([59.864643, 30.400984], 'Фрунзенский район', 7.1, 6.2),
              ([59.888202, 30.184059], 'Канонерский остров', 6, 4.2), ([59.990601, 30.160678], 'Лахта', 5, 4.1),
              ([60.050234, 30.283695], 'Новоорловский Заповедник', 2.9, 1.9),
              ([59.957976, 30.468765], 'Красногвардейский район', 7.2, 5.9),
              ([60.037398, 30.282470], 'Орловский карьер', 6.9, 6.4), ([59.973886, 30.387137], 'Полюстрово', 7.1, 7)]


class PeterMap:
    def __init__(self):
        self.map = folium.Map(location=[59.941081, 30.317631], zoom_start=11)
        self.loc = [59.941081, 30.317631]
        self.top_air = sorted(SPB_COORDS, key=lambda x: x[2])[:5]
        self.top_noise = sorted(SPB_COORDS, key=lambda x: x[3])[:5]
        folium.Marker([59.937224, 30.336738], popup='Центр. воздух - 8.2 шум - 7.7',
                      icon=folium.Icon(icon='cloud', color='white', icon_color='#f7980a')).add_to(self.map)
        for elem in SPB_COORDS:
            air, noise = elem[2], elem[3]
            popup = f'{elem[1]}.\n воздух-{air} шум-{noise}'
            color = None
            if (air + noise) / 2 <= 3:
                color = '#7cfc00'
            elif 3 < (air + noise) / 2 <= 6:
                color = '#f7e00a'
            elif 6 < (air + noise) / 2 <= 8:
                color = '#f7980a'
            else:
                color = '#ff4500'
            folium.Marker(elem[0], popup=popup, icon=folium.Icon(icon='cloud', color='white',
                                                                 icon_color=color, prefix='fa')).add_to(self.map)

    def show(self):
        self.map.show_in_browser()


template = '''
<?xml version="1.0" encoding="UTF-8"?>
<ui version="4.0">
 <class>MainWindow</class>
 <widget class="QMainWindow" name="MainWindow">
  <property name="geometry">
   <rect>
    <x>0</x>
    <y>0</y>
    <width>1112</width>
    <height>655</height>
   </rect>
  </property>
  <property name="windowTitle">
   <string>MainWindow</string>
  </property>
  <widget class="QWidget" name="centralwidget">
   <widget class="QComboBox" name="cityChoiceBox">
    <property name="geometry">
     <rect>
      <x>20</x>
      <y>160</y>
      <width>211</width>
      <height>51</height>
     </rect>
    </property>
    <property name="styleSheet">
     <string notr="true">QComboBox:focus {
	border: 2px solid rgb(1, 1, 1)
}
</string>
    </property>
    <property name="editable">
     <bool>true</bool>
    </property>
   </widget>
   <widget class="QWidget" name="horizontalLayoutWidget">
    <property name="geometry">
     <rect>
      <x>400</x>
      <y>40</y>
      <width>561</width>
      <height>32</height>
     </rect>
    </property>
    <property name="font">
     <font>
      <pointsize>10</pointsize>
     </font>
    </property>
    <layout class="QHBoxLayout" name="horizontalLayout">
     <item>
      <widget class="QPushButton" name="pushButton_2">
       <property name="font">
        <font>
         <pointsize>10</pointsize>
        </font>
       </property>
       <property name="styleSheet">
        <string notr="true">background-color: rgb(124, 252, 0);
border-radius: 10px;</string>
       </property>
       <property name="text">
        <string>1-3</string>
       </property>
      </widget>
     </item>
     <item>
      <widget class="QPushButton" name="pushButton_5">
       <property name="font">
        <font>
         <pointsize>10</pointsize>
        </font>
       </property>
       <property name="styleSheet">
        <string notr="true">background-color: rgb(247, 224, 10);
border-radius: 10px;</string>
       </property>
       <property name="text">
        <string>4-6</string>
       </property>
      </widget>
     </item>
     <item>
      <widget class="QPushButton" name="pushButton_4">
       <property name="font">
        <font>
         <pointsize>10</pointsize>
        </font>
       </property>
       <property name="styleSheet">
        <string notr="true">background-color: rgb(247, 152, 10);
border-radius: 10px;</string>
       </property>
       <property name="text">
        <string>7-8</string>
       </property>
      </widget>
     </item>
     <item>
      <widget class="QPushButton" name="pushButton_3">
       <property name="font">
        <font>
         <pointsize>10</pointsize>
        </font>
       </property>
       <property name="styleSheet">
        <string notr="true">background-color: rgb(255, 69, 0);
border-radius: 10px;</string>
       </property>
       <property name="text">
        <string>9-10</string>
       </property>
      </widget>
     </item>
    </layout>
   </widget>
   <widget class="QPushButton" name="apply_btn">
    <property name="geometry">
     <rect>
      <x>20</x>
      <y>440</y>
      <width>211</width>
      <height>31</height>
     </rect>
    </property>
    <property name="font">
     <font>
      <pointsize>10</pointsize>
     </font>
    </property>
    <property name="styleSheet">
     <string notr="true">QPushButton {
	border-radius: 7px;
	background-color: rgb(255, 255, 255)
}

QPushButton:hover {
	background-color: rgb(245, 245, 245);
	border: 2px solid rgb(1, 1, 1) 
}</string>
    </property>
    <property name="text">
     <string>применить</string>
    </property>
   </widget>
   <widget class="QPushButton" name="feedbackButton">
    <property name="geometry">
     <rect>
      <x>20</x>
      <y>520</y>
      <width>211</width>
      <height>31</height>
     </rect>
    </property>
    <property name="font">
     <font>
      <pointsize>10</pointsize>
     </font>
    </property>
    <property name="styleSheet">
     <string notr="true">QPushButton {
	border-radius: 7px;
	background-color: rgb(255, 255, 255)
}

QPushButton:hover {
	background-color: rgb(245, 245, 245);
	border: 2px solid rgb(1, 1, 1) 
}</string>
    </property>
    <property name="text">
     <string>оставить отзыв</string>
    </property>
   </widget>
   <widget class="QLabel" name="label_2">
    <property name="geometry">
     <rect>
      <x>90</x>
      <y>130</y>
      <width>141</width>
      <height>16</height>
     </rect>
    </property>
    <property name="font">
     <font>
      <pointsize>12</pointsize>
     </font>
    </property>
    <property name="text">
     <string>город:</string>
    </property>
   </widget>
   <widget class="QLabel" name="cityLabel">
    <property name="geometry">
     <rect>
      <x>20</x>
      <y>10</y>
      <width>381</width>
      <height>51</height>
     </rect>
    </property>
    <property name="font">
     <font>
      <pointsize>11</pointsize>
     </font>
    </property>
    <property name="text">
     <string>карта воздушного и шумового загрязнения
 города Москва</string>
    </property>
   </widget>
   <widget class="QWidget" name="horizontalLayoutWidget_2">
    <property name="geometry">
     <rect>
      <x>290</x>
      <y>110</y>
      <width>791</width>
      <height>491</height>
     </rect>
    </property>
    <layout class="QHBoxLayout" name="lay"/>
   </widget>
   <widget class="QPushButton" name="see_feed">
    <property name="geometry">
     <rect>
      <x>20</x>
      <y>560</y>
      <width>211</width>
      <height>31</height>
     </rect>
    </property>
    <property name="font">
     <font>
      <pointsize>10</pointsize>
     </font>
    </property>
    <property name="styleSheet">
     <string notr="true">QPushButton {
	border-radius: 7px;
	background-color: rgb(255, 255, 255)
}

QPushButton:hover {
	background-color: rgb(245, 245, 245);
	border: 2px solid rgb(1, 1, 1) 
}</string>
    </property>
    <property name="text">
     <string>посмотреть отзывы</string>
    </property>
   </widget>
   <widget class="QToolButton" name="instr_btn">
    <property name="geometry">
     <rect>
      <x>90</x>
      <y>90</y>
      <width>51</width>
      <height>26</height>
     </rect>
    </property>
    <property name="font">
     <font>
      <pointsize>11</pointsize>
     </font>
    </property>
    <property name="styleSheet">
     <string notr="true">QToolhButton {
	border-radius: 7px;
	background-color: rgb(255, 255, 255)
}

QToolButton:hover {
	background-color: rgb(245, 245, 245);
	border: 2px solid rgb(1, 1, 1);
	border-radius: 5px
}</string>
    </property>
    <property name="text">
     <string>...</string>
    </property>
   </widget>
  </widget>
  <widget class="QMenuBar" name="menubar">
   <property name="geometry">
    <rect>
     <x>0</x>
     <y>0</y>
     <width>1112</width>
     <height>26</height>
    </rect>
   </property>
  </widget>
  <widget class="QStatusBar" name="statusbar"/>
 </widget>
 <resources/>
 <connections/>
</ui>
'''

sec_wind = '''
<?xml version="1.0" encoding="UTF-8"?>
<ui version="4.0">
 <class>SecondWindow</class>
 <widget class="QMainWindow" name="SecondWindow">
  <property name="geometry">
   <rect>
    <x>0</x>
    <y>0</y>
    <width>690</width>
    <height>406</height>
   </rect>
  </property>
  <property name="windowTitle">
   <string>MainWindow</string>
  </property>
  <widget class="QWidget" name="centralwidget">
   <widget class="QTableWidget" name="tableWidget">
    <property name="geometry">
     <rect>
      <x>10</x>
      <y>10</y>
      <width>661</width>
      <height>341</height>
     </rect>
    </property>
   </widget>
  </widget>
  <widget class="QMenuBar" name="menubar">
   <property name="geometry">
    <rect>
     <x>0</x>
     <y>0</y>
     <width>690</width>
     <height>26</height>
    </rect>
   </property>
  </widget>
  <widget class="QStatusBar" name="statusbar"/>
 </widget>
 <resources/>
 <connections/>
</ui>
'''

form_win = '''
<?xml version="1.0" encoding="UTF-8"?>
<ui version="4.0">
 <class>MainWindow</class>
 <widget class="QMainWindow" name="MainWindow">
  <property name="geometry">
   <rect>
    <x>0</x>
    <y>0</y>
    <width>788</width>
    <height>401</height>
   </rect>
  </property>
  <property name="windowTitle">
   <string>MainWindow</string>
  </property>
  <widget class="QWidget" name="centralwidget">
   <widget class="QLineEdit" name="EmailEdit">
    <property name="geometry">
     <rect>
      <x>200</x>
      <y>10</y>
      <width>501</width>
      <height>31</height>
     </rect>
    </property>
    <property name="font">
     <font>
      <pointsize>10</pointsize>
     </font>
    </property>
   </widget>
   <widget class="QSpinBox" name="RatingEdit">
    <property name="geometry">
     <rect>
      <x>200</x>
      <y>130</y>
      <width>501</width>
      <height>31</height>
     </rect>
    </property>
    <property name="font">
     <font>
      <pointsize>10</pointsize>
     </font>
    </property>
    <property name="maximum">
     <number>5</number>
    </property>
    <property name="value">
     <number>5</number>
    </property>
   </widget>
   <widget class="QLabel" name="label_4">
    <property name="geometry">
     <rect>
      <x>100</x>
      <y>180</y>
      <width>81</width>
      <height>31</height>
     </rect>
    </property>
    <property name="font">
     <font>
      <pointsize>12</pointsize>
     </font>
    </property>
    <property name="text">
     <string>отзыв</string>
    </property>
   </widget>
   <widget class="QLineEdit" name="NameEdit">
    <property name="geometry">
     <rect>
      <x>200</x>
      <y>70</y>
      <width>501</width>
      <height>31</height>
     </rect>
    </property>
    <property name="font">
     <font>
      <pointsize>10</pointsize>
     </font>
    </property>
   </widget>
   <widget class="QLabel" name="label_5">
    <property name="geometry">
     <rect>
      <x>100</x>
      <y>130</y>
      <width>81</width>
      <height>31</height>
     </rect>
    </property>
    <property name="font">
     <font>
      <pointsize>12</pointsize>
     </font>
    </property>
    <property name="text">
     <string>рейтинг</string>
    </property>
   </widget>
   <widget class="QLabel" name="label_6">
    <property name="geometry">
     <rect>
      <x>100</x>
      <y>70</y>
      <width>61</width>
      <height>31</height>
     </rect>
    </property>
    <property name="font">
     <font>
      <pointsize>12</pointsize>
     </font>
    </property>
    <property name="text">
     <string>имя</string>
    </property>
   </widget>
   <widget class="QLabel" name="label_7">
    <property name="geometry">
     <rect>
      <x>100</x>
      <y>10</y>
      <width>91</width>
      <height>31</height>
     </rect>
    </property>
    <property name="font">
     <font>
      <pointsize>12</pointsize>
     </font>
    </property>
    <property name="text">
     <string>почта</string>
    </property>
   </widget>
   <widget class="QPushButton" name="send_btn">
    <property name="geometry">
     <rect>
      <x>90</x>
      <y>300</y>
      <width>301</width>
      <height>31</height>
     </rect>
    </property>
    <property name="font">
     <font>
      <pointsize>10</pointsize>
     </font>
    </property>
    <property name="styleSheet">
     <string notr="true">QPushButton {
	border-radius: 7px;
	background-color: rgb(250, 250, 250);
	border: 1px solid rgb(110, 110, 110);
}

QPushButton:hover {
	background-color: rgb(245, 245, 245);
	border: 2px solid rgb(1, 1, 1);
}</string>
    </property>
    <property name="text">
     <string>отправить</string>
    </property>
   </widget>
   <widget class="QPushButton" name="cancel_btn">
    <property name="geometry">
     <rect>
      <x>410</x>
      <y>300</y>
      <width>291</width>
      <height>31</height>
     </rect>
    </property>
    <property name="font">
     <font>
      <pointsize>10</pointsize>
     </font>
    </property>
    <property name="styleSheet">
     <string notr="true">QPushButton {
	border-radius: 7px;
	background-color: rgb(250, 250, 250);
	border: 1px solid rgb(110, 110, 110);
}

QPushButton:hover {
	background-color: rgb(245, 245, 245);
	border: 2px solid rgb(1, 1, 1);
}</string>
    </property>
    <property name="text">
     <string>отмена</string>
    </property>
   </widget>
   <widget class="QPlainTextEdit" name="FeedbEdit">
    <property name="geometry">
     <rect>
      <x>200</x>
      <y>180</y>
      <width>501</width>
      <height>91</height>
     </rect>
    </property>
   </widget>
  </widget>
  <widget class="QMenuBar" name="menubar">
   <property name="geometry">
    <rect>
     <x>0</x>
     <y>0</y>
     <width>788</width>
     <height>26</height>
    </rect>
   </property>
  </widget>
  <widget class="QStatusBar" name="statusbar"/>
 </widget>
 <resources/>
 <connections/>
</ui>
'''


class InstrWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        """открывает окно с инструкцией"""
        self.setGeometry(200, 200, 700, 370)
        self.lbl = QPlainTextEdit(self)
        self.lbl.setGeometry(10, 10, 681, 351)
        self.lbl.setStyleSheet('''QPlainTextEdit {
                                                border: 1px solid rgb(10, 10, 10);
                                                font-size: 15px;
                                            }
        ''')
        s = ''
        with open('instruction.txt', encoding='utf-8') as f:
            for i in f.readlines():
                s += i
        self.lbl.setEnabled(False)
        self.lbl.setPlainText(s)


class FormWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        """открывает окно для написания отзыва"""
        f1 = io.StringIO(form_win.strip())
        uic.loadUi(f1, self)
        self.send_btn.clicked.connect(self.send_data)
        self.cancel_btn.clicked.connect(self.cancel)

    def send_data(self):
        """отправляет отзыв, добавляя его в базу данных"""
        conn = sqlite3.connect(DATABASE)
        cur = conn.cursor()
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Icon.Critical)
        email = self.EmailEdit.text()
        name = self.NameEdit.text()
        score = self.RatingEdit.text()
        feedb = self.FeedbEdit.toPlainText()
        print(name)
        if '@' not in email or '.' not in email or email[0] in ['.', '@'] or email[-1] in ['.', '@']:
            msg.setText('Ошибка. Некорректная почта')
            msg.exec()
        if name.isdigit() or any(map(lambda x: x in '!@#$%^&*(){}[].,<>?/\|1234567890', name)):
            msg.setText('Ошибка. Некорректный формат данных')
            msg.exec()
        else:
            yn, ok_pressed = QInputDialog.getItem(self, "?", "Вы действительно хотите отрпавить отзыв?",
                                                 ("Да", "Нет"), 0, False)
            if ok_pressed and yn == 'Да':
                cur.execute('''INSERT INTO feedbackss VALUES (?, ?, ?, ?)''',
                            (email, name, score, feedb))
                msg.setIcon(QMessageBox.Icon.Information)
                msg.setText('Ваш отзыв отправлен!')
                msg.exec()
                conn.commit()
                conn.close()
                self.close()

    def cancel(self):
        """стирает все написанные данные"""
        self.EmailEdit.setText('')
        self.NameEdit.setText('')
        self.RatingEdit.setText('')
        self.FeedbEdit.setText('')


class SecondWindoww(QMainWindow):
    def __init__(self):
        """открывает окно для просмотра отзывов"""
        super().__init__()
        f = io.StringIO(sec_wind.strip())
        uic.loadUi(f, self)
        self.load_table(DATABASE)

    def load_table(self, file):
        """загружвет таблицу с отзывами"""
        conn = sqlite3.connect(file)
        cur = conn.cursor()
        res = cur.execute('''SELECT * FROM feedbackss''').fetchall()
        self.tableWidget.setColumnCount(4)
        self.tableWidget.setHorizontalHeaderLabels(['email', 'name', 'score', 'feedback'])
        self.tableWidget.setRowCount(0)
        for i, row in enumerate(res):
            self.tableWidget.setRowCount(self.tableWidget.rowCount() + 1)
            print(row)
            for j, elem in enumerate(row):
                self.tableWidget.setItem(i, j, QTableWidgetItem(str(elem)))
        self.tableWidget.resizeColumnsToContents()


class Project(QMainWindow):
    def __init__(self):
        """открывает главное окно"""
        super().__init__()
        file = io.StringIO(template.strip())
        uic.loadUi(file, self)
        self.statbar = self.statusBar()
        self.initUI()
        self.cities = ['Moсква', 'Санкт-Петербург']
        self.cities_maps = [MoscowMap, PeterMap]
        self.apply_btn.clicked.connect(self.apply_data)
        self.view = QWebEngineView()
        self.view.setContentsMargins(0, 0, 0, 0)
        self.lay.addWidget(self.view)
        data = io.BytesIO()
        default = MoscowMap()
        default.map.save(data, close_file=False)
        self.view.setHtml(data.getvalue().decode())
        self.see_feed.clicked.connect(self.displ_feed)
        self.feedbackButton.clicked.connect(self.leave_feedb)
        self.instr_btn.clicked.connect(self.instr)
        self.cityLabel.setText(f'карта воздушного и шумового загрязнения\n города Москва')

    def initUI(self):
        """корректирует виджеты"""
        self.statbar.move(20, 690)

        self.cityChoiceBox.addItem('Moсква')
        self.cityChoiceBox.addItem('Санкт-Петербург')
        self.cityChoiceBox.setDuplicatesEnabled(False)

    def leave_feedb(self):
        """вызывает функцию открытия окна для написания отзывов"""
        self.ui2 = FormWindow()
        self.ui2.show()

    def apply_data(self):
        """применяет все выбранные пользователем изменения"""
        city = self.cityChoiceBox.currentText()
        if city in self.cities:
            city_map = self.cities_maps[self.cities.index(city)]()
            try:
                data = io.BytesIO()
                city_map.map.save(data, close_file=False)
                self.view.setHtml(data.getvalue().decode())
                self.cityLabel.setText(f'карта воздушного и шумового загрязнения\n города {city}')
            except Exception as exc:
                print(exc)
        else:
            self.cityLabel.setText(f'К сожалению, карты для города {city} еще нет, но мы работаем над этим')

    def displ_feed(self):
        """вызывает функцию открытия окна для простомтра отзывов"""
        self.ui = SecondWindoww()
        self.ui.show()

    def instr(self):
        """вызывает функцию открытия окна с инструкцией"""
        self.ui3 = InstrWindow()
        self.ui3.show()


def except_hook(cls, exception, traceback):
    """отлавливает исключения и ошибки"""
    sys.__excepthook__(cls, exception, traceback)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Project()
    ex.show()
    sys.excepthook = except_hook
    sys.exit(app.exec())
