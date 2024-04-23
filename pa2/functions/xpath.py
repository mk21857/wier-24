from lxml import html

def overstock(html_content):

    tree = html.fromstring(html_content)

    title_xpath = "//td[@valign='top']/a/b/text()"
    list_price_xpath = "//s/text()"
    price_xpath = "//span[@class='bigred']/b/text()"
    saving_amount_xpath = "//span[@class='littleorange']/text()[contains(., '$')]"
    saving_percent_xpath = "//span[@class='littleorange']/text()[contains(., '%')]"
    content_xpath = "//span[@class='normal']/text()"

    title = tree.xpath(title_xpath)[0]
    list_price = tree.xpath(list_price_xpath)[0]
    price = tree.xpath(price_xpath)[0]
    saving_amount = tree.xpath(saving_amount_xpath)[0].split()[0] if tree.xpath(saving_amount_xpath) else "" 
    saving_percent = tree.xpath(saving_percent_xpath)[0].strip('()').split()[-1] if tree.xpath(saving_percent_xpath) else "" 
    content = tree.xpath(content_xpath)[0]

    data = {
        'Title': title,
        'ListPrice': list_price,
        'Price': price,
        'Saving': saving_amount,
        'SavingPercent': saving_percent,
        'Content': content,
    }

    return data


def rtv(html_content):
    tree = html.fromstring(html_content)

    title_xpath = "//h1/text()"
    subtitle_xpath = "//div[@class='subtitle']/text()"
    lead_xpath = "//p[@class='lead']/text()"
    content_xpath = "//div[@class='article-body']//text()"
    author_xpath = "//div[@class='author-name']/text()"
    published_time_xpath = "//div[@class='publish-meta']/text()"

    title = tree.xpath(title_xpath)[0]
    subtitle = tree.xpath(subtitle_xpath)[0]
    lead = tree.xpath(lead_xpath)[0]
    content = ' '.join(tree.xpath(content_xpath))
    author = tree.xpath(author_xpath)[0]
    published_time = tree.xpath(published_time_xpath)[0]

    data = {
        'Title': title,
        'Subtitle': subtitle,
        'Lead': lead,
        'Content': content,
        'Author': author,
        'PublishedTime': published_time
    }

    return data


def sport_tv(html_content):
    tree = html.fromstring(html_content)

    title_xpath = "//h1[@class='title']/text()"
    lead_xpath = "//h2[@class='main-caption mb-30']/text()"
    author_xpath = "//p[@class='avtor']/strong/text()"
    published_date_xpath = "//div[@class='post-date pull-left']/span/text()"
    content_xpath = "//div[@class='clearfix']/following-sibling::p/text()"

    title = tree.xpath(title_xpath)[0]
    lead = tree.xpath(lead_xpath)[0]
    author = tree.xpath(author_xpath)[0]
    published_date = tree.xpath(published_date_xpath)[0]
    content = ' '.join(tree.xpath(content_xpath))

    data = {
        'Title': title,
        'Lead': lead,
        'Content': content,
        'Author': author,
        'PublishedDate': published_date
    }

    return data


def bolha(html_content):
    tree = html.fromstring(html_content)

    title_xpath = "//h3[@class='entity-title']/a/text()"
    price_xpath = "//strong[@class='price price--hrk']/text()"
    time_xpath = "//time/text()"
    location_xpath = "//span[contains(text(),'Lokacija vozila')]/following-sibling::text()[1]"
    state_xpath = "//div[@class='entity-description-main']/text()"
    year_xpath= "//text()[contains(., 'Leto izdelave: ')]/following-sibling::text()[1]"

    title = tree.xpath(title_xpath)[0].strip()
    price = tree.xpath(price_xpath)[0].strip()
    time = tree.xpath(time_xpath)[0].strip()
    location = tree.xpath(location_xpath)[0].strip()
    state = tree.xpath(state_xpath)[0].strip()
    year = tree.xpath(year_xpath)[0].strip()

    data = {
        'Title': title,
        'Price': price,
        'Time': time,
        'VehicleLocation': location,
        'VehicleState': state,
        'Year': year,
    }

    return data
