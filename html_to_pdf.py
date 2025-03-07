#!/usr/bin/env python
"""
HTML to PDF Converter

This script converts HTML files to PDF using Pyppeteer.
Usage: python html_to_pdf.py <input_html_path> [output_pdf_path]

If output_pdf_path is not provided, it will use the same name as the input file with .pdf extension.
"""

import os
import sys
import asyncio
from pathlib import Path

from pyppeteer import launch


async def generate_pdf(html_path, pdf_path=None):
    """Generate PDF from HTML using pyppeteer."""
    if pdf_path is None:
        # Use the same name as the input file with .pdf extension
        pdf_path = str(Path(html_path).with_suffix('.pdf'))
    
    print(f"Converting {html_path} to {pdf_path}...")
    
    browser = await launch(headless=True)
    page = await browser.newPage()
    
    # Convert to absolute path
    abs_html_path = Path(html_path).absolute().as_uri()
    
    await page.goto(abs_html_path, {'waitUntil': 'networkidle0'})
    
    # Set PDF options
    pdf_options = {
        'path': pdf_path,
        'format': 'A4',
        'printBackground': True,
        'margin': {
            'top': '10mm',
            'right': '10mm',
            'bottom': '10mm',
            'left': '10mm'
        }
    }
    
    await page.pdf(pdf_options)
    await browser.close()
    
    print(f"PDF generated successfully: {pdf_path}")


def main():
    if len(sys.argv) < 2:
        print("Usage: python html_to_pdf.py <input_html_path> [output_pdf_path]")
        sys.exit(1)
    
    html_path = sys.argv[1]
    pdf_path = sys.argv[2] if len(sys.argv) > 2 else None
    
    if not os.path.exists(html_path):
        print(f"Error: Input file '{html_path}' does not exist.")
        sys.exit(1)
    
    asyncio.get_event_loop().run_until_complete(generate_pdf(html_path, pdf_path))


if __name__ == "__main__":
    main() 