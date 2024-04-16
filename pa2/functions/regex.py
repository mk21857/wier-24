import re


def rtv(html):
    title_regex = re.compile(r'<h1>(.*?)</h1>')

    subtitle_regex = re.compile(r'<div class="subtitle">(.*?)</div>')

    lead_regex = re.compile(r'<p class="lead">(.*?)</p>')

    content_regex = re.compile(
        r'<div *?class="article-body">(.*?)<div class="gallery">',
        re.DOTALL)
    # to je ful grd način ma neznam drugače

    author_regex = re.compile(r'<div class="author-name">(.*?)</div>')

    published_time_regex = re.compile(r'<div class="publish-meta">\n\t\t(.*?)<br>')

    data = {
        'Title': re.findall(title_regex, html)[0],
        'Subtitle': re.findall(subtitle_regex, html)[0],
        'Lead': re.findall(lead_regex, html)[0],
        'Content': re.findall(content_regex, html)[0],
        'Author': re.findall(author_regex, html)[0],
        'PublishedTime': re.findall(published_time_regex, html)[0]
    }

    return data
