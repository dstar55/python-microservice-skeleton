# python-microservice-skeleton

create conda environment

```
$  conda create -n skeleton python=3.7
```

activate conda environment
```
$  activate skeleton
```

install dependencies
```
$  pip install -r requirements.txt
```

run test
```
$  python test_api.py
```

run application
```
$  python app.py
```
 
[Swagger UI](http://localhost:9090/v1.0/ui/)

## curl

get all items
```
$  curl http://localhost:9090/v1.0/items/
```






