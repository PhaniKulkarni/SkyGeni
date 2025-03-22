#Import the libraries
import pandas as pd
import matplotlib.pyplot as plt

'''Stored the csv files in data_source folder, read the files from this folder using pandas read_csv function.
The data is stored in the respective dataframes
'''
industry_df = pd.read_csv(r"data_source\industry_client_details.csv")
financial_df = pd.read_csv(r"data_source\finanical_information.csv")
payment_df = pd.read_csv(r"data_source\payment_information.csv")
subscription_df = pd.read_csv(r"data_source\subscription_information.csv")
#Task1
'''
Filter the clients belonging to the "Finance Lending" and "Blockchain" industries using isin function
The shape function give the no of rows and columns in tuple format, so to get the number of records, select the 0 index
'''
finance_blockchain_clients=industry_df[industry_df['industry'].isin(["Finance Lending", "Blockchain"])]
print("TASK1 OUTPUT:"+"\n"+"Number of Finance Lending and Blockchain clients:",finance_blockchain_clients.shape[0])

#Task2
'''
Convert the "renewed" column to boolean type as it is of string type.
Filter only renewed subscriptions. Merge with industry data. Using value_counts gives the count of each unique industry
'''
subscription_df["renewed"] = subscription_df["renewed"].astype(bool)  # Ensure boolean conversion
renewed_clients = subscription_df[subscription_df["renewed"]]
renewal_counts = renewed_clients.merge(industry_df, on="client_id")["industry"].value_counts()
print("TASK2 OUTPUT:"+"\n"+"Renewal Counts"+"\n",renewal_counts)
print("Industry with the highest renewal rate", renewal_counts.idxmax())

#Task3
'''
Join the subscription data (only renewed subscriptions) with financial data
Calculate the average(using mean function) inflation rate from the merged data
'''
subscription_df["start_date"] = pd.to_datetime(subscription_df["start_date"])
subscription_df["end_date"] = pd.to_datetime(subscription_df["end_date"])
financial_df["start_date"] = pd.to_datetime(financial_df["start_date"])
financial_df["end_date"] = pd.to_datetime(financial_df["end_date"])

renewed_subscriptions = subscription_df[subscription_df["renewed"]].merge(financial_df, on="start_date")
print("TASK3 OUTPUT:"+"\n"+"Renewed subscriptions: ",renewed_subscriptions)
avg_inflation_rate = renewed_subscriptions["inflation_rate"].mean()
print("\n"+"Average inflation rate when subscriptions were renewed: ",avg_inflation_rate)

#Task4
'''
Convert "payment_date" column to datetime format
Extract the year from payment dates
Group by year and calculate the median payment amount for each year
'''
payment_df["payment_date"] = pd.to_datetime(payment_df["payment_date"])
payment_df["year"] = payment_df["payment_date"].dt.year
median_payment_per_year = payment_df.groupby("year")["amount_paid"].median()

print("TASK4 OUTPUT:"+"\n"+"Median amount paid each year:"+"\n",median_payment_per_year)

median_payment_per_year.plot(kind="line", marker="o", title="Median Payment Amount per Year", color="green")
plt.xlabel("Year")
plt.ylabel("Median Amount Paid")
plt.show()


'''
OUTPUT:
PS C:\Users\kulka\Downloads\SkyGeni_Assessment> python Analysis.py
TASK1 OUTPUT:
Number of Finance Lending and Blockchain clients: 22
TASK2 OUTPUT:
Renewal Counts
 industry
Gaming             16
Finance Lending    12
Block Chain        11
Hyper Local         9
AI                  7
Name: count, dtype: int64
Industry with the highest renewal rate Gaming
TASK3 OUTPUT:
Renewed subscriptions:      client_id subscription_type start_date end_date_x  renewed  Unnamed: 0 end_date_y  inflation_rate  gdp_growth_rate
0  2315920532           Monthly 2019-04-01 2019-05-01     True           5 2019-06-30            3.84             3.48

Average inflation rate when subscriptions were renewed:  3.84
TASK4 OUTPUT:
Median amount paid each year:
 year
2018    235.7
2019    360.9
2020    284.5
2021    306.8
2022    288.0
Name: amount_paid, dtype: float64
'''