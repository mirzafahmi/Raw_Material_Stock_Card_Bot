import pandas as pd

product_data = pd.read_excel(f'Raw_Data/F037_For_PR_DOA_5.xlsx', sheet_name = None)

#get the name of the sheet to differentiate between uncut_sheet components and others as some products has combinations thus need different function for the uncut_sheet sheet
sheet_name = list(product_data.keys())

#print(sheet_name)
 
z = [x.strip('_1_2') for x in sheet_name]


print(z)
#globals()[f'product_{sheet}_raw']