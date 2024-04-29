from bs4 import BeautifulSoup

""" Token types """
PCDATA = "PCDATA"
TAG = "TAG"
STRING = "STRING"

def get_tag_type(token):
    if '<' in token and '>' in token:
        return "TAG"
    return "STRING"

def is_tag_mismatched(type1, type2, token1, token2):
    if (type1 == TAG and type2 == STRING) or (type1 == STRING and type2 == TAG):
        return True
    if type1 == TAG and type2 == TAG and token1 != token2:
        return True
    return False

def get_closing_tag(i, tokens):
    for i in reversed(range(i)):
        if tokens[i].startswith("</"):
            return tokens[i]

def find_tag(i, tokens, last_tag):
    for token in range(i, len(tokens)):
        if tokens[token] == last_tag:
            return token

def parse_html(html):
    parsed = BeautifulSoup(html, 'html.parser')
    for tag in parsed.recursiveChildGenerator():
        if hasattr(tag, 'attrs'):
            tag.attrs = None
    return parsed

def tokenize_html(html):
    parsed = parse_html(html)
    tokens = parsed.body.prettify().split("\n")
    tokens = [token.strip() for token in tokens]
    return tokens

def road_runner(html1, html2):
    # This call parses and tokenizes the HTML
    tokens1 = tokenize_html(html1)
    tokens2 = tokenize_html(html2)

    # Define variables
    index_1 = 0
    index_2 = 0

    repeating_sections = []
    optional_sections = []
    wrapper = []

    # Start looping through the tokens
    while index_1 < len(tokens1) and index_2 < len(tokens2):
        type1 = get_tag_type(tokens1[index_1])
        type2 = get_tag_type(tokens2[index_2])

        # Check if we have a PCDATA mismatch
        if type1 == STRING and type2 == STRING:
            if len(tokens1[index_1]) > 0:
                tokens1[index_1] = PCDATA
            if len(tokens2[index_2]) > 0:
                tokens2[index_2] = PCDATA

        if is_tag_mismatched(type1, type2, tokens1[index_1], tokens2[index_2]):  # we have a tag mismatch
            last_tag1 = get_closing_tag(index_1, tokens1)
            last_tag2 = get_closing_tag(index_2, tokens2)

            if last_tag1 == last_tag2:
                found_tag_on_line1 = find_tag(index_1, tokens1, last_tag1)
                found_tag_on_line2 = find_tag(index_2, tokens2, last_tag1)

                if found_tag_on_line1 and not found_tag_on_line2:  # check if tag is repeated in tokens1 and not in tokens2
                    last_line_index1 = found_tag_on_line1
                    prev_index_1 = index_1 - 1

                    is_repeating = True
                    for bi in reversed(range(index_1, last_line_index1 + 1)):
                        if tokens1[prev_index_1] == PCDATA:
                            tokens1[bi] = PCDATA
                        elif tokens1[bi] != tokens1[prev_index_1]:
                            is_repeating = False
                        prev_index_1 -= 1

                    if is_repeating:
                        section = tokens1[index_1:last_line_index1 + 1]
                        repeating_sections.append(section)
                        if section not in wrapper:
                            wrapper.append(section)

                if not found_tag_on_line1 and found_tag_on_line2:
                    last_line_index2 = found_tag_on_line2
                    prev_index_2 = index_2 - 1

                    is_repeating = True
                    for bi in reversed(range(index_2, last_line_index2 + 1)):
                        if tokens2[prev_index_2] == PCDATA:
                            tokens2[bi] = PCDATA
                        elif tokens2[bi] != tokens2[prev_index_2]:
                            is_repeating = False
                        prev_index_2 -= 1

                    if is_repeating:
                        section = tokens1[index_2:last_line_index2 + 1]
                        repeating_sections.append(section)
                        if section not in wrapper:
                            wrapper.append(section)

            else:  # check if section is optional
                found_tag_on_line1 = find_tag(index_1, tokens1, last_tag1)
                found_tag_on_line2 = find_tag(index_2, tokens2, last_tag1)

                # no repeating sequence between the two, find optional tags
                if found_tag_on_line1 and found_tag_on_line2 and found_tag_on_line1 is not None and found_tag_on_line2 is not None:
                    if tokens1[index_1].startswith("</"):
                        optional_section = tokens2[index_2:found_tag_on_line2 + 1]
                        if optional_section not in optional_sections:
                            optional_sections.append(optional_section)
                        optional_sections.append(optional_section)
                        i = 0
                        for x in range(index_1, index_1 + len(optional_section)):
                            tokens1.insert(x, optional_section[i])
                            i += 1

                        index_1 = found_tag_on_line1 + 1
                        index_2 = found_tag_on_line2 + 1

                    if tokens2[index_2].startswith("</"):
                        optional_section = tokens1[index_1:found_tag_on_line1 + 1]
                        if optional_section not in optional_sections:
                            optional_sections.append(optional_section)
                        index_1 = found_tag_on_line2 + 1

                    # gledamo za dodatne elemente
                    if found_tag_on_line1 and not found_tag_on_line2:
                        optional_sections.append(tokens1[index_1:found_tag_on_line1])
                        index_1 = found_tag_on_line1 + 1

                    if not found_tag_on_line1 and found_tag_on_line2:
                        optional_section = tokens2[index_2:found_tag_on_line2 + 1]
                        optional_sections.append(optional_section)
                        i = 0
                        for x in range(index_1, index_1 + len(optional_section)):
                            tokens1.insert(x, optional_section[i])
                            i += 1
                        index_2 = found_tag_on_line2 + 1

        index_1 += 1
        index_2 += 1

    regex = "".join(tokens1)
    for sr in repeating_sections:
        sr_string = "".join(sr)
        first_oc = regex.find(sr_string)
        regex = regex.replace(sr_string, "")
        regex = regex[:first_oc] + "(" + sr_string + ")+" + regex[first_oc:]

    for so in optional_sections:
        so_string = "".join(so)
        first_oc = regex.find(so_string)
        regex = regex.replace(so_string, "")
        regex = regex[:first_oc] + "(" + so_string + ")?" + regex[first_oc:]

    return regex
