package kr.ac.dongyang.website.jspwebsite.dao;

import kr.ac.dongyang.website.jspwebsite.db.DbConnector;
import kr.ac.dongyang.website.jspwebsite.dto.BoardDto;

import java.sql.Connection;
import java.sql.PreparedStatement;
import java.sql.ResultSet;
import java.util.ArrayList;
import java.util.List;

public class BoardDao {

    /**
     * 게시판의 게시글 목록을 DB에서 조회하여 반환
     */
    public List<BoardDto> getBoardList() {
        // 결과를 담을 리스트 생성
        List<BoardDto> list = new ArrayList<>();

        // DB 연결 객체 생성
        // 📝 DB 연결 획득 → 시험 
        Connection connection = DbConnector.getConnection();

        // 게시글을 최신순으로 정렬하여 전체 조회
        String sql = "select id, writer, subject, contents, ip_addr, view_count, create_dt, update_dt " +
                "from board order by update_dt desc, create_dt desc";

        try {
            // SQL 실행을 위한 객체 준비
            // 📝 SQL 준비 → 시험 출제 가능
            PreparedStatement preparedStatement = connection.prepareStatement(sql);

            // SQL 실행 및 결과 받아오기
            // 📝 결과 집합 받기 → 시험 출제 가능
            ResultSet rs = preparedStatement.executeQuery();

            // 결과를 한 줄씩 읽어서 BoardDto 객체로 변환 후 리스트에 추가
            while (rs.next()) {
                // 📝 결과를 리스트에 추가 → 시험 출제 가능
                list.add(BoardDto.builder()
                        .id(rs.getLong("id"))
                        .writer(rs.getString("writer"))
                        .subject(rs.getString("subject"))
                        .contents(rs.getString("contents"))
                        .ipAddr(rs.getString("ip_addr"))
                        .viewCount(rs.getInt("view_count"))
                        .createDt(rs.getDate("create_dt"))
                        .updateDt(rs.getDate("update_dt"))
                        .build());  // 📝 DTO 빌더로 객체 생성 → 시험 출제 가능
            }

        } catch (Exception e) {
            e.printStackTrace(); // 예외 발생 시 에러 출력
        }

        return list;
    }

    /**
     * 특정 게시글 1건의 상세 정보를 조회 (id 기준)
     * → 현재는 전체 목록에서 필터링하는 방식 (비효율적이지만 구현은 간단함)
     */
    public BoardDto getBoard(long boardId) {
        // 게시글 목록 중 ID가 일치하는 항목을 찾아 반환
        BoardDto Board = getBoardList().stream()
                .filter(e -> e.getId() == boardId)
                .findFirst()
                .orElse(null);

        return Board;
    }

    /**
     * 게시글을 DB에 새로 추가
     */
    public boolean addBoard(BoardDto board) {
        boolean result = false;

        // DB 연결 객체 생성
        Connection connection = DbConnector.getConnection();  // 📝 DB 연결 획득 → 시험 출제 가능

        // 게시글 삽입 SQL 정의
        String sql = "insert into board (writer, subject, contents, ip_addr) values (?, ?, ?, ?)";
        try {
            // SQL 실행 객체 생성 및 파라미터 바인딩
            PreparedStatement preparedStatement = connection.prepareStatement(sql);  // 📝 SQL 준비 → 시험 출제 가능
            preparedStatement.setString(1, board.getWriter());  // 📝 PreparedStatement에 값 바인딩 → 시험 출제 가능
            preparedStatement.setString(2, board.getSubject());  // 📝 PreparedStatement에 값 바인딩 → 시험 출제 가능
            preparedStatement.setString(3, board.getContents());  // 📝 PreparedStatement에 값 바인딩 → 시험 출제 가능
            preparedStatement.setString(4, board.getIpAddr());  // 📝 PreparedStatement에 값 바인딩 → 시험 출제 가능

            // SQL 실행 후 삽입된 행 수 반환
            int affectedRow = preparedStatement.executeUpdate();  // 📝 DB에 삽입/수정 실행 → 시험 출제 가능
            if (affectedRow > 0) {
                result = true; // 성공 시 true 반환
            }
        } catch (Exception e) {
            e.printStackTrace();
        }

        return result;
    }

    /**
     * 기존 게시글 내용을 수정
     */
    public boolean updateBoard(BoardDto board) {
        boolean result = false;

        // DB 연결 객체 생성
        Connection connection = DbConnector.getConnection();  // 📝 DB 연결 획득 → 시험 출제 가능

        // 게시글 수정 SQL 정의 (작성자, 제목, 내용, IP 수정, 수정일시 갱신)
        String sql = "update board set writer = ?, subject = ?, contents = ?, ip_addr = ?, update_dt = now() where id = ?";
        try {
            // SQL 실행 객체 생성 및 파라미터 바인딩
            PreparedStatement preparedStatement = connection.prepareStatement(sql);  // 📝 SQL 준비 → 시험 출제 가능
            preparedStatement.setString(1, board.getWriter());  // 📝 PreparedStatement에 값 바인딩 → 시험 출제 가능
            preparedStatement.setString(2, board.getSubject());  // 📝 PreparedStatement에 값 바인딩 → 시험 출제 가능
            preparedStatement.setString(3, board.getContents());  // 📝 PreparedStatement에 값 바인딩 → 시험 출제 가능
            preparedStatement.setString(4, board.getIpAddr());  // 📝 PreparedStatement에 값 바인딩 → 시험 출제 가능
            preparedStatement.setLong(5, board.getId());  // 📝 PreparedStatement에 값 바인딩 → 시험 출제 가능

            // SQL 실행 후 변경된 행 수 확인
            int affectedRow = preparedStatement.executeUpdate();  // 📝 DB에 삽입/수정 실행 → 시험 출제 가능
            if (affectedRow > 0) {
                result = true; // 성공 시 true 반환
            }
        } catch (Exception e) {
            e.printStackTrace();
        }

        return result;
    }

}
