import re


def is_all_objects_ids_unique(item_list):
    if len(item_list) == set(list(map(lambda x: x.get('id'), item_list))):
        raise ValueError("All object ids in list must be unique")


def is_datetime_string_iso8601(datetime_string):
    if not isinstance(datetime_string, str):
        raise ValueError("datetime must be str")
    regex_datetime_iso = r"^\d{4}-(0\d|1[0-2])-([0-2]\d|3[0-2])(T(([01]\d|2[0-4]):([0-5]\d)(:[0-5]\d([\.,]\d+)?)?" \
                         r"|([01]\d|2[0-4])(:[0-5]\d([\.,]\d+)?)?|([01]\d|2[0-4])([\.,]\d+)?))?([+-]\d\d(:[0-5]\d)?|Z)?$"

    if re.match(regex_datetime_iso, datetime_string):
        return datetime_string
    else:
        raise ValueError("datetime must be iso8601 format")
