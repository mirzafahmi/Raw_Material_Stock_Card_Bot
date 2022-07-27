import pandas as pd

class ProDetect:
    def __init__(self, product_name, tests_per_box):
        self.product_name = product_name
        self.tests_per_box = tests_per_box

    def min_potential_produced(self):

        #dynamically read the excel file from the name of the product
        product_data = pd.read_excel(f'Raw_Data/F037_For_{self.product_name}.xlsx', sheet_name = None)

        #get the name of the sheet to differentiate between uncut_sheet components and others as some products has combinations thus need different function for the uncut_sheet sheet
        sheet_name = list(product_data.keys())
        all_uncut_sheets = [i for i in sheet_name if "Sheet" in i]
        other_components = [i for i in sheet_name if "Sheet" not in i]

        #create variable
        product_tests_per_box = self.tests_per_box
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

        #for loop for all other components

        for sheet in other_components:
            if (sheet == "Cassette"):
                product_cassette_raw = product_data["Cassette"]

                #trim unnecessary excel cell and assign to columns name
                product_cassette = product_cassette_raw.iloc[10:]
                adjusted_columns_name = product_cassette_raw.iloc[8]

                #renaming the blank columns due to multi-index column
                adjusted_columns_name[1] = "Caps Received"
                adjusted_columns_name[2] = "Caps Issue"
                adjusted_columns_name[4] = "Panels Received"
                adjusted_columns_name[5] = "Panels Issue"
                product_cassette.columns = adjusted_columns_name

                #formula to calculate potential produced goods based on "cap" and "panel", it will read the last value in "Received" column
                potential_produced_product_by_cap = product_cassette["Caps Received"].iloc[-1] / product_tests_per_box
                potential_produced_product_raw_materials[f"potential_produced_{self.product_name}_by_cap"] = potential_produced_product_by_cap
                potential_produced_product_by_panel = product_cassette["Panels Received"].iloc[-1] / product_tests_per_box
                potential_produced_product_raw_materials[f"potential_produced_{self.product_name}_by_panel"] = potential_produced_product_by_panel


        if (sheet == "Pipette"):
            product_pipette_raw = product_data["Pipette"]

            #trim unnecessary excel cell and assign to columns name
            product_pipette = product_pipette_raw.iloc[10:]
            product_pipette.columns = product_pipette_raw.iloc[8]

            #formula to calculate potential produced goods based on "pipette", it will read the last value in "Received" column
            potential_produced_product_by_pipette = (product_pipette["Received"].iloc[-1] / product_tests_per_box)
            potential_produced_product_raw_materials[f"potential_produced_{self.product_name}_by_pipette"] = potential_produced_product_by_pipette

        if (sheet == "Buffer"):
            product_buffer_raw = product_data["Buffer"]

            #trim unnecessary excel cell and assign to columns name
            product_buffer = product_buffer_raw.iloc[10:]
            product_buffer.columns = product_buffer_raw.iloc[8]

            #formula to calculate potential produced goods based on "buffer", it will read the last value in "Received" column
            potential_produced_product_by_buffer = (product_buffer["Received"].iloc[-1] / product_tests_per_box)
            potential_produced_product_raw_materials[f"potential_produced_{self.product_name}_by_buffer"] = potential_produced_product_by_buffer

        #get the "min" component's key to ease tp read the result
        min_boxes_of_product_key = min(potential_produced_product_raw_materials, key = potential_produced_product_raw_materials.get)
        
        #
        #min_boxes_of_product = f'{min_boxes_of_product_key} -> {potential_produced_product_raw_materials[min_boxes_of_product_key]}'
        min_boxes_of_product = {min_boxes_of_product_key:potential_produced_product_raw_materials[min_boxes_of_product_key]}
        
        print(f'{self.product_name}' + '\n')

        for key,value in potential_produced_product_raw_materials.items():
            x = f'{key} -> {value}' + '\n'
            print(x)
        #print([f'{key} -> {value}' for key,value in potential_produced_product_raw_materials.items()])
        print(min_boxes_of_product)
        #print(potential_produced_product_by_pipette)
        

PR_CHK = ProDetect("PR_CHK", 25)

print(PR_CHK.min_potential_produced())