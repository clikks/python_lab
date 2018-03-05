#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = 'lux'

import datetime
import os

from openpyxl import load_workbook, Workbook


file = os.path.join(os.getcwd(), 'courses.xlsx')

def combine():
    inwb = load_workbook(file)
    student = inwb['students']
    study_time = inwb['time']
    inwb.create_sheet('combine')
    combine = inwb['combine']
    time_dict = dict()
    for row in range(2, study_time.max_row+1):
        course = 'B' + str(row)
        time = 'C' + str(row)
        time_dict[study_time[course].value] = study_time[time].value
    for index, row in enumerate(student.iter_rows()):
        for seq, data in enumerate(row):
            combine.cell(row=index+1, column=seq+1, value=data.value)
            time_value = time_dict.get(data.value)
            if seq == 0:
                combine.cell(row=index+1, column=student.max_column+1, value=study_time['C1'].value)
            else:
                combine.cell(row=index+1, column=student.max_column+1, value=time_value)
    inwb.save('courses.xlsx')


def split():
    inwb = load_workbook(file)
    combine = inwb['combine']    
    sheet_dict = dict()
    for index, row in enumerate(combine.iter_rows()):
        if index == 0:
            continue
        else:
            sheet_data[row[0].value] = [i.value for i in row[1:]]
    years = [key.year for key in sheet_dict.keys()]
    for year in years:
        for 
        datetime.datetime.strptime(key, '%Y-%m-%d %H:%M:%S')
        





if __name__ == '__main__':
    combine()
    split()
