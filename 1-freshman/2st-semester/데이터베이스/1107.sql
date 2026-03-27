use homework;

drop table if exists 사원;
drop table if exists 부서;

CREATE TABLE 부서 (
    부서번호  INT            NOT NULL ,
    부서이름  VARCHAR(10)   ,
    PRIMARY KEY (부서번호)
);

CREATE TABLE 사원 (
    사원번호  INT            NOT NULL ,
    사원이름  VARCHAR(10)   , 
    소속부서  INT  , 
    PRIMARY KEY (사원번호) ,   
    FOREIGN KEY (소속부서)
        REFERENCES 부서(부서번호)
);

-- 부서(부서번호 pk, 부서이름)
-- 사원(사원번호 pk, 사원이름, 소속부서 fk)
insert into 부서 values(1,'인사부');
insert into 부서 values(2,'연구부');
insert into 부서 values(3,'홍보부');

insert into 사원 values(1001,'홍길동',3);
insert into 사원 values(1002,'임꺽정',1);
insert into 사원 values(1003,'차명석',1);

select * from 부서;
select * from 사원;

-- 1) 부서번호 3인 홍보부를 삭제하라 (오류 : 자식테이블 참조)
delete from 부서 where 부서번호 = 3;

-- 2) 임꺽정 소속부서를 5로 수정하라 (오류 : 부모테이블 값 없음)
update 사원 set 소속부서='5' where 사원이름='임꺽정';

-- 3) 부서번호 1을 부서번호 9로 수정하라 (오류 : 자식테이블 참조)
update 부서 set 부서번호 = '9' where 부서번호='1';

-- 4) 부서 테이블에 새로운 레코드를 입력하라
insert into 부서 values(4 , '데이터베이스부');

-- 5) 사원 테이블에서 차명석을 삭제하라 (오류 : 세이프모드)
SET SQL_SAFE_UPDATES = 0;
delete from 사원 where 사원이름='차명석';

---------------------------------------

drop table if exists 사원;
drop table if exists 부서;

CREATE TABLE 부서 (
    부서번호  INT            NOT NULL ,
    부서이름  VARCHAR(10)   ,
    PRIMARY KEY (부서번호)
);

CREATE TABLE 사원 (
    사원번호  INT            NOT NULL ,
    사원이름  VARCHAR(10)   , 
    소속부서  INT  , 
    PRIMARY KEY (사원번호) ,   
    FOREIGN KEY (소속부서)
        REFERENCES 부서(부서번호)
        ON DELETE no action
);

insert into 부서 values(1,'인사부');
insert into 부서 values(2,'연구부');
insert into 부서 values(3,'홍보부');

insert into 사원 values(1001,'홍길동',3);
insert into 사원 values(1002,'임꺽정',1);
insert into 사원 values(1003,'차명석',1);

-- no action
delete from 부서 where 부서번호 = 3;

---------------------------------------

drop table if exists 사원;
drop table if exists 부서;

CREATE TABLE 부서 (
    부서번호  INT            NOT NULL ,
    부서이름  VARCHAR(10)   ,
    PRIMARY KEY (부서번호)
);

CREATE TABLE 사원 (
    사원번호  INT            NOT NULL ,
    사원이름  VARCHAR(10)   , 
    소속부서  INT  , 
    PRIMARY KEY (사원번호) ,   
    FOREIGN KEY (소속부서)
        REFERENCES 부서(부서번호)
        ON DELETE cascade
);

insert into 부서 values(1,'인사부');
insert into 부서 values(2,'연구부');
insert into 부서 values(3,'홍보부');

insert into 사원 values(1001,'홍길동',3);
insert into 사원 values(1002,'임꺽정',1);
insert into 사원 values(1003,'차명석',1);

-- cascade
delete from 부서 where 부서번호 = 3;

select * from 부서;
select * from 사원;

---------------------------------------

drop table if exists 사원;
drop table if exists 부서;

CREATE TABLE 부서 (
    부서번호  INT            NOT NULL ,
    부서이름  VARCHAR(10)   ,
    PRIMARY KEY (부서번호)
);

CREATE TABLE 사원 (
    사원번호  INT            NOT NULL ,
    사원이름  VARCHAR(10)   , 
    소속부서  INT  , 
    PRIMARY KEY (사원번호) ,   
    FOREIGN KEY (소속부서)
        REFERENCES 부서(부서번호)
        ON DELETE set null
);

insert into 부서 values(1,'인사부');
insert into 부서 values(2,'연구부');
insert into 부서 values(3,'홍보부');

insert into 사원 values(1001,'홍길동',3);
insert into 사원 values(1002,'임꺽정',1);
insert into 사원 values(1003,'차명석',1);

-- set null
delete from 부서 where 부서번호 = 3;

select * from 부서;
select * from 사원;

---------------------------------------

drop table 고객;

CREATE TABLE 고객 (
      고객아이디    VARCHAR(20),
      고객이름       VARCHAR(10) not null,
      나이             INT,   
      등급             VARCHAR(10) not null,
      직업             VARCHAR(20),
      적립금          INT default 0, 
      PRIMARY KEY(고객아이디)
);

-- 테이블 구조 확인
DESC 고객;

---------------------------------------

drop table 제품;

CREATE TABLE 제품 (
      제품번호    CHAR(3),
      제품명      VARCHAR(20),
      재고량      INT,
      단가        INT,
      제조업체    VARCHAR(20),
      PRIMARY KEY(제품번호),
      CHECK('재고량' >= 0 and '재고량' <= 10000)
);

-- 테이블 구조 확인
DESC 제품;

---------------------------------------

drop table 주문;

CREATE TABLE 주문 (
       주문번호	CHAR(3)	NOT NULL,
       주문고객	VARCHAR(20),
       주문제품	CHAR(3),
       수량		INT,
       배송지		VARCHAR(30),
       주문일자	DATE,
       
       PRIMARY KEY(주문번호),
       FOREIGN KEY (주문고객)
			references 고객(고객아이디),
       FOREIGN KEY (주문제품)
			references 제품(제품번호)
);

desc 주문;