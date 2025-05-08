# family-sun
This repo generates a Plotly sunburst graph from a GEDCOM file (I really like genealogy and wanted to be able to generate pretty sunburst chart to display my lineage).

## Installation
This project uses Python 3.10.
```bash
git clone https://github.com/anacltd/family-sun.git
cd family-sun
python3.10 -m venv venv
source venv/bin/activate
pip install -e .
```

## How to use
If you simply want to display your family tree:
```bash
family-sun --gedcom_path ./gedcom.ged
```

If you want to change the color scale:
```bash
family-sun --gedcom_path ./gedcom.ged --color_scale Sunset
```

If you want to save the family tree as a PNG file:
```bash
family-sun --gedcom_path ./gedcom.ged --save True
```

## Caveat
It does _not_ handle homonyms, so if you happen to have some in your GEDCOM file, I advise you to add Jr. or Sr. so that each individual's name can be truly unique.

# TODO
[ ] Better displaying of names  
[ ] Add option to display dates and places