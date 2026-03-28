import os
import random
import re
import sys

DAMPING = 0.85
SAMPLES = 10000


def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: python pagerank.py corpus")
    corpus = crawl(sys.argv[1])
    ranks = sample_pagerank(corpus, DAMPING, SAMPLES)
    print(f"PageRank Results from Sampling (n = {SAMPLES})")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")
    ranks = iterate_pagerank(corpus, DAMPING)
    print(f"PageRank Results from Iteration")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")
        


def crawl(directory):
    """
    Parse a directory of HTML pages and check for links to other pages.
    Return a dictionary where each key is a page, and values are
    a list of all other pages in the corpus that are linked to by the page.
    """
    pages = dict()

    # Extract all links from HTML files
    for filename in os.listdir(directory):
        if not filename.endswith(".html"):
            continue
        with open(os.path.join(directory, filename)) as f:
            contents = f.read()
            links = re.findall(r"<a\s+(?:[^>]*?)href=\"([^\"]*)\"", contents)
            pages[filename] = set(links) - {filename}

    # Only include links to other pages in the corpus
    for filename in pages:
        pages[filename] = set(
            link for link in pages[filename]
            if link in pages
        )

    return pages


def transition_model(corpus, page, damping_factor):
    """
    Return a probability distribution over which page to visit next,
    given a current page.

    With probability `damping_factor`, choose a link at random
    linked to by `page`. With probability `1 - damping_factor`, choose
    a link at random chosen from all pages in the corpus.
    """
    
    page_links = corpus[page]
    pages = corpus.keys()
    if page_links:

        # probability of every page with damping
        prob_every_page = (1 - damping_factor)/len(corpus)
        
        model = { p : prob_every_page for p in pages}
        
        # probability of linked pages
        
        prob_links = damping_factor/len(page_links)

        for linked_page in page_links:
            model[linked_page] += prob_links
    
        return model
    
    prob_every_page = 1/len(corpus)
    return { page : prob_every_page for page in pages}
    


def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """

    pages = corpus.keys()
    page = random.choice(list(pages))
    samples = {p : 0 for p in pages}
    samples[page] += 1

    # go through samples
    for _ in range(n-1):
        
        transitions = transition_model(corpus, page, damping_factor)
        page = random.choices(list(transitions.keys()), transitions.values())[0]
        samples[page] += 1

    # get ranking
    return { page : count/n for page, count in samples.items()}
    

def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    epsilon = 0.001
    pages = corpus.keys()
    n = len(pages)
    pagerank = {page : 1/n for page in pages }
    changed = True

    while changed:

        changed = False
        new_ranks = {}
        for page in pages:
            # calculate new rank
            term1 = ((1 - damping_factor) / n)
            term2 =  damping_factor * sum(
                 (pagerank[p]) / (len(corpus[p]) if corpus[p] else n) 
                 for p in pages if page in corpus[p] )
    

            new_rank = term1 + term2
            new_ranks[page] = new_rank

            # check for minimum change
            delta = abs(new_rank - pagerank[page])
            if delta > epsilon:
                changed = True
            

        pagerank = new_ranks
    return pagerank



if __name__ == "__main__":
    main()
    #corpus = {"1.html": {"2.html", "3.html"}, "2.html": {"3.html"}, "3.html": {'2.html'}}
    #rank = sample_pagerank(corpus, 0.85, 1000 )
    #print(rank, sum(list(rank.values())))

