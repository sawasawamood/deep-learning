# -*- coding: Shift-JIS -*-
import train as ic
import os.path as op

while True:
    while True:
        imgname = input("\n>> �f�f��������@��FFT���ʂ���͂��Ă�������(�uEND�v�ŏI��) �F ")
        if op.isfile(imgname) or imgname == "END":
            break
        print(">> ���̃t�@�C���͑��݂��܂���I")
    if imgname == "END":
        break

    # �֐����s
    ic.TestProcess(imgname)