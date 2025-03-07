# Automatic CV generation

## 1. Update paper information
```shell
uv run python update_paper_asset.py
```

## 2. Create HTML and PDF files
```shell
uv run python create_cv_html.py
```
This command will:
1. Generate the HTML file from the markdown template
2. Automatically convert the HTML to PDF using Pyppeteer

The generated files will be:
- `index.html` in the root directory
- `./output/Curriculum Vitae - Sangwon Lee.html`
- `./output/Curriculum Vitae - Sangwon Lee.pdf`

## 3. Convert any HTML to PDF (optional)
You can also convert any HTML file to PDF using the standalone script:
```shell
uv run python html_to_pdf.py <input_html_path> [output_pdf_path]
```

If `output_pdf_path` is not provided, it will use the same name as the input file with `.pdf` extension.

### PDF Options
The generated PDF uses the following settings:
* Page size: A4
* Margins: 10mm on all sides
* Background graphics are included