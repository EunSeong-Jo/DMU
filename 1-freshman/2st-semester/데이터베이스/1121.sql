use testdb;

-- [Quiz 1]  (MySQL) 실습: (fruit)

drop table if exists fruit;

create table fruit (
    과일번호 int NOT NULL,
    과일이름 varchar(30),
    가격 int,
    색상 char(12),
    원산지 varchar(30), 

    PRIMARY KEY(과일번호)

);

insert into fruit values('1','사과',2000,'빨간색','한국');
insert into fruit values('2','배',5000,'노란색','한국');
insert into fruit values('3','바나나',1500,'노란색','인도네시아');
insert into fruit values('4','키위',4000,'초록색','호주');
insert into fruit values('5','수박',8000,'초록색','한국');

select * from fruit;

-- 2-5) 색상이 노란색이거나 초록색인 과일이름, 색상을 검색하라(IN 사용)
select * from fruit where 색상 in ('노란색', '초록색');

-- 2-6) 색상이 노란색이거나 초록색인 과일이름, 색상을 검색하라(논리연산자 OR 사용)
select 과일이름, 색상 from fruit where 색상 ='노란색' or 색상 = '초록색';

-- 2-7) 원산지가 한국이 아닌 과일이름, 원산지를 검색하라
select 과일이름, 원산지 from fruit where 원산지 != '한국';


-- [Quiz 2]  (MySQL) 실습: (고객)

drop table if exists 고객;

create table 고객 (
    고객아이디 varchar(8) NOT NULL  ,
    고객이름 varchar(20) NOT NULL  ,
    나이 int ,
    등급 varchar(10) ,
    직업 varchar(20) , 
    적립금 int DEFAULT 0 ,
    PRIMARY KEY(고객아이디)

);

-- 고객(고객아이디,고객이름,나이,등급,직업,적립금)
insert into 고객 values('apple','정소화',20,'gold','학생',1000);
insert into 고객 values('banana','김선우',25,'vip','간호사',2500);
insert into 고객 values('carrot','고명석',28,'gold','교사',4500);
insert into 고객 values('orange','김용축',22,'silver','학생',NULL);
insert into 고객 values('melon','성원용',35,'gold','회사원',5000);
insert into 고객 values('peach','오형준',NULL,'silver','의사',300);
insert into 고객 values('pear','채광주',31,'silver','회사원',500);

select * from 고객;

-- 1) 직업이 학생, 간호사, 교사인 고객의 이름, 직업, 등급을 검색
select 고객이름, 직업, 등급 from 고객 where 직업 in ('학생', '간호사', '교사');

-- 2) 적립금이 300 이상인 고객 중에서 나이를 알 수 없는 고객아이디, 나이, 적립금을 검색하라
select 고객아이디, 나이, 적립금 from 고객 where 적립금 >= 300 and 나이 is null;

-- 3) 등급이 gold인 고객 중에서 고객아이디, 등급, 적립금을 검색하라. 단, 등급을 오름차순 정렬하고 등급이 같으면 적립금의 내림차순 정렬하라
select 고객아이디, 등급, 적립금 from 고객 where 등급 = 'gold' order by 등급 asc, 적립금 desc;