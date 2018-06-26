# Dengue Mobile4D

## Features
### Client-side
1. User: Json request with lat & lng
2. Receive jobs 
3. Take & send photos
### Server-side
1. Find nearest points 
2. Send missing streets
3. Run detection model / store to DB / update missing streets

## Missing Streets
![Missing-streets](doc/missing-streets.png  "Missing Streets")
Missing-streets in Nakhon-si-thammarat province

![Missing-streets](doc/gsv-missing-streets.png  "Missing Streets")
Left (an available of Google street view images), Right (linestrings of the missing streets)

## How to run

* Python Installation
```
pip3 install -r requirements.txt
```

* Initialize server
```
python3 index.py
```
### Test request
* Linux users
```
curl --header "Content-Type: application/json" \
--request POST \
--data '{"send":"okay"}' \
http://localhost:5000/foo

```

* Windows users
```
curl -H "Content-Type: application/json" -X POST http://localhost:5000/foo -d "{\"send\":\"okay\"}"
```

## API Reference

### Request missing streets
Send current location of the user
```json
{
  "type": "Feature",
  "geometry": {
    "type": "Point",
    "coordinates": [99.8, 8.1]
  },
  "properties": {
	"province": "Nakhon Si Thammarat",
	"district": "Phrom Khiri",
	"subdistrict": "Thon Hong"
  }
}
```

### Submit photos
