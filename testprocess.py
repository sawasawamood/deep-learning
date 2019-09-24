# -*- coding: Shift-JIS -*-
import train as ic
import os.path as op

while True:
    while True:
        imgname = input("\n>> 診断したい扇風機のFFT結果を入力してください(「END」で終了) ： ")
        if op.isfile(imgname) or imgname == "END":
            break
        print(">> そのファイルは存在しません！")
    if imgname == "END":
        break

    # 関数実行
    ic.TestProcess(imgname)