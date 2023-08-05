from ..service.abstract_service import Abstract_Service

class Factory(object):
    
    @staticmethod
    def create(instance_name):
        instance = Abstract_Service(instance_name)
        return instance