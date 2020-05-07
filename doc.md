# Networking Project

## Authors: Ubadah Jafry, Hamza Ijaz

## Working

The whole system works in the following manner

* Server are launched using the `server.py` which launches the virtual servers that are set on the port given in the arguments
* Client is launched using the `client.py` where the parameters for launched servers are passed
* The client tries to connect with server and receives a checksum from all the server
* The checksum is generated from the file which is going to be downloaded by the client and will **only** connect to the server which have the same checksum in majority. This is a initial corruption check done by the client
* Now the client will request the file size from one of the server instead of all of them since the same checksum guaretee same size as well
* After receiving the size of file, the client divides them into equal parts (such that they are integers) and send argument to the server
* The argument contains offset and bytes to transfer, which will be parsed by server and the specified part of the file will be sent
* The client after receiving the file will generate combine them and generate a checksum and compare to the original checksum. In case, this fails the client will restart the process
* Once the file is checked, the connection is terminated by the client