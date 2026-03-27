package Day0331;

import java.io.FileWriter;
import java.io.IOException;
import java.util.Scanner;

public class Exam8_4 {

	public static void main(String[] args) {
		// TODO Auto-generated method stub

		Scanner scn = new Scanner(System.in);
		FileWriter fout;
		int i;
		
		try {
			// C:\Users\asus\eclipse-workspace\OOP\src\Day0331\8-4.txt
			fout = new FileWriter("C:\\Users\\asus\\eclipse-workspace\\OOP\\src\\Day0331\\8-4.txt");
			
			while (true) {
				
				String line = scn.nextLine();
				
				if (line.length() == 0) {
					break;
				}
				
				fout.write(line, 0, line.length());
				fout.write("\r\n",0 ,2);
			}
			
			fout.close();
			
		} catch (IOException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
			System.out.println("읽기 오류");
		}
		
		scn.close();
	
	}

}
