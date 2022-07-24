import pandas as pd
import numpy as np
import pathlib
import os

class ProDetect:
    def __init__(self, product_name, tests_per_box):
        self.product_name = product_name
        self.tests_per_box = tests_per_box

    def min_potential_produced(self):
        #load the excel file and assign every sheet into variable
        product_data = pd.read_excel(f'Raw_Data/F037_For_{self.product_name}.xlsx', sheet_name = None)
        product_uncut_sheet_raw = product_data["Uncut Sheet"]
        product_cassette_raw = product_data["Cassette"]

        #trim unnecessary excel cell and assign to columns name
        product_uncut_sheet = product_uncut_sheet_raw.iloc[10:]
        product_uncut_sheet.columns = product_uncut_sheet_raw.iloc[8]


        #trim unnecessary excel cell and assign to columns name
        product_cassette = product_cassette_raw.iloc[10:]
        adjusted_columns_name = product_cassette_raw.iloc[8]

        #renaming the blank columns due to multi-index column
        adjusted_columns_name[1] = "Caps Received"
        adjusted_columns_name[2] = "Caps Issue"
        adjusted_columns_name[4] = "Panels Received"
        adjusted_columns_name[5] = "Panels Issue"
        product_cassette.columns = adjusted_columns_name

        #create variable
        product_tests_per_box = self.tests_per_box
        product_tests_per_uncut_sheet = 70

        #fomula to calculate potential produced goods based on uncutsheet
        potential_produced_product_by_uncut_sheet = (product_uncut_sheet["Received"].iloc[-1] * product_tests_per_uncut_sheet / product_tests_per_box)

        #formula to calculate potential produced goods based on cap and panel
        potential_produced_product_by_cap = product_cassette["Caps Received"].iloc[-1] / product_tests_per_box
        potential_produced_product_by_panel = product_cassette["Panels Received"].iloc[-1] / product_tests_per_box

        potential_produced_product_raw_materials = {f"potential_produced_{self.product_name}_by_uncut_sheet" : potential_produced_product_by_uncut_sheet, f"potential_produced_{self.product_name}_by_cap": potential_produced_product_by_cap, f"potential_produced_{self.product_name}_by_panel" : potential_produced_product_by_panel}

        min_boxes_of_product_key = min(potential_produced_product_raw_materials, key = potential_produced_product_raw_materials.get)

        min_boxes_of_product = f'{min_boxes_of_product_key} : {potential_produced_product_raw_materials[min_boxes_of_product_key]}'

        print(potential_produced_product_raw_materials)
        print(min_boxes_of_product)
