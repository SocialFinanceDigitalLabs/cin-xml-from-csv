from datetime import datetime

from generate_csvs import csv_generator
from generate_xml import generate_xml

if __name__ == "__main__":
    # Simple manual toggle for now:
    mode = "xml"  # change to "xml" to run generate_xml()

    if mode == "csv":
        start_date = datetime(2019, 4, 1)
        csv_generator(
            n_children = 500,
            seed = 42,
            start_date = start_date,
            percent_with_upn = 0.8,
            percent_with_low_char = 0.1,
            percent_with_disabilities = 0.4,
            percent_with_multiple_cin = 0.3,
            percent_nfa = 0.1,
            percent_closed = 0.4,
            percent_with_assessments = 0.7,
            percent_with_factors = 0.6,
            percent_with_plans = 0.8,
            percent_with_s47 = 0.5,
            percent_with_cpp = 0.4,
            percent_with_reviews = 0.5
        )
             
    elif mode == "xml":
        generate_xml(
            INPUT_DIR="csvs",
            OUTPUT_FILE="generated/CIN_output.xml"
        )