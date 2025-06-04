package Day0602;

import java.sql.DriverManager;
import java.sql.SQLException;

import com.mysql.cj.jdbc.Driver;

public class JDBCEx1 {

	public static void main(String[] args) {
		// TODO Auto-generated method stub
		try {
			Class.forName("com.mysql.cj.jdbc.Driver");
			
			DriverManager.getConnection("jdbc:mysql://localhost:3306/sampledb", "root", "asus");
			
			System.out.println("DB 연결 성공");
			
		} catch (ClassNotFoundException | SQLException e) {
			// TODO Auto-generated catch block
			System.out.println("DB 연결 오류");
			e.printStackTrace();
		}
		
	}

}
