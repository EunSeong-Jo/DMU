create database homework;

use homework;

create table 환자(
	환자번호 char(4) not null,
    환자이름 char(20),
	나이 char(3),
    담당의사 char(4),
    
    primary key(환자번호)
);

select * from 환자;

insert into 환자 values ('P001', '오우진', '31', 'D002');
insert into 환자 values ('P002', '채광주', '50', 'D001');
insert into 환자 values ('P003', '김용욱', '43', 'D003');

create table 의사(
	의사번호 char(4) not null,
    의사이름 char(20),
	소속 char(3),
    근무연수 char(4),
    
    primary key(의사번호),
    
    foreign key(의사번호)
		references 환자(담당의사)
);