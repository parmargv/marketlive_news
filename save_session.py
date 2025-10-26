import os
import openpyxl
def save_data(state):
    absolute_path = os.path.dirname(__file__)
    file_path = os.path.join(absolute_path, 'trade_book.xlsx')
    wb = openpyxl.load_workbook(file_path)
    sh1=wb['Sheet1']

    if state=="Y":
        sh1['A2']= "Y"
        wb.save('trade_book.xlsx')
        wb.close()
    elif state=="N":
        sh1['A2'] = "N"
        wb.save('trade_book.xlsx')
        wb.close()