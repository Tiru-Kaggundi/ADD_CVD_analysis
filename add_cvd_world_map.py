import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt


def get_world_with_data(df, remedy_type):
    """
    Aggregating the number of cases by Member/Observer and Type.

    :param df: The input DataFrame containing the data.
    :param remedy_type: The type of remedy to be used for aggregation.
    :return: A world map with the aggregated data merged.
    """
    # Aggregating the number of cases by Member/Observer and Type
    df['Remedy Type'] = df['Type'].str.split('/').str[-1].str.strip()
    cases_count = df.groupby(['Member/Observer',
                              'Remedy Type']).size().unstack(fill_value=0)

    # Load the world map
    world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))
    # Merge world map with data
    world_with_data = world.merge(cases_count[[remedy_type]],
                                  how='left',
                                  left_on='name',
                                  right_on='Member/Observer')
    world_with_data.fillna(0, inplace=True)
    return world_with_data


def plot_world_map(remedy_type, world_with_data, output_path):
    """
    Plot a world map showing the number of cases for a given remedy type.

    Parameters:
    - remedy_type: str, the type of remedy for which cases are being plotted
    - world_with_data: pandas DataFrame, the world map data with remedy cases
    - output_path: str, the file path where the map will be saved as a PNG

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
        if row[remedy_type] > 0:
            plt.text(row['geometry'].centroid.x,
                     row['geometry'].centroid.y,
                     str(int(row[remedy_type])),
                     fontsize=10,
                     fontweight='bold',
                     color='black',
                     ha='center',
                     va='center')

    # Title
    ax.set_title(f"Use of {remedy_type} - Country/Region wise",
                 fontsize=16,
                 fontweight='bold')

    # Save as PNG
    plt.savefig(output_path, format='png', dpi=300, bbox_inches='tight')


# Main script
def main():
    """
    This function reads an Excel file containing remedies analysis, loops through
    the remedy types, creates world maps for each type, and saves the maps to
    specified output paths.
    """
    file_path = 'trade_remedy_analysis/remedies_analysis.xlsx'
    df = pd.read_excel(file_path)

    for remedy_type in ['Anti-dumping', 'Countervailing']:
        world_with_data = get_world_with_data(df, remedy_type)
        output_path = f'trade_remedy_analysis/world_map_{remedy_type.replace(" ", "_").lower()}.png'
        plot_world_map(remedy_type, world_with_data, output_path)
        print(f'Map for {remedy_type} saved to {output_path}')


if __name__ == "__main__":
    main()