CREATE TABLE IF NOT EXISTS users
(
    chat_id   bigint            not null
        constraint users_pk
            primary key,
    username  text,
    full_name text,
    adding_date   timestamp,
    id        serial            not null
);

alter table users
    owner to postgres;

create unique index users_id_uindex
    on users (id);

CREATE TABLE IF NOT EXISTS currency
(
    currency text not null,
    value real not null,
    id serial not null
);

alter table users
    owner to postgres;


CREATE TABLE IF NOT EXISTS last_request
(
    adding_date   timestamp,
    id serial not null
);