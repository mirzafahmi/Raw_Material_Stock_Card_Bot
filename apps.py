import sys
import os
from analysis_module import ProDetect_class as pc


products_list = ['PR_DEN_1', 'PR_DEN_2', 'PR_DEN_3_1', 'PR_DEN_3_2', 'PHA5021C', 'PR_FLU', 'PR_FSV', 'PR_FSVA', 'PR_GAST_3', 'PR_SYP', 'PR_HBSAG', 'PR_DOA_5_1', 'PR_DOA_5_2', 'PR_DOA_4', 'PR_DOA_3', 'PR_DAM', 'PR_DBZ', 'PR_DKE', 'PR_DME', 'PR_DMD', 'PR_DMDA', 'PR_DMO', 'PR_DOP', 'PR_DTH', 'PR_MYP', 'PR_CHK']

# Innitiate the class by products

# Product_Code = ProDetect('product_code', tests_per_box, number_of_buffer_per_box)
PR_DEN_1 = pc.ProDetect('PR_DEN_1', 25, 1)          # For all dengue products as they share materials
PR_DEN_2 = pc.ProDetect('PR_DEN_2', 25, 1)
PR_DEN_3_1 = pc.ProDetect('PR_DEN_3_1', 10, 1)
PR_DEN_3_2 = pc.ProDetect('PR_DEN_3_2', 25, 1)
PHA5021C = pc.ProDetect('PHA5021C', 40, 0)
PR_FLU = pc.ProDetect('PR_FLU', 25, 2)          # For all PR_FLU, PR_FSV and PR_FSVA products as they share materials
PR_FSV = pc.ProDetect('PR_FSV', 25, 2)
PR_FSVA = pc.ProDetect('PR_FSVA', 25, 2)
PR_GAST_3 = pc.ProDetect('PR_GAST_3', 25, 1)
PR_SYP = pc.ProDetect('PR_SYP', 25, 1)
PR_HBSAG = pc.ProDetect('PR_HBSAG', 25, 1)
PR_DOA_5_1 = pc.ProDetect('PR_DOA_5', 25, 0)
PR_DOA_5_2= pc.ProDetect('PR_DOA_5', 25, 0)      # For all DOA combo
PR_DOA_4 = pc.ProDetect('PR_DOA_4', 25, 0)
PR_DOA_3 = pc.ProDetect('PR_DOA_3', 25, 0)
#PR_DOA_5_1 = pc.ProDetect('PR_DOA_5', 50, 0)    # For all DOA combo convert to single strip

# For all single strip DOA test
PR_DAM = pc.ProDetect('PR_DAM', 50, 0)
PR_DBZ = pc.ProDetect('PR_DBZ', 50, 0)
PR_DCO = pc.ProDetect('PR_DCO', 50, 0)
PR_DME = pc.ProDetect('PR_DME', 50, 0)
PR_DKE = pc.ProDetect('PR_DAM', 50, 0)
PR_DMD = pc.ProDetect('PR_DMD', 50, 0)
PR_DMDA = pc.ProDetect('PR_DMDA', 50, 0)
PR_DMO = pc.ProDetect('PR_DMO', 50, 0)
PR_DOP = pc.ProDetect('PR_DOP', 50, 0)
PR_DTH = pc.ProDetect('PR_DTH', 50, 0)

PR_MYP = pc.ProDetect('PR_MYP', 25, 1)
PR_CHK = pc.ProDetect('PR_CHK', 25, 1)

# To access all products raw material
def raw_materials_by_all_products():
    for item_code in products_list:
        print(eval(item_code).min_potential_produced())

def raw_materials_by_all_products_dict():
    for item_code in products_list:
        x = eval(item_code).min_potential_produced_all()
    return x
# To access products raw material by input
def raw_materials_by_input(Item_Code):
    print(Item_Code.min_potential_produced())

def apps():
    # Header
    terminal_size = os.get_terminal_size().columns # Access terminal columns size for print the header
    welcome_text = 'Summary of the Raw Material by Products'
    print('\n' f'{welcome_text:-^{terminal_size}}')

    item_code_input = input('Enter Item Code Here: ').upper().replace('-', '_') # Replace dash sign with underscore as all variable name cannot hava dash symbols

    if (item_code_input in products_list):
        raw_materials_by_input(eval(item_code_input)) # Use eval to strip the string and convert into expression
    elif(item_code_input == 'ALL'):
        raw_materials_by_all_products()
    elif (item_code_input == 'PR_DOA_5_1'):            # Convert raw material form PR-DOA-5 into single strip
        raw_materials_by_input(eval(item_code_input))
    else:
        print('Please enter correct product code in as this format: PR-XXXX')

if __name__ == '__main__':
    apps()
