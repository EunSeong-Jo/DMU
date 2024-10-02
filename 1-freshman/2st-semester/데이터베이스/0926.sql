use testdb;

drop table 학과;

create table 학과(
    학과번호 int not null,
    학과명 varchar(50),
    
    primary key(학과번호)
);

select * from 학과;

insert into 학과 values(1, '컴퓨터소프트웨어공학과');
insert into 학과 values(2, '컴퓨터정보공학과');
insert into 학과 values(3, '인공지능소프트웨어과');

-------------------------------------------

drop table member_tbl;

create table member_tbl(
    C_NO char(5),
    C_NAME varchar(15),
    PHONE varchar(11),
    ADDRESS varchar(50),
    GRADE varchar(6),
    
    primary key(C_NO)
);

select * from member_tbl;

insert into member_tbl values ('10001', '홍길동', '01011112222', '서울시 강남구', '일반');
insert into member_tbl values ('10002', '장발장', '01022223333', '성남시 분당구', '일반');
insert into member_tbl values ('10003', '임꺽정', '01033334444', '대전시 유성구', '일반');
insert into member_tbl values ('20001', '성춘향', '01044445555', '부산시 서구', 'VIP');
insert into member_tbl values ('20002', '이몽룡', '01055556666', '대구시 북구', 'VIP');

-------------------------------------------

create table 제품(
    제품번호 char(3) not null,
    제품명 varchar(20),
    재고량 int,
    단가 int,
    제조업체 varchar(20),
    
    primary key(제품번호)
);

select * from 제품;

insert into 제품 values('p01', '그냥만두', 5000, 4500, '대한식품');
insert into 제품 values('p02', '매운쫄면', 2500, 5500, '민국푸드');
insert into 제품 values('p03', '쿵떡파이', 3600, 2600, '한빛제과');
insert into 제품 values('p04', '맛난초콜렛', 1250, 2500, '한빛제과');
insert into 제품 values('p05', '얼큰라면', 2200, 1200, '대한식품');

-------------------------------------------

drop table 학생;

create table 학생(
    번호 int not null,
    이름 varchar(12),
    학년 int,
    분반 char(2),
    학과번호 int,
    
    foreign key(학과번호)
    references 학과(학과번호),
    
    primary key(번호)
);

select * from 학생;

insert into 학생 values(1, '한지혜', 1, 'YB', 1);
insert into 학생 values(2, '이정우', 1, 'YA', 1);
insert into 학생 values(3, '오지영', 2, 'J1', 2);
insert into 학생 values(4, '강재미', 1, 'YB', 1);
insert into 학생 values(5, '박철호', 2, 'J1', 2);