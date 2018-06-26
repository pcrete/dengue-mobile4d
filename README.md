# Dengue Mobile4D

## Features
1. Simple request
2. Upload image
3. Render HTML 

## Missing Streets
![Missing-streets](doc/missing-streets.png  "Missing Streets")
Left (An available of Google street view images), Right (Linestrings of the missing streets)

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