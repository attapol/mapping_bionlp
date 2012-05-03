import os, inspect
import xml.etree.ElementTree as ET            

def get_doc_contents(doc_id,db):
    results = db.execute('SELECT CLEAN_CONTENT From Papers WHERE ID=?',[doc_id])
    result = results.fetchone()
    if result != None and result[0] != None:
        return result[0]
    else:
        print 'Error: contents for document with id '+str(doc_id)+\
              ' were not found'
        return None

def prep_string(value):
    return str(value).replace(':','&COL').replace(';','&SEM')\
           .replace('|','&BAR').replace('{','&OPEN').replace('}','&CLOSE')

def unprep_string(text):
    return text.replace('&COL',':').replace('&SEM',';').replace('&BAR','|')\
           .replace('&OPEN','{').replace('&CLOSE','}')

#data reading/writing
def get_groups(text):
    """Get lists from text considering recursive embedding"""
    groups = []
    cur_group = ''
    level = 0
    for c in text.strip('{} '):
        if c == '{':
            level += 1
        elif c == '}':
            level -= 1
        if c == '|' and level == 0:
            groups.append(cur_group)
            cur_group = ''
        else:
            cur_group += c
    if len(cur_group) > 0:
        groups.append(cur_group)
    return groups
        
def data_type_write(value):
    if type(value) == list or type(value) == tuple:
        return '{'+'|'.join([data_type_write(v) for v in value])+'}'
    elif type(value) == dict:
        return ';'.join([k+':'+data_type_write(value[k]) for k in value])
    else:
        return prep_string(value)

def data_type_read(text):
    if len(text.strip()) == 0:
        return dict()
    elif ':' in text:
        result = dict()
        for pair in text.split(';'):
            [k,v] = pair.split(':')
            result[k] = data_type_read(v)
        return result
    elif '|' in text:
        return tuple([data_type_read(t) for t in get_groups(text)])
    else:
        try:
            return float(text)
        except:
            return unprep_string(text)

"""Class for the overall representation of all processed data"""
class Representation:
    def __init__(self):
        self.layers = []
        self.layers_dict = dict()

    def add_layer(self,layer):
        self.layers.append(layer)
        self.layers_dict[layer.name] = layer

    def __getitem__(self,key):
        if not key in self.layers_dict:
            print 'Error: Representation Layer '+key+' accessed before creation'
            return None
        return self.layers_dict[key]
    
    def file_save(self,filename):
        f = open(filename,'w')
        f.write('<representation>\n')
        for layer in self.layers:
            layer.file_save(f)
        f.write('</representation>\n')
        f.close()

    def db_save(self,db):
        for layer in self.layers:
            layer.db_save(db)

    def file_load(self,filename):
        tree = ET.ElementTree()
        rep = tree.parse(filename)
        for layerXML in rep.findall('layer'):
            layer = RepresentationLayer(layerXML.attrib["name"])
            layer.file_load(layerXML)
            self.add_layer(layer)

    def db_load(self,db):
        r = db.execute('SELECT DISTINCT Layer FROM Representation')
        for row in r:
            if row[0] != None and row[0] != 'Global':
                layer = RepresentationLayer(row[0])
                layer.db_load(db)
                self.add_layer(layer)

"""The base class for a data representation layer"""
class RepresentationLayer(dict):
    def __init__(self,name):
        self.name = name

    def file_save(self,output_file):
        output_file.write('\t<layer name="'+self.name+'">\n')
        for key in self:
            value = self[key]
            output_file.write('\t\t<pair key="'+data_type_write(key)+\
                              '" features="'+data_type_write(value)+'" />\n')
        output_file.write('\t</layer>\n')

    def db_save(self,db):
        vals = []
        for key in self:
            value = self[key]
            vals.append([self.name,data_type_write(key),data_type_write(value)])
        db.executemany("INSERT INTO Representation VALUES (?,?,?)",vals)
        db.commit()

    def load_value(self,key_text,value_text):
        self[data_type_read(key_text)] = data_type_read(value_text)

    def file_load(self,node):
        for pair in node.findall('pair'):
            self.load_value(pair.attrib['key'],pair.attrib['features'])

    def db_load(self,db):
        print 'loading '+self.name
        result = db.execute("SELECT Key,Features FROM Representation "+\
                            "WHERE Layer=?",[self.name])
        for row in result:
            self.load_value(row[0],row[1])

    def add(self,key):
        self[key] = dict()

    def get(self,key,feature):
        return self[key][feature]

    def set(self,key,feature,value):
        if not key in self:
            self[key] = dict()
        self[key][feature] = value

    def create(self,db,rep):
        #derriving classes will fill this in
        print 'WARNING: Calling base create, nothing will happen!'
        pass


#dynamicly load representations
def create_representation(layer_name,db,rep):
    mod = __import__('layers.'+layer_name)
    for name, obj in inspect.getmembers(mod):
        for name2,obj2 in inspect.getmembers(obj):
            if inspect.isclass(obj2) and \
               name2 == layer_name and \
               RepresentationLayer in inspect.getmro(obj2) and \
               len(inspect.getmro(obj2)) > 1:
                    layer = obj2(name2)
                    layer.create(db,rep)
                    return layer
    return None
          
