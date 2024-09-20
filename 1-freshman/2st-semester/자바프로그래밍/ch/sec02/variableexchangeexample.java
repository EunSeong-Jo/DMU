package ch.sec02;

public class variableexchangeexample {
	public static void main(String[] args) {
		int x = 3;
		int y = 5;
		
		System.out.println("x:" + x + ", y:" + y);
		
		int temp = x;
		x = y;
		y = temp;
		System.out.print("x:" + x + ", y:" + y);
	}

}
