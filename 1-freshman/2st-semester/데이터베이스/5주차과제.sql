# 새로운 데이터베이스를 생성
create database homework;

# 생성된 데이터베이스를 사용
use homework;

drop table 의사;

# 의사 테이블을 생성
create table 의사(
	# 의사번호는 고유값(데이터를 구별하는 값) primary key지정, null값 입력 불가로 지정
	의사번호 char(4) not null,
    의사이름 char(20),
	소속 char(10),
    근무연수 int,
    
    primary key(의사번호)
);

select * from 의사;

# 의사 테이블 데이터입력
insert into 의사 values ('D001', '정지영', '내과', '5');
insert into 의사 values ('D002', '김선주', '피부과', '10');
insert into 의사 values ('D003', '정성호', '정형외과', '15');
insert into 의사 values ('D999', '조은성', '진단과', '999');


drop table 환자;

# 환자 테이블을 생성
create table 환자(
	# 환자번호는 고유값(데이터를 구별하는 값)이기 때문에 primary key, null값 입력 불가로 지정
    환자번호 char(4) not null,
    환자이름 char(20),
	나이 int,
    # 외래키, null값 입력 불가로 지정
    담당의사 char(4) not null,
    
    primary key(환자번호),
	
    # 의사 테이블의 의사번호 값과 환자 테이블의 담당의사 값은 동일함
    # 환자 테이블(서브)의 담당의사를 외래키로 지정해서 의사 테이블(메인)의 의사번호와 연동
    foreign key(담당의사)
		references 의사(의사번호)
);

select * from 환자;

# 환자 테이블에 데이터 입력
insert into 환자 values ('P001', '오우진', '31', 'D002');
insert into 환자 values ('P002', '채광주', '50', 'D001');
insert into 환자 values ('P003', '김용욱', '43', 'D003');
insert into 환자 values ('P999', '조은성', '24', 'D999');


create table 사원(
	사원번호 char(4),
    사원이름 varchar(20),
    나이 int,
    주소 char(20),
    직급 char(10),
    
    primary key(사원번호)
);

select * from 사원;

insert into 사원 values ('E001', '홍준화', 30, '서울시 마포구', '대리');
insert into 사원 values ('E002', '김연주', 28, '서울시 영등포구', '사원');
insert into 사원 values ('E003', '이명기', 32, '서울시 강남구', '사원');
insert into 사원 values ('E004', '조은성', 24, '서울시 구로구', '학생');