import re

LAST_NAME_PREFIXES = {'de', 'da', 'la', 'du', 'del', 'dei', 'vda.', 'dello', 'della', 'degli', 'delle', 'van', 'von',
                      'der', 'den', 'heer', 'ten', 'ter', 'vande', 'vanden', 'vander', 'voor', 'ver', 'aan', 'mc'}
SUFFIX_REGEX = re.compile(r',? +(i{1,3}|iv|vi{0,3}|s(enio)?r|j(unio)?r|phd|apr|rph|pe|md|ma|dmd|cme)$', flags=re.IGNORECASE)
SALUTATION_REGEX = re.compile(r'^(mrs?|m[ia]ster|miss|ms|d(octo)?r|prof|rev|fr|judge|honorable|hon|lord|lady)\.?$',
                              flags=re.IGNORECASE)
INITIAL_REGEX = re.compile(r'^\w\.?$', flags=re.IGNORECASE)
APOSTROPHE_REGEX = re.compile(r'''\w{1}'\w+''', flags=re.IGNORECASE)
LASTNAMES_REGEX = re.compile(r'^(van der|(vda\. )?de la \w+$)', flags=re.IGNORECASE)
SPACES_REGEX = re.compile(r'\s+', flags=re.IGNORECASE)
SPLIT_REGEX = re.compile(r'\s*,\s*', flags=re.IGNORECASE)


def is_last_name_prefix(token):
    return token.lower() in LAST_NAME_PREFIXES


def is_salutation(token):
    return token and SALUTATION_REGEX.match(token)


def is_initial(token):
    # M or W.
    return INITIAL_REGEX.match(token)


def has_apostrophe(token):
    # O'Connor, d'Artagnan match
    # Noda' doesn't match
    return APOSTROPHE_REGEX.match(token)


def adjust_exceptions(first_names, last_names):
    # Adjusting exceptions like
    # "Ludwig Mies van der Rohe"      => ["Ludwig", "Mies van der Rohe"]
    # "Juan Martín de la Cruz Gómez"  => ["Juan Martín", "de la Cruz Gómez"]
    # "Javier Reyes de la Barrera"    => ["Javier", "Reyes de la Barrera"]
    # "Rosa María Pérez Martínez Vda. de la Cruz" => ["Rosa María", "Pérez Martínez Vda. de la Cruz"]
    if len(first_names) > 1 and not is_initial(first_names[len(first_names) - 1]) and LASTNAMES_REGEX.match(
            ' '.join(last_names)):
        while 1:
            last_names.unshift(first_names.pop())
            if len(first_names) <= 2:
                break

    return [first_names, last_names]


def content_or_none(content):
    return content or None


def tokenize_full_name(full_name):
    full_name = full_name.strip()
    full_name = SPACES_REGEX.sub(' ', full_name)
    full_name = SUFFIX_REGEX.sub('', full_name)
    print(full_name)

    if ',' in full_name:
        # ",van helsing" produces  ["", "van helsing"]
        # but it should be [null, "van helsing"] by lib convention
        name_split = SPLIT_REGEX.split(full_name, 2)
        name_split = map(content_or_none, name_split)[::-1]
        return name_split
    else:
        return SPACES_REGEX.split(full_name)


def splitter(full_name):
    tokens = tokenize_full_name(full_name)
    first_names = []
    last_names = []

    while len(tokens):
        token = tokens.pop(0)
        print(token)
        if is_last_name_prefix(token) or has_apostrophe(token) or (len(first_names) > 0 and len(tokens) == 0 and not is_initial(token)):
            last_names.append(token)
            break
        else:
            first_names.append(token)

    last_names = last_names + tokens

    if is_salutation(first_names[0]):
        first_names.pop(0)

    [first_names, last_names] = adjust_exceptions(first_names, last_names)

    return [
        ' '.join(first_names) or None,
        ' '.join(last_names) or None
    ]
