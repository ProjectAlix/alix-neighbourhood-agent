from bs4 import BeautifulSoup

def get_clean_html(html_str:str):
    soup=BeautifulSoup(html_str, "html.parser")
    for tag in soup.find_all():
        tag.attrs = {k: v for k, v in tag.attrs.items() if k == "href"}