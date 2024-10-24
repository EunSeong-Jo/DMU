use testdb;

drop table if exists 주소록;

create table 주소록(
	번호 int auto_increment not null,
    이름 char(10),
    전화번호 char(20),
    주소 varchar(20),
    생일 varchar(20),
    
	primary key(번호)
);

select * from 주소록;
desc 주소록;

insert into 주소록(번호, 이름, 전화번호, 주소, 생일) values (5, '홍길동', '010-1234-5678', '서울', '1월1일');
insert into 주소록(이름, 전화번호, 주소, 생일) values ('이몽룡', '010-9876-5432', '부산', '2월2일');
insert into 주소록(번호, 이름, 전화번호, 주소, 생일) values (1, '최용만', '010-0391-5432', '대전', '3월3일');
insert into 주소록(이름, 전화번호, 주소, 생일) values ('이건우', '010-3817-3198', '경기', '5월5일');

# safe mode 해제
set sql_safe_updates = 0;
SET SQL_SAFE_UPDATES = 0;

# 칸 단위 조작
update 주소록 set 전화번호='000-0000-0000' where 이름='홍길동';
update 주소록 set 주소='남한', 생일='0월0일' where 번호=7;

# 줄 단위 조작
delete from 주소록 where 이름='이몽룡';