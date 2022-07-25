import pandas as pd
import re

class ProDetect:
    def __init__(self, product_name, tests_per_box):
        self.product_name = product_name
        self.tests_per_box = tests_per_box

    def min_potential_produced(self):
            product_data = pd.read_excel(f'Raw_Data/F037_For_{self.product_name}.xlsx', sheet_name = None)
            sheet_name = list(product_data.keys())[1:]

            all_uncut_sheets = [i for i in sheet_name if "Sheet" in i]

            #create variable
            product_tests_per_box = self.tests_per_box
            product_tests_per_uncut_sheet = 70
            potential_produced_product_raw_materials = {}

            for sheet in all_uncut_sheets:
                    product_{sheet}_uncut_sheet_raw = product_data[f"{sheet}"]
                    #trim unnecessary excel cell and assign to columns name
                    [f"product_{sheet}_uncut_sheet"] = f"product_{sheet}_uncut_sheet_raw.iloc[10:]"
                    product_{sheet}_uncut_sheet.columns = product_{sheet}_uncut_sheet_raw.iloc[8]
                    #fomula to calculate potential produced goods based on uncutsheet
                    potential_produced_product_by_{sheet}_uncut_sheet = (product_{sheet}_uncut_sheet["Received"].iloc[-1] * product_tests_per_uncut_sheet / product_tests_per_box)
                    potential_produced_product_raw_materials[f"potential_produced_{self.product_name}_by_{sheet}_uncut_sheet"] = potential_produced_product_by_{sheet}_uncut_sheet



pr = ProDetect("TEST", 25)

print(pr.min_potential_produced())