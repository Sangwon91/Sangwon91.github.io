import yaml
from pathlib import Path
from cvmaker import crawl_paper_info, split_main_and_others


def main():
    ATTRIBUTES = ('keywords', )

    # Load the saved papers if exists.
    # It is used to keep the manually added attributes when updating the papers.
    saved_papers = {}
    if Path('./asset/papers.yml').exists():
        with open('./asset/papers.yml', 'r') as f:
            saved_papers = yaml.safe_load(f)

        # Make title as key for each paper.
        saved_papers = {
            **{p['title']: p for p in saved_papers['main']},
            **{p['title']: p for p in saved_papers['others']},
        }

    papers = crawl_paper_info()
    
    # Add manually added attributes to the papers.
    for paper in papers:
        if paper['title'] not in saved_papers:
            continue

        for attr in ATTRIBUTES:
            if attr not in saved_papers[paper['title']]:
                continue
            paper[attr] = saved_papers[paper['title']][attr]

    # Split the papers into main and others.
    papers = split_main_and_others(papers)

    with open('./asset/papers.yml', 'w') as f:
        yaml.dump(papers, f, default_flow_style=False)


if __name__ == '__main__':
    main()