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

def make_a_row(max_element, e1, e2, e3, e4, last_list):
    row = [""]*max_element
    row[0] = e1
    row[1] = e2
    row[2] = e3
    row[3] = e4
    for idx,val in enumerate(last_list):
        row[idx+4] = val
    #row = [str(e) for e in row]
    #print row
    return ",".join(row)

def main(argv):
    samples = [json.loads(read_file_content(f)) for f in argv[1:]]
    max_chengyu = max([s['exp']['left_list_num']+s['exp']['right_list_num'] for s in samples])
    #print max_chengyu
    max_element =  4 + max_chengyu
    csv = []
    row = make_a_row(max_element, 'code',
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
                str(s['exp']['left_list_num']),
                str(s['exp']['right_list_num']),
                str(len(s['speed']['input'])),
                [k[0] for k in s['exp']['left_list']] + [k[0] for k in s['exp']['right_list']])
        #print row
        csv.append(row)
    print csv
    # 打印csv结果
    f = codecs.open("plb.csv", "w", "utf-8")
    for r in csv:
        f.write(r);
        f.write('\r\n');
    f.close()

if __name__=="__main__":
    if len(sys.argv) == 1:
        print USAGE
        sys.exit(-1)
    main(sys.argv)

