import pandas as pd
import numpy as np
import os
import re
import math

terminal_size = os.get_terminal_size().columns # Access terminal columns size for print the header

class ProDetect:
    def __init__(self, product_name, tests_per_box, number_of_buffer_per_box):
        self.product_name = product_name
        self.tests_per_box = tests_per_box
        self.number_of_buffer_per_box = number_of_buffer_per_box
    global min_boxes_of_all_product
    min_boxes_of_all_product = {}

    def min_potential_produced(self):
        # Dynamically read the excel file from the name of the product
        if (self.product_name == 'PR_DOA_4' or self.product_name == 'PR_DOA_3'):
            product_data = pd.read_excel(f'Raw_Data/F037_For_PR_DOA_5.xlsx', sheet_name = None)
        elif (self.product_name == 'PR_FSV' or self.product_name == 'PR_FSVA'):
            product_data = pd.read_excel(f'Raw_Data/F037_For_PR_FLU.xlsx', sheet_name = None)
        elif (self.product_name == 'PR_DEN_1' or self.product_name == 'PR_DEN_2' or self.product_name == 'PR_DEN_3_1' or self.product_name == 'PR_DEN_3_2'):
            product_data = pd.read_excel(f'Raw_Data/F037_For_PR_DEN.xlsx', sheet_name = None)
        else:
            product_data = pd.read_excel(f'Raw_Data/F037_For_{self.product_name}.xlsx', sheet_name = None)

        # Get the name of the sheet to differentiate between uncut_sheet components and others as some products has combinations thus need different function for the uncut_sheet sheet
        sheet_name = list(product_data.keys())
        all_uncut_sheets = [i for i in sheet_name if 'Sheet' in i]
        all_cassettes = [i for i in sheet_name if 'Cassette' in i]
        all_buffers = [i for i in sheet_name if 'Buffer' in i]
        other_components = [i for i in sheet_name if i not in np.concatenate((all_uncut_sheets, all_cassettes, all_buffers))]

        # Create variable
        product_tests_per_box = self.tests_per_box
        number_of_buffer_per_box = self.number_of_buffer_per_box
        product_tests_per_uncut_sheet = 70
        potential_produced_product_raw_materials = {}
        # Create for loop to dynamically go through all the uncut_sheet sheet

        for sheet in all_uncut_sheets:
            trim_sheet = sheet.strip('_1_2')
            sheet_number = ' '.join(map(str, re.findall(r'\d+', sheet)))

            # Globals() made the dynamic variable name possible
            globals()[f'product_{trim_sheet}_raw'] = product_data[f'{sheet}']
            
            # Trim unnecessary excel cell and assign to columns name
            globals()[f'product_{trim_sheet}'] = globals()[f'product_{trim_sheet}_raw'].iloc[10:]
            globals()[f'product_{trim_sheet}'].columns = globals()[f'product_{trim_sheet}_raw'].iloc[8]
            
            # Fomula to calculate potential produced goods based on 'uncut sheet', it will read the last value in 'Received' column
            globals()[f'potential_produced_product_by_{trim_sheet}'] = globals()[f'product_{trim_sheet}']['Received'].iloc[-1] * product_tests_per_uncut_sheet / product_tests_per_box
            globals()[f'potential_produced_product_by_{trim_sheet}_exp_date'] = globals()[f'product_{trim_sheet}']['Remarks'].iloc[-2]
            
            # Update the dict of corresponding component with another same component that has different lot number
            if (f'potential_produced_{self.product_name}_by_{trim_sheet}') in potential_produced_product_raw_materials:
                potential_produced_product_raw_materials[f'potential_produced_{self.product_name}_by_{trim_sheet}'].update({f'{sheet_number}': {'Qty': globals()[f'potential_produced_product_by_{trim_sheet}'], 'Exp': globals()[f'potential_produced_product_by_{trim_sheet}_exp_date']}})
            else:
                potential_produced_product_raw_materials[f'potential_produced_{self.product_name}_by_{trim_sheet}'] = {f'{sheet_number}': {'Qty': globals()[f'potential_produced_product_by_{trim_sheet}'], 'Exp': globals()[f'potential_produced_product_by_{trim_sheet}_exp_date']}}
        
        for sheet in all_cassettes:
            # Globals() made the dynamic variable name possible
            globals()[f'product_{sheet}_raw'] = product_data[f'{sheet}']

            # Trim unnecessary excel cell and assign to columns name
            globals()[f'product_{sheet}'] = globals()[f'product_{sheet}_raw'].iloc[10:]
            adjusted_columns_name = globals()[f'product_{sheet}_raw'].iloc[8]

            # Renaming the blank columns due to multi-index column
            adjusted_columns_name[1] = 'Caps Received'
            adjusted_columns_name[2] = 'Caps Issue'
            adjusted_columns_name[4] = 'Panels Received'
            adjusted_columns_name[5] = 'Panels Issue'
            globals()[f'product_{sheet}'].columns = adjusted_columns_name

            # Formula to calculate potential produced goods based on 'cap' and 'panel', it will read the last value in 'Received' column
            globals()[f'potential_produced_product_by_{sheet}_caps'] = globals()[f'product_{sheet}']['Caps Received'].iloc[-1] / product_tests_per_box
            potential_produced_product_raw_materials[f'potential_produced_{self.product_name}_by_{sheet}_caps'] = {'Qty': globals()[f'potential_produced_product_by_{sheet}_caps']}
            globals()[f'potential_produced_product_by_{sheet}_panels'] = globals()[f'product_{sheet}']['Panels Received'].iloc[-1] / product_tests_per_box
            potential_produced_product_raw_materials[f'potential_produced_{self.product_name}_by_{sheet}_panels'] = {'Qty': globals()[f'potential_produced_product_by_{sheet}_panels']}

        for sheet in all_buffers:
            trim_sheet = sheet.strip('_1_2')
            sheet_number = ' '.join(map(str, re.findall(r'\d+', sheet)))

            # Globals() made the dynamic variable name possible
            globals()[f'product_{trim_sheet}_raw'] = product_data[f'{sheet}']
            
            # Trim unnecessary excel cell and assign to columns name
            globals()[f'product_{trim_sheet}'] = globals()[f'product_{trim_sheet}_raw'].iloc[10:]
            globals()[f'product_{trim_sheet}'].columns = globals()[f'product_{trim_sheet}_raw'].iloc[8]
            
            globals()[f'potential_produced_product_by_{trim_sheet}'] = globals()[f'product_{trim_sheet}']['Received'].iloc[-1] / number_of_buffer_per_box # different products have diffrent quantity buffer
            globals()[f'potential_produced_product_by_{trim_sheet}_exp_date'] = globals()[f'product_{trim_sheet}']['Remarks'].iloc[-2]

            # Update the dict of corresponding component with another same component that has different lot number
            if (f'potential_produced_{self.product_name}_by_{trim_sheet}') in potential_produced_product_raw_materials:
                potential_produced_product_raw_materials[f'potential_produced_{self.product_name}_by_{trim_sheet}'].update({f'{sheet_number}': {'Qty': globals()[f'potential_produced_product_by_{trim_sheet}'], 'Exp': globals()[f'potential_produced_product_by_{trim_sheet}_exp_date']}})
            else:
                potential_produced_product_raw_materials[f'potential_produced_{self.product_name}_by_{trim_sheet}'] = {f'{sheet_number}': {'Qty': globals()[f'potential_produced_product_by_{trim_sheet}'], 'Exp': globals()[f'potential_produced_product_by_{trim_sheet}_exp_date']}}

        for sheet in other_components:
            # Globals() made the dynamic variable name possible
            globals()[f'product_{sheet}_raw'] = product_data[f'{sheet}']
            
            # Trim unnecessary excel cell and assign to columns name
            globals()[f'product_{sheet}'] = globals()[f'product_{sheet}_raw'].iloc[10:]
            globals()[f'product_{sheet}'].columns = globals()[f'product_{sheet}_raw'].iloc[8]

            globals()[f'potential_produced_product_by_{sheet}'] = globals()[f'product_{sheet}']['Received'].iloc[-1] / product_tests_per_box
            potential_produced_product_raw_materials[f'potential_produced_{self.product_name}_by_{sheet}'] = {'Qty': globals()[f'potential_produced_product_by_{sheet}']}

        # Looping through to find the min value of "Total Qty" in each key
        for key in potential_produced_product_raw_materials.keys():
            total_qty = []
            
            for x in potential_produced_product_raw_materials[key].keys():
                if (x == 'Qty'):
                    total_qty.append(potential_produced_product_raw_materials[key].get(x))
                else:
                    total_qty.append(potential_produced_product_raw_materials[key][x]['Qty'])

            potential_produced_product_raw_materials[f'{key}'].update({'Total Qty': math.floor(sum(total_qty))})
        
        # Create variable for the products combo that shared the raw materials
        PR_DOA_combo = ['PR_DOA_5', 'PR_DOA_4', 'PR_DOA_3']
        PR_DEN_combo = ['PR_DEN_1', 'PR_DEN_2', 'PR_DEN_3_1', 'PR_DEN_3_2']
        PR_FLU_combo = ['PR_FLU', 'PR_RSV', 'PR_ADE', 'PR_FSV', 'PR_FSVA']
        
        # Filter out the components that are not use in the corresponding products
        if self.product_name in PR_DOA_combo:
            PR_DOA_combo.remove(self.product_name)
            for key in list(potential_produced_product_raw_materials.keys()):
                for combo in PR_DOA_combo:
                    if combo in key:
                        potential_produced_product_raw_materials.pop(key)

        if self.product_name == 'PR_DEN_1':
            PR_DEN_combo.remove(self.product_name)
            for key in list(potential_produced_product_raw_materials.keys()):
                for combo in PR_DEN_combo:
                    if combo in key:
                        potential_produced_product_raw_materials.pop(key)
        
        if self.product_name == 'PR_DEN_2':
            PR_DEN_combo.remove(self.product_name)
            for key in list(potential_produced_product_raw_materials.keys()):
                for combo in PR_DEN_combo:
                    if combo in key:
                        potential_produced_product_raw_materials.pop(key)
        
        if self.product_name == 'PR_FLU':
            PR_FLU_combo.remove(self.product_name)
            for key in list(potential_produced_product_raw_materials.keys()):
                for combo in PR_FLU_combo:
                    if combo in key:
                        try:
                            potential_produced_product_raw_materials.pop(key)
                        except:
                            pass

        if self.product_name == 'PR_FSV':
            PR_FLU_combo.remove(self.product_name)
            PR_FLU_combo.remove('PR_RSV')
            PR_FLU_combo.remove('PR_FLU')
            for key in list(potential_produced_product_raw_materials.keys()):
                for combo in PR_FLU_combo:
                    if combo in key:
                        try:
                            potential_produced_product_raw_materials.pop(key)
                        except:
                            pass

        # Assigning 'Total Qty' value to its own variable 
        total_qty_dict = {key: list(val.values())[-1] for key, val in potential_produced_product_raw_materials.items()}
        
        # Find the minimum ammount of product can be produced based on 'Total Qty'
        min_boxes_of_product_key = min(total_qty_dict, key=total_qty_dict.get)
        min_boxes_of_product = f'{min_boxes_of_product_key} -> Qty: {potential_produced_product_raw_materials[min_boxes_of_product_key]["Total Qty"]}'
        
        # Printing section of summary
        opening_text = f'Raw Material Output for {self.product_name} (in boxes)'

        print('\n' f'{opening_text:-^{terminal_size}}')
        for key,value in potential_produced_product_raw_materials.items():
            print(f'{key} -> {value}')
        
        print('\n' f'Limiting Factor of Raw Material for {self.product_name} (in boxes): ' '\n' f'{min_boxes_of_product}')

        closing_text = 'End of Summary'
        print('\n' f'{closing_text:-^{terminal_size}}')
        min_boxes_of_all_product.update({self.product_name: potential_produced_product_raw_materials[min_boxes_of_product_key]["Total Qty"]})
    
    def min_potential_produced_all(self):
        self.min_potential_produced()
        return min_boxes_of_all_product


if __name__ == '__main__':
    print(ProDetect('PR_FLU', 25, 2).min_potential_produced())