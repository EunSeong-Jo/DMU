use testdb;

drop table if exists R;
drop table if exists S;

CREATE TABLE R (
	A char(1) ,
	B char(1)
);

CREATE TABLE S (
	B char(1) ,
	C char(1)
);

INSERT INTO R VALUES ('a', '2');
INSERT INTO R VALUES ('b', '3');
INSERT INTO R VALUES ('c', '3');
INSERT INTO R VALUES ('d', '5');

INSERT INTO S VALUES ('1', 'x');
INSERT INTO S VALUES ('2', 'y');
INSERT INTO S VALUES ('3', 'z');

select * from r;
select * from s;

# 내부조인 : 일치하는 행
# 외부조인 : 불일치 행

# = 만 있으면 세타조인

# * : 동등조인
# a, R.b , c : 자연조인


select * from r,s where r.b = s.b;

select a, r.b, c from r, s where r.b = s.b;

select a, r.b, c from r left outer join s on r.b = s.b;

select a, s.b, c from r right outer join s on r.b = s.b;

select a, r.b, c from r left outer join s on r.b = s.b 
union 
select a, s.b, c from r right outer join s on r.b = s.b;


DROP TABLE if exists emp;

create table emp (
    empno       char(4) PRIMARY KEY ,
    empname   varchar(12) ,
    manager    char(4) ,
    dno          char(1) ,
    FOREIGN KEY (manager) REFERENCES emp(empno)
);

insert into emp values('3011','이수민',NULL,'1');
insert into emp values('3426','박영권','3011','3');
insert into emp values('1003','조민희','3011','1');
insert into emp values('2106','김창섭','3426','2');
insert into emp values('3427','최종철','2106','3');

select * from emp;

select e.empname as 사원명, m.empname as 직속상사명 from emp as e, emp as m where e.manager = m.empno;


DROP TABLE if exists 추천고객;

create table 추천고객 (
    고객아이디   char(20)    NOT NULL PRIMARY KEY ,
    고객이름     varchar(20)  ,
    나이         int ,
    등급         varchar(10) ,
    직업         varchar(10) ,
    적립금       int ,
    추천고객     char(20) ,
    foreign key(추천고객) references 추천고객(고객아이디)
);

-- 추천고객(고객아이디,고객이름,나이,등급,직업,적립금,추천고객)
insert into 추천고객 values('orange','정지영',22,'silver','학생',0, NULL);
insert into 추천고객 values('apple','김현준',20,'gold','학생',1000, 'orange');
insert into 추천고객 values('banana','정소화',25,'vip','간호사',2500, 'orange');
insert into 추천고객 values('carrot','원유선',28,'gold','교사',4500, 'apple');

select * from 추천고객;

select 고객1.고객이름 as 고객명, 고객2.고객이름 as 추천고객명 from 추천고객 as 고객1, 추천고객 as 고객2 where 고객1.추천고객 = 고객2.고객아이디;



drop table if exists employee;
drop table if exists department;

CREATE TABLE department (
     deptno              int          NOT NULL ,
     deptname          varchar(10) ,
     floor                 int ,
     PRIMARY KEY(deptno)
);

INSERT INTO department VALUES(1, '영업', 8);
INSERT INTO department VALUES(2, '기획', 10);
INSERT INTO department VALUES(3, '개발', 9);
INSERT INTO department VALUES(4, '총무', 7);

CREATE TABLE employee (
    empno	         int	              NOT NULL,
    empname     varchar(10)     UNIQUE,
    title	         varchar(10)     DEFAULT '사원',
    manager       int  ,
    salary            int	 ,
    dno              int	 ,
    PRIMARY KEY(empno),
    FOREIGN KEY(dno) REFERENCES department(deptno)
);

INSERT INTO employee VALUES(2106, '김창섭','대리',1003, 2500000, 2);
INSERT INTO employee VALUES(3426, '박영권','과장',4377, 3000000, 1);
INSERT INTO employee VALUES(3011, '이수민','부장',4377, 4000000, 3);
INSERT INTO employee VALUES(1003, '조민희','과장',4377, 3000000, 2);
INSERT INTO employee VALUES(3427, '최종철','사원',3011, 1500000, 3);
INSERT INTO employee VALUES(1365, '김상원','사원',3426, 1500000, 1);
INSERT INTO employee(empno, empname, title, salary, dno) VALUES(4377, '이성래','이사', 5000000, 2);

select * from department;
select * from employee;

select empname, title from employee where title = (select title from employee where empname = '박영권');

select empname, dno, salary from employee as e1 where salary > (select avg(salary) from employee as e2 where e1.dno = e2.dno);

select * from employee e1, employee e2 where e1.dno = e2.dno;



DROP TABLE if exists pro;
DROP TABLE if exists stu;

-- stu(sno, sname, dept, sage)
-- pro(pno, pname, dept, page)

CREATE TABLE pro (
    pno   char(2),
    pname varchar(20), 
    dept  varchar(20),
    page  int,
    primary key(pno)
);

CREATE TABLE stu (
    sno   char(2),
    sname varchar(20), 
    dept  varchar(20),
    sage  int,
    primary key(sno)
);

insert into pro values('p1','이정무','컴퓨터',36);
insert into pro values('p2','우태하','컴퓨터',32);
insert into pro values('p3','이성민','건축',45);

insert into stu values('s1','유준호','컴퓨터',23);
insert into stu values('s2','오정민','컴퓨터',34);
insert into stu values('s3','이태현','건축',22);
insert into stu values('s4','신현주','건축',21);

select * from pro;
select * from stu;

select sname, dept, sage from 