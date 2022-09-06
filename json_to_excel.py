from apps import raw_materials_by_all_products_dict
import warnings

warnings.filterwarnings("ignore")

potential_produced_by_raw_material = raw_materials_by_all_products_dict()


if __name__ == '__main__':
    for x in potential_produced_by_raw_material:
        print(x, potential_produced_by_raw_material[x])
    
    

