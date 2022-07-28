import sys
import os
script_dir = os.path.dirname( __file__ )
#access Class file
ProDetect_class_script_dir = os.path.join( script_dir, "Raw_Data" )
sys.path.append(ProDetect_class_script_dir)
from ProDetect_class import ProDetect

products_list = ["PR_DEN", "PHA5021C", "PR_FLU", "PR_GAST_3", "PR_SYP", "PR_HBSAG", "PR_DOA_5", "PR_DAM", "PR_DBZ", "PR_DKE", "PR_DMD", "PR_DMDA", "PR_DMO", "PR_DOP", "PR_DTH", "PR_MYP", "PR_CHK"]

#innitiate the class by products

#Product_Code = ProDetect("product_code", tests_per_box, number_of_buffer_per_box)
PR_DEN = ProDetect("PR_DEN", 25, 1) #for all dengue products as they share materials
PHA5021C = ProDetect("PHA5021C", 40, 0)
PR_FLU = ProDetect("PR_FLU", 25, 2) #for all PR_FLU, PR_FSV and PR_FSVA products as they share materials
PR_GAST_3 = ProDetect("PR_GAST_3", 25, 1)
PR_SYP = ProDetect("PR_SYP", 25, 1)
PR_HBSAG = ProDetect("PR_HBSAG", 25, 1)
PR_DOA_5 = ProDetect("PR_DOA_5", 25, 0) #for all DOA combo

#for all single strip DOA test
PR_DAM = ProDetect("PR_DAM", 50, 0)
PR_DBZ = ProDetect("PR_DBZ", 50, 0)
PR_DCO = ProDetect("PR_DCO", 50, 0)
PR_DKE = ProDetect("PR_DAM", 50, 0)
PR_DMD = ProDetect("PR_DMD", 50, 0)
PR_DMDA = ProDetect("PR_DMDA", 50, 0)
PR_DMO = ProDetect("PR_DMO", 50, 0)
PR_DOP = ProDetect("PR_DOP", 50, 0)
PR_DTH = ProDetect("PR_DTH", 50, 0)

PR_MYP = ProDetect("PR_MYP", 25, 1)
PR_CHK = ProDetect("PR_CHK", 25, 1)

#to access all products raw material
def raw_materials_by_all_products():
    for item_code in products_list:
        print(eval(item_code).min_potential_produced())

#to access products raw material by input
def raw_materials_by_input(Item_Code):
    print(Item_Code.min_potential_produced())

def apps():
    #header
    terminal_size = os.get_terminal_size().columns #access terminal columns size for print the header
    text = "Summary of the Raw Material by Products"
    print('\n' f'{text:-^{terminal_size}}')

    item_code_input = input("Enter Item Code Here: ").upper().replace("-", "_") #replace dash sign with underscore as all variable name cannot hava dash symbols

    if (item_code_input in products_list):
        raw_materials_by_input(eval(item_code_input)) #use eval to strip the string and convert into expression
    elif(item_code_input == "ALL"):
        raw_materials_by_all_products()
    else:
        print("Please enter correct product code in as this format: 'PR-XXXX'")

apps()
