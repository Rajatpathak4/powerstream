-- Alter weather table
-- depends: 

Alter table weather_data add column if not exists data_date date NOT NULL;
Alter table weather_data add column if not exists revision_no Integer NULL;


