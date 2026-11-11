import math


def _is_finite_number(value):
    return isinstance(value, float) and math.isfinite(value)


def parse_zone(text):
    """Parse 'name:area' into (Name, area_float).

    Returns None if the input is invalid (not a string, wrong format,
    empty name, or area that is not a finite, non-negative number).
    """
    if not isinstance(text, str):
        return None
    parts = text.split(':')
    if len(parts) != 2:
        return None
    name, area_text = parts[0].strip(), parts[1].strip()
    if not name or not area_text:
        return None
    try:
        area = float(area_text)
    except (ValueError, OverflowError):
        return None
    if not _is_finite_number(area) or area < 0:
        return None
    return name.title(), area


def moisture_average(readings_csv):
    """Return the integer average of comma-separated moisture readings.

    Returns None if the input is invalid (not a string, empty, non-integer
    elements, empty elements, or readings outside 0-100).
    """
    if not isinstance(readings_csv, str):
        return None
    items = readings_csv.split(',')
    values = []
    for item in items:
        try:
            value = int(item.strip())
        except (ValueError, OverflowError):
            return None
        if value < 0 or value > 100:
            return None
        values.append(value)
    if not values:
        return None
    return sum(values) // len(values)


def water_needed(text):
    """Return water needed for 'area|rainfall' (area*5 - rainfall, min 0).

    Returns None if the input is invalid (not a string, wrong format,
    non-numeric, non-finite or negative values).
    """
    if not isinstance(text, str):
        return None
    parts = text.split('|')
    if len(parts) != 2:
        return None
    try:
        plot = float(parts[0].strip())
        rain = float(parts[1].strip())
    except (ValueError, OverflowError):
        return None
    if not (_is_finite_number(plot) and _is_finite_number(rain)):
        return None
    if plot < 0 or rain < 0:
        return None
    need = plot * 5 - rain
    if not math.isfinite(need):
        return None
    return max(need, 0)


def main():
    print("==== Running parse_zone ====")
    user_input = input("Enter zone:area in m2 (e.g. north:120): ")
    result = parse_zone(user_input)
    print("Zone and Area:", result if result is not None else "Invalid input")

    print("\n==== Running moisture_average ====")
    user_input = input("Enter moisture readings as CSV (e.g. 40,35,50): ")
    result = moisture_average(user_input)
    print("Average Moisture:", result if result is not None else "Invalid input")

    print("\n==== Running water_needed ====")
    user_input = input("Enter area|rainfall (e.g. 120|8): ")
    result = water_needed(user_input)
    print("Water Needed:", result if result is not None else "Invalid input")


if __name__ == "__main__":
    main()
