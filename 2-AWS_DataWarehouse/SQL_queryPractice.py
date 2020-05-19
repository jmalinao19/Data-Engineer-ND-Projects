# Query Practice From Sample Database in 3NF (Paglia --> link: https://github.com/devrimgunduz/pagila) see picture in repo for visualization


# Create Paglia DB and Load data
# Run this in shell  
!PGPASSWORD = student createdb -h 127.0.0.1 -U student Paglia
!PGPASSWORD = student psql -q -h 127.0.0.1 -U student -d paglia -f Data/pagila-schema.sql
!PGPASSWORD=student psql -q -h 127.0.0.1 -U student -d pagila -f Data/pagila-data.sql


# Connect to createdDB from above

%load_ext sql # load ipython SQL

db_endpoint = '127.0.0.1' 
db = 'pagila'
db_user = 'student'
db_password = 'student'
db_port = '5432'

conn = "postgresql://{}:{}@{}:{}/{}"format.(db_user,db_password,db_endpoint,db_port,db)
print(conn)


%sql $conn # Connect to DB



#### Explore Data Base #### 
# Look at Size/Counts of Data 

nStores = %sql select count(*) from store;
nFilms = %sql select count(*) from film;
nCustomers = %sql select count(*) from customer;
nRentals = %sql select count(*) from rental;
nPayment = %sql select count(*) from payment;
nStaff = %sql select count(*) from staff;
nCity = %sql select count(*) from city;
nCountry = %sql select count(*) from country;

print("nFilms\t\t=", nFilms[0][0])
print("nCustomers\t=", nCustomers[0][0])
print("nRentals\t=", nRentals[0][0])
print("nPayment\t=", nPayment[0][0])
print("nStaff\t\t=", nStaff[0][0])
print("nStores\t\t=", nStores[0][0])
print("nCities\t\t=", nCity[0][0])
print("nCountry\t\t=", nCountry[0][0])

# Check Time Period 
%SQL select min(payment_date) as start, max(payment_date) as end from payment;



# Where Is this happening? i.e query for number of addresses by district,  
%%SQL
    SELECT district,count(address) as n
    FROM address
    GROUP BY district
    ORDER BY n DESC
    LIMIT 10; # Show top 10

