 # -*- coding: Shift-JIS -*-
import train as ic
import os.path as op

i = 0
for filename in ic.FileNames :
    while True :
        dirname = input(">>�u" + ic.ClassNames[i] + "�v�̉摜�̂���f�B���N�g�� �F ")
        if op.isdir(dirname) :
            break
        print(">> ���̃f�B���N�g���͑��݂��܂���I")

    ic.PreProcess(dirname, filename, var_amount=3)
    i += 1