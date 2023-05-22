# -*- coding: utf-8 -*-
"""
Created on Mon Dec 26 16:41:20 2022

@author: CSUST
"""

def transfer_2Dlist_to_1Dlist(orignal_list):
    transferred_list = [n for a in orignal_list for n in a ]
    return transferred_list