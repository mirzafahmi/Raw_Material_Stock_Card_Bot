from apps import raw_materials_by_all_products_dict
import warnings
import gspread
from datetime import datetime
from pathlib import Path

sa_path = str(Path.home() / 'Downloads' / 'service_account.json')

warnings.filterwarnings('ignore')


def timestamp():
    update_times = datetime.now()
    dt_string = update_times.strftime('%d/%m/%Y %H:%M:%S')

    return dt_string


def potential_finished_goods_based_on_raw_materials():
    sa = gspread.service_account(filename=sa_path)
    beta_test = sa.open('Stock_Card')
    work_sheet = beta_test.worksheet('PRODUCT_LIST')

    timestamp()
    print(f'Obtaining and summarize data from excel sheet at {timestamp()}')
    potential_produced_by_raw_material = raw_materials_by_all_products_dict()

    update_times = datetime.now()
    dt_string = update_times.strftime('%d/%m/%Y %H:%M:%S')

    print(f'Update process is inniating at {timestamp()}')

    for item in work_sheet.col_values(2):
        for key, value in potential_produced_by_raw_material.items():
            if item == key:
                cell = work_sheet.find(item)
                work_sheet.update_cell(cell.row, cell.col + 6, potential_produced_by_raw_material[key]['Total Qty'])
                work_sheet.update_cell(cell.row, cell.col + 7, potential_produced_by_raw_material[key]['Exp'])
                
                print(f'Update complete for {item}')

    update_times = datetime.now()
    dt_string = update_times.strftime('%d/%m/%Y %H:%M:%S')

    work_sheet.update('H4:I4', f'Updated by RAW_MATERIAL_BOT at {timestamp()}')
    work_sheet.format('H4:I4', {'horizontalAlignment': 'CENTER' , 'textFormat': {'fontSize': 9, 'bold': True}})
    
    print(f'All up to date on {dt_string}. Cheers. Disclaimer: This update still on the beta test stage, any bugs or problem, you may contact me.')



if __name__ == '__main__':
    potential_finished_goods_based_on_raw_materials()
    
    #   Debugging code
    #print(raw_materials_by_all_products_dict())
    '''for key, value in raw_materials_by_all_products_dict().items():
        print(f'{key}: {raw_materials_by_all_products_dict()[key]}')'''
    

