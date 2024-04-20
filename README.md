# Automatic CV generation

## 1. Update paper information
```shell
python update_paper_asset.py
```

## 2. Create HTML file
```shell
python create_cv_html.py
```

## 4. Convert HTML to PDF
Print `index.html` with following options using Chrome.
* Page size: A4
* Margin: left 5mm, right 5mm, top 12mm, bottom 12mm
* Activate 'Background graphics' option
* Save as `Curriculum Vitae - Sangwon Lee.pdf`