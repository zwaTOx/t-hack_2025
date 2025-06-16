create table tasks (
                       id bigint not null,
                       category varchar(255),
                       created_time timestamp(6),
                       deadline timestamp(6),
                       "desc" varchar(255),
                       name varchar(255),
                       updated_time timestamp(6),
                       user_id bigint,
                       primary key (id)
);
alter table if exists tasks
    add constraint FK6s1ob9k4ihi75xbxe2w0ylsdh
        foreign key (user_id)
            references users;
CREATE TABLE users(
    id BIGINT not null,
    username VARCHAR(128),
    primary key (id)
)