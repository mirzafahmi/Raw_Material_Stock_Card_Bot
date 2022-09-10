import pandas as pd
import numpy as np
import os
import re
import math


terminal_size = os.get_terminal_size().columns # Access terminal columns size for print the header


class Products:
    global min_boxes_of_all_product
    min_boxes_of_all_product = {}
    

    def __init__(self, product_name, tests_per_box, number_of_buffer_per_box):
        self.product_name = product_name
        self.tests_per_box = tests_per_box
        self.number_of_buffer_per_box = number_of_buffer_per_box


    def raw_data(self):
        # Dynamically read the excel file from the name of the product
        if (self.product_name == 'PRODUCT_L_4' or self.product_name == 'PRODUCT_L_3' or self.product_name == 'PRODUCT_L_5_AMP' or self.product_name == 'PRODUCT_L_5_KET'):
            product_data = pd.read_excel(f'Raw_Data/PRODUCT_L.xlsx', sheet_name = None)
        elif (self.product_name == 'PRODUCT_O_1' or self.product_name == 'PRODUCT_O_2' or self.product_name == 'PRODUCT_O_3'):
            product_data = pd.read_excel(f'Raw_Data/PRODUCT_O.xlsx', sheet_name = None)
        elif (self.product_name == 'PRODUCT_F_1' or self.product_name == 'PRODUCT_F_2' or self.product_name == 'PRODUCT_F_3_1' or self.product_name == 'PRODUCT_F_3_2'):
            product_data = pd.read_excel(f'Raw_Data/PRODUCT_F.xlsx', sheet_name = None)
        else:
            product_data = pd.read_excel(f'Raw_Data/{self.product_name}.xlsx', sheet_name = None)

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
        global potential_produced_product_raw_materials
        potential_produced_product_raw_materials = {}
        uncutsheet_expiry_date = []

        # Create for loop to dynamically go through all the uncut_sheet sheet
        for sheet in all_uncut_sheets:
            # Trim the number at end of the sheet to merge it with other sheets of same components
            trim_sheet = re.sub('_\d$', '', sheet)

            # Naming the key of the dict with number from end of the sheet name
            sheet_number = ' '.join(map(str, re.findall(r'\d$', sheet))) 
            
            # Globals() made the dynamic variable name possible
            globals()[f'product_{trim_sheet}_raw'] = product_data[f'{sheet}']
            
            # Trim unnecessary excel cell and assign to columns name
            globals()[f'product_{trim_sheet}'] = globals()[f'product_{trim_sheet}_raw'].iloc[10:]
            globals()[f'product_{trim_sheet}'].columns = globals()[f'product_{trim_sheet}_raw'].iloc[8]
            
            # Fomula to calculate potential produced goods based on 'uncut sheet', it will read the last value in 'Received' column
            globals()[f'potential_produced_product_by_{trim_sheet}'] = globals()[f'product_{trim_sheet}']['Received'].iloc[-1] * product_tests_per_uncut_sheet / product_tests_per_box
            globals()[f'potential_produced_product_by_{trim_sheet}_exp_date'] = globals()[f'product_{trim_sheet}']['Exp Date'].iloc[-2]
            
            # Convert 'exp date' into datetime format 
            sheet_exp = pd.to_datetime(globals()[f'product_{trim_sheet}']['Exp Date'].iloc[-2]).date()
            uncutsheet_expiry_date.append(sheet_exp)
    
            # Update the dict of corresponding component with another same component that has different lot number
            if (f'potential_produced_{self.product_name}_by_{trim_sheet}') in potential_produced_product_raw_materials:
                potential_produced_product_raw_materials[f'potential_produced_{self.product_name}_by_{trim_sheet}'].update({f'{sheet_number}': {'Qty': globals()[f'potential_produced_product_by_{trim_sheet}'], 'Exp': globals()[f'potential_produced_product_by_{trim_sheet}_exp_date']}})
            else:
                potential_produced_product_raw_materials[f'potential_produced_{self.product_name}_by_{trim_sheet}'] = {f'{sheet_number}': {'Qty': globals()[f'potential_produced_product_by_{trim_sheet}'], 'Exp': globals()[f'potential_produced_product_by_{trim_sheet}_exp_date']}}
        

        for sheet in all_cassettes:
            # Trim the number at end of the sheet to merge it with other sheets of same components
            trim_sheet = re.sub('_\d$', '', sheet)

            # Naming the key of the dict with number from end of the sheet name
            sheet_number = ' '.join(map(str, re.findall(r'\d$', sheet)))
            
            # Globals() made the dynamic variable name possible
            globals()[f'product_{trim_sheet}_raw'] = product_data[f'{sheet}']

            # Trim unnecessary excel cell and assign to columns name
            globals()[f'product_{trim_sheet}'] = globals()[f'product_{trim_sheet}_raw'].iloc[10:]
            adjusted_columns_name = globals()[f'product_{trim_sheet}_raw'].iloc[8]

            # Renaming the blank columns due to multi-index column
            adjusted_columns_name[1] = 'Caps Received'
            adjusted_columns_name[2] = 'Caps Issue'
            adjusted_columns_name[4] = 'Panels Received'
            adjusted_columns_name[5] = 'Panels Issue'
            globals()[f'product_{trim_sheet}'].columns = adjusted_columns_name

            # Formula to calculate potential produced goods based on 'cap' and 'panel', it will read the last value in 'Received' column
            globals()[f'potential_produced_product_by_{trim_sheet}_caps'] = globals()[f'product_{trim_sheet}']['Caps Received'].iloc[-1] / product_tests_per_box
            globals()[f'potential_produced_product_by_{trim_sheet}_caps_exp_date'] = globals()[f'product_{trim_sheet}']['Exp Date'].iloc[-2]


            # Update the dict of corresponding component with another same component that has different lot number
            if (f'potential_produced_{self.product_name}_by_{trim_sheet}') in potential_produced_product_raw_materials:
                potential_produced_product_raw_materials[f'potential_produced_{self.product_name}_by_{trim_sheet}_caps'].update({f'{sheet_number}': {'Qty': globals()[f'potential_produced_product_by_{trim_sheet}_caps'], 'Exp': globals()[f'potential_produced_product_by_{trim_sheet}_caps_exp_date']}})
            else:
                potential_produced_product_raw_materials[f'potential_produced_{self.product_name}_by_{trim_sheet}_caps'] = {f'{sheet_number}': {'Qty': globals()[f'potential_produced_product_by_{trim_sheet}_caps'], 'Exp': globals()[f'potential_produced_product_by_{trim_sheet}_caps_exp_date']}}
        
            globals()[f'potential_produced_product_by_{trim_sheet}_panels'] = globals()[f'product_{trim_sheet}']['Panels Received'].iloc[-1] / product_tests_per_box
            globals()[f'potential_produced_product_by_{trim_sheet}_panels_exp_date'] = globals()[f'product_{trim_sheet}']['Exp Date'].iloc[-2]
            
            if (f'potential_produced_{self.product_name}_by_{trim_sheet}') in potential_produced_product_raw_materials:
                potential_produced_product_raw_materials[f'potential_produced_{self.product_name}_by_{trim_sheet}_panels'].update({f'{sheet_number}': {'Qty': globals()[f'potential_produced_product_by_{trim_sheet}_panels'], 'Exp': globals()[f'potential_produced_product_by_{trim_sheet}_panels_exp_date']}})
            else:
                potential_produced_product_raw_materials[f'potential_produced_{self.product_name}_by_{trim_sheet}_panels'] = {f'{sheet_number}': {'Qty': globals()[f'potential_produced_product_by_{trim_sheet}_panels'], 'Exp': globals()[f'potential_produced_product_by_{trim_sheet}_panels_exp_date']}}
            

        for sheet in all_buffers:
            # Trim the number at end of the sheet to merge it with other sheets of same components
            trim_sheet = re.sub('_\d$', '', sheet)
            
            # Naming the key of the dict with number from end of the sheet name
            sheet_number = ' '.join(map(str, re.findall(r'\d$', sheet)))

            # Globals() made the dynamic variable name possible
            globals()[f'product_{trim_sheet}_raw'] = product_data[f'{sheet}']
            
            # Trim unnecessary excel cell and assign to columns name
            globals()[f'product_{trim_sheet}'] = globals()[f'product_{trim_sheet}_raw'].iloc[10:]
            globals()[f'product_{trim_sheet}'].columns = globals()[f'product_{trim_sheet}_raw'].iloc[8]
            
            globals()[f'potential_produced_product_by_{trim_sheet}'] = globals()[f'product_{trim_sheet}']['Received'].iloc[-1] / number_of_buffer_per_box # different products have diffrent quantity buffer
            globals()[f'potential_produced_product_by_{trim_sheet}_exp_date'] = globals()[f'product_{trim_sheet}']['Exp Date'].iloc[-2]

            # Update the dict of corresponding component with another same component that has different lot number
            if (f'potential_produced_{self.product_name}_by_{trim_sheet}') in potential_produced_product_raw_materials:
                potential_produced_product_raw_materials[f'potential_produced_{self.product_name}_by_{trim_sheet}'].update({f'{sheet_number}': {'Qty': globals()[f'potential_produced_product_by_{trim_sheet}'], 'Exp': globals()[f'potential_produced_product_by_{trim_sheet}_exp_date']}})
            else:
                potential_produced_product_raw_materials[f'potential_produced_{self.product_name}_by_{trim_sheet}'] = {f'{sheet_number}': {'Qty': globals()[f'potential_produced_product_by_{trim_sheet}'], 'Exp': globals()[f'potential_produced_product_by_{trim_sheet}_exp_date']}}

        for sheet in other_components:
            # Trim the number at end of the sheet to merge it with other sheets of same components
            trim_sheet = re.sub('_\d$', '', sheet)

            # Naming the key of the dict with number from end of the sheet name
            sheet_number = ' '.join(map(str, re.findall(r'\d$', sheet)))

            # Globals() made the dynamic variable name possible
            globals()[f'product_{trim_sheet}_raw'] = product_data[f'{sheet}']
            
            # Trim unnecessary excel cell and assign to columns name
            globals()[f'product_{trim_sheet}'] = globals()[f'product_{trim_sheet}_raw'].iloc[10:]
            globals()[f'product_{trim_sheet}'].columns = globals()[f'product_{trim_sheet}_raw'].iloc[8]

            globals()[f'potential_produced_product_by_{trim_sheet}'] = globals()[f'product_{trim_sheet}']['Received'].iloc[-1] / product_tests_per_box
            globals()[f'potential_produced_product_by_{trim_sheet}_exp_date'] = globals()[f'product_{trim_sheet}']['Exp Date'].iloc[-2]
            
            # Update the dict of corresponding component with another same component that has different lot number
            if (f'potential_produced_{self.product_name}_by_{trim_sheet}') in potential_produced_product_raw_materials:
                potential_produced_product_raw_materials[f'potential_produced_{self.product_name}_by_{trim_sheet}'].update({f'{sheet_number}': {'Qty': globals()[f'potential_produced_product_by_{trim_sheet}'], 'Exp': globals()[f'potential_produced_product_by_{trim_sheet}_exp_date']}})
            else:
                potential_produced_product_raw_materials[f'potential_produced_{self.product_name}_by_{trim_sheet}'] = {f'{sheet_number}': {'Qty': globals()[f'potential_produced_product_by_{trim_sheet}'], 'Exp': globals()[f'potential_produced_product_by_{trim_sheet}_exp_date']}}

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
        PRODUCT_L_combo = ['PRODUCT_L_5', 'PRODUCT_L_4', 'PRODUCT_L_3']
        PRODUCT_F_combo = ['PRODUCT_F_1', 'PRODUCT_F_2', 'PRODUCT_F_3_1', 'PRODUCT_F_3_2']
        PRODUCT_O_1_combo = ['PRODUCT_O_1', 'C1', 'C2', 'PRODUCT_O_2', 'PRODUCT_O_3']
        
        # Filter out the components that are not use in the corresponding products

        # Removing the product name in loop to flush out unnecessary component
        # For PR-DOA-5 products
        for combo in PRODUCT_L_combo:
            if combo in self.product_name:
                PRODUCT_L_combo.remove(combo)
        
        for combo in PRODUCT_L_combo:
            for key in list(potential_produced_product_raw_materials.keys()):
                if combo in key:
                    potential_produced_product_raw_materials.pop(key)
                if 'AMP' in self.product_name and 'KET' in key:
                    potential_produced_product_raw_materials.pop(key)
                if 'KET' in self.product_name and 'AMP' in key:
                    potential_produced_product_raw_materials.pop(key)
        
        # For PR-DEN products
        if self.product_name == 'PRODUCT_F_1':
            PRODUCT_F_combo.remove(self.product_name)
            for key in list(potential_produced_product_raw_materials.keys()):
                for combo in PRODUCT_F_combo:
                    if combo in key:
                        potential_produced_product_raw_materials.pop(key)
        
        if self.product_name == 'PRODUCT_F_2':
            PRODUCT_F_combo.remove(self.product_name)
            for key in list(potential_produced_product_raw_materials.keys()):
                for combo in PRODUCT_F_combo:
                    if combo in key:
                        potential_produced_product_raw_materials.pop(key)
        
        if self.product_name == 'PRODUCT_F_3_1' or self.product_name == 'PRODUCT_F_3_2':
            for key in list(potential_produced_product_raw_materials.keys()):
                for combo in PRODUCT_F_combo:
                    if 'F_1_Cassette' in key or 'F_2_Cassette' in key:
                        try:
                            potential_produced_product_raw_materials.pop(key)
                        except:
                            pass
        
        # For PRODUCT_O_1 combo
        if self.product_name == 'PRODUCT_O_1':
            PRODUCT_O_1_combo.remove(self.product_name)
            for key in list(potential_produced_product_raw_materials.keys()):
                for combo in PRODUCT_O_1_combo:
                    if combo in key:
                        try:
                            potential_produced_product_raw_materials.pop(key)
                        except:
                            pass

        if self.product_name == 'PRODUCT_O_2':
            PRODUCT_O_1_combo.remove(self.product_name)
            PRODUCT_O_1_combo.remove('C1')
            PRODUCT_O_1_combo.remove('PRODUCT_O_1')
            for key in list(potential_produced_product_raw_materials.keys()):
                for combo in PRODUCT_O_1_combo:
                    if combo in key or 'O_1_Cassette' in key:
                        try:
                            potential_produced_product_raw_materials.pop(key)
                        except:
                            pass
        
        if self.product_name == 'PRODUCT_O_3':
            for key in list(potential_produced_product_raw_materials.keys()):
                for combo in PRODUCT_O_1_combo:
                    if 'O_1_Cassette' in key or 'O_2_Cassette' in key:
                        try:
                            potential_produced_product_raw_materials.pop(key)
                        except:
                            pass
        
        # Assigning 'Total Qty' value to its own variable 
        total_qty_dict = {key: list(val.values())[-1] for key, val in potential_produced_product_raw_materials.items()}
        
        # Find the minimum ammount of product can be produced based on 'Total Qty'
        global min_boxes_of_product_key
        global min_boxes_of_product
        min_boxes_of_product_key = min(total_qty_dict, key=total_qty_dict.get)
        min_boxes_of_product = f'{min_boxes_of_product_key} -> Qty: {potential_produced_product_raw_materials[min_boxes_of_product_key]["Total Qty"]}'
        min_boxes_of_all_product.update({(self.product_name).replace('_', '-'): {'Total Qty': potential_produced_product_raw_materials[min_boxes_of_product_key]["Total Qty"], 'Exp': min(uncutsheet_expiry_date).strftime('%Y-%m')}})
        
        
    def min_potential_produced(self):
        self.raw_data()
        # Printing section of summary
        opening_text = f'Raw Material Output for {self.product_name} (in boxes)'

        print('\n' f'{opening_text:-^{terminal_size}}')
        for key,value in potential_produced_product_raw_materials.items():
            print(f'{key} -> {value}')
        
        print('\n' f'Limiting Factor of Raw Material for {self.product_name} (in boxes): ' '\n' f'{min_boxes_of_product}')

        closing_text = 'End of Summary'
        print('\n' f'{closing_text:-^{terminal_size}}')
        
    def min_potential_produced_all(self):
        self.raw_data()
        return min_boxes_of_all_product


if __name__ == '__main__':
    x = Products('PRODUCT_O_3', 25, 2).raw_data()
    print(potential_produced_product_raw_materials)
    print(min_boxes_of_all_product)
    