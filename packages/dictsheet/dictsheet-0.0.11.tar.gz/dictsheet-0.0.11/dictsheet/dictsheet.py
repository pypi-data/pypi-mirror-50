# -*- coding: utf-8 -*-
from __future__ import print_function
from collections import OrderedDict
from pprintpp import pprint as pp
import copy
import json
from .row import Row

class DictSheet (object):
    def gen_alphabet_list():
        alphabet_list = []
        less26 = " ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        for s in less26:
            alphabet_list.append(s)
        for i in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
            for j in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
                alphabet_list.append("%s%s" % (i, j))
        return alphabet_list 
    alphabet_list = gen_alphabet_list()

    def __init__(self, wks, mapping=None):
        self.wks = wks
        """
        input: 
            wks: working sheet
            kc_map: k, v mapping

        sheet1 =  {
            2: {}, <- Row
            3: {},
        }
        """

        self.__len__, self._width = self._get_len_width()
        self._id = wks._id
        if mapping is None:
            mapping = self._get_kc_map()
        self.mapping = mapping

        #self._mapping =  _mapping
        self.keys = self.mapping
        #self._update_row_mapping()

    def _get_kc_map(self):
        mapping = {}
        col_list = self.wks.row_values(1)
        for idx, value in enumerate(col_list, start=1):
            if value is not "":
                mapping[value.strip()] = idx
        return mapping

    @property
    def mapping(self):
        return self._mapping

    @mapping.setter
    def mapping(self, mapping):
        """
        input: 
            wks from gspread 
            mapping: {
                'col_1': 1,
                'col_2': 2,
                ...
            } or 
            mapping: [
                'col_1', 'col_2', '', 'col_3'
            ]
        output: dict of key, col mapping 
                ex: { id: 1, name: 2, ... }
        """
        if '_mapping' not in self.__dict__:
            _mapping = {}
        else:
            _mapping = self._mapping

        if type(mapping) is list:
            for idx, val in enumerate(mapping):
                _mapping[val] = idx

        if type(mapping) is dict:
            _mapping  = mapping

        self._mapping = _mapping
        # TO-DO upadte first rows in sheet 
        
        last_col = len(self.wks.row_values(1))
        if last_col>26:
            last_col = 26
        #pp(last_col)
        #pp(DictSheet.alphabet_list[last_col])
        first_row_range = "A1:%s1" % DictSheet.alphabet_list[last_col]
        #pp(first_row_range)
        cells = self.wks.range(first_row_range)
        #cells = self.wks.range("A1:Z1")
        inv_mapping = {v: k for k, v in self._mapping.items()}
        for cell in cells:
            cell.value = ""
            if cell.col in inv_mapping:
                cell.value = inv_mapping[cell.col]
        self.wks.update_cells(cells)

        self._update_row_mapping()
        _wks_len, _wks_width = self._get_len_width()
        if _wks_width > self._width:
            self._width = _wks_width
        return _mapping

    def _get_row_cells(self, idx):
        #width = DictSheet.alphabet_list[self._width]
        range_str = 'A%s:%s%s' % (str(idx), DictSheet.alphabet_list[self._width], str(idx))
        #print range_str
        row_cells = self.wks.range(range_str)
        return row_cells

    def _update_row_mapping(self):
        """
        return {
            2: {},
            3: {}, ..
        }
        """
        rows = {}
        Row.kc_map[self._id] = self._mapping
        for idx in range(2, self.__len__ + 1):
            row_cells = self._get_row_cells(idx)
            row = Row(wks=self.wks, row_cells=row_cells)
            rows[idx] = row
            self.__dict__[idx] = row
        # TO-DO 
        # self.__dict__[0] return k,v of row 1
        return rows

    def update(self, data_dict):
        """
        input:
            {idx: {k1: v1, k2:v2, ..}
            ex:
            {
                2: { u'蜂蜜棒腿': 123, ...},
                3: { u'麻辣豬肋排': 'sss', ...}
            }
        """
        try:
            for idx, data in data_dict.items():
                row_cells = self._get_row_cells(idx)
                row = Row(wks=self.wks, row_cells=row_cells)
                row.update(data)
                self.__dict__[idx] = row 
        except Exception as e:
            return -1
        return 0 

    def append(self, dict_data):
        # TO-DO: append list of dict
        idx = self.__len__  + 1
        try:
            row_cells = self._get_row_cells(idx=idx)
            row = Row(wks=self.wks, row_cells=row_cells)
            row.update(dict_data)
            self.__len__ = idx
            self.__dict__[self.__len__] = row
        except Exception as e:
            raise RuntimeError('append fails')
        return row

    def __repr__(self):
        _ = copy.deepcopy(self.__dict__)
        # return json.dumps(_).encode('utf-8')
        # return repr(self.__dict__)
        return repr(_)

    def _get_len_width(self):
        all_values = self.wks.get_all_values()
        wks_len = len(all_values)
        try:
            wks_width = max([len(_) for _ in all_values])
        except Exception as e:
            wks_width = 0
        return wks_len, wks_width

    def __idx_convert__(self, idx):
        if idx >= 2:
            return idx
        elif idx < 0:
            idx = self.__len__ + idx + 1 
            return idx
        else:
            raise IndexError('getitem', 'idx error')

    def __getitem__(self, key):
        if type(key) is int:
            idx = self.__idx_convert__(key)
            if idx not in self.__dict__:
                row_cells = self._get_row_cells(idx=idx)
                row = Row(wks=self.wks, row_cells=row_cells)
                self.__dict__[idx] = row
                if idx > self.__len__:
                    self.__len__ = idx
            return self.__dict__[idx]
        return self.__dict__[key]

    def __setitem__(self, key, item):
        if type(key) is int:
            idx = self.__idx_convert__(key)
            if idx == 1:
                raise IndexError('setitem', 'idx shoud not be 1') 
            if idx not in self.__dict__: # Insert 
                if type(item) is dict:
                    self.append(item)
                elif type(item) is Row:
                    self.__len__ += 1
                    range_str = 'A%s:%s%s' % (str(self.__len__), DictSheet.alphabet_list[self._width], str(self.__len__))
                    row_list = self.wks.range(range_str)
                    row = Row(wks=self.wks, row_cells=row_list)
                    row.update(item.kv())
                    self.__dict__[self.__len__] = row
                else:
                    raise Exception('setitem', 'type error')
            else:  # Update 
                row = self.__dict__[idx]
                row.clear()
                if type(item) is dict:
                    # replace
                    # ds[4] = {'LINE ID': 'test1', 'Email': 'email'}
                    #row = self.__dict__[idx]
                    row.update(item)
                    self.__dict__[idx] = row
                elif type(item) is Row:
                    #row = self.__dict__[idx]
                    row.update(item.kv())
                    self.__dict__[idx] = row
                else:
                    raise Exception('setitem', 'type error')
            if idx > self.__len__:
                self.__len__ = idx
        else:
            self.__dict__[key] = item

    def get(self, key):
        match = {}
        for row in self.rows:
            if key in row:
                for idx, item in row.items():
                    match[idx] = item
        return match

    def extend(self):
        pass

    def iteritems(self):
        for k in range(2, self.__len__+1):
            if k in self.__dict__:
                yield (k, self.__dict__[k])

    def items(self):
        for k in range(2, self.__len__+1):
            if k in self.__dict__:
                yield (k, self.__dict__[k])

    def __iter__(self):
        # TO-DO: Test __iter__ func    
        # http://stackoverflow.com/questions/4019971/how-to-implement-iter-self-for-a-container-object-python
        for k in range(1, self.__len__+1):
            if k in self.__dict__:
                yield self.__dict__[k]

    def get_col_mapping(self, max_len):
        if max_len <=26:
            return " ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        if max_len <=26*26:
            col_list = [' ']
            alphabets ="ABCDEFGHIJKLMNOPQRSTUVWXYZ"
            for alphabet in alphabets:
                for alphabet2 in alphabets:
                    if len(col_list) <= max_len:
                        col_list.append("%s%s" % (alphabet, alphabet2))
                    else:
                        return col_list
        raise RuntimeError('append fails')
