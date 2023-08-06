import logging

class mdtree(Object):
    
    def __init__(self, raw='', file='', *args, **kwargs):
        data = ''
        if raw != '':
            data = raw
        elif file != '':
            with open(file, "r") as f:
                data = f.read()
        else :
            ("You must provide markdown raw or file!")

