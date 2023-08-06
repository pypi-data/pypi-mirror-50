from __future__ import absolute_import, division, print_function, unicode_literals

import re
from datetime import datetime
from hashlib import sha256
from pycountry import countries
from . import fb_normalize_and_hash_constants


def _normalizeYear(input):
    result = None
    if input is not None:
        if looksLikeHashed(input):
            result = input
        else:
            if input.isdigit():
                if len(input) == 4:
                    result = input
                elif len(input) == 2:
                    result = datetime.strptime(input, "%y").strftime("%Y")
    return result


def _normalizeMonth(input):
    result = None
    if input is not None:
        if looksLikeHashed(input):
            result = input
        else:
            input = str(input)
            if input.isdigit():
                if 0 < int(input) <= 12:
                    result = input.zfill(2)
            elif input.isalpha():
                if len(input) == 3:
                    try:
                        result = datetime.strptime(input, "%b").strftime("%m")
                    except Exception:
                        pass
                elif len(input) >= 3:
                    try:
                        result = datetime.strptime(input, "%B").strftime("%m")
                    except Exception:
                        pass
    return result


def _normalizeDay(input):
    result = None
    if input is not None:
        if looksLikeHashed(input):
            result = input
        else:
            input = str(input)
            if input.isdigit():
                if 0 < int(input) <= 31:
                    result = input.zfill(2)
    return result


def _normalizeEmail(input):
    def isEmail(input):
        return re.search(fb_normalize_and_hash_constants.EMAIL_RE, input)

    result = None
    if input is not None:
        if looksLikeHashed(input):
            result = input
        elif isinstance(input, str):
            cleanedUp = input.strip().lower()
            result = cleanedUp if isEmail(cleanedUp) else None
    return result


def _normalizePhoneNumber(input):
    def isInternationalPhoneNumber(input):
        trimmedNumber = re.sub(
            fb_normalize_and_hash_constants.PHONE_TRIM_HYPHEN_WHITESPACE, "", input
        )
        trimmedNunber = re.sub(
            fb_normalize_and_hash_constants.PHONE_TRIM_LEADING_PLUS, "", trimmedNumber
        )

        if trimmedNunber[0] == "0":
            return False
        if trimmedNumber[0] == "1":
            return re.search(
                fb_normalize_and_hash_constants.US_NUMBER_RE, trimmedNumber
            )
        if trimmedNumber[:2] == "47":
            return re.search(
                fb_normalize_and_hash_constants.NORWAY_NUMBER_RE, trimmedNumber
            )
        return re.search(fb_normalize_and_hash_constants.INTL_NUMBER_RE, trimmedNumber)

    result = None
    if input is not None:
        if looksLikeHashed(input):
            result = input
        else:
            stringifiedInput = str(input)
            stringifiedInput = re.sub(
                fb_normalize_and_hash_constants.PHONE_IGNORE_CHAR_SET,
                "",
                stringifiedInput,
            )
            stringifiedInput = re.sub(
                fb_normalize_and_hash_constants.PHONE_DROP_PREFIX_ZEROS,
                "",
                stringifiedInput,
            )
            if isInternationalPhoneNumber(stringifiedInput):
                result = stringifiedInput
    return result


def _normalizeGender(input):
    GENDER_ENUM = ["m", "f"]
    result = None
    if input is not None:
        if looksLikeHashed(input):
            result = input
        elif input.strip().lower() in GENDER_ENUM:
            result = input.strip().lower()
    return result


def _normalizeString(input, params):
    result = None
    if input is not None:
        if looksLikeHashed(input) and isinstance(input, str):
            if not params.get("rejectHashed"):
                result = input
        else:
            stringifiedInput = str(input)
            if params.get("strip") is not None:
                stringifiedInput = stringifiedInput.replace(params["strip"], "")
            if params.get("lowercase"):
                stringifiedInput = stringifiedInput.lower()
            elif params.get("uppercase"):
                stringifiedInput = stringifiedInput.upper()

            if params.get("truncate") is not None and params.get("truncate") != 0:
                stringifiedInput = stringifiedInput[: params["truncate"]]
            if params.get("test") is not None and params.get("test") != "":
                if re.search(params["test"], stringifiedInput):
                    result = stringifiedInput
            else:
                result = stringifiedInput
    return result


def _normalizeName(input, typeParams=None):
    NAME_PARAMS = {
        "lowercase": True,
        "rejectHashed": False,
        "strip": " ",
        "test": None,
        "truncate": None,
        "uppercase": False,
    }
    if typeParams is not None:
        NAME_PARAMS = typeParams
    return _normalizeString(input, NAME_PARAMS)


def _normalizeInitial(input, typeParams=None):
    INITIAL_PARAMS = {
        "lowercase": True,
        "rejectHashed": False,
        "strip": " ",
        "test": None,
        "truncate": 1,
        "uppercase": False,
    }
    if typeParams is not None:
        INITIAL_PARAMS = typeParams
    return _normalizeString(input, INITIAL_PARAMS)


def _normalizeState(input):
    result = None
    if input is not None and isinstance(input, str):
        if looksLikeHashed(input):
            result = input
        else:
            maybeState = input.lower().strip()
            if maybeState in fb_normalize_and_hash_constants.us_state_abbrev.values():
                result = maybeState
            elif maybeState in fb_normalize_and_hash_constants.us_state_abbrev:
                result = fb_normalize_and_hash_constants.us_state_abbrev[maybeState]
    return result


def _normalizeCity(input, typeParams=None):
    CITY_PARAMS = {
        "lowercase": True,
        "rejectHashed": False,
        "strip": " ",
        "test": r"^[a-z]+",
        "truncate": None,
        "uppercase": False,
    }
    if typeParams is not None:
        CITY_PARAMS = typeParams
    return _normalizeString(input, CITY_PARAMS)


def _normalizePostalCode(input):
    result = None

    if input is not None and isinstance(input, str):
        if looksLikeHashed(input):
            result = input
        else:
            maybeZIP = str(input).strip().lower().split("-", 1)[0]
            if len(maybeZIP) >= 2:
                result = maybeZIP
    return result


def _normalizeCountry(input):
    result = None
    if input is not None:
        if looksLikeHashed(input):
            result = input
        else:
            input = input.strip()
            if len(input) == 2:
                result = input.lower()
            else:
                try:
                    result = countries.get(name=input).alpha_2.lower()
                except Exception:
                    pass
    return result


def _normalizeMobileAdvertiserID(input):
    result = None
    if input is not None and isinstance(input, str):
        if looksLikeHashed(input):
            result = input
        else:
            input = input.strip().lower()
            if re.search(fb_normalize_and_hash_constants.MOBILE_ADV_TEST, input):
                result = input
    return result


def normalize(input, key, typeParams=None):
    key_switcher = {
        "EMAIL": _normalizeEmail,
        "PHONE": _normalizePhoneNumber,
        "GEN": _normalizeGender,
        "DOBY": _normalizeYear,
        "DOBM": _normalizeMonth,
        "DOBD": _normalizeDay,
        "LN": _normalizeName,
        "FN": _normalizeName,
        "FI": _normalizeInitial,
        "ST": _normalizeState,
        "CT": _normalizeCity,
        "ZIP": _normalizePostalCode,
        "COUNTRY": _normalizeCountry,
        "MADID": _normalizeMobileAdvertiserID,
    }
    if key in ["LN", "FN", "FI", "CT"]:
        return key_switcher[key](input, typeParams)
    return key_switcher[key](input)


def looksLikeHashed(input):
    return re.search("^[a-f0-9]{64}$", input)


def hash(o):
    return sha256(str(o)).hexdigest()
