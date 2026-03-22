-- alter weather table
-- depends:


alter table weather_data add column if not exists city_id integer;
