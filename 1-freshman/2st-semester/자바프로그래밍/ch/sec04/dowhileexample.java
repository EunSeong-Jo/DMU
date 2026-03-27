package ch.sec04;

import java.util.Scanner;

public class dowhileexample {

	public static void main(String[] args) {
		// TODO Auto-generated method stub
		System.out.println("input massage");
		System.out.println("insert q, exit program");
		
		Scanner scanner = new Scanner(System.in);
		String inputString;
		
		do {
			System.out.print(">");
			inputString = scanner.nextLine();
			System.out.println(inputString);
		} while(!inputString.equals("q"));
		
		System.out.println("exit program");
	}
}
