-- ch5 SQL ("SQL과 NoSQL 기반의 데이터베이스 입문", 박성진, 생능
-- (MySQL)
-- handb 데이터베이스 존재할 경우, 데이터베이스 삭제
drop database if exists univDB;

-- 교재 5장 스키마 생성
CREATE DATABASE `univDB` 
  DEFAULT CHARACTER SET utf8mb4;

-- 사용할 데이터베이스 선택
use univDB;

DROP TABLE if exists 수강;
DROP TABLE if exists 과목;
DROP TABLE if exists 학생;

-- 과목(과목번호, 이름, 강의실, 개설학과, 시수)
-- 학생(학번, 이름, 주소, 학년, 나이, 휴대폰번호, 소속학과)
-- 수강(학번, 과목번호, 신청날짜, 중간성적, 기말성적, 평가학점)

CREATE TABLE 과목 (
	  과목번호 char(4)            NOT NULL     PRIMARY KEY , 
	  이름       VARCHAR(20)   NOT NULL , 
	  강의실    CHAR(3)          NOT NULL ,
	  개설학과 VARCHAR(20)   NOT NULL ,
	  시수       INT                 NOT NULL 
) ; 

CREATE TABLE 학생 (
	  학번       CHAR(4)           NOT NULL ,
	  이름       VARCHAR(20)    NOT NULL ,
	  주소       VARCHAR(50)     DEFAULT '미정' , 
	  학년       INT                  NOT NULL ,
	  나이       INT  ,
	  성별       CHAR(1)           NOT NULL ,
	  휴대폰번호  CHAR(14) , 
                소속학과    VARCHAR(20) ,
	  PRIMARY KEY (학번) 
) ; 

CREATE TABLE 수강 (
	  학번        char(6)            NOT NULL ,
	  과목번호  CHAR(4)          NOT NULL ,
	  신청날짜   DATE             NOT NULL ,
	  중간성적   INT                  DEFAULT 0 ,
	  기말성적   INT                  DEFAULT 0 , 
	  평가학점   CHAR(1) ,        
	  PRIMARY KEY(학번, 과목번호) 
) ; 

-- 학생 테이블 입력
INSERT INTO 학생
VALUES ('s001', '김연아', '서울 서초', 4, 23, '여', '010-1111-2222',  '컴퓨터') ;
INSERT INTO 학생
VALUES ('s002', '홍길동', DEFAULT, 1, 26, '남', NULL,  '통계') ;
INSERT INTO 학생
VALUES ('s003', '이승엽', NULL, 3, 30, '남', NULL,  '정보통신') ;
INSERT INTO 학생
VALUES ('s004', '이영애', '경기 분당', 2, NULL, '여', '010-4444-5555', '정보통신') ;
INSERT INTO 학생
VALUES ('s005', '송윤아', '경기 분당', 4, 23, '여', '010-6666-7777', '컴퓨터') ;
INSERT INTO 학생
VALUES ('s006', '홍길동', '서울 종로', 2, 26, '남', '010-8888-9999', '컴퓨터') ;
INSERT INTO 학생
VALUES ('s007', '이은진', '경기 과천', 1, 23, '여', '010-2222-3333', '경영') ;

-- 과목 테이블 입력
INSERT INTO 과목
VALUES ('c001', '데이터베이스', 126, '컴퓨터', 3) ;
INSERT INTO 과목
VALUES ('c002', '정보보호', 137, '정보통신', 3) ;
INSERT INTO 과목
VALUES ('c003', '모바일웹', 128, '컴퓨터', 3) ;
INSERT INTO 과목
VALUES ('c004', '철학개론', 117, '철학', 2) ;
INSERT INTO 과목
VALUES ('c005', '전공글쓰기', 120, '교양학부', 1) ;

-- 수강 테이블 입력
INSERT INTO 수강
VALUES ('s001', 'c002', '2019-09-03', 93, 98, 'A') ;
INSERT INTO 수강
VALUES ('s004', 'c005', '2019-03-03', 72, 78, 'C') ;
INSERT INTO 수강
VALUES ('s003', 'c002', '2017-09-06', 85, 82, 'B') ;
INSERT INTO 수강
VALUES ('s002', 'c001', '2018-03-10', 31, 50, 'F') ;
INSERT INTO 수강
VALUES ('s001', 'c004', '2019-03-05', 82, 89, 'B') ;
INSERT INTO 수강
VALUES ('s004', 'c003', '2020-09-03', 91, 94, 'A') ;
INSERT INTO 수강
VALUES ('s001', 'c005', '2020-09-03', 74, 79, 'C') ;
INSERT INTO 수강
VALUES ('s003', 'c001', '2019-03-03', 81, 82, 'B') ;
INSERT INTO 수강
VALUES ('s004', 'c002', '2018-03-05', 92, 95, 'A') ;

-- 과목(과목번호, 이름, 강의실, 개설학과, 시수)
-- 학생(학번, 이름, 주소, 학년, 나이, 휴대폰번호, 소속학과)
-- 수강(학번, 과목번호, 신청날짜, 중간성적, 기말성적, 평가학점)

select * from 과목;
select * from 학생;
select * from 수강;
