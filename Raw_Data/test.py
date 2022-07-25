import pandas as pd

class ProDetect:
    def __init__(self, product_name, tests_per_box):
        self.product_name = product_name
        self.tests_per_box = tests_per_box

    def min_potential_produced(self):
        product_data = pd.read_excel(f'Raw_Data/F037_For_{self.product_name}.xlsx', sheet_name = None)
        sheet_name = list(product_data.keys())[1:]

        #create variable
        product_tests_per_box = self.tests_per_box
        product_tests_per_uncut_sheet = 70
        potential_produced_product_raw_materials = {}

        for sheet in sheet_name:
            
            if (sheet == "Uncut Sheet"):
                product_uncut_sheet_raw = product_data["Uncut Sheet"]
                #trim unnecessary excel cell and assign to columns name
                product_uncut_sheet = product_uncut_sheet_raw.iloc[10:]
                product_uncut_sheet.columns = product_uncut_sheet_raw.iloc[8]
                #fomula to calculate potential produced goods based on uncutsheet
                potential_produced_product_by_uncut_sheet = (product_uncut_sheet["Received"].iloc[-1] * product_tests_per_uncut_sheet / product_tests_per_box)
                potential_produced_product_raw_materials[f"potential_produced_{self.product_name}_by_uncut_sheet"] = potential_produced_product_by_uncut_sheet
            
            if (sheet == "Uncut Sheet 1"):
                product_uncut_sheet_raw_1 = product_data["Uncut Sheet 1"]
                #trim unnecessary excel cell and assign to columns name
                product_uncut_sheet_1 = product_uncut_sheet_raw_1.iloc[10:]
                product_uncut_sheet_1.columns = product_uncut_sheet_raw_1.iloc[8]
                #fomula to calculate potential produced goods based on uncutsheet
                potential_produced_product_by_uncut_sheet_1 = (product_uncut_sheet_1["Received"].iloc[-1] * product_tests_per_uncut_sheet / product_tests_per_box)
                potential_produced_product_raw_materials[f"potential_produced_{self.product_name}_by_uncut_sheet_1"] = potential_produced_product_by_uncut_sheet_1

            if (sheet == "Uncut Sheet 2"):
                product_uncut_sheet_raw_2 = product_data["Uncut Sheet 2"]
                #trim unnecessary excel cell and assign to columns name
                product_uncut_sheet_2 = product_uncut_sheet_raw_2.iloc[10:]
                product_uncut_sheet_2.columns = product_uncut_sheet_raw_2.iloc[8]
                #fomula to calculate potential produced goods based on uncutsheet
                potential_produced_product_by_uncut_sheet_2 = (product_uncut_sheet_2["Received"].iloc[-1] * product_tests_per_uncut_sheet / product_tests_per_box)
                potential_produced_product_raw_materials[f"potential_produced_{self.product_name}_by_uncut_sheet_2"] = potential_produced_product_by_uncut_sheet_2
            
            if (sheet == "Uncut Sheet 3"):
                product_uncut_sheet_raw_3 = product_data["Uncut Sheet 3"]
                #trim unnecessary excel cell and assign to columns name
                product_uncut_sheet_3 = product_uncut_sheet_raw_3.iloc[10:]
                product_uncut_sheet_3.columns = product_uncut_sheet_raw_3.iloc[8]
                #fomula to calculate potential produced goods based on uncutsheet
                potential_produced_product_by_uncut_sheet_3 = (product_uncut_sheet_3["Received"].iloc[-1] * product_tests_per_uncut_sheet / product_tests_per_box)
                potential_produced_product_raw_materials[f"potential_produced_{self.product_name}_by_uncut_sheet_3"] = potential_produced_product_by_uncut_sheet_3


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
        

        min_boxes_of_product_key = min(potential_produced_product_raw_materials, key = potential_produced_product_raw_materials.get)

        min_boxes_of_product = f'{min_boxes_of_product_key} : {potential_produced_product_raw_materials[min_boxes_of_product_key]}'

        print(potential_produced_product_raw_materials)
        print(min_boxes_of_product)

PHA5021C = ProDetect("PHA5021C", 40)

PR_FLU = ProDetect("PR_FLU", 25)

print(PHA5021C.min_potential_produced())
print(PR_FLU.min_potential_produced())