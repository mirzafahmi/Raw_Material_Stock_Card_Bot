import sys
import os
script_dir = os.path.dirname( __file__ )
#access Class file
ProDetect_class_script_dir = os.path.join( script_dir, "Raw_Data" )
sys.path.append(ProDetect_class_script_dir)
from ProDetect_class import ProDetect

PR_DEN_1 = ProDetect("PR_DEN_1", 25)
PHA5021C = ProDetect("PHA5021C", 40)

def apps():
    print(PR_DEN_1.min_potential_produced())
    print(PHA5021C.min_potential_produced())

apps()
#add exp date fx