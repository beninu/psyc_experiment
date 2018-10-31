#!/usr/bin/env python
# coding=utf-8
#
# Author : beninu@gmail.com
# Created: 2018 Oct 28 Sun 22:13:35 CST

import sys
import json
import codecs
import fileinput

USAGE="""用法:
    python plb.py ~/Downloads/*.stage2.txt

    运行成功之后，会在当前目录产生plb.csv文件，该文件的中文是UTF-8编码的
"""

def read_file_content(filename):
    with open(filename, 'r') as f:
        return f.read()

def make_a_row(max_element, e1, e2, e3, e4, e5, last_list):
    row = [""]*max_element
    row[0] = e1
    row[1] = e2
    row[2] = e3
    row[3] = e4
    row[4] = e5
    for idx,val in enumerate(last_list):
        row[idx+4] = val
    #row = [str(e) for e in row]
    #print row
    return ",".join(row)

def write_bom_utf_16_le(csv):
    # 打印csv结果
    with open("plb.csv", "w") as f:
        f.write(codecs.BOM_UTF16_LE);
        for r in csv:
            f.write(r.encode('utf-16-le'))
            f.write('\r\n'.encode('utf-16-le'));

def main(argv):
    samples = [json.loads(read_file_content(f)) for f in argv[1:]]
    max_chengyu = max([s['exp']['left_list_num']+s['exp']['right_list_num'] for s in samples])
    #print max_chengyu
    max_element =  5 + max_chengyu
    csv = []
    row = make_a_row(max_element, 'code',
            'xuanze',
            'number_of_chengyu_starts_with_number',
            'number_of_chengyu_starts_without_number',
            "number_of_speed_input_character",
            [])
    #print row
    csv.append(row)
    for s in samples:
        #print s
        #print s['user_id'], s['exp']['left_list_num'], s['exp']['right_list_num'], len(s['speed']['input'])
        row = make_a_row(max_element,
                s['user_id'],
                s['xuanze'],
                str(s['exp']['left_list_num']),
                str(s['exp']['right_list_num']),
                str(len(s['speed']['input'])),
                [k[0] for k in s['exp']['left_list']] + [k[0] for k in s['exp']['right_list']])
        #print row
        csv.append(row)
    #print csv
    write_bom_utf_16_le(csv)
    print "processing done, please import plb.csv into excel"

if __name__=="__main__":
    if len(sys.argv) == 1:
        print USAGE
        sys.exit(-1)
    main(sys.argv)

