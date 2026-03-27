drop table if exists R1;
drop table if exists S1;

CREATE TABLE R1 (
	A int ,
	B int 
);

CREATE TABLE S1 (
	A int ,
	C int ,
             D int 
);

INSERT INTO R1 VALUES (1, 4);
INSERT INTO R1 VALUES (2, 5);

INSERT INTO S1 VALUES (1,3,4);
INSERT INTO S1 VALUES (2,2,6);
INSERT INTO S1 VALUES (3,1,9);

select * from r1;
select * from s1;


select * from r1, s1;

select * from r1, s1 where r1.a = s1.a;

select r1.a, b, c, d from r1, s1 where r1.a = s1.a;

select * from r1, s1 where r1.a >= c;


drop table if exists omember;
drop table if exists group_ex;

CREATE TABLE omember ( 
   id         CHAR(3)     NOT NULL ,
   groupid CHAR(1)
);

CREATE TABLE group_ex ( 
   groupid   CHAR(1)   NOT NULL ,
   position   VARCHAR(12)
);

INSERT INTO omember VALUES('100', 'A');
INSERT INTO omember VALUES('101', 'B');
INSERT INTO omember VALUES('102', 'A');
INSERT INTO omember VALUES('102', 'F');

INSERT INTO group_ex VALUES('A', '서울');
INSERT INTO group_ex VALUES('B', '대구');
INSERT INTO group_ex VALUES('C', '광주');
INSERT INTO group_ex VALUES('D', '부산');
INSERT INTO group_ex VALUES('E', '대전');

SELECT * FROM omember;
SELECT * FROM group_ex;

select * from omember, group_ex;

select * from omember, group_ex where omember.groupid = group_ex.groupid;

select id, omember.groupid, position from omember, group_ex where omember.groupid = group_ex.groupid;


select * from omember inner join group_ex on omember.groupid = group_ex.groupid;

select * from omember left outer join group_ex on omember.groupid = group_ex.groupid;

select * from omember right outer join group_ex on omember.groupid = group_ex.groupid;

select * from omember left outer join group_ex on omember.groupid = group_ex.groupid 
union 
select * from omember right outer join group_ex on omember.groupid = group_ex.groupid;

-- 

drop table if exists 정회원;
drop table if exists 준회원;
 
CREATE TABLE 정회원 (
    번호 		INT 	PRIMARY KEY  ,
    이름 		varCHAR(12) 	NOT NULL ,
    주민번호 	CHAR(14) 	NOT NULL ,
    휴대폰번호 	CHAR(14) 	NOT NULL,
    이메일 	VARCHAR(30) ,
    등록일 	CHAR(8)
);

CREATE TABLE 준회원 (
    번호 		INT 	PRIMARY KEY  ,
    이름 		varCHAR(12) 	NOT NULL ,
    주민번호 	CHAR(14) 	NOT NULL ,
    휴대폰번호 	CHAR(14) 	NOT NULL,
    이메일 	VARCHAR(30) ,
    등록일 	CHAR(8)
);

INSERT INTO 정회원 ( 번호, 이름, 주민번호, 휴대폰번호, 이메일, 등록일)
VALUES ( 1, '홍길동', '820416-1234567', '(011) 123-1231','gdhong@hitel.net','20070302');
INSERT INTO 정회원 ( 번호, 이름, 주민번호, 휴대폰번호, 이메일, 등록일)
VALUES ( 2, '임꺽정', '830507-2345678', '(010) 122-1222','jung@hanmail.net','20050422');
 
INSERT INTO 준회원 ( 번호, 이름, 주민번호, 휴대폰번호, 이메일, 등록일)
VALUES ( 1, '홍길동', '820416-1234567', '(011) 123-1231','gdhong@hitel.net','20070302');
INSERT INTO 준회원 ( 번호, 이름, 주민번호, 휴대폰번호, 이메일, 등록일)
VALUES ( 3, '박찬호', '850321-1456789', '(010) 133-1231','chpark@hanmail.net','20090512');
INSERT INTO 준회원 ( 번호, 이름, 주민번호, 휴대폰번호, 이메일, 등록일)
VALUES ( 4, '선동열', '761122-1889911', '(010) 144-1222','sun@naver.com','20080605');
 
SELECT * FROM 정회원;
SELECT * FROM 준회원;

select 이름, 이메일 from 정회원 union select 이름, 이메일 from 준회원;

select 이름, 이메일 from 정회원 union all select 이름, 이메일 from 준회원;

--

drop table if exists emp;
drop table if exists project;

CREATE TABLE emp ( 
    ename    VARCHAR(12)  NOT NULL ,
    pno       int
);

CREATE TABLE project ( 
   pno        int                  NOT NULL ,
   pname    VARCHAR(20)
);

INSERT INTO emp VALUES('홍길동', 101);
INSERT INTO emp VALUES('임꺽정', 102);
INSERT INTO emp VALUES('박찬호', 101);
INSERT INTO emp VALUES('박찬호', 103);
INSERT INTO emp VALUES('신동엽', NULL);

INSERT INTO project VALUES(101, '작전중');
INSERT INTO project VALUES(102, '특공대');
INSERT INTO project VALUES(103, '유레카');
INSERT INTO project VALUES(104, '다모여');

SELECT * FROM emp;
SELECT * FROM project;

-- 1) 카티션 프로덕트
select * from emp, project;

-- 2) 동등 조인
select * from emp, project where emp.pno = project.pno;

-- 3) 자연 조인
select ename, emp.pno, pname from emp, project where emp.pno = project.pno;

-- 4) 내부 조인
select * from emp inner join project on emp.pno = project.pno;

-- 5) 왼쪽 외부조인
select * from emp left outer join project on emp.pno = project.pno;

-- 6) 오른쪽 외부조인
select * from emp right outer join project on emp.pno = project.pno;

-- 7) 완전 외부조인
select * from emp left outer join project on emp.pno = project.pno
union 
select * from emp right outer join project on emp.pno = project.pno;