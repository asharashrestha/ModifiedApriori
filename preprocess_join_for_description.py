import pandas as pd

filepath = "/Users/aasharashrestha/Documents/PycharmProjects/SeasonalTrends/Seasonality_Project/Paper_5/Project/"
ccs_file_path=  "/Users/aasharashrestha/Documents/PycharmProjects/SeasonalTrends/Seasonality_Project/Paper_5/Project/icd_ccs_No_Dups.csv"
file = "d5k.csv"

ccs= pd.read_csv(ccs_file_path,dtype ='str')#ccs data import
#removing unnecessary columns from ccs
remove_cols = ['OPTIONAL_CCS_CATEGORY_DESCRIPTION','OPTIONAL_CCS_CATEGORY','ICD_9_CM_CODE_DESCRIPTION']

ccs.drop(remove_cols, inplace = True, axis =1)

#importing claims file
df = pd.read_csv(filepath + file,dtype ='str')

#joining Admission Diag Code and ICD Code with CCS

df = pd.merge(df, ccs, left_on='Primary Diagnosis Code', right_on='ICD9_Code', how = 'left')

#dropping unwanted columns
columns = ['CCS_CATEGORY', 'ICD9_Code', 'Primary Diagnosis Code']
df.drop(columns, inplace=True, axis=1)
df = df.rename(columns={'CCS_CATEGORY_DESCRIPTION': 'Primary Diagnosis Code'})

#joining for disposition description
df_disp = pd.read_csv("/Users/aasharashrestha/Documents/PycharmProjects/SeasonalTrends/Seasonality_Project/Paper_5/Project/VersionControl/ModifiedApriori/disposition_dictionary.csv", dtype= str)

# check if all value of disposition in main file is present in dictionary
for i in df.index:
    if df.Disposition[i] not in df_disp.Disposition.values:
        print(df.Disposition[i])

df = pd.merge(df, df_disp, left_on='Disposition', right_on='Disposition', how = 'left')
#dropping unwanted columns
columns = ['Disposition']
df.drop(columns, inplace=True, axis=1)
df = df.rename(columns={'Description': 'Disposition'})


df.loc[(df['Discharge_Status'] == '1') ,'Discharge_Status'] = 'Discharged'
df.loc[(df['Discharge_Status'] == '0') ,'Discharge_Status'] = 'Not Discharged'

df.loc[(df['Type_of_Admission'] == '1') ,'Type_of_Admission'] = 'Urgent'
df.loc[(df['Type_of_Admission'] == '2') ,'Type_of_Admission'] = 'Emergency'
df.loc[(df['Type_of_Admission'] == '3') ,'Type_of_Admission'] = 'Elective'

df.to_csv('d5k_preprocessed.csv', sep=',')
print("Successfully dumped...")




