#! /Users/williamp/anaconda3/bin/python

import pandas as pd
import numpy as np
import glob, os, sys, pathlib

## This script should read in a concatenated output file (from isolates/) and return a file in a MDDI-appropriate format

# output dictionary from shigatyper.py for reference
SfDic = {"Shigella flexneri Yv": ["Xv"],
         "Shigella flexneri serotype 1a": ["gtrI"],
         "Shigella flexneri serotype 1b": ["gtrI", "Oac1b"],
         "Shigella flexneri serotype 2a": ["gtrII"],
         "Shigella flexneri serotype 2b": ["gtrII", "gtrX"],
         "Shigella flexneri serotype 3a": ["gtrX", "Oac"],
         "Shigella flexneri serotype 3b": ["Oac"],
         "Shigella flexneri serotype 4a": ["gtrIV"],
         "Shigella flexneri serotype 4av": ["gtrIV", "Xv"],
         "Shigella flexneri serotype 4b": ["gtrIV", "Oac"],
         "Shigella flexneri serotype 5a": (["gtrV", "Oac"], ['gtrV']),
         "Shigella flexneri serotype 5b": (["gtrV", "gtrX", "Oac"], ['gtrV', 'gtrX']),
         "Shigella flexneri serotype X": ["gtrX"],
         "Shigella flexneri serotype Xv (4c)": ["gtrX", "Xv"],
         "Shigella flexneri serotype 1c (7a)": ['gtrI', 'gtrIC'],
         "Shigella flexneri serotype 7b": ['gtrI', "gtrIC", "Oac1b"]}

# echo "sample\tprediction\tipaB" > {output}


shigatype_dataframe = pd.read_csv( "isolates/output.txt", sep="\t", header=None )

shigatype_dataframe.to_excel( "shigatypes.xlsx" )

