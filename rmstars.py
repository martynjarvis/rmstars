#! /usr/bin/env python
import sys
import re

matches = re.compile("import \*")

filename = ""
file_lines = []

def get_import_star_lines(f):
    global file_lines # could seek(0)
    file_lines = f.readlines()
    stars = filter(matches.search, file_lines)
    return stars

def get_module_names(import_lines):
    modules = []
    for line in import_lines:
        module_path = line.split()[1]
        module_resolved = module_path.split('.')
        modules.append(module_resolved)
    return modules

def dir_modules(modules=[]):
    module_contents = {}
    for module in modules:
        module_name  = '.'.join(module)
        _temp = __import__(module_name, globals(), locals(), [module_name], -1)
        module_contents[module_name] = dir(_temp)
    return module_contents

def find_module_usage(module_contents={}):
    print filename
    print "="*len(filename)
    for line_number, line in enumerate(file_lines):
        if line[0]=='#':
            continue
        for module_name, contents in module_contents.iteritems():
            for obj in contents:
                o_test = re.compile('[ \(,]{0}[ \(,]'.format(obj))
                if o_test.search(line):
                    line_seg = line[:20] if len(line)>20 else line[:-1]
                    print "{num}: {l}...\t{o} from {m}".format(num=line_number,
                            l=line_seg, o=obj, m=module_name)

def run():
    global filename
    try:
        filename = sys.argv[1]
    except IndexError:
        print "usage: ./cleanup.py <filename>"
        exit()

    try:
        with open(filename,'r') as f:
            stars = get_import_star_lines(f)
            module_names = get_module_names(stars)
            module_contents = dir_modules(module_names[0:1])
            find_module_usage(module_contents)
    except IOError:
        print "File {f} does not exist".format(f=filename)

if __name__=='__main__':
    run()
