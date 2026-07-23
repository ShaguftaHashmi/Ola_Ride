use ola;
show tables;

SELECT 
    *
FROM
    ola_data;
ALTER TABLE ola_data
MODIFY COLUMN Date DATE,
MODIFY COLUMN Time  TIME,
MODIFY COLUMN Booking_id VARCHAR(20),
MODIFY COLUMN Customer_ID  VARCHAR(20),
MODIFY COLUMN V_TAT  int,
MODIFY COLUMN C_TAT  int;
describe ola_data;
ALTER TABLE ola_data
MODIFY COLUMN Customer_Rating float,
MODIFY COLUMN Driver_Ratings  float;

/*1. Retrieve all successful bookings:*/
SELECT 
    *
FROM
    ola_data
WHERE
    booking_status = 'Success';

/*2.Find the average ride distance for each vehicle type:*/
SELECT 
    vehicle_type, AVG(ride_distance) AS average_distance
FROM
    ola_data
GROUP BY vehicle_type;

/*3.Get the total number of cancelled rides by customers*/
SELECT 
    Canceled_Rides_by_Customer, COUNT(*) AS total
FROM
    ola_data
WHERE
    Canceled_Rides_by_Customer IS NOT NULL
GROUP BY Canceled_Rides_by_Customer;
/*4. List the top 5 customers who booked the highest number of rides*/

SELECT 
    Customer_ID, COUNT(*) AS total_rides
FROM
    ola_data
GROUP BY Customer_ID
ORDER BY total_rides DESC
LIMIT 5;

/*5. Get the number of rides cancelled by drivers due to personal and car-related issues:*/
SELECT 
    Canceled_Rides_by_Driver, COUNT(*) AS total
FROM
    ola_data
WHERE
    Canceled_Rides_by_Driver = 'Personal & Car related issue'
GROUP BY Canceled_Rides_by_Driver;

/*6. Find the maximum and minimum driver ratings for Prime Sedan bookings:*/

SELECT 
    MAX(driver_ratings) AS top_rating,
    MIN(driver_ratings) AS least_rating
FROM
    ola_data
WHERE
    vehicle_type = 'Prime Sedan';
/*7. Retrieve all rides where payment was made using UPI:*/
SELECT 
    *
FROM
    ola_data
WHERE
    payment_method = 'upi';
 
/*8. Find the average customer rating per vehicle type:*/
SELECT 
    vehicle_type, AVG(customer_rating)
FROM
    ola_data
GROUP BY vehicle_type;
/*9.Calculate the total booking value of rides completed successfully*/

SELECT 
    SUM(Booking_Value) AS total_booking_value
FROM
    ola_data
WHERE
    Booking_Status = 'Success';

/*10.List all incomplete rides along with the reason*/

SELECT 
    Booking_ID,
    Booking_Status,
    Incomplete_Rides,
    Incomplete_Rides_Reason
FROM
    ola_data
WHERE
    Incomplete_Rides = 'Yes';