# Dengue Mobile4D

## How to run

* Installation
```
pip3 install -r requirements.txt
```

* Server side
```
python3 index.py
```

* Test request - Linux
```
curl --header "Content-Type: application/json" \
--request POST \
--data '{"send":"okay"}' \
http://localhost:5000/foo

```

* Windows
```
curl -H "Content-Type: application/json" -X POST http://localhost:5000/foo -d "{\"send\":\"okay\"}"
```

## Features
1. Simple request
2. Upload image
3. Render HTML 