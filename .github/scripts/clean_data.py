import os
import pandas as pd
import re
import csv
import copy

#csv_path = 'raw/full_wine_list.csv'
#output_path = 'data/clean/cleaned_wine_list.csv'

def convert_to_int(v):
    if pd.isna(v):
        return v  # Keep NaN as is
    try:
        return int(float(v))  # Convert to int if possible
    except ValueError:
        return v  # Leave unchanged if conversion fails
        
def remove_non_rated(df):
    # Remove rows where 'Your rating' is NaN or an empty string
    df_cleaned = df[df['Your rating'].notna()]          # remove NaNs
    df_cleaned = df_cleaned[df_cleaned['Your rating'].astype(str).str.strip() != '']  # remove empty strings
    return df_cleaned

def clean_vintage(df):
    df['Vintage'] = df['Vintage'].apply(convert_to_int)
    return df

def clean_countries(df):
    corr_dict={'us':'United States',
               'it':'Italy',
               'es':'Spain',
               'il':'Israel',
               'fr':'France',
               'hr':'Croatia'}
    df['Country'] = df['Country'].replace(corr_dict)
    return df

def apply_manual_corrections(df):
    """
    Applies manual corrections to a DataFrame based on matching 'Wine name'.

    Parameters:
    - df (pd.DataFrame): The DataFrame to correct.
    - corrections_dict (dict): Dictionary where keys are 'Wine name' values and
      values are dicts of field corrections.

    Returns:
    - pd.DataFrame: The corrected DataFrame.
    """
    corrections = {
    "Viso Barbera - Nebbiolo": {
        "Winery": "Viso",
        "Country": "Italy",  
        "Region": "Piedmont",  
        'Regional wine style':'Northern Italy Red'
    },
    
    "Viña Bouchon Pinot Pais": {
        "Winery": "Viña Bouchon",
        'Vintage':2023
    },
    
    "Lirio Verdejo": {
        "Winery": "Lirio",
        "Region": 'Rueda',
        'Scan/Review Location': 'Postino'
        
    },
    "El Correo  Sauvignon Blanc": {
        "Winery": "El Correo"
        
    },
    "The Puppet Skin Contact": {
        "Winery": "The Puppet",
        'Scan/Review Location': "Trader Joe's"
        
    },
    "Centenario Cabernet Sauvignon": {
        "Winery": "Centenario",
        'Scan/Review Location': "Postino Arcadia Winecafe"
    },
    "Rimon Red Semi Sweet Pomegranete": {
        "Winery": "Rimon Winery",
        'Country': 'Israel',
        'Region': 'Upper Galilee',
        "Regional wine style": "Israeli Red",
        "Wine type" : 'Red Wine'
    }
}
  
    
    df_corrected = df.copy()

    for wine_name, updates in corrections.items():
        matches = df_corrected['Wine name'] == wine_name

        if matches.any():
            for column, new_value in updates.items():
                df_corrected.loc[matches, column] = new_value
        else:
            print(f"⚠️ Warning: '{wine_name}' not found in DataFrame")

    return df_corrected

def no_winery(df):
    # Detect both NaN and empty strings (after stripping whitespace)
    missing_winery_df = df[df['Winery'].isna() | (df['Winery'].astype(str).str.strip() == '')]
    return missing_winery_df

def print_row_indices(df):
    """
    Prints the index (row number) of each row in the DataFrame.

    Parameters:
    - df (pd.DataFrame): The DataFrame to loop through
    """
    for idx in df.index:
        print(idx)

def cleaning_process(df):
    #copies just in case
    df_copy=copy.deepcopy(df)
    #removes non-rated
    df=remove_non_rated(df)
    #cleans vintage
    df=clean_vintage(df)
    #cleans countries
    df =  clean_countries(df)
    ##makes manual corrections
    df = apply_manual_corrections(df)
    clean_df=copy.deepcopy(df)
    return clean_df

# ========== Main Entry Point ==========

def main():
    if len(sys.argv) != 3:
        print("Usage: python clean_data.py input.csv output.csv")
        sys.exit(1)

    input_path = sys.argv[1]
    output_path = sys.argv[2]

    print(f"📥 Loading: {input_path}")
    df = pd.read_csv(input_path)

    df_cleaned = cleaning_process(df)

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    df_cleaned.to_csv(output_path, index=False)
    print(f"✅ Cleaned data saved to: {output_path}")

if __name__ == "__main__":
    main()
