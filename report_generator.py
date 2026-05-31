import json


def save_report(report_data, filename):

    with open(filename, "w") as file:
        json.dump(report_data, file, indent=4)