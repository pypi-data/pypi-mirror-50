#! /usr/bin/env python

"""
Library module related with naming convention for the complete rigging toolkit
"""


from __future__ import print_function, division, absolute_import, unicode_literals


import copy
import json
import os
from collections import OrderedDict

import tpNameIt as tp
from tpPyUtils import strings as string_utils


_NAMING_REPO_ENV = 'NAMING_REPO'

_tokens = dict()
_rules = {'_active': None}


class Serializable(object):

    def data(self):
        # We use copy.deepcopy because a dictionary in Python is a mutable type and we do not want
        # to change the dictionary outside this class
        ret_val = copy.deepcopy(self.__dict__)

        # We create some internal properties to validate the new instance
        ret_val['_Serializable_classname'] = type(self).__name__
        ret_val['_Serializable_version'] = '1.0'

        return ret_val

    @classmethod
    def from_data(cls, data):

        # First of all, we have to validate the data
        if data.get('_Serializable_classname') != cls.__name__:
            return None

        # After the validation we delete validation property
        del data['_Serializable_classname']
        if data.get('_Serializable_version') is not None:
            del data['_Serializable_version']

        this = cls()
        this.__dict__.update(data)
        return this


class Token(Serializable, object):

    def __init__(self, name):
        super(Token, self).__init__()
        self._name = name
        self._default = None
        self._items = dict()

    @staticmethod
    def is_iterator(name):
        """
        Returns true if the passed name is an iterator or False otherwise
        :param name: str, name to check
        :return: bool
        """

        if '#' in name or '@' in name:
            return True
        return False

    def name(self):
        """
        Returns the name of the token
        """

        return self._name

    def set_name(self, name):
        """
        Sets the name of the token
        """

        self._name = name

    def set_default(self, value):
        """
        Return the default item of the token
        """

        self._default = value

    def default(self):
        """
        Set the default item for the token
        """

        # If there is not a default value defined and we have items in the token, we define the first item as default
        if self._default is None and len(self._items):
            self._default = self._items.values()[0]
        return self._default

    def add_item(self, name, value):
        """
        Adds a new item to the token
        """

        self._items[name] = value

    def is_required(self):
        """
        Return True if it is required to pass this token to solve the nomenclature
        """

        return self.default() is None

    def solve(self, name=None):
        """
        Solve the token | Fields -> Solved Name
        """

        # If we don't pass any name the token will be solved as the default item value

        if name is None:
            if self.is_iterator(self.default()):
                return self._get_default_iterator_value(0)
            else:
                return self.default()

        if 'iterator' in self._items:
            if name not in self._items:
                return self._get_default_iterator_value(name)
            else:
                return name
        else:
            return self._items.get(name)

    def _get_default_iterator_value(self, name):
        iterator_format = active_rule().iterator_format()
        if '@' in iterator_format:
            return string_utils.get_alpha(name, capital=('^' in iterator_format))
        elif '#' in iterator_format:
            return str(name).zfill(len(iterator_format))
        else:
            return name

    def parse(self, value):

        """ Parse a value taking in account the items of the token | Solved Name - Fields """

        for k, v in self._items.items():
            if v == value:
                return k

    def save(self, file_path):

        """ Saves token to a file as JSON data """
        file_path = os.path.join(file_path, self.name() + '.token')
        if self.data():
            with open(file_path, 'w') as fp:
                json.dump(self.data(), fp)
            return True
        return False
    # endregion


class Rule(Serializable, object):

    def __init__(self, name, iterator_format='@', auto_fix=False):
        super(Rule, self).__init__()
        self._name = name
        self._auto_fix = auto_fix
        self._iterator_format = iterator_format
        self._fields = list()

    def name(self):
        """
        Returns the name of the rule
        """

        return self._name

    def fields(self):
        """
        Return a list of the fields of the rule
        """

        return tuple(self._fields)

    def iterator_format(self):
        """
        Returns iterator type for this rule
        """

        return self._iterator_format

    def auto_fix(self):
        """
        Returns if rule should auto fix its patter if necessary
        :return: bool
        """

        return self._auto_fix

    def set_auto_fix(self, flag):
        """
        Sets auto fix
        :param flag: bool
        """

        self._auto_fix = flag

    def add_fields(self, token_names):
        """
        Adds new fields to the rule
        """

        self._fields.extend(token_names)
        return True

    def solve(self, **values):
        """
        Solve the pattern taking into consideration the current fields of the rule
        """

        # if len(values) > 0:
        #     return self._pattern().format(**values)

        if len(values) <= 0:
            return

        # Get only valid pattern values (we don't use None values)
        valid_values = OrderedDict()
        for field in self._fields:
            for k, v in values.items():
                if k == field:
                    if v is None:
                        if self._auto_fix:
                            continue
                        else:
                            tp.logger.warning('Missing field: "{}" when generating new name (None will be used instead)!'.format(k))
                    valid_values[k] = v

        # We get pattern taking into account if we want to fix automatically the pattern or not
        valid_pattern = self._pattern(valid_values.keys())

        return valid_pattern.format(**valid_values)

    def parse(self, name):
        """
        Parse a rule taking in account the fields of the rule
        """

        ret_val = dict()

        # Take tokens from the current name using a separator character
        split_name = name.split('_')

        # Loop trough each field of the current active rule
        for i, f in enumerate(self.fields()):

            # Get current value and its respective token
            value = split_name[i]
            token = _tokens[f]

            if token.is_required():
                # We are in a required field, and we simply return the value from the split name
                ret_val[f] = value
                continue

            # Else, we parse the token directly
            ret_val[f] = token.parse(value)

        return ret_val

    def save(self, file_path):
        """
        Saves rule to a file as JSON data
        """

        file_path = os.path.join(file_path, self.name() + '.rule')
        if self.data():
            with open(file_path, 'w') as fp:
                json.dump(self.data(), fp)
            return True
        return False

    def _pattern(self, fields=None):
        """
        Returns the pattern for the rules
        """

        if fields is None:
            fields = self._fields

        return "{{{}}}".format("}_{".join(fields))


# ======================= RULES ======================= #

def add_rule(name, iterator_type='@', *fields):
    """
    Adds a new rule to the rules dictionary
    """

    rule = Rule(name, iterator_type)
    rule.add_fields(fields)
    _rules[name] = rule
    if active_rule() is None:
        set_active_rule(name)
    return rule


def has_rule(name):
    """
    Get True if a rule its in the curret rules list
    """

    return name in _rules.keys()


def remove_rule(name):
    """
    Removes a rule, if exists, from the current rules list
    """

    if has_rule(name):
        del _rules[name]
        return True
    return False


def remove_all_rules():
    """
    Deletes any rules saved previosluy
    """

    _rules.clear()
    _rules['_active'] = None
    return True


def active_rule():
    """
    Return the current active rule
    """

    k = _rules['_active']

    return _rules.get(str(k))


def set_active_rule(name):
    """
    Sets the current active rule
    """

    if not has_rule(name):
        return False
    _rules['_active'] = name
    return True


def set_rule_auto_fix(name, flag):
    """
    Sets if given rule should fix its pattern automatically if necessary or not
    :param name: str, name of the rule
    :param flag: bool
    """
    if not has_rule(name):
        return

    _rules[name].set_auto_fix(flag)


def get_rule(name):
    """
    Gets a rule from the dictionary of rules by its name
    """

    return _rules.get(name)


def save_rule(name, filepath):
    """
    Saves a serialized rule in a JSON format file
    """

    rule = get_rule(name)
    if not rule:
        return False
    with open(filepath, 'w') as fp:
        json.dump(rule.data(), fp)
    return True


def load_rule(filepath):
    """
    Loads a serialized rule from a JSON and deserialize it and creates a new one
    """

    if not os.path.isfile(filepath):
        return False
    try:
        with open(filepath) as fp:
            data = json.load(fp)
    except Exception:
        return False

    rule = Rule.from_data(data)
    _rules[rule.name()] = rule

    return True


def add_token(name, **kwargs):
    """
    Adds a new token to the tokens dictionary
    """

    token = Token(name)
    for k, v in kwargs.items():
        # If there is a default value we set it
        if k == 'default':
            token.set_default(v)
            continue
        token.add_item(k, v)
    _tokens[name] = token
    return token


def has_token(name):
    """
    Get True if a token its in the current tokens list
    """

    return name in _tokens.keys()


def remove_token(name):
    """
    Removes a token, if exists, from the current tokens list
    """

    # If the token name exists in the tokens list ...
    if has_token(name):
        del _tokens[name]
        return True
    return False


def remove_all_tokens():
    """
    Deletes any tokens saved previously
    """

    _tokens.clear()
    return True


def get_token(name):
    """
    Get a token from the dictionary of tokens by its name
    """

    return _tokens.get(name)


def get_token_by_index(index):
    """
    Get a token from the dictionary of token by its index
    """

    return _tokens.values()[index]


def save_token(name, filepath):
    """
    Saves a serialized token in a JSON format file
    """

    token = get_token(name)
    if not token:
        return False
    with open(filepath, 'w') as fp:
        json.dump(token.data(), fp)
    return True


def load_token(filepath):
    """
    Loads a serialized token from a JSON and deserialize it and creates a new one
    """

    if not os.path.isfile(filepath):
        return False
    try:
        with open(filepath) as fp:
            data = json.load(fp)
    except Exception:
        return False

    token = Token.from_data(data)
    _tokens[token.name()] = token
    return True


def solve(*args, **kwargs):
    """
    Solve the nomenclature using different techniques:
        - Explicit Conversion
        - Default Conversion
        - Token Management
    """

    i = 0
    values = dict()
    rule = active_rule()

    # Loop trough each field of the current active rule
    for f in rule.fields():
        # Get tpToken object from the dictionary of tokens
        if _tokens.has_key(f):
            token = _tokens[f]

            if token.is_required():
                # We are in a required token (a token is required if it does not has default value)
                if kwargs.get(f) is not None:
                    # If the field is in the keywords passed, we get its value
                    values[f] = kwargs[f]
                    continue
                else:
                    # Else, we get the passed argument (without using keyword)
                    try:
                        values[f] = args[i]
                    except Exception:
                        values[f] = None
                    i += 1
                    continue
            # If all fails, we try to get the field for the token
            values[f] = token.solve(kwargs.get(f))
        else:
            tp.logger.warning('Expression not valid: token {} not found in tokens list'.format(f))
            return
    return rule.solve(**values)


def parse(name):

    """
    Parse a current solved name and return its different fields (metadata information)
        - Implicit Conversion
    """

    # Parse name comparing it with the active rule
    rule = active_rule()
    return rule.parse(name)


def get_repo():
    env_repo = os.environ.get(_NAMING_REPO_ENV)
    local_repo = os.path.join(os.path.expanduser('~'), '.config', 'naming')
    return env_repo, local_repo


def save_session(repo=None):

    repo = repo or get_repo()

    # Tokens and rules
    for name, token in _tokens.items():
        file_path = os.path.join(repo, name + '.token')
        save_token(name, file_path)

    for name, rule in _rules.items():
        if not isinstance(rule, Rule):
            continue
        file_path = os.path.join(repo, name + '.rule')
        save_rule(name, file_path)

    # Extra configuration
    active = active_rule()
    config = {'set_active_rule': active.name() if active else None}
    file_path = os.path.join(repo, 'naming.conf')
    with open(file_path, 'w') as fp:
        json.dump(config, fp)
    return True


def load_session(repo=None):

    repo = repo or get_repo()
    if not os.path.exists(repo):
        os.mkdir(repo)

    # Tokens and rules
    for dir_path, dir_names, file_names in os.walk(repo):
        for file_name in file_names:
            file_path = os.path.join(dir_path, file_name)
            if file_name.endswith('.token'):
                load_token(file_path)
            elif file_name.endswith('.rule'):
                load_rule(file_path)

    # Extra configuration
    file_path = os.path.join(repo, 'naming.conf')
    if os.path.exists(file_path):
        with open(file_path) as fp:
            config = json.load(fp)
        for k, v in config.items():
            globals()[k](v)
    return True
