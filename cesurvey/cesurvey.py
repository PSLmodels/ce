import os
import requests
import tempfile
import logging
import glob
from zipfile import ZipFile

import pandas as pd
import numpy as np


def read_fmli_quarter(filename, year, quarter):
    fmli = pd.read_csv(filename)
    fmli.insert(0, 'nominal_year', year)
    fmli.insert(1, 'nominal_quarter', quarter)
    fmli.insert(2, 'cu_id', fmli.NEWID.apply(lambda x: get_unit_id(x)))
    fmli.insert(3, 'interview_id', fmli.NEWID.apply(lambda x: get_interview_id(x)))
    fmli.insert(4, 'interview_mo', fmli['QINTRVMO'])
    fmli.insert(5, 'interview_yr', fmli['QINTRVYR'])
    fmli.insert(6, 'months_in_scope', fmli.apply(
        lambda row: months_in_scope(row['interview_mo'], row['nominal_quarter']), axis=1
        ))
    fmli.insert(6, 'weight', fmli['FINLWT21'])
    return fmli

def months_in_scope(interview_mo, quarter):
    """quarter is nominal quarter"""
    months_in_scope = np.nan
    if quarter in [1, 2, 3, 4]:
        if interview_mo in [1, 2, 3]:
            months_in_scope = interview_mo - 1
        elif interview_mo in [4, 5, 6, 7, 8, 9, 10, 11, 12]:
            months_in_scope = 3
        else:
            raise ValueError(f"interview_mo {interview_mo} outside of range")
    elif quarter == 5:
        if interview_mo in [1, 2, 3]:
            months_in_scope = 4 - interview_mo
        else:
            raise ValueError(f"interview_mo {interview_mo} outside of range")
    else:
        raise ValueError(f"quarter {quarter} outside of range")
    return months_in_scope

def get_unit_id(newid):
    return int(str(newid)[:-1])

def get_interview_id(newid):
    return int(str(newid)[-1])


# installed openpyxl
def get_data_dictionary():
    vars_df = pd.read_excel(
        "https://www.bls.gov/cex/pumd/ce_pumd_interview_diary_dictionary.xlsx",
        sheet_name=1,
        engine='openpyxl'
    )

    codes_df = pd.read_excel(
        "https://www.bls.gov/cex/pumd/ce_pumd_interview_diary_dictionary.xlsx",
        sheet_name=2,
        engine='openpyxl'
    )
    return {'vars': vars_df, 'codes': codes_df}


def get_interview_data(year, revised_q1=True):
    last_two = str(year)[2:]
    next_year_last_two = str(year + 1)[2:]
    
    f = tempfile.TemporaryFile()
    
    url = f"https://www.bls.gov/cex/pumd/data/comma/intrvw{last_two}.zip"
    results = requests.get(url)
    
    f.write(results.content)
   
    # TODO (baogorek): perhaps split up so you save the data in one step.
    # More flexibility to get other things
    myfile = ZipFile(f)
    tempdir = tempfile.mkdtemp()
    logging.info("Extracting {year} files to {tempdir}")
    myfile.extractall(path=tempdir)

    fmli_path = glob.glob(os.path.join(tempdir, '**/fmli***.csv'), recursive=True)[0]
    fmli_dir = os.path.dirname(fmli_path)

    q1_suffix = "x" if revised_q1 else ""
    
    fmli_path_q1 = os.path.join(fmli_dir, f"fmli{last_two}1{q1_suffix}.csv")
    fmli_path_q2 = os.path.join(fmli_dir, f"fmli{last_two}2.csv")
    fmli_path_q3 = os.path.join(fmli_dir, f"fmli{last_two}3.csv")
    fmli_path_q4 = os.path.join(fmli_dir, f"fmli{last_two}4.csv")
    fmli_path_q5 = os.path.join(fmli_dir, f"fmli{next_year_last_two}1.csv")
    
    # TODO (baogorek): remove this opportunity for inconsistency
    # The year is also nominal year, which I need to make more clear
    fmli_q1 = read_fmli_quarter(fmli_path_q1, year, 1)
    fmli_q2 = read_fmli_quarter(fmli_path_q2, year, 2)
    fmli_q3 = read_fmli_quarter(fmli_path_q3, year, 3)
    fmli_q4 = read_fmli_quarter(fmli_path_q4, year, 4)
    fmli_q5 = read_fmli_quarter(fmli_path_q5, year, 5)
    
    # TODO (baogorek): package should also let people point at local data
    #  in case they wanted to work offline
    fmli_df = pd.concat([fmli_q1, fmli_q2, fmli_q3, fmli_q4, fmli_q5])
    fmli_df = fmli_df.sort_values(['cu_id', 'interview_id'])

    return fmli_df


def estimate_annual_quantity(var_name, fmli_df, var_type="expense"):
    if len(set(fmli_df['nominal_year'])) > 1:
        raise NotImplementedError("Multi-survey year estimation not yet supported")
    if var_type not in ["expense", "demographics"]:
        raise ValueError("var_type must be of type 'expense' or 'demographics'")

    MONTHS_PER_QUARTER = 3
    var_name = 'FINCBTXM'
    var_name = 'ALCBEVPQ'
    var_name = 'ALCBEVCQ'
    nominal_quarter_ests = []
    for nominal_quarter in [1, 2, 3, 4, 5]:
        fmli_j = fmli_df.loc[fmli_df['nominal_quarter'] == nominal_quarter]
        proportion_in_scope = fmli_j['months_in_scope'] / MONTHS_PER_QUARTER
        if var_type == "demographics":
            w = fmli_j['weight'] * proportion_in_scope  # NOTE: redefine weight?
            numerator = np.sum(w * fmli_j[var_name])
            denominator = np.sum(w)
        elif var_type == "expense":
            logging.info("expense")
            w = fmli_j['weight'] 
            numerator = np.sum(w * fmli_j[var_name])
            # Note that proportion_in_scope < 1 will scale up number
            # some proportion_in_scope vals are 0 so 1/x is problematic
            denominator = np.sum(w * proportion_in_scope)
        est = numerator / denominator
        nominal_quarter_ests.append(est)

        if var_type == "demographics":
            result = np.mean(nominal_quarter_ests)     
        elif var_type == "expense":
            # Summed 5 numbers, but there are 4 quarters
            result = np.sum(nominal_quarter_ests) * (4 / 5)
    return result

