file = 'C:/_Projects/_REPO/_otherREPO/DataAnalysis/LogExp/S_2021_7_5__21_56_5.csv'
file2 = file.split('/')[-1]
print(file2[0])
import re

def check_string_structure(input_string):
    pattern = r"^[ASE]_\d{4}_\d{1,2}_\d{1,2}__\d{1,2}_\d{1,2}_\d{1,2}\.csv$"
    return re.match(pattern, input_string) is not None

test_string = file2
if check_string_structure(test_string):
    print("String has the correct structure")
else:
    print("String does not have the correct structure")

pattern = r"^[ASE]_\d{4}_\d{1,2}_\d{1,2}__\d{1,2}_\d{1,2}_\d{1,2}\.csv$"
"""
^: Start of the string 
[ASE]: either "A", "S", or "E" 
_: character 
\d{4}: Matches exactly 4 digits 
\d{1,2}: Matches 1 or 2 digits 
\.csv: Matches the ".csv" extension
$: End of the string
"""

string_to_check = "S_2021_7_5__21_56_5.csv"

if re.match(pattern, string_to_check) is None:
    print("String matches the pattern.")