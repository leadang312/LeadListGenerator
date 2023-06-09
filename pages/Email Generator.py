import streamlit as st
import pandas as pd
import time

def create_email(df):

    count = 0
    for idx, row in df.iterrows():
    
        # Template for AI
        if not pd.isna(row['FIRSTNAME']) and not pd.isna(row['CITY']) and not pd.isna(row['TITLE']) and not pd.isna(row['MESSAGE']):
            
            # Extract the frist 15 skills
            comma = ","
            skills = row['MESSAGE'].split(comma)
            
            # Fill in the template
            template = f"Hey {row['FIRSTNAME']}, I hope your day is going well in {row['CITY'].split(comma)[0]}. The reason for my message is that I noticed your experience as an {row['TITLE'].split(comma)[0]}"
            
            template += f"as well as with {', '.join(skills)}."
            
        
            # Insert the text and print it
            df.loc[idx, 'MESSAGE'] = template
            st.write(idx, df.loc[idx, 'MESSAGE'])


        elif not pd.isna(row['FIRSTNAME']) and not pd.isna(row['CITY']) and not pd.isna(row['TITLE']):
            # Fill in the template
            comma = ","
            template = f"Hey {row['FIRSTNAME']}, I hope your day is going well in {row['CITY'].split(comma)[0]}. The reason for my message is that I noticed your experience as an {row['TITLE'].split(comma)[0]}."
        
            # Insert the text and print it
            df.loc[idx, 'MESSAGE'] = template
            print(idx, df.loc[idx, 'MESSAGE'])

    return df

# Heading
st.title('Email Generator')

# File Uploader for Merged File
st.write("")
st.write("**🤖 LEAD LIST**")
required_cols = ['LINKEDIN_PROFILE__C', 'FIRSTNAME', 'LASTNAME', 'TITLE', 'COMPANY', 'CITY', 'MESSAGE']

merged = st.file_uploader("Required columns: " + ', '.join(required_cols), key="Merged")

me = pd.DataFrame()
if merged is not None:
    me = pd.read_csv(merged)

    if st.button('Show Content',key="Merged Button"):
        st.write(me)

# Process and Dowload
st.write("")
st.write("**📥 PROCESS AND DOWNLOAD LEAD LIST**")
process, download = st.columns(2)

# Process
with process: 
    proc = st.button('Create Lead List')
    
    
email = pd.DataFrame()
    
if proc:
    if not me.empty:
        email = create_email(me)
        st.success('Email creation succesfull')
    else:
        st.error('You have to insert the file and the key first!')

# Download
@st.cache_data
def convert_df(df):
    return df.to_csv().encode('utf-8')

with download:  
    
    if not email.empty:
        csv = convert_df(email)
        downl = st.download_button(label="Download Lead List",  data=csv, file_name='LeadList.csv', mime='text/csv')
