use apexleaderboard$leaderboard;

drop table if exists record;
drop table if exists fencer;

create table fencer (
    fencer_id bigint not null primary key,
    first_name varchar(50) not null,
    middle_name varchar(50),
    last_name varchar(50) not null,
    active int not null)
ENGINE = InnoDB;


create table record (
    id int auto_increment not null primary key,
    fencer_id bigint not null,
    tournament_name varchar(100) not null,
    tournament_type varchar(8) not null,
    tournament_date date,
    event_type varchar(10) not null,
    fencer_place smallint unsigned not null,
    num_competitors smallint unsigned not null,
    rating_pctg tinyint unsigned not null,
    index(fencer_id),
    foreign key (fencer_id) references fencer(fencer_id)
        on update cascade
        on delete cascade
        )
ENGINE = InnoDB;