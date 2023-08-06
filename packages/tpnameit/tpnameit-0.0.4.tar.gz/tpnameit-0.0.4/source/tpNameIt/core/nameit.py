#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
Manager that controls the naming convention used on rigging tools
"""

from __future__ import print_function, division, absolute_import

# TODO: When changing a token name, check the list of expressions and update them if an expression was already using that token

import os
import re
from functools import partial
from collections import OrderedDict

from Qt.QtCore import *
from Qt.QtWidgets import *

import tpQtLib
from tpQtLib.core import base

import tpNameIt
from tpPyUtils import jsonio
from tpNameIt.core import namelib as naming


class NameItWindow(tpQtLib.MainWindow, object):
    def __init__(self):
        super(NameItWindow, self).__init__(
            name='NamingManagerWindow',
            title='RigLib - Naming Manager',
            size=(800, 535),
            fixed_size=False,
            auto_run=True,
            frame_less=True,
            use_style=False
        )

        # Setup ToolBar
        self._setup_toolbar()

    def ui(self):
        super(NameItWindow, self).ui()

        self._name_it = NameIt()
        self.main_layout.addWidget(self._name_it)

    def _setup_toolbar(self):
        toolbar = self.add_toolbar('Main ToolBar')
        toolbar.setMovable(True)
        toolbar.setAllowedAreas(Qt.TopDockWidgetArea | Qt.BottomDockWidgetArea)

        if self._is_renamer_tool_available():
            play_icon = tpNameIt.resource.icon('rename')
            renamer_btn = QToolButton()
            renamer_btn.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
            run_tasks_action = QAction(play_icon, 'Renamer', renamer_btn)
            renamer_btn.setDefaultAction(run_tasks_action)
            renamer_btn.clicked.connect(self._on_open_renamer_tool)
            toolbar.addWidget(renamer_btn)
        else:
            toolbar.setVisible(False)

    def _on_open_renamer_tool(self):
        """
        Internal function that is used by toolbar to open Renamer Tool
        """

        try:
            import tpRenamer
            tpRenamer.run(True)
        except Exception:
            tpNameIt.logger.warning('Renamer Tools is not available!')
            return None

    def _is_renamer_tool_available(self):
        """
        Returns whether or not tpRenamer tool is available or not
        :return: bool
        """

        try:
            import tpRenamer
        except Exception:
            return False

        return True


class NameIt(base.BaseWidget, object):

    ACTIVE_RULE = None

    # You can override this function to store naming data files in custom path
    DATA_FILE = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'data', 'naming_data.json')

    def __init__(self, parent=None):
        super(NameIt, self).__init__(parent=parent)

    @staticmethod
    def get_active_rule():

        """
        Returns the current naming active rule
        """

        return naming.active_rule()

    @classmethod
    def set_active_rule(cls, name):
        """
        Sets the current active rule
        :param name: str
        """

        # First, we clean the status of the naming library
        naming.remove_all_tokens()
        naming.remove_all_rules()

        # Load rules from the naming manager
        rules = NamingData.get_rules(data_file=cls.DATA_FILE)
        for rule in rules:
            expressions = rule.get_expression_tokens()
            naming.add_rule(rule.name, rule.iterator_format, *expressions)

        # Load tokens from the naming manager
        tokens = NamingData.get_tokens(data_file=cls.DATA_FILE)
        for token in tokens:
            tokens_keywords = token.get_values_as_keyword()
            naming.add_token(token.name, **tokens_keywords)

        naming.set_active_rule(name)

    @classmethod
    def set_active_rule_iterator(cls, iterator_format):
        active_rule = cls.get_active_rule()
        if not active_rule:
            return

    @classmethod
    def set_active_rule_auto_fix(cls, auto_fix):
        active_rule = cls.get_active_rule()
        if not active_rule:
            return

        naming.set_rule_auto_fix(active_rule.name(), auto_fix)

    @classmethod
    def parse_field_from_string(cls, string_to_parse, field_name):
        active_rule = cls.get_active_rule()
        if not active_rule:
            return None

        string_split = string_to_parse.split('_')
        if len(string_split) <= 0:
            return None

        rule_fields = active_rule.fields()
        if len(rule_fields) != len(string_split):
            tpNameIt.logger.warning('Given string "{}" is not a valid name generated with current nomenclature rule: {}'.format(string_to_parse, active_rule.name()))
            return None

        found_index = -1
        for rule_field in rule_fields:
            if rule_field == field_name:
                found_index += 1
                break
            found_index += 1

        if found_index > -1:
            return string_split[found_index]

        return None

    @staticmethod
    def solve(*args, **kwargs):
        if len(args) > 0 and len(kwargs) > 0:
            return naming.solve(*args, **kwargs)
        else:
            if len(args) > 0:
                return naming.solve(*args)
            else:
                return naming.solve(**kwargs)

    def ui(self):
        super(NameIt, self).ui()

        base_layout = QHBoxLayout()
        base_layout.setContentsMargins(0,0,0,0)
        base_layout.setSpacing(0)
        self.main_layout.addLayout(base_layout)

        left_panel_widget = QWidget()
        left_panel_widget.setFixedWidth(250)
        left_panel_layout = QVBoxLayout()
        left_panel_layout.setContentsMargins(5, 0, 5, 0)
        left_panel_widget.setLayout(left_panel_layout)
        base_layout.addWidget(left_panel_widget)

        # Tab Widget
        rules_tab = QWidget()
        tokens_tab = QWidget()

        self.tabs = QTabWidget()
        self.tabs.addTab(rules_tab, 'Rules')
        self.tabs.addTab(tokens_tab, 'Tokens')
        left_panel_layout.addWidget(self.tabs)

        # Rules Tab
        rules_main_layout = QVBoxLayout()
        rules_main_layout.setContentsMargins(5, 5, 5, 5)
        rules_main_layout.setSpacing(0)
        self.rules_list = QListWidget()
        rules_main_layout.addWidget(self.rules_list)
        left_panel_buttons_layout_rules = QHBoxLayout()
        left_panel_buttons_layout_rules.setContentsMargins(5, 5, 5, 0)
        rules_main_layout.addLayout(left_panel_buttons_layout_rules)
        self.add_rule_btn = QPushButton('+')
        self.remove_rule_btn = QPushButton('-')
        left_panel_buttons_layout_rules.addItem(QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Minimum))
        left_panel_buttons_layout_rules.addWidget(self.add_rule_btn)
        left_panel_buttons_layout_rules.addItem(QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Minimum))
        left_panel_buttons_layout_rules.addWidget(self.remove_rule_btn)
        left_panel_buttons_layout_rules.addItem(QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Minimum))
        rules_tab.setLayout(rules_main_layout)

        # Tokens Tab
        tokens_main_layout = QVBoxLayout()
        tokens_main_layout.setContentsMargins(5, 5, 5, 5)
        tokens_main_layout.setSpacing(0)
        self.tokens_list = QListWidget()
        tokens_main_layout.addWidget(self.tokens_list)
        left_panel_buttons_layout_tokens = QHBoxLayout()
        left_panel_buttons_layout_tokens.setContentsMargins(5, 5, 5, 0)
        tokens_main_layout.addLayout(left_panel_buttons_layout_tokens)
        self.add_token_btn = QPushButton('+')
        self.remove_token_btn = QPushButton('-')
        left_panel_buttons_layout_tokens.addItem(QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Minimum))
        left_panel_buttons_layout_tokens.addWidget(self.add_token_btn)
        left_panel_buttons_layout_tokens.addItem(QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Minimum))
        left_panel_buttons_layout_tokens.addWidget(self.remove_token_btn)
        left_panel_buttons_layout_tokens.addItem(QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Minimum))
        tokens_tab.setLayout(tokens_main_layout)

        # === PROPERTIES === #
        main_group = QGroupBox('Properties')
        base_layout.addWidget(main_group)
        group_layout = QVBoxLayout()
        group_layout.setContentsMargins(5, 5, 5, 5)
        group_layout.setSpacing(0)
        main_group.setLayout(group_layout)

        # Rules Panel
        self.rules_widget = QWidget()
        rules_layout = QVBoxLayout()
        self.rules_widget.setLayout(rules_layout)
        expression_layout = QHBoxLayout()
        expression_layout.setContentsMargins(5, 5, 5, 5)
        expression_layout.setSpacing(5)
        expression_lbl = QLabel('Expression:  ')
        self.expression_line = QLineEdit()
        self.expression_btn = QPushButton('   <')
        self.expression_btn.setEnabled(False)
        self.expression_btn.setStyleSheet("QPushButton::menu-indicator{image:url(none.jpg);}")
        self.expression_menu = QMenu(self)
        self.expression_btn.setMenu(self.expression_menu)
        expression_layout.addWidget(expression_lbl)
        expression_layout.addWidget(self.expression_line)
        expression_layout.addWidget(self.expression_btn)
        rules_layout.addLayout(expression_layout)

        iterator_layout = QHBoxLayout()
        iterator_layout.setContentsMargins(5, 5, 5, 5)
        iterator_layout.setSpacing(5)
        iterator_lbl = QLabel('Iterator:         ')
        self.iterator_cbx = QComboBox()
        self.iterator_cbx.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        for it_format in ['@', '@^', '#', '##', '###']:
            self.iterator_cbx.addItem(it_format)
        iterator_layout.addWidget(iterator_lbl)
        iterator_layout.addWidget(self.iterator_cbx)
        rules_layout.addLayout(iterator_layout)

        description_rule_layout = QHBoxLayout()
        description_rule_layout.setContentsMargins(5, 5, 5, 5)
        description_rule_layout.setSpacing(5)
        description_rule_lbl_layout = QVBoxLayout()
        description_rule_lbl = QLabel('Description: ')
        description_rule_lbl.setAlignment(Qt.AlignTop)
        description_rule_layout.addWidget(description_rule_lbl)
        self.description_rule_text = QTextEdit()
        description_rule_layout.addLayout(description_rule_lbl_layout)
        description_rule_layout.addWidget(self.description_rule_text)
        rules_layout.addLayout(description_rule_layout)
        rules_layout.addItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Minimum))
        group_layout.addWidget(self.rules_widget)

        # Tokens Panel
        self.tokens_widget = QWidget()
        tokens_layout = QVBoxLayout()
        self.tokens_widget.setLayout(tokens_layout)
        values_layout = QHBoxLayout()
        values_layout.setContentsMargins(5, 5, 5, 5)
        values_layout.setSpacing(5)
        valuesLbl = QLabel('Values: ')
        values_layout.addWidget(valuesLbl)
        values_layout.addItem(QSpacerItem(25, 20, QSizePolicy.Minimum, QSizePolicy.Minimum))
        data = {'key': [], 'value': []}
        self.values_table = TokensTable(data, 0, 2)
        values_layout.addWidget(self.values_table)
        self.values_table.setColumnWidth(0, 140)
        self.values_table.setColumnWidth(1, 140)
        self.values_table.setFixedWidth(300)
        values_buttons_layout = QVBoxLayout()
        values_buttons_layout.setContentsMargins(5, 5, 5, 0)
        values_layout.addLayout(values_buttons_layout)
        self.add_key_value_btn = QPushButton('+')
        self.remove_key_value_btn = QPushButton('-')
        values_buttons_layout.addWidget(self.add_key_value_btn)
        values_buttons_layout.addItem(QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Minimum))
        values_buttons_layout.addWidget(self.remove_key_value_btn)
        values_buttons_layout.addItem(QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Minimum))
        default_layout = QHBoxLayout()
        default_layout.setContentsMargins(5, 5, 5, 5)
        default_layout.setSpacing(5)
        default_lbl = QLabel('Default: ')
        self.default_cbx = QComboBox()
        self.default_cbx.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Maximum)
        default_layout.addWidget(default_lbl)
        default_layout.addItem(QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Minimum))
        default_layout.addWidget(self.default_cbx)
        description_token_layout = QHBoxLayout()
        description_token_layout.setContentsMargins(5, 5, 5, 5)
        description_token_layout.setSpacing(5)
        description_token_lbl = QLabel('Description: ')
        self.description_token_text = QTextEdit()
        description_token_layout.addWidget(description_token_lbl)
        description_token_layout.addWidget(self.description_token_text)
        tokens_layout.addLayout(values_layout)
        tokens_layout.addLayout(default_layout)
        tokens_layout.addLayout(description_token_layout)
        group_layout.addWidget(self.tokens_widget)
        self.tokens_widget.hide()

        # Initialize database
        self._init_db()

        # First update of the UI
        self.update_expression_menu()
        self.update_tokens_properties_state()
        self.update_rules_properties_state()

    def setup_signals(self):
        super(NameIt, self).setup_signals()

        self.tabs.currentChanged.connect(self.on_change_tab)
        self.add_rule_btn.clicked.connect(self.on_add_rule)
        self.remove_rule_btn.clicked.connect(self.on_remove_rule)
        self.rules_list.currentItemChanged.connect(self.on_change_rule)
        self.rules_list.itemChanged.connect(self.on_edit_rule_name)
        self.expression_line.textChanged.connect(self.on_edit_rule_expression)
        self.description_rule_text.textChanged.connect(self.on_edit_rule_description)
        self.iterator_cbx.currentIndexChanged.connect(self.on_edit_rule_iterator)
        self.add_token_btn.clicked.connect(self.on_add_token)
        self.remove_token_btn.clicked.connect(self.on_remove_token)
        self.tokens_list.currentItemChanged.connect(self.on_change_token)
        self.tokens_list.itemChanged.connect(self.on_edit_token_name)
        self.values_table.itemChanged.connect(self.on_change_token_value)
        self.add_key_value_btn.clicked.connect(self.on_add_token_value)
        self.remove_key_value_btn.clicked.connect(self.on_remove_token_value)
        self.description_token_text.textChanged.connect(self.on_edit_token_description)
        self.default_cbx.currentIndexChanged.connect(self.on_edit_token_default)

    def add_expression(self, name):

        """
        Add an expression to the list of expressions
        :param str name: Expression name
        :return: None
        """

        if self.expression_line.text() == '':
            self.expression_line.setText('{' + name + '}')
        else:
            self.expression_line.setText(self.expression_line.text() + '_{' + name + '}')

    def update_expression_menu(self):

        """
        Updates the expression menu
        :return:
        """

        # First, we clear the expression menu
        self.expression_menu.clear()

        tokens = NamingData.get_tokens(data_file=self.DATA_FILE)
        if tokens and len(tokens) > 0:
            self.expression_btn.setEnabled(True)
            tokens = NamingData.get_tokens(data_file=self.DATA_FILE)
            for token in tokens:
                self.expression_menu.addAction(token.name, partial(self.add_expression, token.name))
        else:
            self.expression_btn.setEnabled(False)

    def update_expression_state(self):
        # TODO: This method is used to check the name of the expression (its different parts) and
        # TODO: check if some token of the expression does not exist and in that case, update the expression
        # TODO: so it becomes a valid expression
        pass

    def update_rules_properties_state(self):
        if self.rules_list.count() <= 0 or self.rules_list.currentItem() is None:
            self.expression_line.setText('')
            self.description_rule_text.setText('')
            self.iterator_cbx.setCurrentIndex(0)
            self.rules_widget.setEnabled(False)
        else:
            rule = NamingData.get_rule(self.rules_list.currentRow(), data_file=self.DATA_FILE)
            if rule is not None:
                self.expression_line.setText(rule.expression)
                self.description_rule_text.setText(rule.description)
                self.iterator_cbx.setCurrentText(rule.iterator_format)
            self.rules_widget.setEnabled(True)

    def update_tokens_properties_state(self):
        if self.tokens_list.currentItem() is None:
            self.tokens_widget.setEnabled(False)
        else:
            self.tokens_widget.setEnabled(True)

    def update_default_token_list(self):

        self.default_cbx.blockSignals(True)

        for i in range(self.default_cbx.count()):
            self.default_cbx.removeItem(self.default_cbx.count() - 1)

        item = self.tokens_list.currentRow()
        self.default_cbx.addItem('')
        tokens = NamingData.get_tokens(data_file=self.DATA_FILE)
        for value in tokens[item].values['key']:
            self.default_cbx.addItem(value)

        self.default_cbx.setCurrentIndex(NamingData.get_default_index(item, data_file=self.DATA_FILE))

        self.default_cbx.blockSignals(False)

    def update_tokens_key_table(self):

        item = self.tokens_list.currentRow()
        self.clean_tokens_key_table()
        if self.tokens_list.count() > 0:
            keys = []
            values = []
            tokens = NamingData.get_tokens(data_file=self.DATA_FILE)
            for i in range(len(tokens[item].values['key'])):
                self.values_table.insertRow(self.values_table.rowCount())
                keys.append(QTableWidgetItem())
                values.append(QTableWidgetItem())

            for index, value in enumerate(tokens[item].values['key']):
                keys[index].setText(value)
                self.values_table.setItem(index, 0, keys[index])

            for index, value in enumerate(tokens[item].values['value']):
                values[index].setText(value)
                self.values_table.setItem(index, 1, values[index])

    def clean_tokens_key_table(self):
        for i in range(self.values_table.rowCount()):
            self.values_table.removeRow(self.values_table.rowCount() - 1)

    def on_change_tab(self, tab_index):

        """
        This methods changes the properties tab widgets
        :param tab_index: Index of the current tab (0:rules tab, 1:tokens tab)
        :return: None
        """

        if tab_index == 0:
            self.rules_widget.show()
            self.tokens_widget.hide()
            self.update_expression_menu()
            self.update_expression_state()
        else:
            self.rules_widget.hide()
            self.tokens_widget.show()
            self.update_tokens_properties_state()

    def on_add_rule(self, *args):

        """
        Creates a new standard rule and add it to the Naming Manager
        :return:
        """

        load_rule = True
        if len(args) == 0:
            load_rule = False

        self.description_rule_text.blockSignals(True)

        rule = None
        if not load_rule:
            rule = Rule()
        elif load_rule and len(args) == 1 and isinstance(args[0], Rule):
            rule = args[0]

        if rule is not None:
            # Create a new item based on the rule name and add it
            item = QListWidgetItem(rule.name)
            item.setFlags(item.flags() | Qt.ItemIsEditable)
            self.rules_list.addItem(item)

            # Add the data of the rule to our JSON data file
            if len(args) == 0:
                NamingData.add_rule(rule, data_file=self.DATA_FILE)

            # Update necessary UI Widgets
            if not load_rule:
                self.rules_list.setCurrentItem(item)
            self.update_expression_menu()
            self.update_rules_properties_state()

        self.description_rule_text.blockSignals(False)

    def on_remove_rule(self):

        """
        Remove the selected rule from the list of rules
        :return: True if the element deletion is successfull or False otherwise
        """

        self.description_rule_text.blockSignals(True)

        curr_rule = self.rules_list.currentItem()
        if curr_rule is not None:
            rule_index = self.rules_list.currentRow()
            name = self.rules_list.currentItem().text()
            if rule_index > -1 and name is not None:
                rule = NamingData.get_rule(rule_index, data_file=self.DATA_FILE)
                if rule is not None:
                    if rule.name == name:
                        NamingData.remove_rule(rule_index, data_file=self.DATA_FILE)
                        self.rules_list.takeItem(self.rules_list.row(self.rules_list.currentItem()))
                self.update_rules_properties_state()

        self.description_rule_text.blockSignals(False)

    def on_change_rule(self, rule_item):

        """
        Change the selected rule
        :param rule_item: new QListWidgetItem selected
        :return: None
        """

        if rule_item is not None:
            if rule_item.listWidget().count() > 0:
                rule = NamingData.get_rule(rule_item.listWidget().currentRow(), data_file=self.DATA_FILE)
                if rule is not None:
                    self.description_rule_text.setText(rule.description)
                    self.expression_line.setText(rule.expression)
                    self.iterator_cbx.setCurrentText(rule.iterator_format)
                    self.update_expression_menu()
                    self.update_rules_properties_state()

    def on_edit_rule_name(self, rule_item):

        """
        Changes name of the rule
        :param rule_item: Renamed QListWidgetItem
        :return: None
        """

        rule_index = rule_item.listWidget().currentRow()
        NamingData.set_rule_name(rule_index, rule_item.text(), data_file=self.DATA_FILE)
        rules = NamingData.get_rules(data_file=self.DATA_FILE)
        rules[rule_index].name = rule_item.text()

    def on_edit_rule_expression(self):

        """
        Changes expression of the selected rule
        :return: None
        """

        rule_index = self.rules_list.currentRow()
        NamingData.set_rule_expression(rule_index, self.expression_line.text(), data_file=self.DATA_FILE)
        rules = NamingData.get_rules(data_file=self.DATA_FILE)
        if len(rules) > 0:
            rules[rule_index].expression = self.expression_line.text()

    def on_edit_rule_description(self):

        """
        Changes description of the selected rule
        :return: None
        """

        rule_index = self.rules_list.currentRow()
        NamingData.set_rule_description(rule_index, self.description_rule_text.toPlainText(), data_file=self.DATA_FILE)
        rules = NamingData.get_rules(data_file=self.DATA_FILE)
        rules[rule_index].description = self.description_rule_text.toPlainText()

    def on_edit_rule_iterator(self, iterator_index):
        """
        Changes iterator of the selected rule
        :param iterator_index: int
        :return: None
        """

        rule_index = self.rules_list.currentRow()
        NamingData.set_rule_iterator_format(rule_index, self.iterator_cbx.itemText(iterator_index), data_file=self.DATA_FILE)
        rules = NamingData.get_rules(data_file=self.DATA_FILE)
        rules[rule_index].iterator_format = self.iterator_cbx.itemText(iterator_index)

    def on_add_token(self, *args):

        """
        Creates a new token and add it to the Naming Manager
        :return: None
        """

        load_token = True
        if len(args) == 0:
            load_token = False

        self.description_rule_text.blockSignals(True)

        token = None
        if not load_token:
            token = Token()
        elif load_token and len(args) == 1 and isinstance(args[0], Token):
            token = args[0]

        if token is not None:
            # Create a new item based on the token name and add it
            item = QListWidgetItem(token.name)
            item.setFlags(item.flags() | Qt.ItemIsEditable)
            self.tokens_list.addItem(item)

            # Add the data of the token to our JSON data file
            if len(args) == 0:
                NamingData.add_token(token, data_file=self.DATA_FILE)

            # Update necessary UI wigdets
            if not load_token:
                self.tokens_list.setCurrentItem(item)
            self.update_expression_menu()
            self.update_tokens_properties_state()

        self.description_rule_text.blockSignals(False)

    def on_remove_token(self):

        """
        Remove the selected token from the list of tokens
        :return: True if the element deletion is successfull or False otherwise
        """

        self.description_rule_text.blockSignals(True)

        curr_token = self.tokens_list.currentItem()
        if curr_token is not None:
            token_index = self.tokens_list.currentRow()
            name = self.tokens_list.currentItem().text()
            if token_index > -1 and name is not None:
                token = NamingData.get_token(token_index, data_file=self.DATA_FILE)
                if token is not None:
                    if token.name == name:
                        NamingData.remove_token(token_index, data_file=self.DATA_FILE)
                        self.tokens_list.takeItem(self.tokens_list.row(self.tokens_list.currentItem()))
                self.update_tokens_properties_state()

        self.description_rule_text.blockSignals(False)

    def on_change_token(self, token_item):

        """
        Change the selected token
        :param token_item: new QListWidgetItem selected
        :return: None
        """

        if token_item is not None:
            if token_item.listWidget().count() > 0:
                token = NamingData.get_token(token_item.listWidget().currentRow(), data_file=self.DATA_FILE)
                if token is not None:
                    self.description_token_text.setText(token.description)
                    self.default_cbx.setCurrentIndex(int(token.default))
                    self.update_tokens_properties_state()
                    self.update_tokens_key_table()
                    self.update_default_token_list()

    def on_edit_token_name(self, token_item):

        """
        Changes name of the token
        :param token_item: Renamed QListWidgetItem
        :return:
        """

        token_index = token_item.listWidget().currentRow()
        NamingData.set_token_name(token_index, token_item.text(), data_file=self.DATA_FILE)
        tokens = NamingData.get_tokens(data_file=self.DATA_FILE)
        tokens[token_index].name = token_item.text()

    def on_change_token_value(self, item):

        """
        Called when we change a token value name
        :return: None
        """

        if item.column() == 0:
            NamingData.set_token_key(self.tokens_list.currentRow(), item.row(), item.text(), data_file=self.DATA_FILE)
        else:
            NamingData.set_token_value(self.tokens_list.currentRow(), item.row(), item.text(), data_file=self.DATA_FILE)
        self.update_default_token_list()

    def on_add_token_value(self, *args):

        self.description_rule_text.blockSignals(True)

        item_index = self.tokens_list.currentRow()
        key_data = NamingData.add_token_value(item_index, data_file=self.DATA_FILE)
        if key_data:
            tokens = NamingData.get_tokens(data_file=self.DATA_FILE)
            tokens[item_index].values = key_data
            self.clean_tokens_key_table()

            keys = []
            values = []
            for i in range(len(key_data['key'])):
                self.values_table.insertRow(self.values_table.rowCount())
                keys.append(QTableWidgetItem())
                values.append(QTableWidgetItem())

            for index, value in enumerate(key_data['key']):
                keys[index].setText(value)
                self.values_table.setItem(index, 0, keys[index])

            for index, value in enumerate(key_data['value']):
                values[index].setText(value)
                self.values_table.setItem(index, 1, values[index])

            self.update_default_token_list()

            # newIndex = self.defaultCbx.currentIndex() + 2
            # self.defaultCbx.setCurrentIndex(newIndex)

        self.description_rule_text.blockSignals(False)

    def on_remove_token_value(self):
        """
        Removes a token value from the list of tokens values
        """

        self.description_rule_text.blockSignals(False)

        item_index = self.tokens_list.currentRow()
        key_data = NamingData.remove_token_value(item_index, self.values_table.currentRow(), data_file=self.DATA_FILE)
        if key_data:
            tokens = NamingData.get_tokens(data_file=self.DATA_FILE)
            tokens[item_index].values = key_data
            self.clean_tokens_key_table()

            keys = []
            values = []
            for i in range(len(key_data['key'])):
                self.values_table.insertRow(self.values_table.rowCount())
                keys.append(QTableWidgetItem())
                values.append(QTableWidgetItem())

            for index, value in enumerate(key_data['key']):
                keys[index].setText(value)
                self.values_table.setItem(index, 0, keys[index])

            for index, value in enumerate(key_data['value']):
                values[index].setText(value)
                self.values_table.setItem(index, 1, values[index])

            self.update_default_token_list()

            new_index = self.default_cbx.currentIndex()
            NamingData.set_default_token(item_index, new_index, data_file=self.DATA_FILE)
            tokens[item_index].default = new_index
            self.default_cbx.setCurrentIndex(new_index)

        self.description_rule_text.blockSignals(True)

    def on_edit_token_default(self, index):
        """
        Edits the default token
        :param index: int, index of the token to edit
        """

        item = self.tokens_list.currentRow()
        NamingData.set_default_token(item, index, data_file=self.DATA_FILE)

    def on_edit_token_description(self):
        """
        Edits the token description
        """
        item = self.tokens_list.currentRow()
        NamingData.set_token_description(item, self.description_token_text.toPlainText(), data_file=self.DATA_FILE)

    def _init_db(self):

        """
        Initializes the naming data base
        """

        if not os.path.isfile(self.DATA_FILE):
            f = open(self.DATA_FILE, 'w')
            f.close()


        data = jsonio.read_file(self.DATA_FILE)
        if data is None:
            data = {'nameit':
                {
                    'rules':
                        [],
                    'tokens':
                        []
                },
            }
            jsonio.write_to_file(data, self.DATA_FILE)
        else:
            self._init_data()

    def _init_data(self):
        if self._load_rules():
            self._load_tokens()

    def _load_rules(self):

        """
        Load rules from data file
        """

        try:
            rules = NamingData.get_rules(data_file=self.DATA_FILE)
            if rules is not None:
                for rule in rules:
                    self.on_add_rule(rule)
            return True
        except Exception:
            pass
        return False

    def _load_tokens(self):

        """
        Load tokens from data file
        """

        try:
            tokens = NamingData.get_tokens(data_file=self.DATA_FILE)
            if tokens is not None:
                for token in tokens:
                    self.on_add_token(token)
            return True
        except:
            pass
        return False


class ValuesTableModel(QAbstractTableModel, object):
    """
    Base model for the tokens table
    """

    def __init__(self, parent, myList, header, *args):
        super(ValuesTableModel, self).__init__(parent, *args)
        self.my_list = myList
        self.header = header

    def rowCount(self, parent):
        return len(self.my_list)

    def columnCount(self, parent):
        return len(self.my_list[0])

    def data(self, index, role):
        if not index.isValid():
            return None
        elif role != Qt.DisplayRole:
            return None
        return self.my_list[index.row()][index.column()]

    def headerData(self, col, orientation, role):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return self.header[col]
        return None


class TokensTable(QTableWidget):
    def __init__(self, data, *args):
        super(TokensTable, self).__init__(*args)
        self.data = data
        self.set_data()
        self.resizeColumnsToContents()
        self.resizeRowsToContents()

    def set_data(self):
        horHeaders = []
        for n, key in enumerate(sorted(self.data.keys())):
            horHeaders.append(key)
            for m, item in enumerate(self.data[key]):
                newItem = QTableWidgetItem(item)
                self.setItem(m, n, newItem)
        self.setHorizontalHeaderLabels(horHeaders)


class Rule (object):

    """
    Class that defines a rule in the naming manager
    Is used only as information container. To work with rules and tokens use NamingData
    """

    def __init__(self, name='New_Rule', expression='', description='', iterator_format='@'):
        """
        Naming manager rule
        :param str name: Name of the rule
        :param str expression: Expression of the rule
        :param str description: Description of the rule
        """
        self.name = name
        self.expression = expression
        self.description = description
        self.iterator_format = iterator_format

    def data(self):
        return self.__dict__

    def get_expression_tokens(self):

        return re.findall(r"\{([^}]+)\}", re.sub('_', '_', self.expression))


class Token (object):

    """
    Class that defines a token in the naming manager
    Is used only as information container. To work with rules and tokens use NamingData
    """

    def __init__(self, name='New_Token', values={'key': [], 'value': []}, default=0, description='',
                 override_value=''):

        """
        Naming manager token
        :param name: Name of the token
        :param values: Value for the token
        :param default: Default value that token has to toke
        :param description: Description of the token
        :param override_value: Override value for the token
        """

        self.name = name
        self.values = values
        self.default = default
        self.description = description
        self.override_value = ''

    def data(self):
        return self.__dict__

    def get_values_as_keyword(self):
        keys = self.values['key']
        values = self.values['value']
        keywords = OrderedDict()
        for i, key in enumerate(keys):
            keywords[key] = values[i]
        if self.default > 0:
            keywords['default'] = self.values['value'][self.default-1]
        return keywords


class NamingData(object):
    """
    Class that can be used to access elements of the naming JSON data file
    """

    _n = 'nameit'
    _t = 'tokens'
    _r = 'rules'
    _k = 'key'
    _v = 'value'

    @classmethod
    def load_data(cls, data_file):

        """
        Load JSON Naming manager data
        :return str: JSON Naming data
        """

        try:
            data = jsonio.read_file(data_file)
            return data
        except Exception:
            pass
        return None

    @classmethod
    def write_data(cls, data, data_file):
        """
        Writes data into Naming manager data
        :param data: JSON Naming manager data
        :return:
        """
        try:
            return jsonio.write_to_file(data, data_file)
        except Exception:
            pass
        return False

    @classmethod
    def add_rule(cls, rule, data_file):

        """
        Adds a new rule into the naming data
        :param rule: rule to add
        :return:
        """

        data = cls.load_data(data_file)
        if data is not None and rule is not None:
            data[cls._n][cls._r].append(rule.data())
            return cls.write_data(data, data_file=data_file)
        return False

    @classmethod
    def remove_rule(cls, rule_index, data_file):

        """
        Removes a rule from the naming data
        :param rule_index: int, index of the rule to delete
        :return: True if the rule is deleted successfully or False otherwise
        """

        data = cls.load_data(data_file)
        if data is not None and rule_index > -1:
            try:
                data[cls._n][cls._r].pop(rule_index)
                return cls.write_data(data, data_file=data_file)
            except Exception:
                pass
        return False

    @classmethod
    def get_rule(cls, rule_index, data_file):

        """
        Returns a rule from the naming data
        :param rule_index: int, index of the ruel to return
        :return: rule
        """

        data = cls.load_data(data_file)
        if data is not None and rule_index > -1:
            try:
                rule = data[cls._n][cls._r][rule_index]
                return Rule(rule['name'], rule['expression'], rule['description'], rule['iterator_format'])
            except Exception:
                pass
            return None

    @classmethod
    def get_rules(cls, data_file):

        """
        Get a list of all the rules on the Naming manager data
        :return list(tpNamingManger.tpRule): List of rules
        """

        data = cls.load_data(data_file)
        if data is not None:
            try:
                rules_list = []
                rules = data[cls._n][cls._r]
                for rule in rules:
                    rules_list.append(Rule(rule['name'], rule['expression'], rule['description'], rule['iterator_format']))
                return rules_list
            except Exception:
                pass
        return None

    @classmethod
    def set_rule_name(cls, rule_index, rule_name, data_file):
        """
        Set the name of a rule
        :param int rule_index: Index list of the rule
        :param str rule_name: New name for the rule
        :return str: Updated data or False if an error happens
        """

        data = cls.load_data(data_file)
        if data is not None and rule_index > -1 and isinstance(rule_name, unicode):
            try:
                data[cls._n][cls._r][rule_index]['name'] = rule_name
                return NamingData.write_data(data, data_file=data_file)
            except Exception:
                pass
        return False

    @classmethod
    def set_rule_expression(cls, rule_index, rule_expression, data_file):
        data = cls.load_data(data_file)
        if data is not None and rule_index > -1 and isinstance(rule_expression, unicode):
            try:
                data[cls._n][cls._r][rule_index]['expression'] = rule_expression
                return NamingData.write_data(data, data_file=data_file)
            except Exception:
                pass
        return False

    @classmethod
    def set_rule_description(cls, rule_index, rule_description, data_file):
        data = cls.load_data(data_file)
        if data is not None and rule_index > -1 and isinstance(rule_description, unicode):
            try:
                data[cls._n][cls._r][rule_index]['description'] = rule_description
                return NamingData.write_data(data, data_file=data_file)
            except Exception:
                pass
        return False

    @classmethod
    def set_rule_iterator_format(cls, rule_index, iterator_format, data_file):
        data = cls.load_data(data_file)
        if data is not None and rule_index > -1 and isinstance(iterator_format, unicode):
            try:
                data[cls._n][cls._r][rule_index]['iterator_format'] = iterator_format
                return NamingData.write_data(data, data_file=data_file)
            except Exception:
                pass
        return False

    @classmethod
    def add_token(cls, token, data_file):

        """
        Add a token to the list of tokens
        :param Token token: Token to add to the list
        :return: New Naming Manager data or False if the addition is not correct
        """

        data = cls.load_data(data_file)
        if data is not None and token is not None:
            data[cls._n][cls._t].append(token.data())
            return cls.write_data(data, data_file=data_file)
        return False

    @classmethod
    def remove_token(cls, token_index, data_file):

        """
        Removes a token with a given index from the list of tokens
        :param  int token_index: Index of the token to delete
        :return: New Naming Manager data or False if the deletion is not correct
        """

        data = cls.load_data(data_file)
        if data is not None and token_index > -1:
            try:
                data[cls._n][cls._t].pop(token_index)
                return cls.write_data(data, data_file=data_file)
            except Exception:
                pass
        return False

    @classmethod
    def get_token(cls, token_index, data_file):

        """
        Gets token by its index
        :param int token_index: Index of the token
        :return: tpToken with that index
        """

        data = cls.load_data(data_file)
        if data is not None and token_index > -1:
            try:
                token = data[cls._n][cls._t][token_index]
                return Token(token['name'], token['values'], token['default'], token['description'], token['override_value'])
            except Exception:
                pass
        return None

    @classmethod
    def get_tokens(cls, data_file):

        """
        Get a list of all the tokens on the Naming manager data
        :return list(tpNamingManger.tpToken): List of tokens
        """

        data = cls.load_data(data_file)

        if data is not None:
            try:
                tokens_list = []
                tokens = data[cls._n][cls._t]
                for token in tokens:
                    tokens_list.append(Token(token['name'], token['values'], token['default'], token['description'], token['override_value']))
                return tokens_list
            except Exception:
                pass
        return None

    @classmethod
    def set_token_name(cls, token_index, token_name, data_file):

        """
        Set the name of a token
        :param int token_index: Index list of the token
        :param str token_name: New name for the token
        :return str: Updated data or False if an error happens
        """

        data = cls.load_data(data_file)
        if data is not None and token_index > -1 and isinstance(token_name, unicode):
            try:
                data[cls._n][cls._t][token_index]['name'] = token_name
                return NamingData.write_data(data, data_file=data_file)
            except Exception:
                pass
        return False

    @classmethod
    def add_token_value(cls, token_index, data_file):
        data = cls.load_data(data_file)
        if data is not None and token_index > -1:
            keyData = data[cls._n][cls._t][token_index]['values']
            keyData[cls._k].append('New_Tag')
            keyData[cls._v].append('New_Value')
            data[cls._n][cls._t][token_index]['values'] = keyData
            cls.write_data(data, data_file=data_file)
            return keyData
        return False

    @classmethod
    def remove_token_value(cls, token_index, token_value_index, data_file):
        data = cls.load_data(data_file)
        if data is not None and token_index > -1 and token_value_index > -1:
            keyData = data[cls._n][cls._t][token_index]['values']
            keyData[cls._k].pop(token_value_index)
            keyData[cls._v].pop(token_value_index)
            data[cls._n][cls._t][token_index]['values'] = keyData
            cls.write_data(data, data_file=data_file)
            return keyData
        return False

    @classmethod
    def set_default_token(cls, token_value_index, token_index, data_file):
        data = cls.load_data(data_file)
        if data is not None and token_value_index > -1 and token_index > -1:
            data[cls._n][cls._t][token_value_index]['default'] = token_index
            return cls.write_data(data, data_file=data_file)
        return False

    @classmethod
    def get_default_index(cls, token_value_index, data_file):
        data = cls.load_data(data_file)
        if data is not None and token_value_index > -1:
            return data[cls._n][cls._t][token_value_index]['default']
        return None

    @classmethod
    def set_token_key(cls, token_index, item_row, token_key, data_file):
        data = cls.load_data(data_file)
        if data is not None and token_index > -1 and item_row > -1 and isinstance(token_key, unicode):
            data[cls._n][cls._t][token_index]['values']['key'][item_row] = token_key
            return cls.write_data(data, data_file=data_file)
        return False

    @classmethod
    def set_token_value(cls, token_index, item_row, token_value, data_file):
        data = cls.load_data(data_file)
        if data is not None and token_index > -1 and item_row > -1 and isinstance(token_value, unicode):
            data[cls._n][cls._t][token_index]['values']['value'][item_row] = token_value
            return cls.write_data(data, data_file=data_file)
        return False

    @classmethod
    def set_token_description(cls, token_index, token_description, data_file):
        data = cls.load_data(data_file)
        if data is not None and token_index > -1 and isinstance(token_description, unicode):
            data[cls._n][cls._t][token_index]['description'] = token_description
            return cls.write_data(data, data_file=data_file)
        return False


def run():
    win = NameItWindow()
    win.show()

    return win
