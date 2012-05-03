import sys, os, subprocess
from representation import *

def shell_command(command):
    """Runs a shell command and pipes it through python's stdout"""
    print str(command)
    return subprocess.call(command, stdin=None, stdout=sys.stdout,
                          stderr=sys.stderr,shell=True) == 0

"""Basic stage of operation over the data representation"""
class Stage:
    def __init__(self,name,layer,feature='NONE'):
        self.name = name
        self.layer = layer
        self.feature = feature   

    def processAll(self,db,rep):
        lay = rep[self.layer]
        self.pre_process(db,rep)
        for k in lay:
            result = self.process(k,lay[k],db,rep)
            if result != None:
                lay.set(k,self.feature,result)
        self.post_process(db,rep)

    def pre_process(self,db,rep):
        pass

    def process(self,key,features,db,rep):
        pass

    def post_process(self,db,rep):
        pass
    
        
def run_stage(stage,db,representation):
    """dynamicly load and run a stage"""
    mod = __import__('stages.'+stage)
    for name, obj in inspect.getmembers(mod):
        for name2,obj2 in inspect.getmembers(obj):
            if inspect.isclass(obj2) and Stage in inspect.getmro(obj2) and \
               stage == name2 and len(inspect.getmro(obj2)) > 1:
                stage = obj2(name2)
                stage.processAll(db,representation)
                return True
    return False

