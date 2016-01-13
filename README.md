# Export content from HubSpot blog

A set of Python scripts to facilitate blog migration from HubSpot's website platform to Ghost.

* Export content from HubSpot to JSON and HTML
* Export comments to to WXR/Disqus format
* Create an import file ready for import in Ghost

Limitations:

* Ignores some meta data maintained in hubspot
* Ghost tags and authors are not generated

## Setup

```
virtualenv venv
source venv/bin/activate
pip install -r requirements.txt
cp config-dist.py config.py
```

Adjust the settings in `config.py`.


# Usage


## 1. Create Hubspot dump to an internal format

```
python dump.py
```

This will produce data in the folder `export` which can then be exported in the next step.

## 2. Export articles to Ghost format

```
python to_ghost.py
```

This results in a file `ghost.json`.

## 3. Export comments to WXR/Disqus format

```
python to_wxr.py
```

This results in a file `disqus.xml`.
