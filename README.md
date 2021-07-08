# Docker Container Builer


## Getting started

### Install
```shell
python3 setup.py install
```

It may require root, so:
```shell
sudo python3 setup.py install
```

### How to Use
To build and push
```shell
container-builder build path/to/root-dir IMAGE_NAME \
  --repository=repository-name \
  --tag=latest \
  --push
```
