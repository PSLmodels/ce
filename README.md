# `cesurvey`
Python package for working with the US Consumer Expenditure Survey


# Example usage

```
import cesurvey

fmli_2019 = cesurvey.get_interview_data(2019)
fmli_2018 = cesurvey.get_interview_data(2018)

lku = cesurvey.get_data_dictionary()

income_bf_tax_2019 = cesurvey.estimate_annual_quantity("FINCBTXM", fmli_2019)
income_bf_tax_2018 = cesurvey.estimate_annual_quantity("FINCBTXM", fmli_2018)
```
