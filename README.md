# GRPC_python
GRPC python implementation with SQL Alchemy


## Prerequisites
First, install Python3:

```
brew install python3 // On Mac
sudo apt-get install python3 // On Ubuntu
```

Normally, pip comes with python3 if you're downloading the latest version (or any version above 3.4). If that is not the case, install pip by running the following:

```
curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
python3 get-pip.py
```

Install virtualenv:
```
pip3 install virtualenv
```

Install solidity compiler:
- On Mac:
    ```
    brew update
    brew upgrade
    brew tap ethereum/ethereum
    brew install solidity
    ```
- On Ubuntu:
    ``` 
    sudo add-apt-repository ppa:ethereum/ethereum
    sudo apt-get update
    sudo apt-get install solc
    ```

## Instructions
Clone the repository
```
git clone https://github.com/cyber-republic/elastos-smartweb-service.git
cd elastos-smartweb-service
```

To get the API service running, run the following terminal commands:
```
virtualenv -p `which python3` venv
```
```
source venv/bin/activate
```
```
pip3 install -r requirements.txt
```
```
cp .env.example .env
```

## Starting Postgres server:

```
cd tools
# This script automatically runs the scripts located at grpc_adenine/database/scripts/
./postgres.sh
cd ..
```

## Start the server:

Export Path:
```
export PYTHONPATH="$PYTHONPATH:$PWD/grpc_adenine/stubs/"
```

Run the following command:
```
python3 grpc_adenine/server.py
```

### Additional Info:
Command to build protocol buffer files:
```
cd $PWD/grpc_adenine/
python3 -m grpc_tools.protoc -I definitions --python_out=stubs --grpc_python_out=stubs definitions/common.proto
```

### Debugging:
Connect to postgresql database
```
docker container exec -it smartweb-postgres psql -h localhost -U gmu -d smartweb_master
```
Look at the tables
```
\dt 
```
Get all items from the table 'users'
``` 
select * from users;
```
