import grpc
import time
import replicate_pb2_grpc
import rocksdb
import replicate_pb2
import queue

from concurrent import futures

_ONE_DAY_IN_SECONDS = 60 * 60 * 24

class MyReplicateServicer(replicate_pb2_grpc.ReplicateServicer):
    def __init__(self):
        self.db = rocksdb.DB("mdb.db", rocksdb.Options(create_if_missing=True))
        self.queueofoper = queue.Queue()
    def putdecorator(func):
        def func_wrapper(self, request, context):
            
              slaveoper = replicate_pb2.Operation_sync(
                    operation=func.__name__, 
                    key=request.key.encode(), 
                    data=request.val.encode()
                 ) 
              self.queueofoper.put(slaveoper)
              return func(self, request, context)
        return func_wrapper
    
    def deletedecorator(func):
        def func_wrapper(self, request, context):
            
              slaveoper = replicate_pb2.Operation_sync(
                    operation=func.__name__, 
                    key=request.key.encode(), 
                    
                 ) 
              self.queueofoper.put(slaveoper)
              return func(self, request, context)
        return func_wrapper

    @putdecorator
    def put(self, request, context):
        keyref=request.key
        dataref=request.val
        print("Put key {} and value {} into the database ".format(keyref, dataref))
        self.db.put(keyref.encode(), dataref.encode())
	
        return replicate_pb2.Response(data='working')

    @deletedecorator
    def delete(self, request, context):
        keyref=request.key
        print("Delete {} data from the database".format(keyref))
        self.db.delete(keyref.encode())
        return replicate_pb2.Response(data='working')
        
    

    def synchronization(self, request, context):
        print("Connection is establised with the slave")
        while True:
            perform = self.queueofoper.get()
            print("performing these operation by sending these {}, {}, {} to the client/slave ".format(perform.operation, perform.key, perform.data))
            yield perform

def run(host, port):
    '''
    Run the GRPC server
    '''
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=2))
    replicate_pb2_grpc.add_ReplicateServicer_to_server(MyReplicateServicer(), server)
    server.add_insecure_port('%s:%d' % (host, port))
    server.start()

    try:
        while True:
            print("Server started at...%d" % port)
            time.sleep(_ONE_DAY_IN_SECONDS)
    except KeyboardInterrupt:
        server.stop(0)


if __name__ == '__main__':
    run('0.0.0.0', 3000)

		

