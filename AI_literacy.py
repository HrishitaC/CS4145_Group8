import pandas as pd
import matplotlib.pyplot as plt
import textwrap


def calculate_ai_literacy_table(file_paths, column_start=9):
    survey_data = pd.concat([pd.read_excel(file_path) for file_path in file_paths])
    # Remove whitespace from every cell in the DataFrame
    survey_data = survey_data.applymap(lambda x: x.strip() if isinstance(x, str) else x)
    # Group the responses by question and count the frequencies
    grouped_data = survey_data.iloc[:, column_start:12].apply(pd.Series.value_counts)

    return grouped_data

file_paths = [
    "Data/survey_results/control_loan.xlsx",
    "Data/survey_results/experiment_loan.xlsx",
    "Data/survey_results/control_recidivism.xlsx",
    "Data/survey_results/experiment_recidivism.xlsx"
]

# Map answers to numbers
mapping = {
    'Strongly Agree': 5,
    'Moderately Agree': 4,
    'Neutral': 3,
    'Moderately Disagree': 2,
    'Strongly Disagree': 1,
}


frequency_table = calculate_ai_literacy_table(file_paths, column_start=9)
frequency_table = frequency_table.T
ax = frequency_table.plot(kind='bar', rot=0)
plt.xlabel('Question')
plt.ylabel('Count')
plt.title('Survey Responses')
plt.legend(title='Response')

# Wrap the x-axis labels and display them on new lines
wrapped_labels = [textwrap.fill(label, width=15) for label in frequency_table.index]
ax.set_xticklabels(wrapped_labels, rotation='horizontal')

# Adjust the layout to prevent label overlapping
plt.tight_layout()
plt.show()