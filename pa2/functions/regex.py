import re
import json


def rtv(html):
    title_regex = re.compile(r'<h1>(.*?)</h1>')

    subtitle_regex = re.compile(r'<h2 class="subtitle">(.*?)</h2>')

    lead_regex = re.compile(r'<p class="lead">(.*?)</p>')

    content_regex = re.compile(r'<div class="article-body">(.*?)</div>')

    author_regex = re.compile(r'<p class="author-name">(.*?)</p>')

    # published_time_regex = re.compile(r'<time datetime="(.*?)">')
    # Nevem kako točno dobit published time

    data = {
        'Title': re.search(title_regex, html),
        'Subtitle': re.search(subtitle_regex, html),
        'Lead': re.search(lead_regex, html),
        'Content': re.search(content_regex, html),
        'Author': re.search(author_regex, html),
        # 'PublishedTime': re.search(published_time_regex, html)
    }

    return json.dumps(data, ensure_ascii=False)
