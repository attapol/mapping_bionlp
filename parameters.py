from representation import *

def load_parameters(filename):
    pars = RepresentationLayer('Global')
    f = open(filename,'r')
    for l in f:
        if not l.startswith('#') and '=' in l:
            [prop,value] = l[:-1].split('=')
            pars.load_value(prep_string(prop.strip()),
                            prep_string(value.strip()))
    return pars

def get_required_param(param,rep):
    if param in rep['Global']:
        return rep['Global'][param]
    else:
        print 'Error: required parameter '+param+' not specified!'
        exit(2)

def get_optional_param(param,rep,default=None):
    if param in rep['Global']:
        return rep['Global'][param]
    else:
        return default

def get_required_int_param(param,rep):
    val = get_required_param(param,rep)
    try:
        return int(val)
    except:
        print 'Error: parameter '+param+' is not an integer!'
        exit(2)
