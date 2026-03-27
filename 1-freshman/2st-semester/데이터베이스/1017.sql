use testdb;

drop table 사원;

# 사원(사원번호,사원명,연락처,생일)
CREATE TABLE 사원 (
    사원번호     char(4) ,
    사원명        varchar(20) , 
    연락처        char(13) ,
    생일           varchar(15)  ,
    
    PRIMARY KEY(사원번호)
);

select * from 사원;

insert into 사원(사원번호, 사원명, 연락처) values('D001', '정지영', '');
insert into 사원(사원번호, 사원명, 연락처, 생일) values('D002', '김선주', '010-1111-1111', null);
insert into 사원(사원번호, 사원명, 연락처, 생일) values('D003', '정성호', null, '10월04일');

----------------------------------------------------------------------

# create database studydb;
use studydb;

drop table 학생;
drop table 과목;
drop table 수강;

create table 학생(
	학번 char(4) not null,
    학생명 char(10),
    학년 int,
    
    primary key(학번)
);

create table 과목(
    과목번호 char(10) not null,
    과목명 char(20),
    
    primary key(과목번호)
);

create table 수강(
	학번 char(4) not null,
    과목번호 char(10) not null,
    성적 int,
    
    primary key(학번, 과목번호),
    
    foreign key(학번)
		references 학생(학번),
    
    foreign key(과목번호)
		references 과목(과목번호)
);

insert into 학생 values('1111','홍길동', 1);
insert into 학생 values('2222','김윤식', 3);
insert into 학생 values('3333','이정진', 2);
insert into 학생 values('4444','홍진아', 1);

insert into 과목 values('CS100','데이터베이스');
insert into 과목 values('CS101','운영체제');
insert into 과목 values('CS102','자료구조');

insert into 수강 values('1111','CS100',98);
insert into 수강 values('1111','CS102',88);
insert into 수강 values('2222','CS102',90);
insert into 수강 values('3333','CS100',92);

select * from 학생;
select * from 과목;
select * from 수강;