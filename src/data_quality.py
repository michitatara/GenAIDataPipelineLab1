import pandas as pd
import sqlite3 as sql

##starting python code##
#print("Starting data quality pipeline")

#read the csv using pandas into df var
df = pd.read_csv('C:\\Users\\torte\\Documents\\Self studying\\Professional Coding Projects\\GenAIDataPipelineLab1\\data\\monitoring_metrics.csv')

#Get the row and columns as a tuple and save it using df.shape
dimensions = df.shape
#print(dimensions)

#displays column types and non-null counts using df.info
info = df.info
#print(info)

#displays first 5 rows of table using df.head
head = df.head
#print(head)

#Count the non null values per column
nonnull = df.count
#print(nonnull)

#Count the missing values with df.isna, then sum it with sum
missing = df.isna().sum()
#print(missing)

#display duplicated rows without removing them from the dataframe. df.duplicate
#marks all occurences of duplicate rows. df filters the dataframe to keep only
#rows marked as true. keep false keeps both duplicate copies
duplicate = df[df.duplicated(keep=False)]
#print(duplicate)

#take the value column and count how many null values are there using isna().sum()
#isna=isnull
nullval = df['value'].isna().sum()
#print(nullval)

#use drop duplicate to drop duplicate values. use dropna to drop all duplicate values
#in the values column. dropna=drop null
cleaned = df.drop_duplicates().dropna(subset=['value'])
#print(cleaned)

#count the amount of rows using len and save it in rowcount
rowcount = len(df)
#print(df)

#counts the duplicate rows without removing them 
duplicatecount = df.duplicated().sum()
#print(duplicatecount)

#look in the value column and count how many are missing
missingval = df['value'].isna().sum()
#print(missingval)

#print the cleaned dataframe dimensions
cleandimensions = cleaned.shape
#print(cleandimensions)

#first initialise a list of the columns you want to see
columns = ['team', 'service', 'metric', 'timestamp']
#from the entire list show me these four columns.any() checks
#whether at least one value is true. axis=1 tells pandas to check accross 
#columns in each row. It is asking whether any required field is missing
#in each record. axis=0 checks down each column
missingcolumns = df[columns].isna().any(axis=1)
#print(missingcolumns)


###starting sql practice###
#sql.connect is a sql function to connect through alias to the location you set
#for your sql. conn stores it
conn = sql.connect("data/monitoring.db")

#Load cleaned dataframe into a sql table. create a new table and load it in the sql
cleaned.to_sql( #writes the dataframe you made into a variable
    "monitoring_metrics", #the name of the table you are creating
    conn, #the sqlite connection to data/monitoring.db
    if_exists="replace", #replaces the table if it already exists
    index=False #prevents pandas from saving its dataframe row numbers as an extra column
)

#to perform sql in a python file, you make a variable and store the sql text in "".
#"" make it a python string. 
selectall = "select * from monitoring_metrics"
#then you make another variable and perform read query on it to do the sql, it takes
#two arguments, the sql query variable and database connection variable
sqldf = pd.read_sql_query(selectall,conn)
#pass the variable to the print
#print(sqldf)

#in order to find the average of the dataset, you need to pass in the value column.
#to answer avg per service you have to group by service and in sql group by comes after from
#to have service listed as well, you need select service. 
avg = "select service, avg(value) as avgcol from monitoring_metrics group by service" 
#then you had to use the sql read from pandas and pass in the query and connection variable
sql2df = pd.read_sql_query(avg, conn)
#pass the variable to the print
#print(sql2df)

#for count, you select the column name you want to display and the count of the values
#and then you group by environment.
count = "select environment, count(value) as countcol from monitoring_metrics group by environment"
#then you use read query and enter the sql query and db connection as the arguments
sql3df = pd.read_sql_query(count, conn)
#then you pass the variable to print to print it
print(sql3df)

#convert df to csv with to_csv, put the new filename and index=false so pandas doesn't
#add another row for index.
cleaned.to_csv('data/monitoring_metrics_clean.csv', index=False)
conn.close()

print("Analysis complete.")
print("# of raw records: ", nonnull)
#len returns the number of rows in the dataframe.
cc = len(cleaned)
print("# of clean records: ", cc)
print("# of duplicates: ", duplicatecount)
print("Missing columns: ", missingcolumns)

#to export findings into a csv, first declare a dictionary with the key and values you fund
cleandict = {
    "nonnull": nonnull,
    "cc": cc,
    "duplicatecount": duplicatecount,
    "missingcolumns": missingcolumns
}

#now take the dictionary and convert it to a df using pd and save it in summarydf
summarydf = pd.DataFrame(cleandict)
#call to_csv on the new df you created
summarydf.to_csv('data/summary_monitoring_metrics.csv', index=False)


