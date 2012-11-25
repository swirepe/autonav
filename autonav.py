#!/usr/bin/python
import ConfigParser
import glob
import os
import sys
import tempfile

from collections import defaultdict


def getPaths():
    conf = sys.argv[1:]    
    parser = ConfigParser.SafeConfigParser(allow_no_value=True)
    parser.optionxform = str  # make it case sensitive
    parser.read(conf)
   
    items = []
 
    if parser.has_section("include"):
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
    

def pathsAndNames(paths):
    """
    if two top-level names are the same, disambiguate them
    by putting in a hyphen
    
    replace spaces with underscores in the name
    """
    dupes = defaultdict(list)
    
    for path in paths:
        dupes[ os.path.basename(path).replace(" ", "_") ].append(path)
        
    pairs = []
    for base, path in dupes.iteritems():
        if len(path) > 1:
            for p in path:
                prefix = os.path.basename(os.path.dirname(p))
                pairs.append( (p, prefix + "-" + base) )
        else:
            pairs.append( (path[0], base) )

    return pairs
    

def lowercasePathsAndNames(pathPairs):
    """doubles the length of this by turning things into lowercase also."""
    newPairs = pathPairs[:]
    
    for path, base in pathPairs:
        if base.lower() != base:
            newPairs.append( (path, base.lower() ) )
        
                
    return newPairs


def writeFn(path, name, f):
    strtemplate = """
    
function %s {
    cd '%s'
}
    
""" % ( name, path)
    
    f.write(strtemplate)


def writeMappings(pathPairs, f):
    pathmax = max([len(path) for (path, name) in pathPairs])
    namemax = max([len(name) for (path, name) in pathPairs])
    
    # put things in order, plz
    pathPairs.sort(key=lambda tup: tup[1])
    
    # start the function
    f.write("function viewnavs {\n\n" )
    
    for path, name in pathPairs:
        f.write('    echo "%s\t%s"\n' % (name.ljust(namemax), path.rjust(pathmax)) )
        
    f.write("\n\n}\n")
    
    


if __name__ == "__main__":
    paths = getPaths()
    f = tempfile.NamedTemporaryFile(delete=False)

    pathPairs = lowercasePathsAndNames(pathsAndNames(paths))

    for path, name in pathPairs:
        writeFn(path, name, f)

    writeMappings(pathPairs, f)
    
    print f.name
    f.close()
