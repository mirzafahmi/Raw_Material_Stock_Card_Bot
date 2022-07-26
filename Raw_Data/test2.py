import pandas as pd
import re

class ProDetect:
    def __init__(self, product_name, tests_per_box):
        self.product_name = product_name
        self.tests_per_box = tests_per_box

    def min_potential_produced(self):
        product_data = pd.read_excel(f'Raw_Data/F037_For_{self.product_name}.xlsx', sheet_name = None)
        sheet_name = list(product_data.keys())
        #print(product_data["Cassette"])
        all_uncut_sheets = [i for i in sheet_name if "Sheet" in i]
        other_components = [i for i in sheet_name if "Sheet" not in i]

        #create variable
        product_tests_per_box = self.tests_per_box
        product_tests_per_uncut_sheet = 70
        potential_produced_product_raw_materials = {}

        for sheet in all_uncut_sheets:
            globals()[f"product_{sheet}_uncut_sheet_raw"] = product_data[f"{sheet}"]
            
            #trim unnecessary excel cell and assign to columns name
            globals()[f"product_{sheet}_uncut_sheet"] = globals()[f"product_{sheet}_uncut_sheet_raw"].iloc[10:]
            globals()[f"product_{sheet}_uncut_sheet"].columns = globals()[f"product_{sheet}_uncut_sheet_raw"].iloc[8]
            
            #fomula to calculate potential produced goods based on uncutsheet
            globals()[f"potential_produced_product_by_{sheet}_uncut_sheet"] = globals()[f"product_{sheet}_uncut_sheet"]["Received"].iloc[-1] * product_tests_per_uncut_sheet / product_tests_per_box
            x = f"potential_produced_{self.product_name}_by_{sheet}_uncut_sheet"
            potential_produced_product_raw_materials[x] = globals()[f"potential_produced_product_by_{sheet}_uncut_sheet"]

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

                #formula to calculate potential produced goods based on cap and panel
                potential_produced_product_by_cap = product_cassette["Caps Received"].iloc[-1] / product_tests_per_box
                potential_produced_product_raw_materials[f"potential_produced_{self.product_name}_by_cap"] = potential_produced_product_by_cap
                potential_produced_product_by_panel = product_cassette["Panels Received"].iloc[-1] / product_tests_per_box
                potential_produced_product_raw_materials[f"potential_produced_{self.product_name}_by_panel"] = potential_produced_product_by_panel


        if (sheet == "Pipette"):
            product_pipette_raw = product_data["Pipette"]

            #trim unnecessary excel cell and assign to columns name
            product_pipette = product_pipette_raw.iloc[10:]
            product_pipette.columns = product_pipette_raw.iloc[8]

            potential_produced_product_by_pipette = (product_pipette["Received"].iloc[-1] / product_tests_per_box)
            potential_produced_product_raw_materials[f"potential_produced_{self.product_name}_by_pipette"] = potential_produced_product_by_pipette

        if (sheet == "Buffer"):
            product_buffer_raw = product_data["Buffer"]

            #trim unnecessary excel cell and assign to columns name
            product_buffer = product_buffer_raw.iloc[10:]
            product_buffer.columns = product_buffer_raw.iloc[8]

            potential_produced_product_by_buffer = (product_buffer["Received"].iloc[-1] / product_tests_per_box)
            potential_produced_product_raw_materials[f"potential_produced_{self.product_name}_by_buffer"] = potential_produced_product_by_buffer

        print(potential_produced_product_raw_materials)
        

pr = ProDetect("TEST", 25)

print(pr.min_potential_produced())