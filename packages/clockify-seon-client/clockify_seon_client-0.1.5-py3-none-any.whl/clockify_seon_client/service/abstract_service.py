import pika
import uuid
import os
import json
from pprint import pprint
from rabbitmqX.patterns.client.rpc_client import RPC_Client

class Abstract_Service (RPC_Client):
    
    def integrate(self, clockify_key = None, clockify_workspace_id = None, tfs_id = None):
        
        data = {'clockify_key': clockify_key, 
                'clockify_workspace_id': clockify_workspace_id,
                'tfs_id': tfs_id}       
        return self.do(data)