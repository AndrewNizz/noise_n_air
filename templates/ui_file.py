import sys
import io
import sqlite3
import datetime
import folium
from PyQt6 import uic
from PyQt6.QtWebEngineWidgets import QWebEngineView
from PyQt6.QtWidgets import QApplication, QMainWindow, QTableWidgetItem, QMessageBox
import requests
from bs4 import BeautifulSoup
import math

USER_DATABASE = "C:/Users/andre/Downloads/project_db.db"
ECO_DATABASE = "C:/Users/andre/Downloads/air_noise.db"

abbreviations = {'Moсква': 'MSK', 'Санкт-Петербург': 'SPB'}

electro_car_rise = 1.23
industry_greening = 1.03
deforest = 1.04
urbanisation = 1.32   
exhaust_fumes = 1.09
climate_change = 0.699
planting_level = 0.8
recycl_level = 1.03
prev_year_data = 0

MOS_COORDS = [[(55.749853, 37.537020), 'Москва-Сити', 70], [(55.713126, 37.541422), 'Воробьевы Горы', 52],
              [(55.628241, 37.563677), 'Битца', 34], [(55.763637, 37.445481), 'Строгино', 48],
              [(55.816686, 37.611600), 'ВДНХ', 61], [(55.627512, 37.694004), 'Царицыно', 43],
              [(55.848843, 37.728767), 'Лосиный Остров', 30], [(55.659942, 37.662291), 'Коломенское', 38],
              [(55.731220, 37.600704), 'Парк Горького', 56], [(55.698837, 37.707587), 'Нагатинский Затон', 54],
              [(55.751169, 37.612464), 'Красная Площадь', 61], [(55.844008, 37.468894), 'Речной вокзал', 55],
              [(55.775228, 37.763203), 'Измайлово', 47], [(55.656637, 37.467807), 'Тропарево', 53],
              [(55.814904, 37.551343), 'Тимирязевский район', 48], [(55.691032, 37.589121), 'Академический район', 44],
              [(55.675603, 37.756233), 'Люблино', 45], [(55.656017, 37.835771), 'Котельники', 50],
              [(55.698872, 37.480085), 'Кинематографический квартал', 51], [(55.715932, 37.412900), 'Можайский район', 48],
              [(55.883797, 37.552636), 'Дегунино', 42], [(55.876011, 37.617004), 'Медведково', 48],
              [(55.805857, 37.661461), 'Сокольники', 52], [(55.767516, 37.689812), 'Лефортово', 43],
              [(55.730777, 37.815186), 'Вешняки', 49], [(55.587926, 37.637105), 'Бирюлёво', 41]]

SPB_COORDS = [[(59.941081, 30.317631), 'Центр', 65], [(59.972888, 30.224723), 'Зенит арена', 54],
              [(59.927249, 30.236472), 'Севкабель порт', 57], [(59.962177, 30.299465), 'Петроградскй остров', 50],
              [(59.942524, 30.186356), 'Морской Порт', 62], [(59.939838, 30.260718), 'Васильевский остров', 47],
              [(59.921963, 30.315275), 'Река Фонтанка', 53], [(59.869476, 30.328729), 'Парк Победы', 42],
              [(59.923274, 30.385698), 'Александро-Невская Лавра', 43], [(60.021637, 30.352435), 'Парк Сосновка', 39],
              [(59.914400, 30.467052), 'Невский район', 49], [(59.864643, 30.400984), 'Фрунзенский район', 46],
              [(59.888202, 30.184059), 'Канонерский остров', 45], [(59.990601, 30.160678), 'Лахта', 44],
              [(60.050234, 30.283695), 'Новоорловский Заповедник', 38],
              [(59.957976, 30.468765), 'Красногвардейский район', 49],
              [(60.037398, 30.282470), 'Орловский карьер', 52], [(59.973886, 30.387137), 'Полюстрово', 51]]


def modify_data(spis):
    for el in spis:
        url = f'https://yandex.ru/pogoda/ru-RU/details/running?lat={el[0][0]}&lon={el[0][1]}&lang=ru&via=prsw'
        try:
            resp = requests.get(url)
            soup = BeautifulSoup(resp.text, 'lxml')
            data = soup.findAll('span', class_='sc-a9fb3bce-5 jEpyhm', attrs={'aria-hidden': 'true'})
            start, end = 24, 48
            data = list(map(lambda x: int(x.text), data[start:end]))
            value = math.floor(sum(data) / len(data))
            el.append(value)
        except Exception as e:
            print(e)


modify_data(MOS_COORDS)
modify_data(SPB_COORDS)


class Mapp:
    def __init__(self, places, center):
        self.map = folium.Map(location=center, zoom_start=10)
        self.markers = []
        self.top_air = sorted(places, key=lambda x: x[3])[:5]
        self.top_noise = sorted(places, key=lambda x: x[2])[:5]
        print(self.top_noise)
        for el in places:
            n, a = el[2], el[3]
            if n < 50 and a < 50:
                color = '#7cfc00'
            elif 59 > n > 50 or 200 > a > 50:
                color = '#f7e00a'
            elif 69 > n > 59 or 350 > a > 200:
                color = '#f7980a'
            else:
                color = '#ff4500'
            folium.Marker(el[0], popup=f'{el[1]}. воздух-{a} шум-{n}', icon=folium.Icon(icon='cloud', color='white',
                                                             icon_color=color, prefix='fa')).add_to(self.map)
        '''if (air + noise) / 2 <= 3:
            color = '#7cfc00'
        elif 3 < (air + noise) / 2 <= 6:
            color = '#f7e00a'
        elif 6 < (air + noise) / 2 <= 8:
            color = '#f7980a'
        else:
            color = '#ff4500'
        folium.Marker(elem[0], popup=popup, icon=folium.Icon(icon='cloud', color='white',
                                                             icon_color=color, prefix='fa')).add_to(self.map)'''

    def show(self):
        self.map.show_in_browser()


class MoscowMap(Mapp):
    def __init__(self):
        super().__init__(MOS_COORDS, [55.751783, 37.623642])


class PeterMap(Mapp):
    def __init__(self):
        super().__init__(SPB_COORDS, [59.941081, 30.317631])


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
    <height>672</height>
   </rect>
  </property>
  <property name="font">
   <font>
    <family>MS Shell Dlg 2</family>
    <pointsize>10</pointsize>
    <weight>50</weight>
    <italic>false</italic>
    <bold>false</bold>
    <underline>false</underline>
    <strikeout>false</strikeout>
    <kerning>true</kerning>
   </font>
  </property>
  <property name="windowTitle">
   <string>Noise'N'Air</string>
  </property>
  <widget class="QWidget" name="centralwidget">
   <widget class="QComboBox" name="cityChoiceBox">
    <property name="geometry">
     <rect>
      <x>30</x>
      <y>310</y>
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
   <widget class="QPushButton" name="apply_btn">
    <property name="geometry">
     <rect>
      <x>30</x>
      <y>460</y>
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
	background-color: rgb(255, 255, 255);
	border: 1px solid rgb(110, 110, 110) 
}

QPushButton:hover {
	background-color: rgb(245, 245, 245);
	border: 2px solid rgb(1, 1, 1) 
}</string>
    </property>
    <property name="text">
     <string>Применить</string>
    </property>
   </widget>
   <widget class="QPushButton" name="leave_feedback">
    <property name="geometry">
     <rect>
      <x>30</x>
      <y>530</y>
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
	background-color: rgb(255, 255, 255);
	border: 1px solid rgb(110, 110, 110)  
}

QPushButton:hover {
	background-color: rgb(245, 245, 245);
	border: 2px solid rgb(1, 1, 1) 
}</string>
    </property>
    <property name="text">
     <string>Оставить отзыв</string>
    </property>
   </widget>
   <widget class="QLabel" name="label_2">
    <property name="geometry">
     <rect>
      <x>40</x>
      <y>280</y>
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
     <string>Город:</string>
    </property>
   </widget>
   <widget class="QLabel" name="lbl">
    <property name="geometry">
     <rect>
      <x>40</x>
      <y>30</y>
      <width>401</width>
      <height>41</height>
     </rect>
    </property>
    <property name="font">
     <font>
      <pointsize>12</pointsize>
     </font>
    </property>
    <property name="text">
     <string>Карта воздушного и шумового загрязнения
    города</string>
    </property>
   </widget>
   <widget class="QWidget" name="horizontalLayoutWidget_2">
    <property name="geometry">
     <rect>
      <x>290</x>
      <y>180</y>
      <width>791</width>
      <height>431</height>
     </rect>
    </property>
    <layout class="QHBoxLayout" name="lay"/>
   </widget>
   <widget class="QCheckBox" name="air_check">
    <property name="geometry">
     <rect>
      <x>50</x>
      <y>190</y>
      <width>191</width>
      <height>21</height>
     </rect>
    </property>
    <property name="font">
     <font>
      <pointsize>11</pointsize>
     </font>
    </property>
    <property name="layoutDirection">
     <enum>Qt::LeftToRight</enum>
    </property>
    <property name="text">
     <string>Воздух</string>
    </property>
   </widget>
   <widget class="QCheckBox" name="noise_check">
    <property name="geometry">
     <rect>
      <x>50</x>
      <y>220</y>
      <width>191</width>
      <height>31</height>
     </rect>
    </property>
    <property name="font">
     <font>
      <pointsize>11</pointsize>
     </font>
    </property>
    <property name="layoutDirection">
     <enum>Qt::LeftToRight</enum>
    </property>
    <property name="text">
     <string>Шум</string>
    </property>
   </widget>
   <widget class="QLabel" name="air_top">
    <property name="geometry">
     <rect>
      <x>430</x>
      <y>80</y>
      <width>241</width>
      <height>91</height>
     </rect>
    </property>
    <property name="styleSheet">
     <string notr="true">QLabel {
	border: 1px solid rgb(10, 10, 10);
	border-radius: 8px;
}</string>
    </property>
    <property name="text">
     <string>TextLabel</string>
    </property>
   </widget>
   <widget class="QPushButton" name="see_feedback">
    <property name="geometry">
     <rect>
      <x>30</x>
      <y>570</y>
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
	background-color: rgb(255, 255, 255);
	border: 1px solid rgb(110, 110, 110) 
}

QPushButton:hover {
	background-color: rgb(245, 245, 245);
	border: 2px solid rgb(1, 1, 1) 
}</string>
    </property>
    <property name="text">
     <string>Посмотреть отзывы</string>
    </property>
   </widget>
   <widget class="QLabel" name="noise_top">
    <property name="geometry">
     <rect>
      <x>700</x>
      <y>80</y>
      <width>221</width>
      <height>91</height>
     </rect>
    </property>
    <property name="styleSheet">
     <string notr="true">QLabel {
	border: 1px solid rgb(10, 10, 10);
	border-radius: 8px;
}</string>
    </property>
    <property name="text">
     <string>TextLabel</string>
    </property>
   </widget>
   <widget class="QDateEdit" name="dateEdit">
    <property name="geometry">
     <rect>
      <x>100</x>
      <y>100</y>
      <width>151</width>
      <height>31</height>
     </rect>
    </property>
    <property name="font">
     <font>
      <pointsize>10</pointsize>
     </font>
    </property>
    <property name="dateTime">
     <datetime>
      <hour>0</hour>
      <minute>0</minute>
      <second>0</second>
      <year>2024</year>
      <month>12</month>
      <day>12</day>
     </datetime>
    </property>
   </widget>
   <widget class="QLabel" name="label">
    <property name="geometry">
     <rect>
      <x>40</x>
      <y>100</y>
      <width>51</width>
      <height>31</height>
     </rect>
    </property>
    <property name="font">
     <font>
      <pointsize>12</pointsize>
     </font>
    </property>
    <property name="text">
     <string>Дата</string>
    </property>
   </widget>
   <widget class="QLabel" name="label_3">
    <property name="geometry">
     <rect>
      <x>50</x>
      <y>150</y>
      <width>131</width>
      <height>31</height>
     </rect>
    </property>
    <property name="font">
     <font>
      <pointsize>11</pointsize>
     </font>
    </property>
    <property name="text">
     <string>Лучшие места:</string>
    </property>
   </widget>
   <widget class="Line" name="line">
    <property name="geometry">
     <rect>
      <x>30</x>
      <y>140</y>
      <width>221</width>
      <height>16</height>
     </rect>
    </property>
    <property name="orientation">
     <enum>Qt::Horizontal</enum>
    </property>
   </widget>
   <widget class="Line" name="line_2">
    <property name="geometry">
     <rect>
      <x>30</x>
      <y>250</y>
      <width>221</width>
      <height>21</height>
     </rect>
    </property>
    <property name="orientation">
     <enum>Qt::Horizontal</enum>
    </property>
   </widget>
   <widget class="QLabel" name="label_4">
    <property name="geometry">
     <rect>
      <x>520</x>
      <y>60</y>
      <width>55</width>
      <height>16</height>
     </rect>
    </property>
    <property name="text">
     <string>Воздух</string>
    </property>
   </widget>
   <widget class="QLabel" name="label_5">
    <property name="geometry">
     <rect>
      <x>780</x>
      <y>60</y>
      <width>55</width>
      <height>16</height>
     </rect>
    </property>
    <property name="text">
     <string>Шум</string>
    </property>
   </widget>
   <widget class="QLabel" name="cityLabel">
    <property name="geometry">
     <rect>
      <x>130</x>
      <y>50</y>
      <width>91</width>
      <height>21</height>
     </rect>
    </property>
    <property name="font">
     <font>
      <pointsize>12</pointsize>
      <weight>75</weight>
      <bold>true</bold>
      <underline>true</underline>
     </font>
    </property>
    <property name="text">
     <string>Москва</string>
    </property>
   </widget>
   <widget class="QLabel" name="label_6">
    <property name="geometry">
     <rect>
      <x>440</x>
      <y>10</y>
      <width>31</width>
      <height>31</height>
     </rect>
    </property>
    <property name="text">
     <string/>
    </property>
    <property name="pixmap">
     <pixmap>../../../Downloads/Thumb (1) (1).png</pixmap>
    </property>
   </widget>
   <widget class="QLabel" name="label_7">
    <property name="geometry">
     <rect>
      <x>880</x>
      <y>10</y>
      <width>41</width>
      <height>31</height>
     </rect>
    </property>
    <property name="text">
     <string/>
    </property>
    <property name="pixmap">
     <pixmap>../../../Downloads/Remove-bg.ai_1733685943525 (1) (1).png</pixmap>
    </property>
   </widget>
   <widget class="QPushButton" name="pushButton_2">
    <property name="geometry">
     <rect>
      <x>480</x>
      <y>10</y>
      <width>92</width>
      <height>41</height>
     </rect>
    </property>
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
     <string>1-3
0-50</string>
    </property>
   </widget>
   <widget class="QPushButton" name="pushButton_5">
    <property name="geometry">
     <rect>
      <x>580</x>
      <y>10</y>
      <width>91</width>
      <height>41</height>
     </rect>
    </property>
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
     <string>4-6
51-250</string>
    </property>
   </widget>
   <widget class="QPushButton" name="pushButton_4">
    <property name="geometry">
     <rect>
      <x>680</x>
      <y>10</y>
      <width>91</width>
      <height>41</height>
     </rect>
    </property>
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
     <string>7-8
251-400</string>
    </property>
   </widget>
   <widget class="QPushButton" name="pushButton_3">
    <property name="geometry">
     <rect>
      <x>780</x>
      <y>10</y>
      <width>91</width>
      <height>41</height>
     </rect>
    </property>
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
     <string>9-10
401-500</string>
    </property>
   </widget>
   <widget class="QPushButton" name="forecast_btn">
    <property name="geometry">
     <rect>
      <x>960</x>
      <y>70</y>
      <width>121</width>
      <height>31</height>
     </rect>
    </property>
    <property name="font">
     <font>
      <pointsize>11</pointsize>
     </font>
    </property>
    <property name="styleSheet">
     <string notr="true">QPushButton {
	border-radius: 7px;
	background-color: rgb(255, 255, 255);
	border: 1px solid rgb(110, 110, 110) 
}

QPushButton:hover {
	background-color: rgb(245, 245, 245);
	border: 2px solid rgb(1, 1, 1) 
}</string>
    </property>
    <property name="text">
     <string>прогноз</string>
    </property>
   </widget>
   <widget class="QPushButton" name="graph_btn">
    <property name="geometry">
     <rect>
      <x>960</x>
      <y>120</y>
      <width>121</width>
      <height>28</height>
     </rect>
    </property>
    <property name="font">
     <font>
      <pointsize>11</pointsize>
     </font>
    </property>
    <property name="styleSheet">
     <string notr="true">QPushButton {
	border-radius: 7px;
	background-color: rgb(255, 255, 255);
	border: 1px solid rgb(110, 110, 110) 
}

QPushButton:hover {
	background-color: rgb(245, 245, 245);
	border: 2px solid rgb(1, 1, 1) 
}</string>
    </property>
    <property name="text">
     <string>график</string>
    </property>
   </widget>
   <widget class="QLabel" name="label_9">
    <property name="geometry">
     <rect>
      <x>880</x>
      <y>10</y>
      <width>31</width>
      <height>31</height>
     </rect>
    </property>
    <property name="text">
     <string/>
    </property>
    <property name="pixmap">
     <pixmap>../../../Downloads/dislike (1).png</pixmap>
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

forecast_win = '''
<?xml version="1.0" encoding="UTF-8"?>
<ui version="4.0">
 <class>MainWindow</class>
 <widget class="QMainWindow" name="MainWindow">
  <property name="geometry">
   <rect>
    <x>0</x>
    <y>0</y>
    <width>650</width>
    <height>262</height>
   </rect>
  </property>
  <property name="windowTitle">
   <string>ForecastWindow</string>
  </property>
  <widget class="QWidget" name="centralwidget">
   <widget class="QLabel" name="forecast_lbl">
    <property name="geometry">
     <rect>
      <x>10</x>
      <y>70</y>
      <width>631</width>
      <height>51</height>
     </rect>
    </property>
    <property name="font">
     <font>
      <pointsize>11</pointsize>
     </font>
    </property>
    <property name="styleSheet">
     <string notr="true">QLabel {
	border: 1px solid rgb(10, 10, 10);
	border-radius: 8px;
}</string>
    </property>
    <property name="text">
     <string/>
    </property>
   </widget>
   <widget class="QLabel" name="verdict_lbl">
    <property name="geometry">
     <rect>
      <x>10</x>
      <y>140</y>
      <width>631</width>
      <height>51</height>
     </rect>
    </property>
    <property name="font">
     <font>
      <pointsize>9</pointsize>
     </font>
    </property>
    <property name="styleSheet">
     <string notr="true">QLabel {
	border: 1px solid rgb(10, 10, 10);
	border-radius: 8px;
}</string>
    </property>
    <property name="text">
     <string/>
    </property>
   </widget>
   <widget class="QLabel" name="year_lbl">
    <property name="geometry">
     <rect>
      <x>130</x>
      <y>10</y>
      <width>451</width>
      <height>31</height>
     </rect>
    </property>
    <property name="font">
     <font>
      <pointsize>11</pointsize>
      <weight>75</weight>
      <bold>true</bold>
     </font>
    </property>
    <property name="text">
     <string>прогноз атомсферного загрязнеия на 2025 год</string>
    </property>
   </widget>
  </widget>
  <widget class="QMenuBar" name="menubar">
   <property name="geometry">
    <rect>
     <x>0</x>
     <y>0</y>
     <width>650</width>
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

chart_win = '''
<?xml version="1.0" encoding="UTF-8"?>
<ui version="4.0">
 <class>MainWindow</class>
 <widget class="QMainWindow" name="MainWindow">
  <property name="geometry">
   <rect>
    <x>0</x>
    <y>0</y>
    <width>755</width>
    <height>441</height>
   </rect>
  </property>
  <property name="windowTitle">
   <string>ChartWindow</string>
  </property>
  <widget class="QWidget" name="centralwidget">
   <widget class="QLabel" name="label">
    <property name="geometry">
     <rect>
      <x>10</x>
      <y>0</y>
      <width>731</width>
      <height>391</height>
     </rect>
    </property>
    <property name="text">
     <string/>
    </property>
    <property name="pixmap">
     <pixmap>../../../Downloads/chartV2.jpg</pixmap>
    </property>
   </widget>
  </widget>
  <widget class="QMenuBar" name="menubar">
   <property name="geometry">
    <rect>
     <x>0</x>
     <y>0</y>
     <width>755</width>
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


class ChartWindow(QMainWindow):
    def __init__(self, city1):
        super().__init__()
        f3 = io.StringIO(chart_win.strip())
        uic.loadUi(f3, self)


class ForecastWindow(QMainWindow):
    def __init__(self, year1, city1):
        super().__init__()
        f2 = io.StringIO(forecast_win.strip())
        uic.loadUi(f2, self)
        self.predict(year1, city1)

    def predict(self, year1, city1):
        now = datetime.date.today().year
        db = sqlite3.connect(ECO_DATABASE)
        cur = db.cursor()
        q = f'SELECT AVG(rate) FROM air_pollution WHERE city = "{city1}" AND year = {now}'
        now_year_data = cur.execute(q).fetchone()[0]
        print(now_year_data)
        try:
            if year1 < now:
                raise ValueError
            else:
                delta = year1 - now
                if delta:
                    benef = [electro_car_rise, planting_level, industry_greening, recycl_level, prev_year_data]
                    disadv = [deforest, exhaust_fumes, climate_change, urbanisation, prev_year_data]
                    rate = sum(map(lambda x: x * delta, disadv)) / sum(map(lambda x: x * delta, benef))
                    res = (rate ** delta) * now_year_data
                    self.year_lbl.setText(f'прогноз атомсферного загрязнения на {year1} год')
                    self.forecast_lbl.setText(f'Среднее предполагаемое загрязнение - {res:.2f} из 10')
                    if res > now_year_data:
                        self.verdict_lbl.setText(f'Ожидается дальнейшее загрязнение на {100 - now_year_data / res * 100:.2f}%')
                    else:
                        self.verdict_lbl.setText(f'Ожидается спад загрязнения на {100 - now_year_data / res * 100:.2f}%')
                else:
                    raise ValueError
        except ValueError:
            self.forecast_lbl.setText(':(')
            self.verdict_lbl.setText('')
            return 0


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
        conn = sqlite3.connect(USER_DATABASE)
        cur = conn.cursor()
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Icon.Critical)
        email = self.EmailEdit.text()
        name = self.NameEdit.text()
        score = self.RatingEdit.text()
        feedb = self.FeedbEdit.toPlainText()
        if '@' not in email or '.' not in email or email[0] in ['.', '@'] or email[-1] in ['.', '@']:
            msg.setText('Ошибка. Некорректная почта')
            msg.exec()
        if name.isdigit() or any(map(lambda x: x in '!@#$%^&*(){}[].,<>?/\|1234567890', name)):
            msg.setText('Ошибка. Некорректный формат данных')
            msg.exec()
        else:
            cur.execute('''INSERT INTO feedbs VALUES (?, ?, ?, ?)''',
                        (email, name, score, feedb))
            msg.setIcon(QMessageBox.Icon.Information)
            msg.setText('Ваш отзыв отправлен!')
            msg.exec()
            conn.commit()
            conn.close()
            self.close()

    def cancel(self):
        self.EmailEdit.setText('')
        self.NameEdit.setText('')
        self.RatingEdit.setText('')
        self.FeedbEdit.setPlainText('')


class SecondWindoww(QMainWindow):
    def __init__(self):
        super().__init__()
        f = io.StringIO(sec_wind.strip())
        uic.loadUi(f, self)
        self.load_table(USER_DATABASE)

    def load_table(self, file):
        conn = sqlite3.connect(file)
        cur = conn.cursor()
        res = cur.execute('''SELECT * FROM feedbs''').fetchall()
        self.tableWidget.setColumnCount(4)
        self.tableWidget.setHorizontalHeaderLabels(['email', 'name', 'score', 'feedback'])
        self.tableWidget.setRowCount(0)
        for i, row in enumerate(res):
            self.tableWidget.setRowCount(self.tableWidget.rowCount() + 1)
            for j, elem in enumerate(row):
                self.tableWidget.setItem(i, j, QTableWidgetItem(str(elem)))
        self.tableWidget.resizeColumnsToContents()


class Project(QMainWindow):
    def __init__(self):
        super().__init__()
        file = io.StringIO(template.strip())
        uic.loadUi(file, self)
        self.statbar = self.statusBar()
        self.initUI()
        self.cities = ['Moсква', 'Санкт-Петербург']
        self.cities_maps = [MoscowMap, PeterMap]
        self.apply_btn.clicked.connect(self.apply_data)
        self.leave_feedback.clicked.connect(self.leave_feedb)
        self.see_feedback.clicked.connect(self.displ_feed)
        self.forecast_btn.clicked.connect(self.see_forecast)
        self.graph_btn.clicked.connect(self.show_graph)
        self.view = QWebEngineView()
        self.air_check.setChecked(True)
        self.noise_check.setChecked(True)
        self.apply_data()
        self.view.setContentsMargins(0, 0, 0, 0)
        self.lay.addWidget(self.view)
        data = io.BytesIO()
        default = MoscowMap()
        default.map.save(data, close_file=False)
        self.view.setHtml(data.getvalue().decode())

    def initUI(self):
        self.statbar.move(20, 690)

        self.cityChoiceBox.addItem('Moсква')
        self.cityChoiceBox.addItem('Санкт-Петербург')
        self.cityChoiceBox.setDuplicatesEnabled(False)

    def apply_data(self):
        city = self.cityChoiceBox.currentText()
        if city in self.cities:
            city_map = self.cities_maps[self.cities.index(city)]()
            try:
                data = io.BytesIO()
                city_map.map.save(data, close_file=False)
                self.view.setHtml(data.getvalue().decode())
                self.cityLabel.setText(f'{city}')
                if self.air_check.isChecked():
                    to_displ = ''
                    for el in city_map.top_air:
                        line = f'{el[1]} - {el[3]}\n'
                        to_displ += line
                    self.air_top.setText(to_displ[:-1])
                    self.air_top.setStyleSheet('''QLabel {
                                                border: 1px solid rgb(10, 10, 10);
                                                border-radius: 8px;
                                            }''')
                if self.noise_check.isChecked():
                    to_displ = ''
                    for el in city_map.top_noise:
                        line = f'{el[1]} - {el[2]}\n'
                        to_displ += line
                    self.noise_top.setText(to_displ[:-1])
                    self.noise_top.setStyleSheet('''QLabel {
                                                  border: 1px solid rgb(10, 10, 10);
                                                  border-radius: 8px;
                                              }''')
                if not self.air_check.isChecked():
                    self.air_top.setText('')
                    self.air_top.setStyleSheet('')
                if not self.noise_check.isChecked():
                    self.noise_top.setText('')
                    self.noise_top.setStyleSheet('')
            except Exception as exc:
                print(exc)
        else:
            self.lbl.setText(f'К сожалению, карты для города {city} еще нет, но мы работаем над этим')
            self.cityLabel.setText('')

    def leave_feedb(self):
        self.ui2 = FormWindow()
        self.ui2.show()

    def displ_feed(self):
        self.ui = SecondWindoww()
        self.ui.show()

    def see_forecast(self):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Icon.Critical)
        year = self.dateEdit.date().year()
        city = self.cityChoiceBox.currentText()
        if year <= datetime.date.today().year:
            msg.setText('Прогноз осущетсвляется только на будущие года, попробуй еще раз')
            msg.exec()
        else:
            self.ui3 = ForecastWindow(year, abbreviations[city])
            self.ui3.show()

    def show_graph(self):
        city = self.cityChoiceBox.currentText()
        self.ui4 = ChartWindow(city)
        self.ui4.show()


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Project()
    ex.show()
    sys.excepthook = except_hook
    sys.exit(app.exec())