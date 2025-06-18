package kr.ac.dongyang.website.jspwebsite.db;

import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.SQLException;

public class DbConnector {

    /**
     * MySQL 데이터베이스와 연결을 생성하여 반환하는 메서드
     */
    public static Connection getConnection() {
        try {
            // MySQL JDBC 드라이버를 메모리에 로드
            Class.forName("com.mysql.cj.jdbc.Driver");

        } catch (ClassNotFoundException e) {
            // 드라이버 클래스가 없을 경우 예외 출력
            e.printStackTrace();
        }

        // DB 접속 정보 설정
        String host = "localhost";           // DB 서버 주소
        int port = 43307;                    // 포트 번호 (기본은 3306, 이 프로젝트는 커스텀)
        String id = "jsp_user";              // DB 사용자 ID
        String pwd = "1234";                 // DB 사용자 비밀번호
        String dbInstance = "jsp_db";        // 접속할 DB 스키마 이름

        // 접속 URL 문자열 생성 (JDBC 규약에 맞게 구성)
        String url = String.format("jdbc:mysql://%s:%d/%s", host, port, dbInstance);

        Connection connection = null;        // 최종 반환할 Connection 객체

        try {
            // DB에 실제로 연결 수행
            connection = DriverManager.getConnection(url, id, pwd);
        } catch (SQLException e) {
            // 연결 실패 시 예외 출력
            e.printStackTrace();
        }

        // 연결된 Connection 객체 반환 (실패 시 null)
        return connection;
    }

}
