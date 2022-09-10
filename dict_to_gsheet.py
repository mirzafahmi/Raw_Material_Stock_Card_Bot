from apps import raw_materials_by_all_products_dict
import warnings
import gspread
from datetime import datetime


warnings.filterwarnings('ignore')


def timestamp():
    update_times = datetime.now()
    dt_string = update_times.strftime('%d/%m/%Y %H:%M:%S')

    return dt_string


def potential_finished_goods_based_on_raw_materials():
    sa = gspread.service_account()
    beta_test = sa.open('stock_card_beta_test')
    work_sheet = beta_test.worksheet('PRODUCT LIST')

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
                work_sheet.update_cell(cell.row, cell.col + 11, potential_produced_by_raw_material[key]['Total Qty'])
                work_sheet.update_cell(cell.row, cell.col + 12, potential_produced_by_raw_material[key]['Exp'])
                
                print(f'Update complete for {item}')

    update_times = datetime.now()
    dt_string = update_times.strftime('%d/%m/%Y %H:%M:%S')

    work_sheet.update('M9:N9', f'Updated by RAW_MATERIAL_BOT at {timestamp()}')
    work_sheet.format('M9:N9', {'horizontalAlignment': 'CENTER' , 'textFormat': {'fontSize': 12, 'bold': True}})
    
    print(f'All up to date on {dt_string}. Cheers. Disclaimer: This update still on the beta test stage, any bugs or problem, you may contact HQ.')



if __name__ == '__main__':
    potential_finished_goods_based_on_raw_materials()


    #   Debugging code
    #print(raw_materials_by_all_products_dict())
    '''for key, value in raw_materials_by_all_products_dict().items():
        print(f'{key}: {raw_materials_by_all_products_dict()[key]}')'''
    

