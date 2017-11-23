import replicate_pb2
import grpc
import rocksdb
import replicate_pb2_grpc
import string


PORT = 3000

class TestRep():														
    def __init__(self, host='0.0.0.0', port=PORT):
        self.channel = grpc.insecure_channel('%s:%d' % (host, port))
        self.stub = replicate_pb2_grpc.ReplicateStub(self.channel)

    def put(self, key, val):
        return self.stub.put(replicate_pb2.Request(key=key, val=val))

    def delete(self, key):
        return self.stub.delete(replicate_pb2.Request(key=key))

def main():

    testing = TestRep()
    
    for i in range(0,7):
      i = str(i)
      output = testing.put(i,i)
      print(output.data)
     
    output = testing.delete('2')
    print(output.data)

if __name__ == "__main__":
    main()


