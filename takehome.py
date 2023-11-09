from typing import Optional, List
from datetime import datetime


def fizzbuzz() -> None:
    """Print numbers 1 - 100, inclusive, printing 'Fizz' or 'Buzz'
    or FizzBuzz when divisible by 3, 5, or 3 and 5, respectively"""
    for i in range(1, 101):
        div3 = i % 3
        div5 = i % 5
        if div3 == 0 and div5 == 0:
            print("FizzBuzz")
        elif div3 == 0:
            print("Fizz")
        elif div5 == 0:
            print("Buzz")
        else:
            print(i)


def convert_to_float(input_str: str, default: float) -> float:
    """Return float value from string, otherwise return given default"""
    try:
        return float(input_str)
    except:
        return default


def list_matching_field_value_in_medications(
    data_obj: dict, field: str, value: str, partial_match: Optional[bool] = False
) -> List:
    """Generic function to return list of medications with a value matching
    given field (partial or exact match; exact match by default)"""
    res = []
    medications = data_obj.get("medications")
    if medications is not None:
        for med in medications:
            desired_field = med.get(field)
            if desired_field:
                if isinstance(desired_field, list):
                    for trait in desired_field:
                        if partial_match and value in trait:
                            res.append(med)
                            break  # stop searching this field if medication already identified
                        elif not partial_match and value == trait:
                            res.append(med)
                            break  # stop searching this field if medication already identified
                else:  # default is String
                    if partial_match and value in desired_field:
                        res.append(med)
                    elif not partial_match and value == desired_field:
                        res.append(med)
    return res


def get_antihtn_meds(data_obj: dict) -> List:
    """return list of all medications that have 'antihtn' in 'drugGroup' field"""
    field = "drugGroup"
    value = "antihtn"
    partial_match = False
    return list_matching_field_value_in_medications(
        data_obj, field, value, partial_match
    )


def get_tablet_meds(data_obj: dict) -> List:
    """return list of all medications whose 'doseForm' is any type of 'tablet'"""
    field = "doseForm"
    value = "tablet"
    partial_match = True
    return list_matching_field_value_in_medications(
        data_obj, field, value, partial_match
    )


def get_latest_med_filled(data_obj: dict) -> Optional[dict]:
    """return entire medication data for most recently filled;
    if there is a tie, return one item only, no preference"""
    medications = data_obj.get("medications")
    if not medications:
        return None

    latest_filldate = datetime.min
    latest_med = None
    for med in medications:
        fills = med.get("fills")
        if fills:
            for f in fills:
                fillDate = f.get("fillDate")
                if fillDate:
                    current_med_filldate = datetime.fromisoformat(fillDate)
                    if current_med_filldate > latest_filldate:
                        latest_med = med
    return latest_med


def get_latest_med_ndc(data_obj: dict) -> Optional[str]:
    latest_med = get_latest_med_filled(data_obj)
    if not latest_med:
        return None
    else:
        return latest_med.get("ndc9")


print("Test fizzbuzz")
fizzbuzz()
print()
print("Test convert_to_float")
test_float_1 = convert_to_float("85.0", 0.0)
test_float_2 = convert_to_float("8.5E25", 0.0)
test_float_3 = convert_to_float("kevin", 0.0)
print(f"expected: 85.0,    actual: {test_float_1}")
print(f"expected: 8.5e+25, actual: {test_float_2}")
print(f"expected: 0.0,     actual: {test_float_3}")
print()

sample_data_obj = {
    "etlUpdated": "2012-12-21T23:58:00",
    "id": "123",
    "medications": [
        {
            "ndc9": "39017-0147",
            "brandName": "AMLODIPINE BESYLATE",
            "dosageStrength": "5",
            "dosageUnit": "mg",
            "doseForm": "tablet",
            "drugGroup": ["ccb", "antihtn"],
            "route": "oral",
            "quantity": "90",
            "daysSupply": "90",
            "fills": [
                {"fillDate": "2012-02-18", "daysSupply": "90", "quantity": "90"},
                {"fillDate": "2012-05-16", "daysSupply": "90", "quantity": "90"},
                {"fillDate": "2012-08-06", "daysSupply": "90", "quantity": "90"},
                {"fillDate": "2012-11-01", "daysSupply": "90", "quantity": "90"},
            ],
            "display": "AMLODIPINE BESYLATE 5 MG",
            "unitsPerDay": "1",
            "dosePerDay": "5",
        },
        {
            "ndc9": "60505-2671",
            "brandName": "ATORVASTATIN CALCIUM",
            "genericName": "ATORVASTATIN CALCIUM",
            "dosageStrength": "80",
            "dosageUnit": "mg",
            "doseForm": "tablet, film coated",
            "drugGroup": [
                "statin",
                "azoleddi",
                "antilipid",
                "cms_statin",
                "cms_spc_statin",
            ],
            "route": "oral",
            "quantity": "90",
            "daysSupply": "90",
            "fills": [
                {"fillDate": "2012-04-10", "daysSupply": "90", "quantity": "90"},
                {"fillDate": "2012-07-09", "daysSupply": "90", "quantity": "90"},
                {"fillDate": "2012-10-09", "daysSupply": "90", "quantity": "90"},
                {"fillDate": "2012-01-03", "daysSupply": "90", "quantity": "90"},
                {"fillDate": "2012-04-01", "daysSupply": "90", "quantity": "90"},
            ],
            "unitsPerDay": "1",
            "dosePerDay": "80",
        },
        {
            "ndc9": "68382-0136",
            "brandName": "LOSARTAN POTASSIUM",
            "genericName": "LOSARTAN POTASSIUM",
            "dosageStrength": "50",
            "dosageUnit": "mg",
            "doseForm": "tablet, film coated",
            "drugGroup": ["arb", "antihtn", "cms_rasa"],
            "route": "oral",
            "quantity": "90",
            "daysSupply": "90",
            "fills": [
                {"fillDate": "2012-02-25", "daysSupply": "90", "quantity": "90"},
                {"fillDate": "2012-05-25", "daysSupply": "90", "quantity": "90"},
                {"fillDate": "2012-07-14", "daysSupply": "90", "quantity": "90"},
                {"fillDate": "2012-10-15", "daysSupply": "90", "quantity": "90"},
            ],
            "unitsPerDay": "1",
            "dosePerDay": "50",
        },
        {
            "ndc9": "00378-0018",
            "brandName": "METOPROLOL TARTRATE",
            "genericName": "METOPROLOL TARTRATE",
            "dosageStrength": "25",
            "dosageUnit": "mg",
            "doseForm": "tablet, film coated",
            "drugGroup": ["antihtn", "betablocker"],
            "route": "oral",
            "quantity": "180",
            "daysSupply": "90",
            "fills": [
                {"fillDate": "2012-02-06", "daysSupply": "90", "quantity": "180"},
                {"fillDate": "2012-05-16", "daysSupply": "90", "quantity": "180"},
                {"fillDate": "2012-08-13", "daysSupply": "90", "quantity": "180"},
                {"fillDate": "2012-11-12", "daysSupply": "90", "quantity": "180"},
                {"fillDate": "2012-02-16", "daysSupply": "90", "quantity": "180"},
            ],
            "unitsPerDay": "2",
            "dosePerDay": "50",
        },
    ],
    "resourceType": "cmr",
}
print("Test get_antihtn_meds:")
test_antihtn_1 = get_antihtn_meds(sample_data_obj)
print("3 expected ndc9s: 39017-0147, 68382-0136, 00378-0018")
print(f"{len(test_antihtn_1)} antihtn medications returned:")
for i, t in enumerate(test_antihtn_1):
    ndc9 = t.get("ndc9")
    print(f"antihtn med ndc9 {i+1}: {ndc9}")
print()

print("Test get_tablet_meds:")
test_tablet_1 = get_tablet_meds(sample_data_obj)
print("4 expected ndc9s: 39017-0147, 60505-2671, 68382-0136, 00378-0018")
print(f"{len(test_tablet_1)} tablet medications returned:")
for i, t in enumerate(test_tablet_1):
    ndc9 = t.get("ndc9")
    print(f"tablet med ndc9 {i+1}: {ndc9}")
print()

print("Test get_latest_med_ndc:")
print("expected latest ndc9: 00378-0018")
test_ndc_1 = get_latest_med_ndc(sample_data_obj)
print(f"actual ndc9: {test_ndc_1}")
print()
