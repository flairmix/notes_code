import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

class DataframeVisualizer:
    """
    A class for visualizing and analyzing processed DataFrame from CSVProcessor.

    Features:
    - Displays basic statistics for each category column
    - Highlights entries per column (e.g., how many were flagged)
    - Allows inspection of specific columns
    - Generates bar plots for flagged counts per category
    - Reports number of rows with no comments
    """

    def __init__(self, df: pd.DataFrame):
        self.df = df
        sns.set_theme(style="whitegrid")  # Apply seaborn style globally

    def display_basic_statistics(self):
        print("--- Basic Column Statistics ---")
        print(f"Total rows: {len(self.df)}")
        total_flagged = 0
        flag_columns = []

        for col in self.df.columns:
            if self.df[col].dtype in [int, float] and col != "ID":
                flagged_count = self.df[col].sum()
                total_flagged += flagged_count
                flag_columns.append(col)
                print(f"{col}: {flagged_count} flagged")

        print(f"Rows with no comments: {self.df['Комментарии'].astype(str).str.strip().replace('', pd.NA).isna().sum()}")

    def plot_flagged_counts(self):
        count_data = {}
        flag_columns = []

        for col in self.df.columns:
            if self.df[col].dtype in [int, float] and col != "ID":
                count_data[col] = self.df[col].sum()
                flag_columns.append(col)

        count_data["Has Comments"] = self.df["Комментарии"].astype(str).str.strip().replace('', pd.NA).notna().sum()
        count_data["No Comments"] = self.df["Комментарии"].astype(str).str.strip().replace('', pd.NA).isna().sum()

        plt.figure(figsize=(12, 6))
        barplot = sns.barplot(x=list(count_data.keys()), y=list(count_data.values()), palette="viridis")
        barplot.set_title("Flagged Rows by Category", fontsize=16, weight='bold')
        barplot.set_ylabel("Count", fontsize=12)
        barplot.set_xlabel("Category", fontsize=12)
        barplot.bar_label(barplot.containers[0], fmt='%d', label_type='edge', padding=3)

        for container in barplot.containers:
            for bar in container:
                height = bar.get_height()
                barplot.text(
                    bar.get_x() + bar.get_width() / 2,
                    height + 1,
                    f'{int(height)}',
                    ha='center', va='bottom', fontsize=10, fontweight='bold'
                )

        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()
        plt.show()

    def inspect_column(self, column_name):
        if column_name not in self.df.columns:
            print(f"Column '{column_name}' not found.")
            return
        print(f"--- Entries with '{column_name}' Flagged ---")
        flagged = self.df[self.df[column_name] == 1]
        print(flagged[["ID", "Содержание", column_name, "Комментарии"]])

    def show_summary(self):
        self.display_basic_statistics()
        self.plot_flagged_counts()