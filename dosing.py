# USCD Senior Clinical Data Engineer Coding Challenge
# Ken Kroel
# 20190731

import pandas as pd


def main():
    """Read 2 csv files into dataframes, merge them, filter results and output a subset of columns to a new csv."""
    reg_file = r't2_registry 20190619.csv'
    ec_file = r't2_ec 20190619.csv'
    output_file = r'results.csv'

    join_cols = ['RID', 'VISCODE']
    output_cols = ['ID', 'RID', 'USERID', 'VISCODE', 'SVDOSE', 'ECSDSTXT']

    # cast columns explicitly
    reg_converters = {'VISCODE': str, 'SVDOSE': str}
    reg_df = pd.read_csv(reg_file, converters=reg_converters)

    # convert after read since ECSDSTXT cotains NANs
    ec_df = pd.read_csv(ec_file)
    ec_df = ec_df[ec_df['ID'].notna()]
    ec_df['ECSDSTXT'] = ec_df['ECSDSTXT'].astype(int)

    full_df = pd.merge(reg_df, ec_df, on=join_cols, how='left', suffixes=('', '_y'))

    final_df = full_df[(full_df['VISCODE'] == 'w02') &
                       (full_df['SVDOSE'] == 'Y') &
                       (~(full_df['ECSDSTXT'] == 280))]

    final_df.to_csv(output_file, columns=output_cols, index=None)

    return final_df


if __name__ == "__main__":
    # execute if run as script
    main()


#  --- used by pytest. uncommment if pytest is available ---
# def setup_module():
#     import pytest


# test results with pytest
# def test_results():
#     final_df = main()
#     assert final_df['RID'].values.tolist() == [19, 17]
#     assert final_df['SVDOSE'].values.tolist() == ['Y', 'Y']
#     assert final_df['ECSDSTXT'].values.tolist() == [-4, 140]
