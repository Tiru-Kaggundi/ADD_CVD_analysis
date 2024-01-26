import pandas as pd
from collections import Counter

"""
This code basically takes in the excel sheet of add/cvd cases and counts the 
chapters and products that suffer ADD/CVD
It also takes in the excel sheet of add/cvd cases and generates the top 3 
trading partners for each chapter.
"""

def clean_and_split(data_column):
    """
    Function to clean and split a data column.

    Args:
        data_column (list): The list of items to be processed.

    Returns:
        list: The list of cleaned and split items.
    """
    split_items = [str(item).split(", ") for item in data_column]
    flattened_items = [item.strip() for sublist in split_items for item in sublist]
    return flattened_items

def get_top_partners(data, chapters, top_n=3):
    """
    Return the top trading partners for each chapter based on the provided data.

    Args:
        data (pandas.DataFrame): The data containing information about trading partners and product chapters.
        chapters (list): The list of chapters to analyze.
        top_n (int, optional): The number of top partners to return for each chapter. Defaults to 3.

    Returns:
        dict: A dictionary where the keys are chapters and the values are lists of top trading partners.
    """
    top_partners = {}
    for chapter in chapters:
        filtered_data = data[data['Product chapters'].str.contains(str(chapter), na=False)]
        partners_count = Counter(filtered_data['Trading partners'])
        top_partners[chapter] = partners_count.most_common(top_n)
    return top_partners

def main():
    """
    This function performs analysis on the 'remedies_analysis.xlsx' Excel file and 
    generates separate sheets with the data filtered by type, count occurrences 
    for Anti-dumping and Countervailing, extract top chapters and their top partners, 
    create dataframes, sort the dataframes, and write the results to a new Excel file 
    with separate sheets.
    """
    # Load the original Excel file
    data = pd.read_excel('trade_remedy_analysis/remedies_analysis.xlsx')

    # Filter data by Type
    anti_dumping_data = data[data['Type'].str.contains("Anti-dumping")]
    countervailing_data = data[data['Type'].str.contains("Countervailing")]

    # Count occurrences for Anti-dumping and Countervailing
    anti_dumping_chapters_count = Counter(clean_and_split(anti_dumping_data['Product chapters']))
    anti_dumping_products_count = Counter(clean_and_split(anti_dumping_data['Products']))
    countervailing_chapters_count = Counter(clean_and_split(countervailing_data['Product chapters']))
    countervailing_products_count = Counter(clean_and_split(countervailing_data['Products']))

    # Extract top chapters and get their top partners
    top_anti_dumping_chapters = [item[0] for item in anti_dumping_chapters_count.most_common()]
    top_countervailing_chapters = [item[0] for item in countervailing_chapters_count.most_common()]
    top_partners_anti_dumping = get_top_partners(anti_dumping_data, top_anti_dumping_chapters)
    top_partners_countervailing = get_top_partners(countervailing_data, top_countervailing_chapters)

    # Create dataframes
    df_anti_dumping_chapters = pd.DataFrame(anti_dumping_chapters_count.items(), columns=['Product Chapter', 'Count'])
    df_anti_dumping_products = pd.DataFrame(anti_dumping_products_count.items(), columns=['Product', 'Count'])
    df_countervailing_chapters = pd.DataFrame(countervailing_chapters_count.items(), columns=['Product Chapter', 'Count'])
    df_countervailing_products = pd.DataFrame(countervailing_products_count.items(), columns=['Product', 'Count'])
    df_top_partners_anti_dumping = pd.DataFrame([(chapter, partners) for chapter, partners in top_partners_anti_dumping.items()], columns=['Product Chapter', 'Top 3 Partners'])
    df_top_partners_countervailing = pd.DataFrame([(chapter, partners) for chapter, partners in top_partners_countervailing.items()], columns=['Product Chapter', 'Top 3 Partners'])

    # Sort the dataframes
    df_anti_dumping_chapters.sort_values(by='Count', ascending=False, inplace=True)
    df_anti_dumping_products.sort_values(by='Count', ascending=False, inplace=True)
    df_countervailing_chapters.sort_values(by='Count', ascending=False, inplace=True)
    df_countervailing_products.sort_values(by='Count', ascending=False, inplace=True)

    # Write to a new Excel file with separate sheets
    with pd.ExcelWriter('trade_remedy_analysis/remedies_product_wise.xlsx') as writer:
        df_anti_dumping_chapters.to_excel(writer, sheet_name='Anti-Dumping Chapters', index=False)
        df_anti_dumping_products.to_excel(writer, sheet_name='Anti-Dumping Products', index=False)
        df_countervailing_chapters.to_excel(writer, sheet_name='Countervailing Chapters', index=False)
        df_countervailing_products.to_excel(writer, sheet_name='Countervailing Products', index=False)
        df_top_partners_anti_dumping.to_excel(writer, sheet_name='Top Partners Anti-Dumping', index=False)
        df_top_partners_countervailing.to_excel(writer, sheet_name='Top Partners Countervailing', index=False)

if __name__ == "__main__":
    main()
