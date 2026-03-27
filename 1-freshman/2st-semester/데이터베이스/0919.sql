use testdb;

select * from 고객;
select 고객명, 거주지 from 고객;
select * from 고객 where 고객번호 ='c101';
select * from 고객 where 포인트 <= 400;

select * from 제품;
select 제품명, 재고량 from 제품;
select 제품명, 단가, 제조업체 from 제품 where 제조업체 = '대한식품';

# key 종류
# 기본키(Primary Key) : 중복 불가(PK), 필수 입력(NN)

create database studydb default character set utf8mb4;

use studydb;

create table 학과(
    학과번호 int,
    학과명 varchar(30),
    
    primary key(학과번호)
);

select * from 학과;

update 학과 set 학과명 = '컴소' where 학과번호 = 1;
insert into 학과 values(2, '컴정');
insert into 학과 values(3, '인소');



