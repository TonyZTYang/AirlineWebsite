-- Zetong Yang, zy891
insert into airline values
('china eastern');

insert into airport values
('jfk','nyc'),
('pvg','shanghai');

insert into customer values 
("jack@gmail.com", "Jack Smith", 'adfasf', '40', 'Marine Dr.', 'Philadelphia',
'Pennsylvania', '7784567364', 'NJ8539245', '2020-05-23', 'USA', '1980-04-10'),
 ("Makoto@gmail.com", "Makoto Taro", 'asdfas', '11', 'Jaclson st.', 'Tokyo',
'Tokyo', '7384746378', 'MU65547', '2023-01-22', 'Japan', '1989-03-16');

insert into airplane values
(12345,300,'china eastern'),
(67890,400,'china eastern');

insert into airline_staff values
('asdfa','asdfadf','tony','yang','1997-9-1','china eastern'),
('abc@123.com','abcd','t','y','1997-09-01','china eastern');

insert into flight values
(1,'2019-11-5 11:12:12','2019-11-6 10:00:00',125,'on-time','china eastern',12345,'jfk','pvg'),
(3,'2019-12-20 11:11:11','2019-12-22 11:11:11',150,'delayed','china eastern',12345,'pvg','jfk'),
(2,'2019-11-11 11:11:11','2019-11-12 11:11:11',150,'delayed','china eastern',67890,'pvg','jfk');

insert into booking_agent values
('asdf@sd.com','safasef','1');

insert into ticket values
('1','131','credit','123423134','tony yang','2024-1-1','2019-11-4','12:23:34','1','2019-11-5 11:12:12','china eastern','jack@gmail.com','1'),
('2','145','credit','123452345','yang tony','2024-1-1','2019-11-3','12:21:34','1','2019-11-5 11:12:12','china eastern','jack@gmail.com',NULL);
