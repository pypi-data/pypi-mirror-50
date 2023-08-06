import base64

from Crypto.Cipher import PKCS1_OAEP
from Crypto.PublicKey import RSA
from PyQt5.QtCore import QSize, QMetaObject, QRect, pyqtSlot, Qt, \
    QCoreApplication
from PyQt5.QtGui import QStandardItemModel, QStandardItem, QBrush, QColor
from PyQt5.QtWidgets import QListView, QMenuBar, QMenu, QStatusBar, QAction, \
    QTextEdit, QWidget, QMainWindow, qApp, QMessageBox, QDialog, QPushButton, \
    QLineEdit, QLabel, QComboBox

from jim.utils import Message
from .exceptions import ServerError


class UiMainClientWindow(object):
    """
    Класс, создающий интерфейс главного окна.
    """
    def __init__(self, main_client_window):
        main_client_window.setObjectName("MainClientWindow")
        main_client_window.resize(756, 534)
        main_client_window.setMinimumSize(QSize(756, 534))
        self.centralwidget = QWidget(main_client_window)
        self.centralwidget.setObjectName("centralwidget")
        self.label_contacts = QLabel(self.centralwidget)
        self.label_contacts.setGeometry(QRect(10, 0, 101, 16))
        self.label_contacts.setObjectName("label_contacts")
        self.btn_add_contact = QPushButton(self.centralwidget)
        self.btn_add_contact.setGeometry(QRect(10, 450, 121, 31))
        self.btn_add_contact.setObjectName("btn_add_contact")
        self.btn_remove_contact = QPushButton(self.centralwidget)
        self.btn_remove_contact.setGeometry(QRect(140, 450, 121, 31))
        self.btn_remove_contact.setObjectName("btn_remove_contact")
        self.label_history = QLabel(self.centralwidget)
        self.label_history.setGeometry(QRect(300, 0, 391, 21))
        self.label_history.setObjectName("label_history")
        self.text_message = QTextEdit(self.centralwidget)
        self.text_message.setGeometry(QRect(300, 360, 441, 71))
        self.text_message.setObjectName("text_message")
        self.label_new_message = QLabel(self.centralwidget)
        self.label_new_message.setGeometry(QRect(300, 330, 450,
                                                 16))  # Правка тут
        self.label_new_message.setObjectName("label_new_message")
        self.list_contacts = QListView(self.centralwidget)
        self.list_contacts.setGeometry(QRect(10, 20, 251, 411))
        self.list_contacts.setObjectName("list_contacts")
        self.list_messages = QListView(self.centralwidget)
        self.list_messages.setGeometry(QRect(300, 20, 441, 301))
        self.list_messages.setObjectName("list_messages")
        self.btn_send = QPushButton(self.centralwidget)
        self.btn_send.setGeometry(QRect(610, 450, 131, 31))
        self.btn_send.setObjectName("btn_send")
        self.btn_clear = QPushButton(self.centralwidget)
        self.btn_clear.setGeometry(QRect(460, 450, 131, 31))
        self.btn_clear.setObjectName("btn_clear")
        main_client_window.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(main_client_window)
        self.menubar.setGeometry(QRect(0, 0, 756, 21))
        self.menubar.setObjectName("menubar")
        self.menu = QMenu(self.menubar)
        self.menu.setObjectName("menu")
        self.menu_2 = QMenu(self.menubar)
        self.menu_2.setObjectName("menu_2")
        main_client_window.setMenuBar(self.menubar)
        self.statusBar = QStatusBar(main_client_window)
        self.statusBar.setObjectName("statusBar")
        main_client_window.setStatusBar(self.statusBar)
        self.menu_exit = QAction(main_client_window)
        self.menu_exit.setObjectName("menu_exit")
        self.menu_add_contact = QAction(main_client_window)
        self.menu_add_contact.setObjectName("menu_add_contact")
        self.menu_del_contact = QAction(main_client_window)
        self.menu_del_contact.setObjectName("menu_del_contact")
        self.menu.addAction(self.menu_exit)
        self.menu_2.addAction(self.menu_add_contact)
        self.menu_2.addAction(self.menu_del_contact)
        self.menu_2.addSeparator()
        self.menubar.addAction(self.menu.menuAction())
        self.menubar.addAction(self.menu_2.menuAction())

        self.retranslate_ui(main_client_window)
        self.btn_clear.clicked.connect(self.text_message.clear)
        QMetaObject.connectSlotsByName(main_client_window)

    def retranslate_ui(self, main_client_window):
        _translate = QCoreApplication.translate
        main_client_window.setWindowTitle(
            _translate("MainClientWindow", "Чат Программа alpha release"))
        self.label_contacts.setText(
            _translate("MainClientWindow", "Список контактов:"))
        self.btn_add_contact.setText(
            _translate("MainClientWindow", "Добавить контакт"))
        self.btn_remove_contact.setText(
            _translate("MainClientWindow", "Удалить контакт"))
        self.label_history.setText(
            _translate("MainClientWindow", "История сообщений:"))
        self.label_new_message.setText(
            _translate("MainClientWindow", "Введите новое сообщение:"))
        self.btn_send.setText(
            _translate("MainClientWindow", "Отправить сообщение"))
        self.btn_clear.setText(_translate("MainClientWindow", "Очистить поле"))
        self.menu.setTitle(_translate("MainClientWindow", "Файл"))
        self.menu_2.setTitle(_translate("MainClientWindow", "Контакты"))
        self.menu_exit.setText(_translate("MainClientWindow", "Выход"))
        self.menu_add_contact.setText(
            _translate("MainClientWindow", "Добавить контакт"))
        self.menu_del_contact.setText(
            _translate("MainClientWindow", "Удалить контакт"))


class ClientMainWindow(QMainWindow):
    """
    Класс - основное окно пользователя.
    Содержит всю основную логику работы клиентского модуля.
    """
    def __init__(self, database, transport):
        super().__init__()
        # основные переменные
        self.database = database
        self.transport = transport

        # Загружаем конфигурацию окна
        self.ui = UiMainClientWindow(self)

        self.select_dialog = None
        self.remove_dialog = None

        # Кнопка "Выход"
        self.ui.menu_exit.triggered.connect(qApp.exit)

        # Кнопка отправить сообщение
        self.ui.btn_send.clicked.connect(self.send_message)

        # "добавить контакт"
        self.ui.btn_add_contact.clicked.connect(self.add_contact_window)
        self.ui.menu_add_contact.triggered.connect(self.add_contact_window)

        # Удалить контакт
        self.ui.btn_remove_contact.clicked.connect(self.delete_contact_window)
        self.ui.menu_del_contact.triggered.connect(self.delete_contact_window)

        # Дополнительные требующиеся атрибуты
        self.contacts_model = None
        self.history_model = None
        self.messages = QMessageBox()
        self.current_chat = None
        self.current_chat_key = None
        self.encryptor = None
        self.ui.list_messages.setHorizontalScrollBarPolicy(
            Qt.ScrollBarAlwaysOff)
        self.ui.list_messages.setWordWrap(True)

        # Даблклик по листу контактов отправляется в обработчик
        self.ui.list_contacts.doubleClicked.connect(self.select_active_user)

        self.clients_list_update()
        self.set_disabled_input()
        self.show()

    def set_disabled_input(self):
        """
        Метод делающий поля ввода неактивными.
        :return:
        """
        # Надпись  - получатель.
        self.ui.label_new_message.setText(
            'Для выбора получателя дважды кликните на нем в окне контактов.')
        self.ui.text_message.clear()
        if self.history_model:
            self.history_model.clear()

        # Поле ввода и кнопка отправки неактивны до выбора получателя.
        self.ui.btn_clear.setDisabled(True)
        self.ui.btn_send.setDisabled(True)
        self.ui.text_message.setDisabled(True)

    def history_list_update(self):
        """
        Метод заполняющий соответствующий QListView
        историей переписки с текущим собеседником.
        :return:
        """
        # Получаем историю сортированную по дате
        sorted_list = sorted(self.database.get_history(self.current_chat),
                             key=lambda item: item[3])
        # Если модель не создана, создадим.
        if not self.history_model:
            self.history_model = QStandardItemModel()
            self.ui.list_messages.setModel(self.history_model)
        # Очистим от старых записей
        self.history_model.clear()
        # Берём не более 20 последних записей.
        length = len(sorted_list)
        start_index = 0
        if length > 20:
            start_index = length - 20
        # Заполнение модели записями, так-же стоит разделить входящие
        # и исходящие выравниванием и разным фоном.
        # Записи в обратном порядке, поэтому выбираем их с конца и не более 20
        for i in range(start_index, length):
            item = sorted_list[i]
            if item[1] == 'in':
                mess = QStandardItem(
                    f'Входящее от '
                    f'{item[3].replace(microsecond=0)}:\n {item[2]}')
                mess.setEditable(False)
                mess.setBackground(QBrush(QColor(255, 213, 213)))
                mess.setTextAlignment(Qt.AlignLeft)
                self.history_model.appendRow(mess)
            else:
                mess = QStandardItem(
                    f'Исходящее от '
                    f'{item[3].replace(microsecond=0)}:\n {item[2]}')
                mess.setEditable(False)
                mess.setTextAlignment(Qt.AlignRight)
                mess.setBackground(QBrush(QColor(204, 255, 204)))
                self.history_model.appendRow(mess)
        self.ui.list_messages.scrollToBottom()

    def select_active_user(self):
        """
        Метод обработчик события двойного клика по списку контактов.
        :return:
        """
        # Выбранный пользователем (даблклик) находится
        # в выделеном элементе в QListView
        self.current_chat = self.ui.list_contacts.currentIndex().data()
        # вызываем основную функцию
        self.set_active_user()

    def set_active_user(self):
        """
        Метод активации чата с собеседником.
        :return:
        """
        # Запрашиваем публичный ключ пользователя и создаём объект шифрования
        try:
            self.current_chat_key = self.transport.key_request(
                self.current_chat)
            if self.current_chat_key:
                self.encryptor = PKCS1_OAEP.new(
                    RSA.import_key(self.current_chat_key))
        except (OSError):
            self.current_chat_key = None
            self.encryptor = None

        # Если ключа нет то ошибка, что не удалось начать чат с пользователем
        if not self.current_chat_key:
            self.messages.warning(
                self, 'Ошибка',
                'Для выбранного пользователя нет ключа шифрования.')
            return

        # Ставим надпись и активируем кнопки
        self.ui.label_new_message.setText(
            f'Введите сообщенние для {self.current_chat}:')
        self.ui.btn_clear.setDisabled(False)
        self.ui.btn_send.setDisabled(False)
        self.ui.text_message.setDisabled(False)

        # Заполняем окно историю сообщений по требуемому пользователю.
        self.history_list_update()

    def clients_list_update(self):
        """
        Метод обновляющий список контактов.
        :return:
        """
        contacts_list = self.database.get_contacts()
        self.contacts_model = QStandardItemModel()
        for i in sorted(contacts_list):
            item = QStandardItem(i)
            item.setEditable(False)
            self.contacts_model.appendRow(item)
        self.ui.list_contacts.setModel(self.contacts_model)

    def add_contact_window(self):
        """
        Метод создающий окно - диалог добавления контакта.
        :return:
        """
        self.select_dialog = AddContactDialog(self.transport, self.database)
        self.select_dialog.btn_ok.clicked.connect(
            lambda: self.add_contact_action(self.select_dialog))
        self.select_dialog.show()

    def add_contact_action(self, item):
        """
        Метод обработчк нажатия кнопки "Добавить.
        :param item:
        :return:
        """
        new_contact = item.selector.currentText()
        self.add_contact(new_contact)
        item.close()

    def add_contact(self, new_contact):
        """
        Метод добавляющий контакт в серверную и клиентсткую BD.
        После обновления баз данных обновляет и содержимое окна.
        :param new_contact:
        :return:
        """
        try:
            self.transport.add_contact(new_contact)
        except ServerError as err:
            self.messages.critical(self, 'Ошибка сервера', err.text)
        except OSError as err:
            if err.errno:
                self.messages.critical(self, 'Ошибка',
                                       'Потеряно соединение с сервером!')
                self.close()
            self.messages.critical(self, 'Ошибка', 'Таймаут соединения!')
        else:
            self.database.add_contact(new_contact)
            new_contact = QStandardItem(new_contact)
            new_contact.setEditable(False)
            self.contacts_model.appendRow(new_contact)
            # logger.info(f'Успешно добавлен контакт {new_contact}')
            self.messages.information(self, 'Успех',
                                      'Контакт успешно добавлен.')

    def delete_contact_window(self):
        """
        Метод создающий окно удаления контакта.
        :return:
        """
        self.remove_dialog = DelContactDialog(self.database)
        self.remove_dialog.btn_ok.clicked.connect(
            lambda: self.delete_contact(self.remove_dialog))
        self.remove_dialog.show()

    def delete_contact(self, item):
        """
        Метод удаляющий контакт из серверной и клиентсткой BD.
        После обновления баз данных обновляет и содержимое окна.
        :param item: Выбранный контакт.
        :return:
        """
        selected = item.selector.currentText()
        try:
            self.transport.remove_contact(selected)
        except ServerError as err:
            self.messages.critical(self, 'Ошибка сервера', err.text)
        except OSError as err:
            if err.errno:
                self.messages.critical(self, 'Ошибка',
                                       'Потеряно соединение с сервером!')
                self.close()
            self.messages.critical(self, 'Ошибка', 'Таймаут соединения!')
        else:
            self.database.del_contact(selected)
            self.clients_list_update()
            # logger.info(f'Успешно удалён контакт {selected}')
            self.messages.information(self, 'Успех', 'Контакт успешно удалён.')
            item.close()
            # Если удалён активный пользователь, то деактивируем поля ввода.
            if selected == self.current_chat:
                self.current_chat = None
                self.set_disabled_input()

    def send_message(self):
        """
        Функция отправки сообщения текущему собеседнику.
        Реализует шифрование сообщения и его отправку.
        :return:
        """
        # Текст в поле, проверяем что поле не пустое,
        # затем забирается сообщение и поле очищается
        message_text = self.ui.text_message.toPlainText()
        self.ui.text_message.clear()
        if not message_text:
            return
        message_text_encrypted = self.encryptor.encrypt(
            message_text.encode('utf8'))
        message_text_encrypted_base64 = base64.b64encode(
            message_text_encrypted)
        try:
            self.transport.send_message(
                self.current_chat,
                message_text_encrypted_base64.decode('ascii'))
        except ServerError as err:
            self.messages.critical(self, 'Ошибка', err.text)
        except OSError as err:
            if err.errno:
                self.messages.critical(self, 'Ошибка',
                                       'Потеряно соединение с сервером!')
                self.close()
            self.messages.critical(self, 'Ошибка', 'Таймаут соединения!')
        except (ConnectionResetError, ConnectionAbortedError):
            self.messages.critical(self, 'Ошибка',
                                   'Потеряно соединение с сервером!')
            self.close()
        else:
            if self.current_chat != self.transport.user_name:
                self.database.save_message(self.current_chat, "out",
                                           message_text)
            self.history_list_update()

    # Слот приёма нового сообщений
    @pyqtSlot(Message)
    def message(self, message: Message):
        """
        Слот обработчик поступаемых сообщений, выполняет дешифровку
        поступаемых сообщений и их сохранение в истории сообщений.
        Запрашивает пользователя если пришло сообщение не от текущего
        собеседника. При необходимости меняет собеседника.
        :param message: Полученное сообщение
        :return:
        """
        sender = message.sender
        # Получаем строку байтов
        encrypted_message = base64.b64decode(message.text)
        # Декодируем строку, при ошибке выдаём сообщение и завершаем функцию
        try:
            decrypted_message = self.transport.decrypter.decrypt(
                encrypted_message)
        except (ValueError, TypeError):
            self.messages.warning(self, 'Ошибка',
                                  'Не удалось декодировать сообщение.')
            return
        # Сохраняем сообщение в базу и обновляем историю сообщений
        # или открываем новый чат.
        self.database.save_message(sender, 'in',
                                   decrypted_message.decode('utf8'))
        if sender == self.current_chat:
            self.history_list_update()
        else:
            # Проверим есть ли такой пользователь у нас в контактах:
            if self.database.check_contact(sender):
                # Если есть, спрашиваем и желании открыть с ним чат
                # и открываем при желании
                if self.messages.question(
                        self, 'Новое сообщение',
                        f'Получено новое сообщение от '
                        f'{sender}, открыть чат с ним?', QMessageBox.Yes,
                        QMessageBox.No) == QMessageBox.Yes:
                    self.current_chat = sender
                    self.set_active_user()
            else:
                # Раз нету,спрашиваем хотим ли добавить юзера в контакты.
                if self.messages.question(
                        self, 'Новое сообщение',
                        f'Получено новое сообщение от '
                        f'{sender}.\n Данного пользователя нет в '
                        f'вашем контакт-листе.\n '
                        f'Добавить в контакты и открыть чат с ним?',
                        QMessageBox.Yes, QMessageBox.No) == QMessageBox.Yes:
                    self.add_contact(sender)
                    self.current_chat = sender
                    self.set_active_user()

    @pyqtSlot()
    def connection_lost(self):
        """
        Слот обработчик потери соеднинения с сервером.
        Выдаёт окно предупреждение и завершает работу приложения.
        :return:
        """
        self.messages.warning(self, 'Сбой соединения',
                              'Потеряно соединение с сервером. ')
        self.close()

    def make_connection(self, trans_obj):
        """
        Метод обеспечивающий соединение сигналов и слотов.
        :param trans_obj:
        :return:
        """
        trans_obj.new_message.connect(self.message)
        trans_obj.connection_lost.connect(self.connection_lost)


class UserNameDialog(QDialog):
    """
    Класс реализующий стартовый диалог с запросом логина и пароля
    пользователя.
    """
    def __init__(self):
        super().__init__()

        self.ok_pressed = False

        self.setWindowTitle('Привет!')
        self.setFixedSize(175, 135)

        self.label = QLabel('Введите имя пользователя:', self)
        self.label.move(10, 10)
        self.label.setFixedSize(150, 10)

        self.client_name = QLineEdit(self)
        self.client_name.setFixedSize(154, 20)
        self.client_name.move(10, 30)

        self.btn_ok = QPushButton('Начать', self)
        self.btn_ok.move(10, 105)
        self.btn_ok.clicked.connect(self.click)

        self.btn_cancel = QPushButton('Выход', self)
        self.btn_cancel.move(90, 105)
        self.btn_cancel.clicked.connect(qApp.exit)

        self.label_passwd = QLabel('Введите пароль:', self)
        self.label_passwd.move(10, 55)
        self.label_passwd.setFixedSize(150, 15)

        self.client_passwd = QLineEdit(self)
        self.client_passwd.setFixedSize(154, 20)
        self.client_passwd.move(10, 75)
        self.client_passwd.setEchoMode(QLineEdit.Password)

        self.show()

    def click(self):
        """
        Метод обрабтчик кнопки ОК, если поле вводе не пустое,
        ставим флаг и завершаем приложение.
        :return:
        """
        if self.client_name.text():
            self.ok_pressed = True
            qApp.exit()


class AddContactDialog(QDialog):
    """
    Диалог добавления пользователя в список контактов.
    Предлагает пользователю список возможных контактов и
    добавляет выбранный в контакты.
    """
    def __init__(self, transport, database):
        super().__init__()
        self.transport = transport
        self.database = database

        self.setFixedSize(350, 120)
        self.setWindowTitle('Выберите контакт для добавления:')
        self.setAttribute(Qt.WA_DeleteOnClose)
        self.setModal(True)

        self.selector_label = QLabel('Выберите контакт для добавления:', self)
        self.selector_label.setFixedSize(200, 20)
        self.selector_label.move(10, 0)

        self.selector = QComboBox(self)
        self.selector.setFixedSize(200, 20)
        self.selector.move(10, 30)

        self.btn_refresh = QPushButton('Обновить список', self)
        self.btn_refresh.setFixedSize(100, 30)
        self.btn_refresh.move(60, 60)

        self.btn_ok = QPushButton('Добавить', self)
        self.btn_ok.setFixedSize(100, 30)
        self.btn_ok.move(230, 20)

        self.btn_cancel = QPushButton('Отмена', self)
        self.btn_cancel.setFixedSize(100, 30)
        self.btn_cancel.move(230, 60)
        self.btn_cancel.clicked.connect(self.close)

        # Заполняем список возможных контактов
        self.update_possible_contacts()
        # Назначаем действие на кнопку обновить
        self.btn_refresh.clicked.connect(self.update_possible_contacts)

    def possible_contacts_update(self):
        """
        Метод заполнения списка возможных контактов.
        Создаёт список всех зарегистрированных пользователей
        за исключением уже добавленных в контакты и самого себя.
        :return:
        """
        self.selector.clear()
        # множества всех контактов и контактов клиента
        contacts_list = set(self.database.get_contacts())
        users_list = set(self.database.get_connected())
        # Удалим сами себя из списка пользователей,
        # чтобы нельзя было добавить самого себя
        users_list.remove(self.transport.user_name)
        # Добавляем список возможных контактов
        self.selector.addItems(users_list - contacts_list)

    def update_possible_contacts(self):
        """
        Метод обновления списка возможных контактов. Запрашивает с сервера
        список известных пользователей и обновляет содержимое окна.
        :return:
        """
        try:
            self.transport.user_list_update()
        except OSError:
            pass
        else:
            self.possible_contacts_update()


class DelContactDialog(QDialog):
    """
    Диалог удаления контакта. Прделагает текущий список контактов,
    не имеет обработчиков для действий.
    """
    def __init__(self, database):
        super().__init__()
        self.database = database

        self.setFixedSize(350, 120)
        self.setWindowTitle('Выберите контакт для удаления:')
        self.setAttribute(Qt.WA_DeleteOnClose)
        self.setModal(True)

        self.selector_label = QLabel('Выберите контакт для удаления:', self)
        self.selector_label.setFixedSize(200, 20)
        self.selector_label.move(10, 0)

        self.selector = QComboBox(self)
        self.selector.setFixedSize(200, 20)
        self.selector.move(10, 30)

        self.btn_ok = QPushButton('Удалить', self)
        self.btn_ok.setFixedSize(100, 30)
        self.btn_ok.move(230, 20)

        self.btn_cancel = QPushButton('Отмена', self)
        self.btn_cancel.setFixedSize(100, 30)
        self.btn_cancel.move(230, 60)
        self.btn_cancel.clicked.connect(self.close)

        # заполнитель контактов для удаления
        self.selector.addItems(sorted(self.database.get_contacts()))
