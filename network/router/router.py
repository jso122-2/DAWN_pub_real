# network/router/router.py
"""Network Router for DAWN"""

class Router:
    def __init__(self):
        self.routes = {}
        self.active = True
        
    def route(self, source, target, data):
        return data
        
    def add_route(self, name, handler):
        self.routes[name] = handler
        
    def get_status(self):
        return {'active': self.active, 'routes': len(self.routes)}


router = Router()
