package Day0602;

import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.sql.Statement;

public class JDBCEx2 {

	public static void main(String[] args) {
		// TODO Auto-generated method stub
		try {
			Class.forName("com.mysql.cj.jdbc.Driver");
			Connection conn = DriverManager.getConnection("jdbc:mysql://localhost:3306/sampledb", "root", "asus");
			
			System.out.println("DB 연결 성공\n");
			
			// Statement 는 프로그램을 구성하는 가장 작은 독립 요소, 기본 단위이자 최소 실행 단위
			// Statement 는 명령문이라고도 불리며, 컴퓨터에서 명령과 지시를 내리는 역할
			Statement stmt = conn.createStatement();
			
//			String sql = "select * from student;";
//			String sql = "insert into student values('2024004', '동미래', '인공지능학과');";
//			String sql = "update student set dept = '자연지능학과' where name = '동미래';";
			String sql = "delete from student where name = '동미래';";
			
			stmt.executeUpdate(sql);
			
			System.out.println("데이터 입력 완료");
			
//			ResultSet rs = stmt.executeQuery(sql);
//			
//			while (rs.next()) {
//				System.out.println(rs.getString(1));
//				System.out.println(rs.getString(2));
//				System.out.println(rs.getString(3));
////				System.out.println(rs.getString(4));
//				System.out.println();
//			}
//			
//			rs.close();
			stmt.close();
			conn.close();
			
		} catch (ClassNotFoundException | SQLException e) {
			// TODO Auto-generated catch block
			System.out.println("DB 연결 오류");
			e.printStackTrace();
		}
		
	}

}