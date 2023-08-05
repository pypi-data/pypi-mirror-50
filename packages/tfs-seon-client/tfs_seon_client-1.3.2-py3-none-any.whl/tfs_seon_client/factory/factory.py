from ..service.tfs_service import TFS_Service

class Factory(object):
    
    @staticmethod
    def create(instance_name):
        instance = TFS_Service(instance_name)
        return instance