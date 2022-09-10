import sys
import os
from analysis_module import products_class as pc


products_list = ['PRODUCT_F_1', 'PRODUCT_F_2', 'PRODUCT_F_3_1', 'PRODUCT_F_3_2', 'PRODUCT_A', 'PRODUCT_O_1', 'PRODUCT_O_2', 'PRODUCT_O_3', 'PRODUCT_P', 'PRODUCT_S', 'PRODUCT_Q', 'PRODUCT_L_5_AMP', 'PRODUCT_L_5_KET', 'PRODUCT_L_4', 'PRODUCT_L_3', 'PRODUCT_C', 'PRODUCT_D', 'PRODUCT_E', 'PRODUCT_G', 'PRODUCT_J', 'PRODUCT_H', 'PRODUCT_I', 'PRODUCT_K', 'PRODUCT_M', 'PRODUCT_N', 'PRODUCT_R', 'PRODUCT_B']

# Innitiate the class by products

# Product_Code = Products('product_code', tests_per_box, number_of_buffer_per_box)
PRODUCT_F_1 = pc.Products('PRODUCT_F_1', 25, 1)          # For all F products as they share materials
PRODUCT_F_2 = pc.Products('PRODUCT_F_2', 25, 1)
PRODUCT_F_3_1 = pc.Products('PRODUCT_F_3_1', 10, 1)
PRODUCT_F_3_2 = pc.Products('PRODUCT_F_3_2', 25, 1)
PRODUCT_A = pc.Products('PRODUCT_A', 40, 0)
PRODUCT_O_1 = pc.Products('PRODUCT_O_1', 25, 2)          # For all PRODUCT_O_1, PRODUCT_O_2 and PRODUCT_O_3 products as they share materials
PRODUCT_O_2 = pc.Products('PRODUCT_O_2', 25, 2)
PRODUCT_O_3 = pc.Products('PRODUCT_O_3', 25, 2)
PRODUCT_P = pc.Products('PRODUCT_P', 25, 1)
PRODUCT_S = pc.Products('PRODUCT_S', 25, 1)
PRODUCT_Q = pc.Products('PRODUCT_Q', 25, 1)
PRODUCT_L_5_AMP = pc.Products('PRODUCT_L_5_AMP', 25, 0)
PRODUCT_L_5_KET= pc.Products('PRODUCT_L_5_KET', 25, 0)      
PRODUCT_L_4 = pc.Products('PRODUCT_L_4', 25, 0)
PRODUCT_L_3 = pc.Products('PRODUCT_L_3', 25, 0)

PRODUCT_C = pc.Products('PRODUCT_C', 50, 0)
PRODUCT_D = pc.Products('PRODUCT_D', 50, 0)
PRODUCT_E = pc.Products('PRODUCT_E', 50, 0)
PRODUCT_J = pc.Products('PRODUCT_J', 50, 0)
PRODUCT_G = pc.Products('PRODUCT_G', 50, 0)
PRODUCT_H = pc.Products('PRODUCT_H', 50, 0)
PRODUCT_I = pc.Products('PRODUCT_I', 50, 0)
PRODUCT_K = pc.Products('PRODUCT_K', 50, 0)
PRODUCT_M = pc.Products('PRODUCT_M', 50, 0)
PRODUCT_N = pc.Products('PRODUCT_N', 50, 0)

PRODUCT_R = pc.Products('PRODUCT_R', 25, 1)
PRODUCT_B = pc.Products('PRODUCT_B', 25, 1)

# To access all products raw material
def raw_materials_by_all_products():
    for item_code in products_list:
        print(eval(item_code).min_potential_produced())


# To create dict for all the min summary of potetial raw material can produced for all product
def raw_materials_by_all_products_dict():
    for item_code in products_list:
        summary_of_all_product = eval(item_code).min_potential_produced_all()
    return summary_of_all_product


# To access products raw material by input
def raw_materials_by_input(Item_Code):
    print(Item_Code.min_potential_produced())


# To access min potential can be prouduce by item code
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
    else:
        print('Please enter correct product code in as this format: PRODUCT_X')

if __name__ == '__main__':
    apps()
