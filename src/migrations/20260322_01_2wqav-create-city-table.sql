-- Create city table
-- depends: 

create table if not exists cities (
    id serial primary key,
    city_id  int8 NOT NULL,
    city_name varchar(255) not null,
    created_at timestamp with time zone default now(),
    updated_at timestamp with time zone default now(),
    is_deleted boolean default false
)