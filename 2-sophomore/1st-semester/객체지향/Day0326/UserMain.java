package Day0326;

import java.io.*;
import java.util.ArrayList;
import java.util.Scanner;

public class UserMain {

	public static void main(String[] args) {
		// TODO Auto-generated method stub
		Scanner scanner = new Scanner(System.in);
		ArrayList<User> userList = new ArrayList<>();

		while (true) {
			System.out.print("이름을 입력하세요 ('그만' 입력 시 종료): ");
			String name = scanner.nextLine();

			if (name.equals("그만")) {
				break;
			}

			System.out.print("나이를 입력하세요: ");
			
			int age = 0;
			
			try {
				age = Integer.parseInt(scanner.nextLine());
			} catch (NumberFormatException e) {
				System.out.println("숫자만 입력해주세요.");
				continue;
			}

			userList.add(new User(name, age));
		}

		// 파일에 저장
		try (BufferedWriter writer = new BufferedWriter(new FileWriter("output.txt"))) {
			for (User user : userList) {
				writer.write(user.toString());
				writer.newLine();
			}
			System.out.println("입력한 정보가 output.txt 파일에 저장되었습니다.");
		} catch (IOException e) {
			System.out.println("파일 저장 중 오류가 발생했습니다.");
			e.printStackTrace();
		}

		scanner.close();
	}
}