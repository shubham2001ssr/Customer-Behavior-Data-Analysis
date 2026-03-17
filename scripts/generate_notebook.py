import json

notebook = {
 "cells": [
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "# Customer Shopping Behavior Analysis\n",
    "## Portfolio Project: Data Cleaning & Exploratory Data Analysis (EDA)\n",
    "---\n",
    "In this notebook, we'll implement the first step of the end-to-end data analytics workflow:\n",
    "1. **Data Import & Exploration:** Load our mock data and evaluate schema.\n",
    "2. **Data Cleaning:** Handle potential missing values or incorrect data types.\n",
    "3. **Visualization (EDA):** Gain a preliminary understanding of the Customer Shopping behavior.\n",
    "4. **Database Export:** Connect to an SQLite database and export the clean data for SQL querying."
   ]
  },
  {
   "cell_type": "code",
   "execution_count": None,
   "metadata": {},
   "outputs": [],
   "source": [
    "import pandas as pd\n",
    "import numpy as np\n",
    "import sqlite3\n",
    "import matplotlib.pyplot as plt\n",
    "import seaborn as sns\n",
    "\n",
    "# Set plotting style\n",
    "sns.set_theme(style=\"whitegrid\")"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "### 1. Data Import & Exploration"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": None,
   "metadata": {},
   "outputs": [],
   "source": [
    "# Load our freshly generated CSV mock dataset\n",
    "df = pd.read_csv('../data/customer_shopping_data.csv')\n",
    "df.head()"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": None,
   "metadata": {},
   "outputs": [],
   "source": [
    "# Check for structure, missing values, and data types\n",
    "df.info()"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "### 2. Data Cleaning\n",
    "(Note: Since this is auto-generated mock data, it might be fairly clean. In a real-world scenario, you'd handle nulls here.)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": None,
   "metadata": {},
   "outputs": [],
   "source": [
    "# Check if there are any missing values\n",
    "print(\"Missing Values:\\n\", df.isnull().sum())\n",
    "\n",
    "# Ensure Purchase Date is datetime\n",
    "df['Purchase Date'] = pd.to_datetime(df['Purchase Date'])"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "### 3. Exploratory Data Analysis (EDA)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": None,
   "metadata": {},
   "outputs": [],
   "source": [
    "# Top 5 most purchased Categories\n",
    "plt.figure(figsize=(8, 5))\n",
    "sns.countplot(data=df, x='Category', order=df['Category'].value_counts().index, palette='Blues_d')\n",
    "plt.title('Transactions per Category')\n",
    "plt.ylabel('Number of Transactions')\n",
    "plt.show()"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": None,
   "metadata": {},
   "outputs": [],
   "source": [
    "# Relationship between Age and Purchase Amount\n",
    "plt.figure(figsize=(10, 6))\n",
    "sns.scatterplot(data=df, x='Age', y='Purchase Amount (USD)', hue='Gender', alpha=0.6)\n",
    "plt.title('Age vs Purchase Amount')\n",
    "plt.show()"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "### 4. Database Export\n",
    "Now we'll dump the clean dataframe into an SQLite Database so we can answer our business questions using SQL in the next stage."
   ]
  },
  {
   "cell_type": "code",
   "execution_count": None,
   "metadata": {},
   "outputs": [],
   "source": [
    "# Connect to SQLite (this generates the db file in the /sql folder)\n",
    "conn = sqlite3.connect('../sql/customer_db.sqlite')\n",
    "\n",
    "# Write the dataframe to SQL\n",
    "df.to_sql('customer_shopping_data', conn, if_exists='replace', index=False)\n",
    "\n",
    "# Test query to verify successful export\n",
    "test_query = pd.read_sql(\"SELECT * FROM customer_shopping_data LIMIT 5\", conn)\n",
    "display(test_query)\n",
    "\n",
    "conn.close()\n",
    "print(\"✅ Data successfully exported to customer_db.sqlite! Proceed to customer_behavior_sql_queries.sql to run the analysis queries.\")"
   ]
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "name": "python",
   "version": "3.8.0"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 4
}

with open('../notebooks/Customer_Shopping_Behavior_Analysis.ipynb', 'w') as f:
    json.dump(notebook, f, indent=1)

print("Notebook generated successfully!")
