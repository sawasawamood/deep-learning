 # -*- coding: Shift-JIS -*-
import train as ic
import os.path as op

i = 0
for filename in ic.FileNames :
    while True :
        dirname = input(">>「" + ic.ClassNames[i] + "」の画像のあるディレクトリ ： ")
        if op.isdir(dirname) :
            break
        print(">> そのディレクトリは存在しません！")

    ic.PreProcess(dirname, filename, var_amount=3)
    i += 1