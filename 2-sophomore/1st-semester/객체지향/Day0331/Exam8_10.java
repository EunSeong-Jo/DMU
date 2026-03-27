package Day0331;

import java.io.File;
import java.io.FileInputStream;
import java.io.FileNotFoundException;
import java.io.FileOutputStream;
import java.io.IOException;

public class Exam8_10 {

	public static void main(String[] args) {
		// TODO Auto-generated method stub

		File src = new File("C:\\Users\\asus\\eclipse-workspace\\OOP\\src\\Day0331\\dongyang.svg");
		File dest = new File("C:\\Users\\asus\\eclipse-workspace\\OOP\\src\\Day0331\\dy.svg");
		
		int i;
		
		try {
			FileInputStream fi = new FileInputStream(src);
			FileOutputStream fo = new FileOutputStream(dest);
			
			while ((i = fi.read()) != -1) {
				fo.write((byte) i);
			}
			
			fi.close();
			fo.close();
			
			System.out.println(src.getPath() + "를 " + dest.getPath() + "로 복사 완료");
			
		} catch (FileNotFoundException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
			System.out.println("파일 찾기 오류");
			
		} catch (IOException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
			System.out.println("파일 읽기 오류");
		}
	}

	
	
	
}
