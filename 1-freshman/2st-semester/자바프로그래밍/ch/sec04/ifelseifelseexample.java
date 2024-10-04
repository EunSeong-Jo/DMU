package ch.sec04;

public class ifelseifelseexample {

	public static void main(String[] args) {
		// TODO Auto-generated method stub
		int score = 75;
		
		if(score >= 90) {
			System.out.println("100 ~ 90");
			System.out.println("A");
		}
		else if(score >= 80) {
			System.out.println("90 ~ 80");
			System.out.println("B");
		}
		else if(score >= 70) {
			System.out.println("80 ~ 70");
			System.out.println("C");
		}
		else {
			System.out.println("70 ~ 0");
			System.out.println("D");	
		}
	}
}