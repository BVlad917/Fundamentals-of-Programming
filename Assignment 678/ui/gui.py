from PyQt5 import QtWidgets, QtCore


def screen_size():
    for display in range(QtWidgets.QDesktopWidget().screenCount()):
        size = QtWidgets.QDesktopWidget().screenGeometry(display)
        return size.width(), size.height()


class Item:
    def __init__(self, title, action_type, text_field_count=None, action=None, on_click=None,
                 labels=None, to_show=None):
        self.title = title
        self.actionType = action_type
        self.textfieldCount = text_field_count
        self.action = action
        self.onClick = on_click
        self.labels = None if labels == [] else labels
        self.toShow = to_show


class ButtonStack(QtWidgets.QWidget):
    def __init__(self, function, person_service, activity_service, undo_service, redo_service):
        super().__init__()
        self.function = function
        self._person_service = person_service
        self._activity_service = activity_service
        self._undo_service = undo_service
        self._redo_service = redo_service
        vbox = QtWidgets.QVBoxLayout()

        items = [
            Item(title="Add Person", action_type="edit", text_field_count=3,
                 on_click=lambda textArray: self._person_service.add_person(textArray[0], textArray[1], textArray[2]),
                 labels=["ID", "Name", "Phone Number"]),

            Item(title="Remove Person", action_type="edit", text_field_count=1,
                 on_click=lambda textArray: self.remove_person_helper(textArray[0]), labels=["ID"]),

            Item(title="Update Person Name", action_type="edit", text_field_count=2,
                 on_click=lambda params: self._person_service.update_person_name(params[0], params[1]),
                 labels=["ID", "New Name"]),

            Item(title="Update Person Phone Number", action_type="edit", text_field_count=2,
                 on_click=lambda params: self._person_service.update_person_phone_number(params[0], params[1]),
                 labels=["ID", "New Phone Number"]),

            Item(title="List all persons", action_type="show",
                 to_show=lambda person_service=self._person_service: person_service.get_all_persons_string()),

            Item(title="Add Activity", action_type="edit", text_field_count=5,
                 on_click=lambda params: self._activity_service.add_activity(params[0], params[1], params[2],
                                                                             params[3], params[4]),
                 labels=['ID', 'Start Datetime', 'End Datetime', 'Description', 'Registered persons']),

            Item(title="Remove Activity", action_type="edit", text_field_count=1,
                 on_click=lambda params: self._activity_service.delete_activity_by_id(params[0]), labels=['ID']),

            Item(title="Update activity starting time", action_type="edit", text_field_count=3,
                 on_click=lambda params: self._activity_service.update_activity_start_date_time(params[0], params[1],
                                                                                                params[2]),
                 labels=['ID', 'New date', 'New time']),

            Item(title="Update activity ending time", action_type="edit", text_field_count=3,
                 on_click=lambda params: self._activity_service.update_activity_end_date_time(params[0], params[1],
                                                                                              params[2]),
                 labels=['ID', 'New date', 'New time']),

            Item(title="Update activity description", action_type="edit", text_field_count=2,
                 on_click=lambda params: self._activity_service.update_activity_description(params[0], params[1]),
                 labels=['ID', 'New description']),

            Item(title="List all activities", action_type="show",
                 to_show=lambda activity_service=self._activity_service: activity_service.get_all_activities_string()),

            Item(title="Add persons to activity", action_type="edit", text_field_count=2,
                 on_click=lambda params: self._activity_service.add_persons_by_id_to_activity(params[0], params[1]),
                 labels=['Activity ID', 'Person IDs']),

            Item(title="Remove persons from activity", action_type="edit", text_field_count=2,
                 on_click=lambda params: self._activity_service.remove_persons_by_id_from_activity(params[0],
                                                                                                   params[1]),
                 labels=['Activity ID', 'Person IDs']),

            Item(title='Search persons by name', action_type='filter', text_field_count=1,
                 on_click=lambda text: self._person_service.get_search_person_by_name_string(text),
                 labels=['Person Name']),

            Item(title='Search persons by phone number', action_type='filter', text_field_count=1,
                 on_click=lambda text: self._person_service.get_search_persons_by_phone_number_string(text),
                 labels=['Phone Number']),

            Item(title='Search activity by description', action_type='filter', text_field_count=1,
                 on_click=lambda text: self._activity_service.get_search_activity_by_description_string(text),
                 labels=['Description']),

            Item(title='Search activity by datetime', action_type='filter', text_field_count=1,
                 on_click=lambda text: self._activity_service.get_search_activity_by_datetime_string(text),
                 labels=['Datetime']),

            Item(title='Sorted activities in given date', action_type='filter', text_field_count=1,
                 on_click=lambda text: self._activity_service.get_sorted_activities_in_given_date_string(text),
                 labels=['Date']),

            Item(title='Busiest days of a person', action_type='filter', text_field_count=1,
                 on_click=lambda text: self._activity_service.get_busiest_days_person_string(text),
                 labels=['Person name/ID']),

            Item(title='All activities with a person', action_type='filter', text_field_count=1,
                 on_click=lambda text: self._activity_service.get_activities_with_given_person_string(text),
                 labels=['Person name/ID']),

            Item(title='Undo', action_type='undo', action=self._undo_service.apply_undo),

            Item(title='Redo', action_type='undo', action=self._redo_service.apply_redo)
        ]
        for item in items:
            button = self.renderButton(item)
            vbox.addWidget(button)
        self.setLayout(vbox)

    def remove_person_helper(self, input_id):
        self._activity_service.delete_person_from_activities(input_id)
        self._person_service.delete_person_by_id(input_id)

    def renderButton(self, item):
        button = QtWidgets.QPushButton(item.title, self)
        button.clicked.connect(lambda: self.onClick(item))
        return button

    @QtCore.pyqtSlot()
    def onClick(self, item):
        self.function(item)


class Home(QtWidgets.QMainWindow):
    def __init__(self, person_service, activity_service, undo_service, redo_service):
        super().__init__()
        self.setWindowTitle("App")
        (width, height) = screen_size()
        self.setGeometry(0, 0, width, height)
        self._person_service = person_service
        self._activity_service = activity_service
        self._undo_service = undo_service
        self._redo_service = redo_service
        self._initUI()


    def _initUI(self):
        self.stackedWidget = QtWidgets.QStackedWidget()
        self.setCentralWidget(self.stackedWidget)
        self.buttonStack = ButtonStack(lambda action: self.navigate(action), self._person_service,
                                       self._activity_service, self._undo_service, self._redo_service)
        self.editPage = EditPage(
            back=lambda: self.stackedWidget.setCurrentWidget(self.buttonStack))
        self.infoPage = InfoPage(
            back=lambda: self.stackedWidget.setCurrentWidget(self.buttonStack))
        self.filterPage = FilterPage(
            back=lambda: self.stackedWidget.setCurrentWidget(self.buttonStack))
        self.stackedWidget.addWidget(self.buttonStack)
        self.stackedWidget.addWidget(self.editPage)
        self.stackedWidget.addWidget(self.infoPage)
        self.stackedWidget.addWidget(self.filterPage)
        self.stackedWidget.setCurrentWidget(self.buttonStack)

    def navigate(self, item):
        if item.action is not None:
            try:
                item.action()
            except Exception as e:
                box = QtWidgets.QMessageBox()
                box.setText((str(e)))
                box.exec_()
        if item.actionType == "edit":
            self.editPage.labels = item.labels
            self.editPage.onClick = item.onClick
            self.editPage.textfieldCount = item.textfieldCount
            self.stackedWidget.setCurrentWidget(self.editPage)
        elif item.actionType == "show":
            try:
                self.infoPage.text = item.toShow()
                self.stackedWidget.setCurrentWidget(self.infoPage)
            except Exception as e:
                box = QtWidgets.QMessageBox()
                box.setText(str(e))
                box.exec_()
        elif item.actionType == 'filter':
            self.filterPage.textfieldLabelText = item.labels[0]
            self.filterPage.onClick = item.onClick
            self.stackedWidget.setCurrentWidget(self.filterPage)


class FilterPage(QtWidgets.QWidget):
    @property
    def text(self):
        return self._text

    @text.setter
    def text(self, newValue):
        self.toShowLabel.setText(newValue)
        self.toShowLabel.repaint()

    @property
    def textfieldLabelText(self):
        return self._textfieldLabelText

    @textfieldLabelText.setter
    def textfieldLabelText(self, newValue):
        self.textfieldLabel.setText(newValue)

    def __init__(self, back):
        super().__init__()
        self.back = back
        vbox = QtWidgets.QVBoxLayout()

        backButton = QtWidgets.QPushButton("Back", self)
        backButton.clicked.connect(self.back)
        vbox.addWidget(backButton)

        itemHbox = QtWidgets.QHBoxLayout()
        self.textfield = QtWidgets.QLineEdit(self)
        self.textfieldLabel = QtWidgets.QLabel()
        self.textfieldLabel.setMinimumWidth(100)
        itemHbox.addWidget(self.textfieldLabel)
        itemHbox.addWidget(self.textfield)
        vbox.addLayout(itemHbox)

        self.toShowLabel = QtWidgets.QLabel()
        vbox.addWidget(self.toShowLabel)

        showButton = QtWidgets.QPushButton("Show", self)
        showButton.clicked.connect(self.onShowClick)
        vbox.addWidget(showButton)
        self.setLayout(vbox)

    @QtCore.pyqtSlot()
    def onShowClick(self):
        if self.onClick is not None:
            try:
                self.text = self.onClick(self.textfield.text())
            except Exception as e:
                box = QtWidgets.QMessageBox()
                box.setText(str(e))
                box.exec_()


class InfoPage(QtWidgets.QWidget):
    @property
    def text(self):
        return self._text

    @text.setter
    def text(self, newValue):
        self.label.setText(newValue)

    def __init__(self, back):
        super().__init__()
        self.back = back
        vbox = QtWidgets.QVBoxLayout()

        backButton = QtWidgets.QPushButton("Back", self)
        backButton.clicked.connect(self.back)
        vbox.addWidget(backButton)

        self.label = QtWidgets.QLabel()
        vbox.addWidget(self.label)

        self.setLayout(vbox)


class EditPage(QtWidgets.QWidget):
    @property
    def textfieldCount(self):
        return self._textfieldCount

    @textfieldCount.setter
    def textfieldCount(self, newValue):
        if newValue is not None:
            self.renderTextfields(newValue)

    def __init__(self, back):
        super().__init__()
        self._textfieldCount = None
        self.textfields = []
        self.labels = []
        self.back = back

        self.vbox = QtWidgets.QVBoxLayout()

        backButton = QtWidgets.QPushButton("Back", self)
        backButton.clicked.connect(self.back)
        self.vbox.addWidget(backButton)

        okButton = QtWidgets.QPushButton("OK", self)
        okButton.clicked.connect(self.onOkClick)
        self.vbox.addWidget(okButton)

        self.setLayout(self.vbox)

    def deleteItemsOfLayout(self, layout, hasButtons):
        if layout is not None:
            r = reversed(range(1, layout.count() - 1)
                         ) if hasButtons else reversed(range(layout.count()))
            for i in r:
                item = layout.takeAt(i)
                widget = item.widget()
                if widget is not None:
                    widget.setParent(None)
                else:
                    self.deleteItemsOfLayout(item.layout(), hasButtons=False)

    def renderTextfields(self, count):
        self.deleteItemsOfLayout(self.vbox, hasButtons=True)
        self.textfields = []
        for i in range(count):
            itemHbox = QtWidgets.QHBoxLayout()
            textfield = QtWidgets.QLineEdit(self)
            label = QtWidgets.QLabel()
            label.setText(self.labels[i])
            label.setMinimumWidth(100)
            itemHbox.addWidget(label)
            itemHbox.addWidget(textfield)
            self.textfields.append(textfield)
            self.vbox.insertLayout(self.vbox.count() - 1, itemHbox)

    @QtCore.pyqtSlot()
    def onOkClick(self):
        if self.onClick is not None:
            try:
                self.onClick(list(map(lambda textfield: textfield.text(), self.textfields)))
                self.back()
            except Exception as e:
                box = QtWidgets.QMessageBox()
                box.setText(str(e))
                box.exec_()

    @QtCore.pyqtSlot()
    def back(self):
        self.back()

