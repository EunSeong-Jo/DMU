create database booksrdb;

use booksrdb;

create table 학교(
    학교명 varchar(10) not null,
    분류 char(5),
    학생수 int,
    주소 varchar(50),

	primary key(학교명)
);

select * from 학교;

insert into 학교 values('송원고', '3', 435, '경기 성남 분당구 황새울로 123');
insert into 학교 values('한빛고', '2', 377, '경기 성남 분당구 판교역로 67');
insert into 학교 values('이슬고', '1', 507, '경기 성남 분당구 미금로 567');

create table 학원생(
	학원생이름 varchar(10),
    폰번호 varchar(20) not null,
    나이 char(3),
    학교이름 varchar(10),
    학년 int,
    반 char(2),
    반번호 char(2),

	foreign key (학교이름)
		references 학교(학교명),
    primary key (폰번호)
);

select * from 학원생;

insert into 학원생 values('홍길동', '010-1237-6542', '19', '송원고', 3, '1', '10');
insert into 학원생 values('김하나', '010-3218-8765', '18', '한빛고', 2, '2', '7');
insert into 학원생 values('홍길동', '010-4587-9834', '19', '송원고', 3, '1', '31');
insert into 학원생 values('박순희', '010-7789-6754', '17', '이슬고', 1, '3', '16');
