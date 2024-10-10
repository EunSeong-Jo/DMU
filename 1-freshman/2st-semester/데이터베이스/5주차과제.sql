# 새로운 데이터베이스를 생성
create database homework;

# 생성된 데이터베이스를 사용
use homework;

drop table 환자;

# homework 데이터베이스에 환자 테이블을 생성
create table 환자(
	환자번호 char(4) not null,
    환자이름 char(20),
	나이 char(3),
	# 담당의사는 고유값(데이터를 구별하는 값)이며 의사 테이블의 의사번호와 연결될 예정이기 때문에 primary key로 지정
    # null값 입력 불가로 지정
    담당의사 char(4) not null,
    
    primary key(담당의사)
);

select * from 환자;

# 환자 테이블에 데이터 입력
insert into 환자 values ('P001', '오우진', '31', 'D002');
insert into 환자 values ('P002', '채광주', '50', 'D001');
insert into 환자 values ('P003', '김용욱', '43', 'D003');

drop table 의사;

# 의사 테이블을 생성
create table 의사(
	# 의사번호는 고유값(데이터를 구별하는 값)
    # 환자 테이블의 담당의사와 연결될 예정이기 때문에 primary key 대신 foreign key로 지정, null값 입력 불가로 지정
	의사번호 char(4) not null,
    의사이름 char(20),
	소속 char(10),
    근무연수 int,
    
    # 의사 테이블의 의사번호 값과 환자 테이블의 담당의사 값은 동일함
    # 의사 테이블(서브)의 의사번호를 외래키로 지정해서 환자 테이블(메인)의 담당의사와 연동
    foreign key(의사번호)
		references 환자(담당의사)
);

select * from 의사;

# 의사 테이블 데이터입력
insert into 의사 values ('D001', '정지영', '내과', '5');
insert into 의사 values ('D002', '김선주', '피부과', '10');
insert into 의사 values ('D003', '정성호', '정형외과', '15');