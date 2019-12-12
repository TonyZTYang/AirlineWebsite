-- Zetong Yang, zy891
insert into airline values
('china eastern');

insert into airport values
('jfk','nyc'),
('bos','boston'),
('bei','beijing'),
('shen','shenzhen'),
('sfo','san francisco'),
('lax','los angles'),
('hka','hong kong'),
('pvg','shanghai');

insert into airplane values
(1,4,'china eastern'),
(2,4,'china eastern'),
(3,50,'china eastern');

insert into flight values
(102,'2019-11-12 13:25:25','2019-11-12 16:50:25',300,'on-time','china eastern',3,'sfo','lax'),
(104,'2019-12-12 13:25:25','2019-12-12 16:50:25',300,'on-time','china eastern',3,'pvg','bei'),
(106,'2019-10-12 13:25:25','2019-10-12 16:50:25',350,'delayed','china eastern',3,'sfo','lax'),
(206,'2020-01-12 13:25:25','2020-01-12 16:50:25',400,'on-time','china eastern',2,'sfo','lax'),
(207,'2020-02-12 13:25:25','2020-02-12 16:50:25',300,'on-time','china eastern',2,'lax','sfo'),
(134,'2019-08-12 13:25:25','2019-08-12 16:50:25',300,'delayed','china eastern',3,'jfk','bos'),
(296,'2020-01-01 13:25:25','2020-01-01 16:50:25',3000,'on-time','china eastern',1,'pvg','sfo'),
(715,'2019-11-28 10:25:25','2019-11-28 13:50:25',500,'delayed','china eastern',1,'pvg','bei'),
(839,'2019-02-12 13:25:25','2019-02-12 16:50:25',300,'on-time','china eastern',1,'shen','bei');



insert into ticket 
(ticket_id,airline_name,flight_number,departure_time,customer_email,booking_agent_id,purchase_date,purchase_time,sold_price,card_type,card_number,name_on_card,Expiration_date)
values
(1,'china eastern',102,'2019-11-12 13:25:25','testcustomer@nyu.edu',1,'2019-10-12','11:55:55',300.0,'credit',1111222233334444,'Test Customer 1','2023-03-31'),
(2,'china eastern',102,'2019-11-12 13:25:25','user1@nyu.edu',NULL,'2019-10-11','11:55:55',300.0,'credit',1111222233335555,'User 1','2023-03-31'),
(3,'china eastern',102,'2019-11-12 13:25:25','user2@nyu.edu',NULL,'2019-11-11','11:55:55',300.0,'credit',1111222233335555,'User 2','2023-03-31'),
(4,'china eastern',104,'2019-12-12 13:25:25','user1@nyu.edu',NULL,'2019-10-21','11:55:55',300.0,'credit',1111222233335555,'User 1','2023-03-31'),
(5,'china eastern',104,'2019-12-12 13:25:25','testcustomer@nyu.edu',1,'2019-11-28','11:55:55',300.0,'credit',1111222233334444,'Test Customer 1','2023-03-31'),
(6,'china eastern',106,'2019-10-12 13:25:25','testcustomer@nyu.edu',1,'2019-10-05','11:55:55',350.0,'credit',1111222233334444,'Test Customer 1','2023-03-31'),
(7,'china eastern',106,'2019-10-12 13:25:25','user3@nyu.edu',NULL,'2019-09-03','11:55:55',350.0,'credit',1111222233335555,'User 3','2023-03-31'),
(8,'china eastern',839,'2019-02-12 13:25:25','user3@nyu.edu',NULL,'2019-02-03','11:55:55',300.0,'credit',1111222233335555,'User 3','2023-03-31'),
(9,'china eastern',102,'2019-11-12 13:25:25','user3@nyu.edu',NULL,'2019-09-03','11:55:55',360.0,'credit',1111222233335555,'User 3','2023-03-31'),
(11,'china eastern',134,'2019-08-12 13:25:25','user3@nyu.edu',2,'2019-02-23','11:55:55',300.0,'credit',1111222233335555,'User 3','2023-03-31'),
(12,'china eastern',715,'2019-11-28 10:25:25','testcustomer@nyu.edu',1,'2019-10-05','11:55:55',500.0,'credit',1111222233334444,'Test Customer 1','2023-03-31'),
(14,'china eastern',206,'2020-01-12 13:25:25','user3@nyu.edu',1,'2019-12-05','11:55:55',400.0,'credit',1111222233335555,'User 3','2023-03-31'),
(15,'china eastern',206,'2020-01-12 13:25:25','user1@nyu.edu',NULL,'2019-12-06','11:55:55',400.0,'credit',1111222233335555,'User 1','2023-03-31'),
(16,'china eastern',206,'2020-01-12 13:25:25','user2@nyu.edu',NULL,'2019-11-19','11:55:55',400.0,'credit',1111222233335555,'User 2','2023-03-31'),
(17,'china eastern',207,'2020-02-12 13:25:25','user1@nyu.edu',1,'2019-10-11','11:55:55',300.0,'credit',1111222233335555,'User 1','2023-03-31'),
(18,'china eastern',207,'2020-02-12 13:25:25','testcustomer@nyu.edu',1,'2019-11-25','11:55:55',300.0,'credit',1111222233334444,'Test Customer 1','2023-03-31'),
(19,'china eastern',296,'2020-01-01 13:25:25','user1@nyu.edu',2,'2019-12-04','11:55:55',3000.0,'credit',1111222233335555,'User 1','2023-03-31'),
(20,'china eastern',296,'2020-01-01 13:25:25','testcustomer@nyu.edu',NULL,'2019-09-12','11:55:55',3000.0,'credit',1111222233334444,'Test Customer','2023-03-31');

insert into comment values
(1,4,'Very Comfortable'),
(2,5,'Relaxing, check-in and onboarding very professional'),
(3,3,'Satisfied and will use the same flight again'),
(5,1,'Customer Care services are not good'),
(4,5,'Comfortable journey and Professional');



-- insert into booking_agent values
-- ('asdf@sd.com','safasef','1');

-- insert into ticket values
-- ('1','131','credit','123423134','tony yang','2024-1-1','2019-11-4','12:23:34','1','2019-11-5 11:12:12','china eastern','jack@gmail.com','1'),
-- ('2','145','credit','123452345','yang tony','2024-1-1','2019-11-3','12:21:34','1','2019-11-5 11:12:12','china eastern','jack@gmail.com',NULL);
