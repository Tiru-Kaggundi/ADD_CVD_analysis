import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt

# This code creates a world map showing the number of cases against each trading partner
# and stores it in a PNG file in the current working directory.

def get_world_with_data_trading_partners(df, remedy_type):
    """
    Aggregating the number of cases against each trading partner.

    :param df: The input pandas DataFrame.
    :param remedy_type: The type of remedy to filter the DataFrame.
    :return: The world map with data on trading partners and their case counts.
    """
    # Aggregating the number of cases against each trading partner
    df_filtered = df[df['Type'].str.contains(remedy_type, na=False)]
    cases_count = df_filtered.groupby('Trading partners').size().reset_index(name='case_count')

    # Load the world map from Natural Earth data
    world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))
    # Merge world map with data
    world_with_data = world.merge(cases_count, how='left', left_on='name', right_on='Trading partners')
    world_with_data.fillna(0, inplace=True)
    return world_with_data

def plot_world_map(remedy_type, world_with_data, output_path):
    """
    Plot a world map with data related to a specific remedy type.

    Parameters:
    - remedy_type: str, the type of remedy for which the data is being plotted
    - world_with_data: pandas DataFrame, the world map data with the remedy data
    - output_path: str, the file path where the plot will be saved

    Returns:
    None
    """
    fig, ax = plt.subplots(1, 1, figsize=(15, 10))
    world_with_data['color'] = '#ffedcc'  # Light color for all countries
    world_with_data.plot(color=world_with_data['color'], ax=ax)

    # Remove lat/long labels
    ax.set_axis_off()

    # Add whole number counts on countries
    for idx, row in world_with_data.iterrows():
        if row['case_count'] > 0:
            plt.text(row['geometry'].centroid.x, row['geometry'].centroid.y, str(int(row['case_count'])),
                     fontsize=8, fontweight='bold', color='black', ha='center', va='center')

    # Title
    ax.set_title(f"Number of {remedy_type} Cases suffered - country wise", fontsize=16, fontweight='bold')

    # Save as PNG
    plt.savefig(output_path, format='png', dpi=300, bbox_inches='tight')

# Main script
def main():
    """
    The main function reads an Excel file, iterates over remedy types, and creates world map plots for each type.
    """
    file_path = 'trade_remedy_analysis/remedies_analysis.xlsx'
    df = pd.read_excel(file_path)

    for remedy_type in ['Anti-dumping', 'Countervailing']:
        world_with_data = get_world_with_data_trading_partners(df, remedy_type)
        output_path = f'trade_remedy_analysis/world_map_{remedy_type.replace(" ", "_").lower()}_against_trading_partners.png'
        plot_world_map(remedy_type, world_with_data, output_path)
        print(f'Map for {remedy_type} against Trading Partners saved to {output_path}')

if __name__ == "__main__":
    main()
