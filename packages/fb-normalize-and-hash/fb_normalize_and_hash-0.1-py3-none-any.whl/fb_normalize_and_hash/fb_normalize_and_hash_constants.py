from __future__ import absolute_import, division, print_function, unicode_literals


EMAIL_RE = r"^[\w!#\$%&'\*\+\/\=\?\^`\{\|\}~\-]+(:?\.[\w!#\$%&'\*\+\/\=\?\^`\{\|\}~\-]+)*@(?:[a-z0-9](?:[a-z0-9\-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9\-]*[a-z0-9])?$"
US_NUMBER_RE = r"^1\(?\d{3}\)?\d{7}$"
NORWAY_NUMBER_RE = r"^47\d{8}$"
INTL_NUMBER_RE = r"^\d{1,4}\(?\d{2,3}\)?\d{4,}$"
PHONE_TRIM_HYPHEN_WHITESPACE = r"[\-\s]+"
PHONE_TRIM_LEADING_PLUS = r"^\+?0{0,2}"
PHONE_DROP_PREFIX_ZEROS = r"^0*"
PHONE_IGNORE_CHAR_SET = r"[\-@#<>'\",; ]|\(|\)|\+|[a-z]"
LOOKS_LIKED_SHA256_HASHED = r"^[a-f0-9]{64}$"
us_state_abbrev = {
    "alabama": "al",
    "alaska": "ak",
    "arizona": "az",
    "arkansas": "ar",
    "california": "ca",
    "colorado": "co",
    "connecticut": "ct",
    "delaware": "de",
    "district of columbia": "dc",
    "florida": "fl",
    "georgia": "ga",
    "hawaii": "hi",
    "idaho": "id",
    "illinois": "il",
    "indiana": "in",
    "iowa": "ia",
    "kansas": "ks",
    "kentucky": "ky",
    "louisiana": "la",
    "maine": "me",
    "maryland": "md",
    "massachusetts": "ma",
    "michigan": "mi",
    "minnesota": "mn",
    "mississippi": "ms",
    "missouri": "mo",
    "montana": "mt",
    "nebraska": "ne",
    "nevada": "nv",
    "new hampshire": "nh",
    "new jersey": "nj",
    "new mexico": "nm",
    "new york": "ny",
    "north carolina": "nc",
    "north dakota": "nd",
    "northern mariana islands": "mp",
    "ohio": "oh",
    "oklahoma": "ok",
    "oregon": "or",
    "palau": "pw",
    "pennsylvania": "pa",
    "puerto rico": "pr",
    "rhode island": "ri",
    "south carolina": "sc",
    "south dakota": "sd",
    "tennessee": "tn",
    "texas": "tx",
    "utah": "ut",
    "vermont": "vt",
    "virgin islands": "vi",
    "virginia": "va",
    "washington": "wa",
    "west virginia": "wv",
    "wisconsin": "wi",
    "wyoming": "wy",
}
