#!/usr/bin/python

import ConfigParser
import glob
import os
import sys
import tempfile

def getPaths():
    conf = sys.argv[1:]    
    parser = ConfigParser.SafeConfigParser(allow_no_value=True)
    parser.read(conf)
    
    if parser.has_section("include"):
        items = []
        for item in parser.items("include"):
            item = os.path.abspath(item[0])
            items.extend(glob.glob(item))
            
        items = filter(os.path.isdir, items)
    
    
    if parser.has_section("exclude"):
        excludes = []
        for ex in parser.items("exclude"):
            ex = os.path.abspath(ex[0])
            excludes.extend(glob.glob(ex))
        
        for ex in excludes:
            if ex in items:
                items.remove(ex)
    
    return items
    



def writeFn(path, f):
    strtemplate = """
    
function %s {
    cd %s
}
    
""" % ( os.path.basename(path), path)
    
    f.write(strtemplate)



if __name__ == "__main__":
    paths = getPaths()
    f = tempfile.NamedTemporaryFile(delete=False)

    map(lambda path: writeFn(path, f), paths)

    print f.name
