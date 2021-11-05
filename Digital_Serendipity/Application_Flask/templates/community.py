import numpy as np
import csv

group1 = ['Gate','W1','W3','W4','N25']
group2 = ['N1','N2','N22']
group3 = ['N5','N9','N10','N11','N13']
group4 = ['N7','W5','W6','W7','W10']
group5 = ['N3','N4','W2','W8','E5','E9','E11','E14','E16']
group6 = ['E18','E20','E21']

Contents_1 = ['Class','Food','Book','Student Club']
Contents_2 = ['Office','Food','Book','Sports Club']
Contents_3 = ['Class','Residence']
Contents_4 = ['Class','Residence']
Contents_5 = ['Office']
Contents_6 = ['Residence','Medical Treatment']

def group_select(Name, Building):
    
    for i in range(1,7):
        x = globals()['group{}'.format(i)]
        y = globals()['Contents_{}'.format(i)]
        for q in x:
            if Building == q:
                print(x)
                print(y)
                t = y
                print(t)
                
    return t










