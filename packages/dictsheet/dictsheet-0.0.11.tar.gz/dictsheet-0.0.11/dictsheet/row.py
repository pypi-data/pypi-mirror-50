# -*- coding: utf-8 -*-
from __future__ import print_function
from collections import OrderedDict
from pprintpp import pprint as pp
import copy
import json


class Row(object):
    """ref http://stackoverflow.com/questions/4014621/a-python-class-that-acts-like-dict"
    """
    kc_map = {}
    #ex: {'_id':{ id: 1, name: 2, ... }}
    inv_kc_map = {}
    #ex: {'id''{ 1: id , 2: name, ... }}
    __ignore_key__ = ['row_cells', 'wks', '_id', 'idx']

    def __init__(self, wks, row_cells):
        """
        input: row_cell_list
            [
                <Cell R1C1 'Timestamp'>,
                <Cell R1C2 u'\u8702\u871c\u68d2\u817f'>,
                ...
            ]
        return:
            {
                "k1": "v1",
                "k2": "v2",..
            }
        """
        self._id = wks.__dict__['_id']
        if self._id not in Row.kc_map:
            #pp(wks.__dict__['_id'])
            #Row.kc_map[self._id] = self._id
            raise Exception('Need define key_col_map')
            # TO-DO make sure how it's works
        if self._id not in Row.inv_kc_map:
            Row.inv_kc_map[self._id] = {v: k for k, v in Row.kc_map[self._id].items()}

        self.wks = wks
        self.row_cells = copy.deepcopy(row_cells)
        self.idx = row_cells[0].row
        #for cell in self.row:
        for cell in self.row_cells:
            if cell.col in Row.inv_kc_map[self._id]:
                self.__dict__[Row.inv_kc_map[self._id][cell.col]] = cell.value
            else:
                pass
                """"maybe raise Exception but it would cause adding a non-mapping cell to spread not
                avaliable."""

    def iteritems(self):
        for k, v in Row.kc_map[self._id].iteritems():
            if k == "":
                continue
            if k not in self.__dict__:
                continue
            yield (k, self.__dict__[k])

    def items(self):
        for k, v in Row.kc_map[self._id].iteritems():
            if k == "":
                continue
            if k not in self.__dict__:
                continue
            val = copy.deepcopy(self.__dict__[k])
            yield (k, val)

    def __setitem__(self, key, item):
        if key == '':
            raise Exception('setitem', 'type error')

        self.__dict__[key] = item
        if key in Row.kc_map[self._id]:
            col_idx = Row.kc_map[self._id][key]
            for cell in self.row_cells:
                if cell.col  == col_idx:
                    cell.value = item
                    self.wks.update_cells([cell])
                    break

    def __contains__(self, key):
        if key in self.__dict__:
            return key in self.__dict__

    def __getitem__(self, key):
        if key not in self.__dict__:
            print("%s is not in row" % key.encode('utf-8'))
        return self.__dict__[key]

    def __repr__(self):
        _ = copy.deepcopy(self.__dict__)
        _.pop('row_cells', None)
        _.pop('wks', None)
        _.pop('_id', None)
        #return json.dumps(_).encode('utf-8')
        #return repr(self.__dict__)
        return repr(_)

    def clear(self):
        update_cells = []
        for cell in self.row_cells:
            if cell.col in Row.inv_kc_map[self._id]:
                self.__dict__[Row.inv_kc_map[self._id][cell.col]] = ""
            cell.value = ""
            update_cells.append(cell)
        self.wks.update_cells(update_cells)

    def update(self, data_dict):
        # data as dict
        """
        input: {
            k1: v1,
            k2, v2
        }
        """
        update_cells = []
        for k, v in data_dict.items():
            if k in Row.kc_map[self._id]:
                # check if key in kc_map
                col_idx = Row.kc_map[self._id][k]
                for cell in self.row_cells:
                    if cell.col  == col_idx:
                        cell.value = v
                        update_cells.append(cell)
                        self.__dict__[k] = v
                        break
        self.wks.update_cells(update_cells)

    def kv(self):
        _ = {}
        for k, v in self.__dict__.items():
            if k in Row.__ignore_key__:
                continue
            _[k] = v
        return _

    def __eq__(self, other):
        if isinstance(other, self.__class__) or type(other) is dict:
            for k, v in self.__dict__.items():
                if k not in Row.__ignore_key__:
                    if k not in other or other[k] != self.__dict__[k]:
                        return False
            return True
        return False

    def __ne__(self, other):
        return not self.__eq__(other)

