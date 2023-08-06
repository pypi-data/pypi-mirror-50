import pika
import uuid
import os
import json
from pprint import pprint
from rabbitmqX.patterns.client.rpc_client import RPC_Client
from rabbitmqX.journal.journal import Journal

class TFS_Service (RPC_Client):
    
    def __init__(self, type):
        RPC_Client.__init__(self,'integration.tfs')
        self.type = type

    def integrate(self, user_key, tfs_url, organization_id):

        data = {'key': user_key, 
                'tfs_url': tfs_url,
                'organization_id': organization_id}       

        journal = Journal(self.type,data,"integration")

        return self.do(journal.__dict__)

