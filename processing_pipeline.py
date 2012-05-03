#######################################################
# BioNLP Document Processing Pipeline
# Brandeis University, cs217, Spring 2012
#
# This is the core file for all pipeline routines.
#######################################################

import os, sys, sqlite3
from representation import *
from stage import *
from parameters import *

def load(rep):
    inf = get_optional_param('input_filename',rep,'')
    if inf != '':
        print 'Loading representation from '+outf
        rep.file_load(inf)
    else:
        indb = get_required_param('input_database',rep)
        print 'Loading representation from db'
        db = sqlite3.connect(indb)
        db.text_factory = str
        rep.db_load(db)

def save(rep):
    outf = get_optional_param('output_filename',rep,'')
    if outf != '':
        print 'Saving representation to '+outf
        rep.file_save(outf)
    else:
        outdbfile = get_required_param('output_database',rep)
        if not os.path.exists(outdbfile):
            print 'DB does not yet exist, creating'
            outdb = sqlite3.connect(outdbfile)
            outdb.execute('CREATE TABLE Representation (Layer TEXT, Key TEXT,'+\
                          ' Features TEXT)')
            outdb.commit()
        else:
            outdb = sqlite3.connect(outdbfile)
        outdb.text_factory = str
        outdb.execute('DELETE FROM Representation')
        print 'Saving representation to db'
        rep.db_save(outdb)

def run_command(command,db,rep):
    parts = command.split(' ')
    if command == 'save':
        save(rep)
    elif command == 'load':
        load(rep)
    elif parts[0].lower() == 'stage':
        print 'Running stage '+parts[1]
        if run_stage(parts[1],db,rep):
            print 'Stage finished successfully!'
        else:
            print 'Could not find stage '+parts[1]
            exit(2)
    elif parts[0].lower() == 'create':
        print 'Creating representation layer '+parts[1]
        layer = create_representation(parts[1],db,rep)
        if layer != None:
            print 'Created layer successfully!'
            rep.add_layer(layer)
        else:
            print 'Could not find representation layer '+parts[1]
            exit(2)
    elif len(parts[0]) == 0 or command.startswith('#'):
        pass
    else:
        print 'Unrecognized command '+str(command)

def run_pipeline(parameter_file):
    #load the params
    rep = Representation()
    rep.add_layer(load_parameters(parameter_file))
    #set up the db
    db = sqlite3.connect(get_required_param('doc_database',rep))
    db.text_factory = str
    #load the sequence
    f = open(get_required_param('stage_file',rep),'r')
    commands = []
    for l in f:
        commands.append(l[:-1])
    f.close()
    #run through the stages
    for c in commands:
        run_command(c,db,rep)
    #save at the end by default
    save(rep)

if len(sys.argv) != 2:
    print 'Usage: python processing_pipeline.py <parameter_file>'
    exit(2)
else:
    run_pipeline(sys.argv[1])
