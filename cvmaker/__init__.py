import requests
from bs4 import BeautifulSoup
from markdown_table_generator import (
    generate_markdown, table_from_string_list, Alignment
)


def crawl_paper_info(user_id='-TInzSAAAAAJ'):
    """Crawl paper information from Google Scholar profile.

    Parameters
    ----------
    user_id : str
        Google Scholar user ID. Default is '-TInzSAAAAAJ'. It's my user ID...

    Returns
    -------
    list
        List of dictionaries containing paper information. Each dictionary
        contains the following keys:
        - title: str
            Paper title.
        - authors: str
            Authors of the paper.
        - journal_info: str
            Journal information of the paper.
        - citations: str
            Number of citations of the paper.
        - year: str
            Year of the paper.
    """
    profile_url = f'https://scholar.google.com/citations?user={user_id}'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }

    response = requests.get(profile_url, headers=headers)

    if response.status_code != 200:
        raise Exception('Failed to retrieve the page.')

    html_code = response.text

    # Parse HTML.
    soup = BeautifulSoup(html_code, 'html.parser')

    # Select tag <tr> containing paper information.
    tr_tags = soup.find_all('tr', class_='gsc_a_tr')

    # Extract information for each <tr> tag.
    info = []
    for tr_tag in tr_tags:
        title = tr_tag.find('a', class_='gsc_a_at').text
        authors = tr_tag.find('div', class_='gs_gray').text
        journal_info = tr_tag.find_all('div', class_='gs_gray')[1].text
        citations = tr_tag.find('a', class_='gsc_a_ac').text
        year = tr_tag.find('span', class_='gsc_a_hc').text

        info.append({
            'title': title,
            'authors': authors,
            'journal_info': journal_info,
            'citations': citations,
            'year': year,
        })
    
    return info


def split_main_and_others(info):
    """Split the information into main and others.

    Parameters
    ----------
    info : list
        List of dictionaries containing paper information.

    Returns
    -------
    dict
        Dictionary containing main and others. The keys are 'main' and 'others'.
    """
    main_papers = []
    other_papers = []
    for p in info:
        if p['title'].startswith('*') or p['title'].startswith('(*'):
            main_papers.append(p)
        else:
            other_papers.append(p)

    return {
        'main': main_papers,
        'others': other_papers
    }


def make_paper_text(paper):
    title = paper['title'].replace('(*', '(').replace('*', '')
    authors = paper['authors'].replace(', ...', ' et al.')
    
    if len(authors.split(',')) > 6:
        authors = authors.split(',')[:3]
        # authors.append('et al.')
        authors = ', '.join(authors) + ' et al.'
    
    text = f"{title}, {authors}, *{paper['journal_info']}*"

    if 'keywords' in paper:
        text += '<br>' + ''.join(
            [f'<span class="badge">{v}</span> ' for v in paper['keywords']]
        )

    return text


def make_paper_markdown_table(papers):
    rows = [['Title', 'Citations', 'Year']]
    for paper in papers:
        row = [
            make_paper_text(paper),
            paper['citations'],
            paper['year'],
        ]

        row = [str(c) for c in row]
        # print(row)

        rows.append(row)

    table1 = table_from_string_list(rows, Alignment.LEFT)
    text = generate_markdown(table1)

    return text