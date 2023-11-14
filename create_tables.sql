
create table stock (
    id serial primary key,
    symbol text not null,
    name text not null,
    exchange text not null,
    is_etf boolean not null
);

create table etf_holding (
    etf_id integer not null,
    holding_id integer not null,
    dt date not null,
    shares numeric,
    weight numeric,
    primary key(etf_id,holding_id,dt),
    constraint fk_etf foreign key (etf_id) references stock (id),
    constraint fk_holding foreign key (holding_id) references stock (id)
);

create table stock_price (
    stock_id integer not null,
    dt timestamp without time zone not null,
    open numeric not null,
    high numeric not null,
    low numeric not null,
    close numeric not null,
    volume numeric not null,
    primary key(stock_id,dt),
    constraint fk_stock foreign key (stock_id) references stock (id)
);

create index on stock_price (stock_id, dt DESC);

select create_hypertable ('stock price','dt')

update stock set is_etf = true
where symbol in ('ARKK','ARKQ','ARKG','ARKF','ARKW')
