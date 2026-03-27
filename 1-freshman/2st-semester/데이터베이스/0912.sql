use testdb;

select * from 학생;

select 학번, 이름 from 학생;
select 이름, 성적 from 학생;

-- 문자열은 대소문자 구분
select * from 학생 where 이름 = 'Kim';
select * from 학생 where 학번 = '500';

select version();