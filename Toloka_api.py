import csv
import requests
import pycountry
import matplotlib.pyplot as plt


API_URL = 'https://toloka.dev/api/v1/user-metadata'
headers = {
    'Authorization': 'OAuth AUTHENTICATION TOKEN',
}

# Function to process a CSV file and save the aggregated country counts to a file
def process_csv_file(input_file, output_file):
    # Open the CSV file
    with open(input_file, 'r') as file:
        reader = csv.reader(file)
        next(reader)
        # Create a dictionary to store the aggregated country values
        country_counts = {}

        # Iterate over each row in the CSV file
        for row in reader:
            user_id = row[0]
            url = f'{API_URL}/{user_id}'
            response = requests.get(url, headers=headers)

            if response.status_code == 200:
                data = response.json()
                country = data['country']
                if country in country_counts:
                    country_counts[country] += 1
                else:
                    country_counts[country] = 1
            else:
                print(f'Request failed with status code {response.status_code} for user ID: {user_id}')

    with open(output_file, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Country', 'Count'])
        for country, count in country_counts.items():
            writer.writerow([country, count])

    print(f'Country counts saved to {output_file}')

# Function to aggregate country counts from multiple files
def aggregate_country_counts(input_files, output_file):
    country_counts = {}

    # Iterate over each input file
    for file in input_files:
        with open(file, 'r') as file:
            reader = csv.reader(file)
            next(reader)

            for row in reader:
                country = row[0]
                count = int(row[1])

                if country in country_counts:
                    country_counts[country] += count
                else:
                    country_counts[country] = count

    with open(output_file, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Country', 'Count'])
        for country, count in country_counts.items():
            writer.writerow([country, count])

    print(f'Aggregated country counts saved to {output_file}')

# Function to convert country codes to full country names
def convert_country_code_to_name(country_code):
    try:
        country = pycountry.countries.get(alpha_2=country_code)
        return country.name
    except LookupError:
        return country_code

# Function to aggregate country counts from multiple files and convert country codes to full country names
def aggregate_country_counts(input_files, output_file):
    country_counts = {}

    # Iterate over each input file
    for file in input_files:
        with open(file, 'r') as file:
            reader = csv.reader(file)
            next(reader)

            for row in reader:
                country_code = row[0]
                count = int(row[1])

                # Convert country code to full country name
                country_name = convert_country_code_to_name(country_code)

                # Aggregate country counts
                if country_name in country_counts:
                    country_counts[country_name] += count
                else:
                    country_counts[country_name] = count

    with open(output_file, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Country', 'Count'])
        for country, count in country_counts.items():
            writer.writerow([country, count])

    print(f'Aggregated country counts with full country names saved to {output_file}')

# Function to plot a pie chart
def plot_pie_chart(data, save_path):
    countries = []
    counts = []

    # Extract countries and counts from the data
    for row in data[1:]:
        countries.append(row[0])
        counts.append(int(row[1]))

    # Set a threshold for grouping countries into "Others"
    threshold = 3
    grouped_countries = []
    grouped_counts = []

    # Group countries below the threshold
    other_count = 0
    for country, count in zip(countries, counts):
        if count >= threshold:
            grouped_countries.append(country)
            grouped_counts.append(count)
        else:
            other_count += count

    # Add "Others" category
    grouped_countries.append("Others")
    grouped_counts.append(other_count)

    # Create the pie chart
    fig, ax = plt.subplots()
    ax.pie(grouped_counts, labels=grouped_countries, autopct='%1.1f%%', startangle=90)
    ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle

    plt.title('Country Distribution')

    # Save the chart with a transparent background if save_path is provided
    if save_path:
        plt.savefig(save_path, transparent=True)

    plt.show()

# # Process the four CSV files and save the results
# process_csv_file('Data/agg_loan_ctrl_results.csv', 'loan_ctrl_counting_countries.csv')
# process_csv_file('Data/agg_loan_exp_results.csv', 'loan_exp_counting_countries.csv')
# process_csv_file('Data/agg_recid_ctrl_results.csv', 'recid_ctrl_counting_countries.csv')
# process_csv_file('Data/agg_recid_exp_results.csv', 'recid_exp_counting_countries.csv')

# Example usage
# input_files = [
#     'loan_ctrl_counting_countries.csv',
#     'loan_exp_counting_countries.csv',
#     'recid_ctrl_counting_countries.csv',
#     'recid_exp_counting_countries.csv'
# ]
# output_file = 'all_results_aggregated.csv'
#
# aggregate_country_counts(input_files, output_file)



# Read the data from the CSV file
data = []
with open('all_results_aggregated.csv', 'r') as file:
    reader = csv.reader(file)
    for row in reader:
        data.append(row)

# Plot the pie chart
save_path = 'Data/pie_chart_transparent.png'
plot_pie_chart(data, save_path)