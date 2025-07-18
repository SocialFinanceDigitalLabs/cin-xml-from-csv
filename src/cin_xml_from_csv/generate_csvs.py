import os
import random
import string
import pandas as pd
from datetime import datetime, timedelta

# Lists of value types
UPN_UNKNOWN_TYPES = ["UN1", "UN2", "UN3", "UN4", "UN5", "UN6", "UN7"]
GENDER_TYPES = ["1", "2", "0", "9"]
ETHNICITY_TYPES = ["WBRI", "WIRI", "WIRT", "WOTH", "WROM", "MOTH", "AOTH", "AIND", "APKN", "ABAN", "MWBC", "MWBA", "MWAS", "BCRB", "BAFR", "BOTH", "CHNE", "OOTH", "REFU", "NOBT"]
DISABILITY_TYPES = ["NONE", "MOB", "HAND", "PC", "INC", "COMM", "LD", "HEAR", "VIS", "BEH", "CON", "AUT","DDA"]
REFERRAL_TYPES = ["1A", "1B", "1C", "1D", "2A", "2B", "3A", "3B"]
ABUSE_TYPES = ["NEG", "PHY", "SAB", "EMO", "MUL"]
NEED_TYPES = ["N1", "N2", "N3", "N4", "N5", "N6", "N7", "N8", "N9"]
CLOSURE_TYPES = ["RC1", "RC2", "RC3", "RC4", "RC5"]
FACTOR_TYPES = ["1A", "1B", "1C", "2C", "2A", "2B", "3A", "3B"]

# Utility functions
def biased_count(min_val=1, max_val=4):
    weights = [0.6, 0.25, 0.1, 0.05][:max_val]
    return random.choices(range(min_val, max_val + 1), weights=weights)[0]

def random_date(start_date):
    return start_date + timedelta(days=random.randint(1, 2190))

def generate_upn():
    first_letter = random.choice(string.ascii_letters)
    digits = ''.join(random.choices(string.digits, k=11))
    last_char = random.choice(string.ascii_letters + string.digits)
    return f"{first_letter}{digits}{last_char}"

def csv_generator(
    n_children,
    seed,
    start_date,
    percent_with_upn,
    percent_with_low_char,
    percent_with_disabilities,
    percent_with_multiple_cin,
    percent_nfa,
    percent_closed,
    percent_with_assessments,
    percent_with_factors,
    percent_with_plans,
    percent_with_s47,
    percent_with_cpp,
    percent_with_reviews
):

    random.seed(seed)
    output_dir = "csvs"
    os.makedirs(output_dir, exist_ok=True)

    # Storage for rows
    children, chars, disabs, cins, assessments, factors = [], [], [], [], [], []
    plans, section47s, cpp, reviews = [], [], [], []

    for i in range(n_children):
        child_id = f"CH{i:05d}"
        row = {"LAchildID": child_id}
        upn_random = random.random()
        if upn_random < percent_with_upn:
            row["UPN"] = generate_upn()
        if random.random() < percent_with_upn:
            row["FormerUPN"] = generate_upn()
        if upn_random >= percent_with_upn:
            row["UPNUnknownType"] = random.choice(UPN_UNKNOWN_TYPES)
        row["PersonBirthDate"] = random_date(start_date=start_date).strftime("%Y-%m-%d")
        if random.random() < percent_with_low_char:
            row["ExpectedPersonBirthDate"] = random_date(start_date=start_date).strftime("%Y-%m-%d")
        row["GenderCurrent"] = random.choice(GENDER_TYPES)
        if random.random() < percent_with_low_char:
            row["PersonDeathDate"] = random_date(start_date=start_date).strftime("%Y-%m-%d")
        children.append(row)


        # Characteristics
        chars.append({
            "LAchildID": child_id,
            "Ethnicity": random.choice(ETHNICITY_TYPES)
        })

        # Disabilities
        if random.random() < percent_with_disabilities:
            n_dis = biased_count()
            for _ in range(n_dis):
                disabs.append({
                    "LAchildID": child_id,
                    "Disability": random.choice(DISABILITY_TYPES)
                })

        # CINdetails
        n_cin = 1 if random.random() > percent_with_multiple_cin else biased_count()
        cin_dates = []
        for _ in range(n_cin):
            ref_str = random_date(start_date=start_date).strftime("%Y-%m-%d")
            cin_dates.append(ref_str)
            if random.random() < percent_nfa:
                nfa = True
            else:
                nfa = False
            s47_chance = random.random()
            icpc_req = random.random()
            cin_row = {"LAchildID": child_id}
            cin_row["CINreferralDate"] = ref_str
            cin_row["ReferralSource"] = random.choice(REFERRAL_TYPES)
            cin_row["PrimaryNeedCode"] = random.choice(NEED_TYPES)
            cin_row["ReferralNFA"] = nfa
            if random.random() < percent_closed:
                cin_row["CINClosureDate"] = random_date(start_date=start_date).strftime("%Y-%m-%d")
                cin_row["ReasonForClosure"] = random.choice(CLOSURE_TYPES)
            if nfa == False and s47_chance < percent_with_s47 and icpc_req < percent_with_cpp:
                cin_row["DateofInitialICPC"] = random_date(start_date=start_date).strftime("%Y-%m-%d")
            cins.append(cin_row)

            # Add loop around nfa

            # Assessments
            if random.random() < percent_with_assessments:
                n_assess = biased_count()
                for _ in range(n_assess):
                    start = random_date(start_date=start_date).strftime("%Y-%m-%d")
                    assessments.append({
                        "LAchildID": child_id,
                        "CINreferralDate": ref_str,
                        "AssessmentActualStartDate": start,
                        "AssessmentInternalReviewDate": random_date(start_date=start_date).strftime("%Y-%m-%d"),
                        "AssessmentAuthorisationDate": random_date(start_date=start_date).strftime("%Y-%m-%d")
                    })
                    # Factors
                    if random.random() < percent_with_factors:
                        n_f = biased_count()
                        for _ in range(n_f):
                            factors.append({
                                "LAchildID": child_id,
                                "CINreferralDate": ref_str,
                                "AssessmentActualStartDate": start,
                                "Factor": random.choice(FACTOR_TYPES)
                            })

            # Plans
            if random.random() < percent_with_plans:
                plans.append({
                    "LAchildID": child_id,
                    "CINreferralDate": ref_str,
                    "CINPlanStartDate": random_date(start_date=start_date).strftime("%Y-%m-%d"),
                    "CINPlanEndDate": random_date(start_date=start_date).strftime("%Y-%m-%d")
                })

            # Section47
            if s47_chance < percent_with_s47:
                s47_row = {"LAchildID": child_id}
                s47_row["CINreferralDate"] = ref_str
                s47_row["S47ActualStartDate"] = random_date(start_date=start_date).strftime("%Y-%m-%d")
                if icpc_req < percent_with_cpp:
                    s47_row["ICPCRequired"] = True
                    s47_row["InitialCPCtarget"] = random_date(start_date=start_date).strftime("%Y-%m-%d")
                    s47_row["DateOfInitialCPC"] = random_date(start_date=start_date).strftime("%Y-%m-%d")
                else:
                    s47_row["ICPCRequired"] = False
                section47s.append(s47_row)

            # CPP
            if random.random() < percent_with_cpp:
                cpp_start_date = random_date(start_date=start_date).strftime("%Y-%m-%d")
                cpp.append({
                    "LAchildID": child_id,
                    "CINreferralDate": ref_str,
                    "CPPstartDate": cpp_start_date,
                    "CPPendDate": random_date(start_date=start_date).strftime("%Y-%m-%d"),
                    "InitialCategoryOfAbuse": random.choice(ABUSE_TYPES),
                    "LatestCategoryOfAbuse": random.choice(ABUSE_TYPES),
                    "NumberOfPreviousCPP": random.randint(0, 3)
                })

                # Reviews
                if random.random() < percent_with_reviews:
                    n_reviews = biased_count()
                    for _ in range(n_reviews):
                        reviews.append({
                            "LAchildID": child_id,
                            "CINreferralDate": ref_str,
                            "CPPstartDate": cpp_start_date,
                            "CPPreviewDate": random_date(start_date=start_date).strftime("%Y-%m-%d")
                        })

    # Save to CSV files
    pd.DataFrame(children).to_csv(f"{output_dir}/ChildIdentifiers.csv", index=False)
    pd.DataFrame(chars).to_csv(f"{output_dir}/ChildCharacteristics.csv", index=False)
    pd.DataFrame(disabs).to_csv(f"{output_dir}/Disabilities.csv", index=False)
    pd.DataFrame(cins).to_csv(f"{output_dir}/CINdetails.csv", index=False)
    pd.DataFrame(assessments).to_csv(f"{output_dir}/Assessments.csv", index=False)
    pd.DataFrame(factors).to_csv(f"{output_dir}/Factors.csv", index=False)
    pd.DataFrame(plans).to_csv(f"{output_dir}/CINPlanDates.csv", index=False)
    pd.DataFrame(section47s).to_csv(f"{output_dir}/Section47.csv", index=False)
    pd.DataFrame(cpp).to_csv(f"{output_dir}/ChildProtectionPlans.csv", index=False)
    pd.DataFrame(reviews).to_csv(f"{output_dir}/Reviews.csv", index=False)

    print(f"Generated CSVs in '{output_dir}/'")

    pass