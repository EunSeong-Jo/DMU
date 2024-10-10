package ch.sec04;

public class switchexpressonsexample {

	public static void main(String[] args) {
		// TODO Auto-generated method stub
		char grade = 'B';
		
		switch(grade) {
			case 'A', 'a' -> {
				System.out.println('A');
			}
			case 'B', 'b' -> {
				System.out.println('B');
			}
			default -> {
				System.out.println('C');
			}
		}
	}
}
