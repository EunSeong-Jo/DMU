package Day0331;

import java.io.FileNotFoundException;
import java.io.FileReader;
import java.io.IOException;

public class Exam8_1 {

	public static void main(String[] args) {
		// TODO Auto-generated method stub
		
		FileReader fin;
		
		try {
			// C:\\Users\\asus\\eclipse-workspace\\OOP\\src\\Day0331\\
			fin = new FileReader("./test.txt");
			
			int i;
			
			// 아스키코드 타입으로 입력
			while((i = fin.read()) != -1) {
				System.out.print((char) i);
			}
				
			fin.close();
			
		} catch (FileNotFoundException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
			System.out.println("파일을 찾을 수 없음");
			
		} catch (IOException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
			System.out.println("읽기 에러");
		}
		
		catch (Exception e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
			System.out.println("에러 발생");
		}
		
	}

}
