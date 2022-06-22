from datetime import datetime, timezone


def convert_datetime_to_iso_8601_with_z_suffix_and_utc(dt: datetime) -> str:
    # dt = dt.astimezone(tz=timezone.utc)
    return dt.strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z'
