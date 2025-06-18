package kr.ac.dongyang.website.jspwebsite.dao;

import kr.ac.dongyang.website.jspwebsite.db.DbConnector;
import kr.ac.dongyang.website.jspwebsite.dto.MemberDto;

import java.sql.Connection;
import java.sql.PreparedStatement;
import java.sql.ResultSet;
import java.util.ArrayList;
import java.util.List;

public class MemberDao {

    /**
     * 회원 목록을 DB에서 모두 조회하여 리스트로 반환하는 메서드
     */
    public List<MemberDto> getMemberList() {

        List<MemberDto> memberList = new ArrayList<>(); // 결과를 담을 리스트 생성
        Connection connection = DbConnector.getConnection(); // DB 연결 객체 생성

        // 회원 목록을 최신순으로 정렬하여 조회하는 SQL
        String sql = "select user_id, user_name, password, create_dt, update_dt " +
                "from member order by update_dt desc, create_dt desc";
        try {
            // SQL 실행을 위한 PreparedStatement 생성
            PreparedStatement preparedStatement = connection.prepareStatement(sql);

            // SQL 실행 및 결과 반환
            ResultSet rs = preparedStatement.executeQuery();

            // 결과 셋에서 한 행씩 MemberDto 객체로 변환하여 리스트에 추가
            while (rs.next()) {
                MemberDto member = MemberDto.builder()
                        .userId(rs.getString("user_id"))
                        .userName(rs.getString("user_name"))
                        .password(rs.getString("password"))
                        .createDt(rs.getDate("create_dt"))
                        .updateDt(rs.getDate("update_dt"))
                        .build();
                memberList.add(member); // 리스트에 추가
            }

        } catch (Exception e) {
            e.printStackTrace(); // 예외 발생 시 오류 출력
        }

        return memberList;
    }

    /**
     * 특정 회원의 상세 정보를 조회 (userId 기준)
     * → 현재는 전체 목록에서 필터링하는 방식 (비효율적이지만 간단)
     */
    public MemberDto getMember(String userId) {
        // 회원 목록 중 userId가 일치하는 항목을 찾아 반환
        MemberDto member = getMemberList().stream()
                .filter(e -> e.getUserId().equals(userId))
                .findFirst()
                .orElse(null);

        return member;
    }

    /**
     * 새로운 회원을 DB에 추가하는 메서드
     */
    public boolean addMember(MemberDto member) {
        boolean result = false;

        Connection connection = DbConnector.getConnection(); // DB 연결

        // 회원 등록을 위한 INSERT SQL 문
        String sql = "insert into member (user_id, user_name, password) values (?, ?, ?)";
        try {
            PreparedStatement preparedStatement = connection.prepareStatement(sql);

            // 바인딩: SQL의 ? 자리에 값 채워넣기
            preparedStatement.setString(1, member.getUserId());
            preparedStatement.setString(2, member.getUserName());
            preparedStatement.setString(3, member.getPassword());

            // SQL 실행 후 영향받은 행 수 확인
            int affectedRow = preparedStatement.executeUpdate();
            if (affectedRow > 0) {
                result = true; // 성공 여부 플래그 설정
            }
        } catch (Exception e) {
            e.printStackTrace();
        }

        return result;
    }

    /**
     * 기존 회원 정보를 수정하는 메서드
     */
    public boolean updateMember(MemberDto member) {
        boolean result = false;

        Connection connection = DbConnector.getConnection(); // DB 연결

        // 회원 정보 업데이트 SQL (비밀번호, 이름 변경 + 수정일 갱신)
        String sql = "update member set user_name = ?, password = ?, update_dt = now() where user_id = ?";
        try {
            PreparedStatement preparedStatement = connection.prepareStatement(sql);

            // 바인딩
            preparedStatement.setString(1, member.getUserName());
            preparedStatement.setString(2, member.getPassword());
            preparedStatement.setString(3, member.getUserId());

            int affectedRow = preparedStatement.executeUpdate();
            if (affectedRow > 0) {
                result = true; // 수정 성공 시 true 반환
            }
        } catch (Exception e) {
            e.printStackTrace();
        }

        return result;
    }

    /**
     * 회원을 삭제하는 메서드 (userId 기준)
     */
    public boolean deleteMember(String userId) {
        boolean result = false;

        Connection connection = DbConnector.getConnection(); // DB 연결

        // 회원 삭제 SQL 문
        String sql = "delete from member where user_id = ?";
        try {
            PreparedStatement preparedStatement = connection.prepareStatement(sql);

            // userId를 바인딩
            preparedStatement.setString(1, userId);

            int affectedRow = preparedStatement.executeUpdate();
            if (affectedRow > 0) {
                result = true; // 삭제 성공 시 true 반환
            }
        } catch (Exception e) {
            e.printStackTrace();
        }

        return result;
    }

}
