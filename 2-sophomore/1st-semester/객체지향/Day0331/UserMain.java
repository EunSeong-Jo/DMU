package Day0331;

import java.io.*;
import java.util.ArrayList;
import java.util.Scanner;

public class UserMain {

	public static void main(String[] args) {
		// TODO Auto-generated method stub
		Scanner scn = new Scanner(System.in);
		ArrayList<User> ul = new ArrayList<User>();
		
		String outputFile = "C:\\Users\\asus\\eclipse-workspace\\OOP\\src\\Day0331\\UserOutput.txt";
		
		while (true) {
			System.out.print("이름을 입력하세요 ('그만' 입력 시 종료): ");
			String name = scn.nextLine();

			if (name.equals("그만")) {
				break;
			}

			System.out.print("나이를 입력하세요: ");
			
			int age = scn.nextInt();
			scn.nextLine();
			
			User user1 = new User(name, age);
			ul.add(user1);

			// 파일에 저장
			// try-with-resources
			// BufferedWriter 객체 내부에 AutoCloseable 메소드가 구현되어 있음 (close() 자동 호출)
			try (BufferedWriter bout = new BufferedWriter(new FileWriter(outputFile))) {
				for (User user : ul) {
					System.out.println(user.toString() + "\n");
					bout.write(user.toString() + "\n");
				}
				
			} catch (IOException e) {
				System.out.println("파일 저장 중 오류가 발생했습니다.");
				e.printStackTrace();
			}
		}
		
		System.out.println("입력한 정보가 UserOutput.txt 파일에 저장되었습니다.");

		scn.close();
	
	}
}