-- Create table actual_data
-- depends: 

CREATE table if not exists actual_data(
    id Serial primary key,
    data_date date null,
    source varchar(255) null,
    actual_demand float null,
    file_name varchar(255) null,
    file_path varchar(255) null,
    created_at timestamp default now(),
    updated_at timestamp default now(),
    created_by integer null,
    updated_by integer null,
    is_deleted boolean default false
);

CREATE table if not exists actual_table_data(
    id Serial primary key,
    actual_data_id integer null,
    block_no integer null,
    block_value float null,
    CONSTRAINT fk_actual_data
        FOREIGN KEY (actual_data_id)
        REFERENCES actual_data (id)
        ON DELETE SET NULL
        ON UPDATE CASCADE
);


create index idx_actual_data_date on actual_data USING btree (data_date);