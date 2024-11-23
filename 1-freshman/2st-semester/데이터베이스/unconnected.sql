-- handb 데이터베이스 존재할 경우, 데이터베이스 삭제
drop database if exists univDB;

-- 교재 5장 스키마 생성
CREATE DATABASE `univDB` DEFAULT CHARACTER SET utf8mb4;

-- 사용할 데이터베이스 선택
use univDB;

DROP TABLE if exists 수강;
DROP TABLE if exists 과목;
DROP TABLE if exists 학생;

-- 과목(과목번호, 이름, 강의실, 개설학과, 시수)
-- 학생(학번, 이름, 주소, 학년, 나이, 휴대폰번호, 소속학과)
-- 수강(학번, 과목번호, 신청날짜, 중간성적, 기말성적, 평가학점)

CREATE TABLE 과목 (
	  과목번호 char(4) NOT NULL PRIMARY KEY, 
	  이름       VARCHAR(20) NOT NULL, 
	  강의실    CHAR(3) NOT NULL,
	  개설학과 VARCHAR(20) NOT NULL,
	  시수 INT NOT NULL
); 

CREATE TABLE 학생 (
	  학번       CHAR(4) NOT NULL,
	  이름       VARCHAR(20) NOT NULL,
	  주소       VARCHAR(50) DEFAULT '미정', 
	  학년       INT NOT NULL,
	  나이       INT,
	  성별       CHAR(1) NOT NULL,
	  휴대폰번호  CHAR(14), 
	  소속학과    VARCHAR(20),
	  PRIMARY KEY (학번) 
);

CREATE TABLE 수강 (
	  학번      char(6) NOT NULL,
	  과목번호   CHAR(4) NOT NULL,
	  신청날짜   DATE NOT NULL,
	  중간성적   INT DEFAULT 0,
	  기말성적   INT DEFAULT 0, 
	  평가학점   CHAR(1),        
	  PRIMARY KEY(학번, 과목번호) 
); 

-- 학생 테이블 입력
INSERT INTO 학생 VALUES ('s001', '김연아', '서울 서초', 4, 23, '여', '010-1111-2222',  '컴퓨터') ;
INSERT INTO 학생 VALUES ('s002', '홍길동', DEFAULT, 1, 26, '남', NULL,  '통계') ;
INSERT INTO 학생 VALUES ('s003', '이승엽', NULL, 3, 30, '남', NULL,  '정보통신') ;
INSERT INTO 학생 VALUES ('s004', '이영애', '경기 분당', 2, NULL, '여', '010-4444-5555', '정보통신') ;
INSERT INTO 학생 VALUES ('s005', '송윤아', '경기 분당', 4, 23, '여', '010-6666-7777', '컴퓨터') ;
INSERT INTO 학생 VALUES ('s006', '홍길동', '서울 종로', 2, 26, '남', '010-8888-9999', '컴퓨터') ;
INSERT INTO 학생 VALUES ('s007', '이은진', '경기 과천', 1, 23, '여', '010-2222-3333', '경영') ;

-- 과목 테이블 입력
INSERT INTO 과목 VALUES ('c001', '데이터베이스', 126, '컴퓨터', 3) ;
INSERT INTO 과목 VALUES ('c002', '정보보호', 137, '정보통신', 3) ;
INSERT INTO 과목 VALUES ('c003', '모바일웹', 128, '컴퓨터', 3) ;
INSERT INTO 과목 VALUES ('c004', '철학개론', 117, '철학', 2) ;
INSERT INTO 과목 VALUES ('c005', '전공글쓰기', 120, '교양학부', 1) ;

-- 수강 테이블 입력
INSERT INTO 수강 VALUES ('s001', 'c002', '2019-09-03', 93, 98, 'A') ;
INSERT INTO 수강 VALUES ('s004', 'c005', '2019-03-03', 72, 78, 'C') ;
INSERT INTO 수강 VALUES ('s003', 'c002', '2017-09-06', 85, 82, 'B') ;
INSERT INTO 수강 VALUES ('s002', 'c001', '2018-03-10', 31, 50, 'F') ;
INSERT INTO 수강 VALUES ('s001', 'c004', '2019-03-05', 82, 89, 'B') ;
INSERT INTO 수강 VALUES ('s004', 'c003', '2020-09-03', 91, 94, 'A') ;
INSERT INTO 수강 VALUES ('s001', 'c005', '2020-09-03', 74, 79, 'C') ;
INSERT INTO 수강 VALUES ('s003', 'c001', '2019-03-03', 81, 82, 'B') ;
INSERT INTO 수강 VALUES ('s004', 'c002', '2018-03-05', 92, 95, 'A') ;

select * from 과목;
select * from 학생;
select * from 수강;


# [실습 1] 다음에 대하여 SQL문법과 실행결과를 작성하라

-- 예제5-1) 전체 학생의 이름과 주소를 검색하시오
select 이름, 주소 from 학생;

-- 예제5-2) 전체 학생의 모든 정보를 검색하시오 (* 로 검색) 
select * from 학생;

-- 예제5-2) 전체 학생의 모든 정보를 검색하시오 (필드명으로 검색)
select 학번, 이름, 주소, 학년, 나이, 성별, 휴대폰번호, 소속학과 from 학생;

-- 예제5-3) 전체 학생의 소속학과 정보를 중복없이 검색하시오 (DISTINCT 사용)
select distinct 소속학과 from 학생;

-- 예제5-3-2) 전체 학생의 소속학과 정보를 모두 검색하시오 (ALL 키워드 사용)
select all 소속학과 from 학생;

-- 예제5-4) 학생 중에서 2학년 이상인 컴퓨터 학과 학생의 이름, 학년, 소속학과, 휴대폰번호 정보를 검색하시오
select 이름, 학년, 소속학과, 휴대폰번호 from 학생
 where (학년 >= 2 and 소속학과 = '컴퓨터');

-- 예제5-5) 1, 2, 3학년 학생이거나 컴퓨터 학과에 소속되지 않은 학생의 이름, 학년, 소속학과, 휴대폰번호 정보를 검색하시오 (부등호 사용)
select 이름, 학년, 소속학과, 휴대폰번호 from 학생
 where (학년 in (1,2,3) or 소속학과 != '컴퓨터');

-- 예제5-5) 1, 2, 3학년 학생이거나 컴퓨터 학과에 소속되지 않은 학생의 이름, 학년, 소속학과, 휴대폰번호 정보를 검색하시오 (BETWEEN AND 사용)
select 이름, 학년, 소속학과, 휴대폰번호 from 학생
 where (학년 between 1 and 3 or 소속학과 <> '컴퓨터');

-- 예제5-6) 컴퓨터 학과나 정보통신 학과의 학생의 이름과 학년, 소속학과 정보를 오름차순으로 검색하시오
select 이름, 학년, 소속학과 from 학생
 where 소속학과 in ('컴퓨터', '정보통신')
 order by 1,2,3 asc;

-- 예제5-7) 전체 학생의 모든 정보를 검색하되 학년을 기준으로 1차 오름차순 정렬하고, 학년이 같은 경우에는 이름을 기준으로 2차 내림차순 정렬하여 검색하시오
select * from 학생
 order by 학년 asc, 이름 desc;


# [실습 2] 집계함수, group by

-- 예제5-8) 전체 학생수를 검색하시오 (* 을 이용)
select count(*) from 학생;

-- 예제5-8) 전체 학생수를 검색하시오 (학번 속성을 이용)
select count(학번) from 학생;

-- 예제5-8) 전체 학생수를 검색하시오 (주소 속성을 이용 - 널 값 제외)
select count(주소) from 학생;

-- 예제5-8-2) 전체학생수, 주소를 입력한 학생수, 주소의 종류를 중복없이 검색한 개수를 검색하시오
select count(*), count(주소), count(distinct 주소) from 학생;

-- 예제5-9) 여 학생의 평균 나이를 검색하시오
select avg(나이) from 학생
 where 성별 = '여';

-- 예제5-10) 전체 학생의 성별 최고 나이와 최저 나이를 검색하시오
select 성별, min(나이), max(나이) from 학생
 group by 성별;

-- 예제5-11) 20대 학생만을 대상으로 나이별 학생수를 검색하시오
select 나이, count(나이) from 학생
 where 나이 like '2%'
 group by 나이;

-- 예제5-12) 각 학년별로 2명 이상의 학생을 갖는 학년에 대해서만 학생별 학생수를 검색하시오
select 학년, count(*) from 학생
 group by 학년
 having count(학년) >= 2;


# [실습 3] LIKE 연산자 / 널 값 검색 / 집합 연산자

-- 예제5-13) 이 씨 성을 가진 학생들의 학번과 학생 이름을 검색하시오
select 학번, 이름 from 학생
 where 이름 like '이%';

-- 예제5-14) 주소지가 '서울'인 학생의 이름, 주소, 학년을 학년순(내림차순)으로 검색하시오
select 이름, 주소, 학년 from 학생
 where 주소 like '서울%'
 order by 학년 desc;

-- 예제5-15) 휴대폰번호가 등록되지 않은(널 값을 갖는) 학생의 이름과 휴대폰번호를 검색하시오
select 이름, 휴대폰번호 from 학생
 where 휴대폰번호 is null;

-- 예제5-16) '여' 학생이거나 'A' 학점을 받은 학생의 학번을 검색하시오
select 학생.학번 from 학생
 inner join 수강 on 학생.학번 = 수강.학번
 where 학생.성별 = '여' or 수강.평가학점='A'
 group by 학생.학번;

-- 예제5-18) 전체 학생의 기본 정보와 모든 수강 정보를 검색하시오 (SELECT FROM WHERE 방법)
select * from 학생, 수강, 과목
 where 학생.학번 = 수강.학번
 and 과목.과목번호 = 수강.과목번호;
 
-- 예제5-18) 전체 학생의 기본 정보와 모든 수강 정보를 검색하시오 (SELECT FROM ON 방법)
select * from 학생
 inner join 수강 on 학생.학번 = 수강.학번
 inner join 과목 on 과목.과목번호 = 수강.과목번호;

-- 예제5-19) 학생 중에서 과목번호가 c002 인 과목을 수강한 학생의 학번과 이름, 과목번호, 변환중간성적(학생별중간성적의 10% 가산점수)을 검색하시오 (SELECT FROM WHERE 방법)
select 학생.학번, 이름, 과목번호, (중간성적 * 0.1) as 변환중간성적 from 학생, 수강
 where 학생.학번 = 수강.학번
 and 수강.과목번호 = 'c002';

-- 예제5-19) 학생 중에서 과목번호가 c002 인 과목을 수강한 학생의 학번과 이름, 과목번호, 변환중간성적(학생별중간성적의 10% 가산점수)을 검색하시오 (SELECT FROM ON 방법)
select 학생.학번, 이름, 과목번호, (중간성적 * 0.1) as 변환중간성적 from 학생
 inner join 수강 on 학생.학번 = 수강.학번
 where 수강.과목번호 = 'c002';

-- 예제5-20) 학생 중에서 정보보호 과목을 수강한 학생의 학번과 이름, 과목번호를 검색하시오 (SELECT FROM WHERE 방법)
select 학생.학번, 학생.이름, 수강.과목번호 from 학생, 수강, 과목
 where 학생.학번 = 수강.학번
 and 수강.과목번호 = 과목.과목번호
 and 과목.이름 = '정보보호';

-- 예제5-20) 학생 중에서 정보보호 과목을 수강한 학생의 학번과 이름, 과목번호를 검색하시오 (SELECT FROM ON 방법)
select 학생.학번, 학생.이름, 수강.과목번호 from 학생
 inner join 수강 on 학생.학번 = 수강.학번
 inner join 과목 on 수강.과목번호 = 과목.과목번호
 where 과목.이름 = '정보보호';

-- 예제5-21) 학생 중에서 과목번호가 c002 인 과목을 수강한 학생의 이름, 과목번호를 검색하시오 (테이블 별칭 as 사용)
select 학생.이름 as '학생의 이름', 수강.과목번호 from 학생, 수강
 where 학생.학번 = 수강.학번
 and 수강.과목번호 = 'c002';

-- 예제5-23) 과목을 수강하지 않은 학생을 포함하여 모든 학생의 학번, 이름과 학생이 수강한 교과목의 평가학점을 검색하시오
-- SELECT 학생.학번, 학생.이름, 과목.이름 AS 과목이름, 평가학점 FROM 학생 LEFT JOIN 수강 ON 학생.학번 = 수강.학번 LEFT JOIN 과목 ON 수강.과목번호 = 과목.과목번호;
select 학생.학번, 학생.이름, 과목.이름 as 과목이름, 평가학점 from 학생, 수강, 과목
 where 학생.학번 = 수강.학번
 and 수강.과목번호 = 과목.과목번호;