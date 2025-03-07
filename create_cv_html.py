import os
import shutil
import subprocess
from datetime import datetime

import yaml
from jinja2 import Environment, FileSystemLoader
from cvmaker import make_paper_markdown_table


def main():
    with open('./asset/papers.yml', 'r') as f:
        papers = yaml.safe_load(f)

    main_table = make_paper_markdown_table(papers['main'])
    others_table = make_paper_markdown_table(papers['others'])

    # Get today's date
    today = datetime.now()

    # Format the date as "Month Day, Year"
    formatted_date = today.strftime("%b %d, %Y")

    env = Environment(loader=FileSystemLoader('.'))
    template = env.get_template('./asset/index_template.md')

    with open('index.md', 'w', encoding='utf-8') as f:
        f.write(template.render(
            table1=main_table,
            table2=others_table,
            today=formatted_date,
            L1='<span class=level>&#9679;</span>',
            L2='<span class=level>&#9679;&#9679;</span>',
            L3='<span class=level>&#9679;&#9679;&#9679;</span>',
        ))

    os.system('pandoc index.md -s --css=./asset/github-pandoc.css --embed-resources --metadata title="Sangwon Lee" -o index.html')
    
    # Copy for PDF generation.
    cv_html_path = './output/Curriculum Vitae - Sangwon Lee.html'
    cv_pdf_path = './output/Curriculum Vitae - Sangwon Lee.pdf'
    shutil.copy('index.html', cv_html_path)
    
    # Generate PDF from HTML using the html_to_pdf.py script
    print("Generating PDF from HTML...")
    subprocess.run(['uv', 'run', 'python', 'html_to_pdf.py', cv_html_path, cv_pdf_path], check=True)


if __name__ == '__main__':
    main()