import sys
from PyQt5 import QtWidgets, QtCore, QtGui


class MyTableModel(QtCore.QAbstractTableModel):
    def __init__(self, data=[[]], headers=[], parent=None):
        QtCore.QAbstractTableModel.__init__(self, parent)  # Родительский конструктор

        # Атрибуты для хранения данных
        self.__data = data  # Для данных
        self.__headers = headers  # Для заголовков

    # Задаем заголовки
    def headerData(self, section, orientation, role):
        if role == QtCore.Qt.DisplayRole:  # Проверяем есть ли ячейка для отображения данных
            if orientation == QtCore.Qt.Horizontal:  # Если это загловки  столбцов

                # для ошибки index is out of range
                if section < len(self.__headers):
                    return self.__headers[section]  # То задаем список заголовков по индексу
                else:
                    return "Temporary"

            else:  # Иначе  это заголовки строк
                return section + 1  # То задаем значение section - индекс ряда

    # Задаем размеры столбцов и строк для табличного представления------------------------------------
    def rowCount(self, parent):  # Задаем количество строк для представления
        return len(self.__data)

    def columnCount(self, parent):  # Задаем количество столбцов для представления---------------------
        return len(self.__data[0])

    # Системный метод который мы перезаписываем чтобы повлиять на поведение моделей ------------------
    def data(self, index, role):
        # При двойном нажатии на ячейку элемент полностью стирается чтобы предотвратить нужно прменить метод-----------
        if role == QtCore.Qt.EditRole:
            row = index.row()
            column = index.column()
            return self.__data[row][column]  # Определяем позицию элемента в массиве
            # Возвращяем значение из массива в отображение

        # Отображение данных в представлении
        if role == QtCore.Qt.DisplayRole:
            row = index.row()  # Индекс строки
            column = index.column()  # Индекс столбца
            value = self.__data[row][column]  # Получение значения по известным индексам
            return value  # Вернуть в представление

    # Возможность редактрования данных в таблице ------------------------------------
    # Для этого нужны 2 метода flags, setData
    def flags(self, index):
        return QtCore.Qt.ItemIsEditable | QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled

    def setData(self, index, value, role=QtCore.Qt.EditRole):
        if role == QtCore.Qt.EditRole:  # Если поле редактируемое
            row = index.row()
            column = index.column()
            new_element = value  # Новое значение
            if new_element:  # Проверка новых данных
                self.__data[row][column] = new_element  # Перезапись элемента
                return True  # Успешно

            else:
                return False  # Не успешно

        # ==============================================================#
        # INSERTING & REMOVING  ITEMS IN THE TABLE
        """ Внедрение(размещение)-INSERTING & Удаление REMOVING  элементов
            Важно запомнить что эти методы должны вызвать в себе 2 метода 
            self.beginInsertRows начать размещение 
            self.endInsertRows()
            они испускают сигнал для представления чтобы он мог корректно отобразить данные  для связи между 
            """
        # ====================================================================#

    def insertRows(self, position, rows, parent=QtCore.QModelIndex()):
        """position - куда в структуре данных будем размещать элемент
           rows - сколько рядов мы будем размещать
           parent - пока можно игнорировать, он нужен для иерархиеского представления
        """
        self.beginInsertRows(parent, position, position + rows - 1)
        """При размещении представление должно быть готовым обновить данные и параметры нужны для этого
        QtCore.QModelIndex - Пустой индекс  нужный парметр для корня 
         position - С какого элемента начать  
         position+rows-1 - последний элемент"""

        """Запускаем цикл для размещения произвольного количества элементов"""
        for i in range(rows):
            # У нас есть списковая структура данных, и внее будем все размещать при помощи .insert(2 параметра)
            # 1) Позиция(в списке) 2)Значение

            defaultValues = [i for i in range(1, 4)]  # Генерируем список от 1 до 4 [1,2,3]
            self.__data.insert(position, defaultValues)  # Внедрение в список

        self.endInsertRows()
        return True  # Если все без ошибок то возвращает истина

    # Удаление рядов в таблице=============================================================
    def removeRows(self, position, rows, parent=QtCore.QModelIndex()):

        self.beginRemoveRows(parent, position, position + rows - 1)  # Старт процесс удаления
        # Removing here
        for i in range(rows):
            value = self.__data[position]  # Получаем позицию ряда
            self.__data.remove(value)  # Удаляем элемент ряд

        self.endRemoveRows()  # Стоп

        return True

    # Добавление столбцов для таблицы ===================================================================
    def insertColumns(self, position, columns, parent=QtCore.QModelIndex()):
        self.beginInsertColumns(parent, position, position + columns - 1)
        """self.beginInsertColumns(index, first, last)"""
        # index - parent
        # first - position
        # last - position + columns - 1 = view ожидает 0 образный элемент

        rowCount = len(self.__data)  # Количество рядов в нашем массиве
        for i in range(columns):  # Перебираем Столбцы

            for j in range(rowCount):  # Преребираем Строки
                self.__data[j].insert(position, "new cell")  # Внедряем данные начиная с 0 ой строки

        self.endInsertColumns()
        return True  # Если все без ошибок то добавление рядов успешны

    # Удаление  столбцов из таблицы ================================================
    def removeColumns(self, position, columns, parent=QtCore.QModelIndex()):
        self.beginRemoveColumns(parent, position, position + columns - 1)  # Старт процесс удаления
        # Removing here

        rowCount = len(self.__data)    # Количество строк

        for i in range(columns):       # Перебираем столбцы   # 1
            for j in range(rowCount):  # Преребираем ряды # 2
                print(self.__data[j])  # ряд
                value = self.__data[j][position]

                self.__data[j].remove(value)

        self.endRemoveColumns()  # Стоп

        return True


#  Мое окно ------------------------------------------------
class MyWindow(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        # данные
        data = [
            ["value", "value", "value"],
            ["value", "value", "value"]
        ]
        # Заголовки
        headers = ["col1", "col2", "col3", ]

        #  Табличное представление
        self.TableView = QtWidgets.QTableView()
        self.TableView.show()

        # Объект из класса MyTableModel ===========================================
        self.model = MyTableModel(data, headers)

        # Добавление строк ===========================================
        self.model.insertRows(0, 1)
        """1) позиция (индекс ряда) начало удаления
           2)Количество рядов(строк) для добавления"""

        # Удаление строк(рядов) и==============================================
        # self.model.removeRows(0, 1)
        """1) позиция (индекс ряда) начало удаления
           2)Количество рядов(строк) для удаления"""

        # Применяем метод добавление столбцов ==============================================
        self.model.insertColumns(0, 1)

        # Применяем метод удаления столбцов ==============================================
        self.model.removeColumns(0, 1)

        # Кладем модель в представление=============================================

        self.modelheader = QtGui.QStandardItemModel()


# Приложение
app = QtWidgets.QApplication(sys.argv)
win = MyWindow()
sys.exit(app.exec_())