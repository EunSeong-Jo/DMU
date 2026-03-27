use testdb;

create table 직원(
	이름 varchar(20) not null,
    주소 varchar(100),
    전화번호 char(13) not null,
    연봉 int default 0,
    
    primary key(이름)
);

select * from 직원;

INSERT INTO 직원 VALUES('우태하','서울시 서초구','010-1111-1111',1000);
INSERT INTO 직원 VALUES('김선우','서울시 구로구','010-2222-2222',2000);
INSERT INTO 직원 VALUES('이영지','서울시 마포구','010-3333-3333',3000);
INSERT INTO 직원 VALUES('유희정','서울시 마포구','010-4444-4444',4000);
INSERT INTO 직원 VALUES('오형준','부산시 연산구','010-5555-5555',5000);
INSERT INTO 직원 VALUES('고진수','서울시 구로구','010-6666-6666',6000);

drop view 직원_뷰;
create view 직원_뷰 as select 이름, 전화번호 from 직원;

select * from 직원_뷰;