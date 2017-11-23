import replicate_pb2
import rocksdb
import grpc
import time
import replicate_pb2_grpc

PORT = 3000
class SlaveRep():
    def __init__(self, host='0.0.0.0', port=PORT):
        self.db = rocksdb.DB("slv.db", rocksdb.Options(create_if_missing=True))
        self.channel = grpc.insecure_channel('%s:%d' % (host, port))
        self.stub = replicate_pb2_grpc.ReplicateStub(self.channel)
    def performsync(self):
        getsync = self.stub.synchronization(replicate_pb2.Request_sync())
        
        time.sleep(5)
        for slaveoper in getsync:
            if slaveoper.operation == 'put':
                putslave(self,slaveoper.key.encode(), slaveoper.data.encode())
            if slaveoper.operation == 'delete':
                deleteslave(self,slaveoper.key.encode())
def putslave(self,key,data):
    self.db.put(key, data)
    print("Put {}:{} into the slave".format(key, data))

def deleteslave(self,key):
    self.db.delete(key)
    print("Delete {} from the slave".format(key))  
        
        
def main():
  slave = SlaveRep()
  slave.performsync()

if __name__ == "__main__":
    main()

