
import os
import re
import weakref
from gaussian import gaussian


class Config(object):
    def __init__(self, file):
        self.config = {}
        self.cbs = {}
        self.file = file
        
        self.load()
        
    def load(self):
        if os.path.isfile(self.file):
            with open(self.file, 'r') as file:
                for line in file:
                    if re.match('^\s*(#.*)?$', line):
                        continue
                        
                    m = re.match('^\s*(\w+)\s*:\s*(.*)$', line)
                    if not m:
                        raise SyntaxError()
                        
                    key, value = m.groups()
                    
                    self[key] = eval(value, globals())
            
    def dump(self):
        with open(self.file, 'w') as file:
            for key in self:
                file.write(key)
                file.write(': ')
                file.write(repr(self[key]))
                file.write('\n')
            
    def use(self, key, default=0, target=None, attr=None, type=lambda x: x, cb=None):
        if key not in self.config:
            self.config[key] = default
            self.cbs[key] = weakref.WeakKeyDictionary()
        
        print len(self.cbs[key])
        
        target = target or self
        ref = weakref.ref(target)
        
        if attr is not None:
            def assign(v):
                setattr(ref(), attr, type(v))
        
            self.use(key, target=target, cb=assign)
            
        if cb is not None:
            if target not in self.cbs[key]:
                self.cbs[key][target] = []
            
            self.cbs[key][target].append(cb)
            cb(self[key])
        
    def update(self, key):
        for cbs in self.cbs[key].values():
            for cb in cbs:
                cb(self.config[key])
            
    def __getitem__(self, key):
        return self.config[key]
        
    def __setitem__(self, key, val):
        if key not in self.cbs:
            self.use(key, val)
        else:
            self.config[key] = val
            self.update(key)
        
    def __delitem__(self, key):
        del self.config[key]
        self.update(key)
        
    def __contains__(self, key):
        return key in self.config
        
    def __iter__(self):
        return iter(self.config)
        

global_config = Config('config.conf')
