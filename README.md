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

* Test request
```
curl --header "Content-Type: application/json" \
--request POST \
--data '{"send":"okay"}' \
http://localhost:5000/foo
```