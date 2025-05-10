# family-sun
This repo generates a Plotly sunburst graph from a GEDCOM file (I really like genealogy and wanted to be able to generate pretty sunburst chart to display my lineage).

## Installation
This project uses Python 3.10.
```bash
pip install family-sun
```

## How to use
If you simply want to display your family tree:
```bash
generate-tree --gedcom-path ./gedcom.ged
```

If you want to change the color scale:
```bash
generate-tree --gedcom-path ./gedcom.ged --color-scale earth
```

If you want to save the family tree as a PNG file:
```bash
generate-tree --gedcom-path ./gedcom.ged --save True
```

If you want to color your tree based on patronyms:
```bash
generate-tree --gedcom-path ./gedcom.ged --color-by patronyms
```

If you want to only display a specific number of generations:
```bash
generate-tree --gedcom-path ./gedcom.ged --nb-of-generation 6
```

## Caveat
It does _not_ handle homonyms, so if you happen to have some in your GEDCOM file, I advise you to add Jr. or Sr. so that each individual's name can be truly unique.


## Contributing
To contribute, please clone and install the repository locally:
```bash
git clone https://github.com/anacltd/family-sun.git
cd family-sun
python3.10 -m venv venv
source venv/bin/activate
pip install -e .
```


# TODO
[ ] Add palettes examples.