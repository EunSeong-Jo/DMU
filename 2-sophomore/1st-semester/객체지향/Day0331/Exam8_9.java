package Day0331;

import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.File;
import java.io.FileNotFoundException;
import java.io.FileReader;
import java.io.FileWriter;
import java.io.IOException;

public class Exam8_9 {

	public static void main(String[] args) {
		// TODO Auto-generated method stub

		//String src = "C:\\Users\\asus\\eclipse-workspace\\OOP\\src\\Day0331\\8-9src.txt";
		File src = new File("C:\\Users\\asus\\eclipse-workspace\\OOP\\src\\Day0331\\8-9src.txt");
		File dest = new File("C:\\Users\\asus\\eclipse-workspace\\OOP\\src\\Day0331\\8-9dest.txt");
		
		int i;
		
		FileReader fr;
		FileWriter fw;
		
		try {
			fr = new FileReader(src);
			BufferedReader bin = new BufferedReader(fr);
			
			fw = new FileWriter(dest);
			BufferedWriter bout = new BufferedWriter(fw);
			
			while((i = bin.read()) != -1) {
				bout.write((char) i);
			}
			
			fr.close();
			fw.close();
			bin.close();
			bout.close();
			
			System.out.println(src.getPath() + "를 " + dest.getPath() + "로 복사 완료");
			
		} catch (FileNotFoundException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
			System.out.println("파일을 찾지 못했음");
		} catch (IOException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
			System.out.println("파일을 읽지 못했음");
		}
	}
}
