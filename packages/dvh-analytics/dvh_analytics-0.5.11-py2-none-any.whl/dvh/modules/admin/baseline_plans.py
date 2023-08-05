#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
baseline plans model for admin view
Created on Tue Dec 25 2018
@author: Dan Cutright, PhD
"""

from __future__ import print_function
from bokeh.models.widgets import Select, Button, TextInput, Div, TableColumn, DataTable
from bokeh.layouts import row, column
from bokeh.models import ColumnDataSource
from ..tools.io.database.sql_connector import DVH_SQL


class Baseline:
    def __init__(self):
        self.source = ColumnDataSource(data=dict(mrn=[]))

        self.condition = TextInput(value='', title="Condition", width=625)
        self.query_button = Button(label='Query', button_type='primary', width=100)

        self.query_button.on_click(self.update_source)

        types = ['status', 'study_date', 'uid', 'mrn']
        titles = ['Baseline Status', 'Sim Study Date', 'Study Instance UID', 'MRN']
        widths = [200, 200, 425, 200]
        self.select = {key: Select(value='', options=[''], width=widths[i], height=100, title=titles[i])
                       for i, key in enumerate(types)}

        self.select['mrn'].on_change('value', self.update_mrn_ticker)
        self.select['study_date'].on_change('value', self.update_study_date_ticker)
        self.select['uid'].on_change('value', self.update_uid_ticker)
        self.select['status'].on_change('value', self.update_status_ticker)

        self.columns = ['mrn', 'sim_study_date', 'physician', 'rx_dose', 'fxs', 'tx_modality', 'tx_site',
                        'study_instance_uid', 'import_time_stamp', 'baseline']
        relative_widths = [1, 1, 0.75, 0.5, 0.3, 1, 1, 3.5, 1.5, 0.5]
        column_widths = [int(250. * rw) for rw in relative_widths]
        table_columns = [TableColumn(field=c, title=c, width=column_widths[i]) for i, c in enumerate(self.columns)]
        self.table = DataTable(source=self.source, columns=table_columns, width=1300, editable=True)

        self.source.on_change('selected', self.source_selection_ticker)

        self.layout = column(Div(text="<b>Query Database</b>", width=1000),
                             row(self.condition, self.query_button),
                             Div(text="<b>Update Database</b>", width=1025),
                             row(self.select['mrn'], self.select['study_date'], self.select['uid'],
                                 self.select['status']),
                             self.table)

    def update_source(self):

        query_cursor = DVH_SQL().query('Plans', ','.join(self.columns).strip(), self.condition.value, order_by='mrn')
        new_data = {c: [str(line[i]) for line in query_cursor] for i, c in enumerate(self.columns)}

        self.source.data = new_data

        self.update_mrns()

    def update_mrns(self):
        options = [mrn for mrn in self.source.data['mrn']]
        if not options:
            options = ['']
        options.sort()

        self.select['mrn'].options = options
        self.select['mrn'].value = options[0]

        self.update_study_dates()

    def update_study_dates(self):

        sim_study_dates = self.source.data['sim_study_date']
        selected_mrn = self.select['mrn'].value
        sim_dates = [sim_study_dates[i] for i, mrn in enumerate(self.source.data['mrn']) if mrn == selected_mrn]
        options = [sim_date for sim_date in sim_dates]
        if not options:
            options = ['']
        options.sort()

        self.select['study_date'].options = options
        self.select['study_date'].value = options[0]

        self.update_uid()

    def update_uid(self):
        sim_dates = self.source.data['sim_study_date']
        uids = self.source.data['study_instance_uid']
        mrns = self.source.data['mrn']
        selected_mrn = self.select['mrn'].value
        selected_date = self.select['study_date'].value
        options = [uids[i] for i, mrn in enumerate(mrns) if mrn == selected_mrn and sim_dates[i] == selected_date]
        if not options:
            options = ['']
        options.sort()

        self.select['uid'].options = options
        self.select['uid'].value = options[0]

        self.update_status_select()

    def update_status_select(self):
        if len(self.source.data['mrn']) == 0:
            self.select['status'].options = ['']
            self.select['status'].value = ''
        else:
            index = self.source.data['study_instance_uid'].index(self.select['uid'].value)
            self.select['status'].options = ['True', 'False']
            self.select['status'].value = self.source.data['baseline'][index]

    def update_mrn_ticker(self, attr, old, new):
        self.update_study_dates()

    def update_study_date_ticker(self, attr, old, new):
        self.update_uid()

    def update_uid_ticker(self, attr, old, new):
        self.update_status_select()

    def update_status_ticker(self, attr, old, new):
        uid = self.select['uid'].value
        current_baseline = DVH_SQL().query('Plans', 'baseline', "study_instance_uid = '" + uid + "'")[0][0]

        if new not in {str(current_baseline), ''}:
            if new == 'True':
                baseline = 1
            else:
                baseline = 0

            DVH_SQL().update('Plans', 'baseline', baseline, "study_instance_uid = '" + self.select['uid'].value + "'")
            self.update_source()

    def source_selection_ticker(self, attr, old, new):
        index = self.source.selected.indices[0]
        self.select['mrn'].value = self.source.data['mrn'][index]
        self.select['study_date'].value = self.source.data['sim_study_date'][index]
        self.select['uid'].value = self.source.data['study_instance_uid'][index]
