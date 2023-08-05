import pika
import uuid
import os
import json
from pprint import pprint
from rabbitmqX.patterns.client.rpc_client import RPC_Client

class Abstract_Service (RPC_Client):
    
    def integrate(self, user_key, tfs_url, organization_url):

        data = {'key': user_key, 
                'tfs_url': tfs_url,
                'organization_url': organization_url}       
        
        self.do(data)