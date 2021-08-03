create database SARS_COV_2;
use SARS_COV_2;

drop table data_per_day;

create table data_per_day(
dateRep varchar(10),
day int(2),
month int(2),
year int(4),
cases int(7),
death int(7),
countriesAndTerritories varchar(20),
geoId varchar(2),
countryterritoryCode varchar(3),
popData2020 varchar(8),
continentExp varchar(6),
constraint PK_data_per_day primary key(dateRep,geoId)
);


create user 'machine'@'localhost' identified by '123456';
grant all privileges on SARS_COV_2.* to 'machine'@'localhost';
