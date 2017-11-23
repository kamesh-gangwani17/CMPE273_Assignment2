# Generate stubs
python3 -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. ./replicate.proto
# Run master file
python3 master.py 
# Run slave file
python3 slave.py
# Run test script
python3 test.py
