#! /usr/bin/env python
import sys
import re

from collections import defaultdict

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

def make_object_tests(module_contents={}):
    tests = defaultdict(dict)
    for module_name, contents in module_contents.iteritems():
        tests[module_name] = dict(zip(contents,
            [re.compile('[ \(,]{0}[ \(,]'.format(obj)) for obj in contents]))
    return tests


def find_module_usage(module_tests={}):
    print filename
    print "="*len(filename)
    for line_number, line in enumerate(file_lines):
        if line[0]=='#':
            #skip comments
            continue
        for module_name, tests in module_tests.iteritems():
            for obj_name, test in tests.iteritems():
                if test.search(line):
                    line_seg = line[:20] if len(line)>20 else line[:-1]
                    print "{num}: {l}...\t{o} from {m}".format(num=line_number,
                            l=line_seg, o=obj_name, m=module_name)

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
            tests = make_object_tests(module_contents)
            find_module_usage(tests)
    except IOError:
        print "File {f} does not exist".format(f=filename)

if __name__=='__main__':
    run()
