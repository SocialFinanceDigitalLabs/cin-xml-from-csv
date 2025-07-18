from pathlib import Path
import pandas as pd
from lxml.etree import Element, SubElement, ElementTree

# Utility Functions
def make_element_from_row(parent, tag, row, exclude_cols=None):
    el = SubElement(parent, tag)
    for col in row.index:
        if exclude_cols and col in exclude_cols:
            continue
        val = row[col]
        if pd.notna(val):
            SubElement(el, col).text = str(val)
    return el

def generate_xml(INPUT_DIR, OUTPUT_FILE):

    # Load CSVs
    INPUT_DIR = Path(INPUT_DIR)
    child_ids = pd.read_csv(INPUT_DIR / "ChildIdentifiers.csv")
    characteristics = pd.read_csv(INPUT_DIR / "ChildCharacteristics.csv")
    disabilities = pd.read_csv(INPUT_DIR / "Disabilities.csv")
    cins = pd.read_csv(INPUT_DIR / "CINdetails.csv")
    assess = pd.read_csv(INPUT_DIR / "Assessments.csv")
    factors = pd.read_csv(INPUT_DIR / "Factors.csv")
    plans = pd.read_csv(INPUT_DIR / "CINPlanDates.csv")
    s47 = pd.read_csv(INPUT_DIR / "Section47.csv")
    cpp = pd.read_csv(INPUT_DIR / "ChildProtectionPlans.csv")
    reviews = pd.read_csv(INPUT_DIR / "Reviews.csv")

    root = Element("CINdetailsCollection")

    for child_id in child_ids["LAchildID"].unique():
        child_el = SubElement(root, "Child")

        # Add identifiers
        id_row = child_ids[child_ids["LAchildID"] == child_id].iloc[0]
        make_element_from_row(child_el, "ChildIdentifiers", id_row)

        # Characteristics
        char_rows = characteristics[characteristics["LAchildID"] == child_id]
        for _, row in char_rows.iterrows():
            char_el = make_element_from_row(child_el, "ChildCharacteristics", row, exclude_cols=["LAchildID"])
            
            # Disabilities (nested inside ChildCharacteristics)
            disab_rows = disabilities[disabilities["LAchildID"] == child_id]
            if not disab_rows.empty:
                disabs_el = SubElement(char_el, "Disabilities")
                for _, d_row in disab_rows.iterrows():
                    if pd.notna(d_row["Disability"]):
                        SubElement(disabs_el, "Disability").text = str(d_row["Disability"])

        # CINdetails
        cin_rows = cins[cins["LAchildID"] == child_id]
        for _, cin_row in cin_rows.iterrows():
            cin_el = make_element_from_row(child_el, "CINdetails", cin_row, exclude_cols=["LAchildID"])

            # Nested: Assessments
            assess_rows = assess[
                (assess["LAchildID"] == child_id) &
                (assess["CINreferralDate"] == cin_row["CINreferralDate"])
                ]
            for _, a_row in assess_rows.iterrows():
                assess_el = make_element_from_row(cin_el, "Assessments", a_row, exclude_cols=["LAchildID", "CINreferralDate"])

                # Factors (nested inside Assessments)
                f_rows = factors[
                    (factors["LAchildID"] == child_id) &
                    (factors["CINreferralDate"] == cin_row["CINreferralDate"]) &
                    (factors["AssessmentActualStartDate"] == a_row["AssessmentActualStartDate"])
                    ]

                if not f_rows.empty:
                    factors_el = SubElement(assess_el, "FactorsIdentifiedAtAssessment")
                    for _, f_row in f_rows.iterrows():
                        if pd.notna(f_row["Factor"]):
                            SubElement(factors_el, "AssessmentFactors").text = str(f_row["Factor"])

            # Nested: CIN Plan Dates
            plan_rows = plans[
                (plans["LAchildID"] == child_id) &
                (plans["CINreferralDate"] == cin_row["CINreferralDate"])
                ]
            for _, p_row in plan_rows.iterrows():
                make_element_from_row(cin_el, "CINPlanDates", p_row, exclude_cols=["LAchildID", "CINreferralDate"])

            # Nested: Section 47
            s47_rows = s47[
                (s47["LAchildID"] == child_id) &
                (s47["CINreferralDate"] == cin_row["CINreferralDate"])
                ]
            for _, s_row in s47_rows.iterrows():
                make_element_from_row(cin_el, "Section47", s_row, exclude_cols=["LAchildID", "CINreferralDate"])

            # Nested: Child Protection Plans
            cpp_rows = cpp[
                (cpp["LAchildID"] == child_id) &
                (cpp["CINreferralDate"] == cin_row["CINreferralDate"])
                ]
            for _, cpp_row in cpp_rows.iterrows():
                cpp_el = make_element_from_row(cin_el, "ChildProtectionPlans", cpp_row, exclude_cols=["LAchildID", "CINreferralDate"])

                # Reviews (nested inside Child Protection Plans)
                rev_rows = reviews[
                    (reviews["LAchildID"] == child_id) &
                    (reviews["CINreferralDate"] == cin_row["CINreferralDate"]) &
                    (reviews["CPPstartDate"] == cpp_row["CPPstartDate"])
                ]
 
                if not rev_rows.empty:
                    rev_el = SubElement(cpp_el, "Reviews")
                    for _, rev_row in rev_rows.iterrows():
                        if pd.notna(rev_row["CPPreviewDate"]):
                            SubElement(rev_el, "CPPreviewDate").text = str(rev_row["CPPreviewDate"])

    tree = ElementTree(root)
    OUTPUT_FILE = Path(OUTPUT_FILE)
    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    tree.write(str(OUTPUT_FILE), pretty_print=True, xml_declaration=True, encoding="utf-8")
    print(f"XML generated at {OUTPUT_FILE}")

    pass