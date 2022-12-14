CREATE TABLE a (
	aid serial PRIMARY KEY,
	aval VARCHAR ( 50 )
);

CREATE TABLE b (
	bid serial PRIMARY KEY,
	bval VARCHAR ( 50 )
);

insert into a values ('1');
insert into a values ('2', '2');
insert into a values ('3');
insert into a values ('4', '4');

insert into b values ('1');
insert into b values ('2', '2');
insert into b values ('5');
insert into b values ('6', '6');

select * from a;
select * from b;

select * from a inner join b on a.aid = b.bid;
select * from a join b on a.aid = b.bid;

-- svak sa svakim
select * from a cross join b;

select * from a full outer join b on a.aid = b.bid;

select * from a left join b on a.aid = b.bid;
select * from a right join b on a.aid = b.bid;

select * from a where a.aval in ('2', '7')
select * from a join b on a.aid = b.bid where a.aval in ('2');
