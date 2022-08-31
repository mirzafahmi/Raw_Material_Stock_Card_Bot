import pandas as pd
import numpy as np
import os

terminal_size = os.get_terminal_size().columns #access terminal columns size for print the header

class ProDetect:
    def __init__(self, product_name, tests_per_box, number_of_buffer_per_box):
        self.product_name = product_name
        self.tests_per_box = tests_per_box
        self.number_of_buffer_per_box = number_of_buffer_per_box

    def min_potential_produced(self):
        #dynamically read the excel file from the name of the product
        product_data = pd.read_excel(f'Raw_Data/F037_For_{self.product_name}.xlsx', sheet_name = None)

        #get the name of the sheet to differentiate between uncut_sheet components and others as some products has combinations thus need different function for the uncut_sheet sheet
        sheet_name = list(product_data.keys())
        all_uncut_sheets = [i for i in sheet_name if "Sheet" in i]
        all_cassettes = [i for i in sheet_name if "Cassette" in i]
        all_buffers = [i for i in sheet_name if "Buffer" in i]
        other_components = [i for i in sheet_name if i not in np.concatenate((all_uncut_sheets, all_cassettes, all_buffers))]

        #create variable
        product_tests_per_box = self.tests_per_box
        number_of_buffer_per_box = self.number_of_buffer_per_box
        product_tests_per_uncut_sheet = 70
        potential_produced_product_raw_materials = {}

        #create for loop to dynamically go through all the uncut_sheet sheet

        for sheet in all_uncut_sheets:

            #globals() made the dynamic variable name possible
            globals()[f"product_{sheet}_raw"] = product_data[f"{sheet}"]
            
            #trim unnecessary excel cell and assign to columns name
            globals()[f"product_{sheet}"] = globals()[f"product_{sheet}_raw"].iloc[10:]
            globals()[f"product_{sheet}"].columns = globals()[f"product_{sheet}_raw"].iloc[8]
            
            #fomula to calculate potential produced goods based on "uncut sheet", it will read the last value in "Received" column
            globals()[f"potential_produced_product_by_{sheet}"] = globals()[f"product_{sheet}"]["Received"].iloc[-1] * product_tests_per_uncut_sheet / product_tests_per_box
            potential_produced_product_raw_materials[f"potential_produced_{self.product_name}_by_{sheet}"] = globals()[f"potential_produced_product_by_{sheet}"]

        for sheet in all_cassettes:
            #globals() made the dynamic variable name possible
            globals()[f"product_{sheet}_raw"] = product_data[f"{sheet}"]

            #trim unnecessary excel cell and assign to columns name
            globals()[f"product_{sheet}"] = globals()[f"product_{sheet}_raw"].iloc[10:]
            adjusted_columns_name = globals()[f"product_{sheet}_raw"].iloc[8]

            #renaming the blank columns due to multi-index column
            adjusted_columns_name[1] = "Caps Received"
            adjusted_columns_name[2] = "Caps Issue"
            adjusted_columns_name[4] = "Panels Received"
            adjusted_columns_name[5] = "Panels Issue"
            globals()[f"product_{sheet}"].columns = adjusted_columns_name

            #formula to calculate potential produced goods based on "cap" and "panel", it will read the last value in "Received" column
            globals()[f"potential_produced_product_by_{sheet}_caps"] = globals()[f"product_{sheet}"]["Caps Received"].iloc[-1] / product_tests_per_box
            potential_produced_product_raw_materials[f"potential_produced_{self.product_name}_by_{sheet}_caps"] = globals()[f"potential_produced_product_by_{sheet}_caps"]
            globals()[f"potential_produced_product_by_{sheet}_panels"] = globals()[f"product_{sheet}"]["Panels Received"].iloc[-1] / product_tests_per_box
            potential_produced_product_raw_materials[f"potential_produced_{self.product_name}_by_{sheet}_panels"] = globals()[f"potential_produced_product_by_{sheet}_panels"]

        for sheet in all_buffers:
            #globals() made the dynamic variable name possible
            globals()[f"product_{sheet}_raw"] = product_data[f"{sheet}"]
            
            #trim unnecessary excel cell and assign to columns name
            globals()[f"product_{sheet}"] = globals()[f"product_{sheet}_raw"].iloc[10:]
            globals()[f"product_{sheet}"].columns = globals()[f"product_{sheet}_raw"].iloc[8]

            
            globals()[f"potential_produced_product_by_{sheet}"] = globals()[f"product_{sheet}"]["Received"].iloc[-1] / number_of_buffer_per_box #different products have diffrent quantity buffer
            potential_produced_product_raw_materials[f"potential_produced_{self.product_name}_by_{sheet}"] = globals()[f"potential_produced_product_by_{sheet}"]
        
        for sheet in other_components:
            #globals() made the dynamic variable name possible
            globals()[f"product_{sheet}_raw"] = product_data[f"{sheet}"]
            
            #trim unnecessary excel cell and assign to columns name
            globals()[f"product_{sheet}"] = globals()[f"product_{sheet}_raw"].iloc[10:]
            globals()[f"product_{sheet}"].columns = globals()[f"product_{sheet}_raw"].iloc[8]

            globals()[f"potential_produced_product_by_{sheet}"] = globals()[f"product_{sheet}"]["Received"].iloc[-1] / product_tests_per_box
            potential_produced_product_raw_materials[f"potential_produced_{self.product_name}_by_{sheet}"] = globals()[f"potential_produced_product_by_{sheet}"]


        #get the "min" component's key to ease tp read the result
        min_boxes_of_product_key = min(potential_produced_product_raw_materials, key = potential_produced_product_raw_materials.get)
        
        #min_boxes_of_product = f'{min_boxes_of_product_key} -> {potential_produced_product_raw_materials[min_boxes_of_product_key]}'
        min_boxes_of_product = {min_boxes_of_product_key:potential_produced_product_raw_materials[min_boxes_of_product_key]} #variant of above code
        
        #print(f'{self.product_name}' + '\n')
        print(f'Raw Material Output for {self.product_name} (in boxes): ')
        for key,value in potential_produced_product_raw_materials.items():
            x = f'{key} -> {value}'
            print(x)
        #print([f'{key} -> {value}' for key,value in potential_produced_product_raw_materials.items()])

        print('\n' f'Limiting Factor of Raw Material for {self.product_name} (in boxes): ' '\n' f'{min_boxes_of_product}')

        closing_text = "End of Summary"
        print('\n' f'{closing_text:-^{terminal_size}}')
        

if __name__ == ' __main__':
    
    print('hi')
    print(ProDetect('PR_DOA_5', 25, 0).min_potential_produced())