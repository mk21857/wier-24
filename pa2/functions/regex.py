import re


def overstock(html):
    title_regex = re.compile(r'</table></td><td valign="top"> \n<a href=[^>]*><b>(.*?)<\/b><\/a>')

    list_price_regex = re.compile(r'<s>(.*?)</s>')

    price_regex = re.compile(r'<span class="bigred"><b>(.*?)</b>')

    saving_regex = re.compile(r'<span class="littleorange">(\$[\d,]+\.\d{2}) \(\d{1,3}%\)<\/span>')

    saving_percent_regex = re.compile(r'<span class="littleorange">(?:.*?\$[\d,]+\.\d{2} )\((\d{1,3}%)\)<\/span>')

    content_regex = re.compile(r'<span class="normal">([^<]*)<br>')

    data = {
        'Title': re.findall(title_regex, html)[0],
        'ListPrice': re.findall(list_price_regex, html)[0],
        'Price': re.findall(price_regex, html)[0],
        'Saving': re.findall(saving_regex, html)[0],
        'SavingPercent': re.findall(saving_percent_regex, html)[0],
        'Content': re.findall(content_regex, html)[0],
    }

    return data


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


def sport_tv(html):
    title_regex = re.compile(r'<h1 class="title">(.*?)</h1>')

    lead_regex = re.compile(r'<h2 class="main-caption mb-30">\n(.*?)</h2>')

    author_regex = re.compile(r'<p class="avtor"><strong>Avtor: (.*?)</strong>')

    published_date_regex = re.compile(r'<div class="post-date pull-left">\s*<span>(.*?)<\/span>')

    content_regex = re.compile(
        r'</div>\s*<div class="clearfix"></div>\s*<p>(.*?)<br>',
        re.DOTALL)

    data = {
        'Title': re.findall(title_regex, html)[0],
        'Lead': re.findall(lead_regex, html)[0],
        'Content': re.findall(content_regex, html)[0],
        'Author': re.findall(author_regex, html)[0],
        'PublishedDate': re.findall(published_date_regex, html)[0]
    }

    return data


def bolha(html):
    title_regex = re.compile(r'<h3 class="entity-title"><a .*?href="\/avto-oglasi\/.*?>(.*?)<\/a><\/h3>')

    price_regex = re.compile(r'<strong class="price price--hrk">\s*([\d.]+)\s*&nbsp;')

    time_regex = re.compile(r'<time[^>]*>(.*?)</time>')

    location_regex = re.compile(r'<span[^>]*>Lokacija vozila: <\/span>(.*?)<br>')

    state_regex = re.compile(r'<div class="entity-description-main">\s*(.*?)<br>')

    year_regex = re.compile(r'Leto izdelave:\s*(\d{4})')

    data = {
        'Title': re.findall(title_regex, html)[0],
        'Price': re.findall(price_regex, html)[0],
        'Time': re.findall(time_regex, html)[0],
        'VehicleLocation': re.findall(location_regex, html)[0],
        'VehicleState': re.findall(state_regex, html)[0],
        'Year': re.findall(year_regex, html)[0],
    }

    return data