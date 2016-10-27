import os
import time
from os.path import abspath
from os.path import dirname

import sys

sys.path.insert(0, abspath(dirname(__file__)))

current_path = abspath(dirname(__file__))
pathlist = os.listdir(current_path)
print(current_path)

def decode_current_all():
    rule = find_rule()
    pathlist = os.listdir(current_path)

    for path in pathlist:
        decode_dat(os.path.join(current_path, path), rule)

def decode_dat(filepath, rule):
    img_dir_path = os.path.join(current_path, 'decode_imgs' )
    if not os.path.exists(img_dir_path):
        os.mkdir(img_dir_path)

    if filepath.endswith('.dat'):
        print('decode:' + filepath)
        localtime = time.localtime(os.path.getctime(filepath))
        format = '%Y-%m-%d_%H-%M-%S_'
        file_ctime = time.strftime(format, localtime)

        filename = filepath.split('\\')[-1].split('.dat')[0]
        out_name = file_ctime + filename + '.jpg'

        out_path = os.path.join(img_dir_path, out_name)
        with open(filepath, 'rb') as f_in:
            in_ints = bytearray(f_in.read())

        with open(out_path, 'wb') as f_out:
            l = [rule[b] for b in in_ints]
            f_out.write(bytearray(l))

def find_rule():
    img_in = os.path.join(current_path, 'rules/in.dat')
    img_out = os.path.join(current_path, 'rules/out.jpg')

    with open(img_in, 'rb') as f_in:
        in_ints = bytearray(f_in.read())

    with open(img_out, 'rb') as f_out:
        out_ints = bytearray(f_out.read())

    rule = [0] * 256
    flag = [False] * 256

    for i in range(len(in_ints)):
        if flag[in_ints[i]] == False:
            rule[in_ints[i]] = out_ints[i]
            flag[in_ints[i]] = True
        if all(flag):
            break
    return rule

if __name__ == '__main__':
    decode_current_all()