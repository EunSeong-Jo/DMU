-- CRUD : 생성(Create), 읽기(Read), 갱신(Update), 삭제(Delete)
CREATE TABLE board (
    id BIGINT NOT NULL AUTO_INCREMENT PRIMARY KEY,   -- 게시글 고유 번호 (자동 증가)
    subject VARCHAR(255),                            -- 제목
    contents TEXT,                                   -- 내용 (길이 제한 없음)
    writer VARCHAR(50),                              -- 작성자 이름
    create_dt DATETIME DEFAULT (now()),              -- 생성 시간 (기본값: 현재 시간)
    update_dt DATETIME,                              -- 수정 시간 (수정 시 갱신)
    view_count INT DEFAULT '0'                       -- 조회 수 (기본값 0)
);


CREATE TABLE member (
    user_id VARCHAR(50) NOT NULL PRIMARY KEY,      -- 사용자 ID (고유)
    user_name VARCHAR(50) NOT NULL,                -- 사용자 이름
    password VARCHAR(50) NOT NULL,                 -- 비밀번호
    create_dt DATETIME NULL DEFAULT (now()),       -- 가입일 (기본값: 현재 시간)
    update_dt DATETIME NULL DEFAULT NULL           -- 수정일 (필요 시 갱신)
);




