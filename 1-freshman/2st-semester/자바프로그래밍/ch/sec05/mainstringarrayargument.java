package ch.sec05;

public class mainstringarrayargument {

	public static void main(String[] args) {
		// TODO Auto-generated method stub

		String[] ary = {"1", "2"};
		
		if(ary.length != 2) {
			System.out.println("input lows 2");
		}
		
		String strNum1 = ary[0];
		String strNum2 = ary[1];
		
		int num1 = Integer.parseInt(strNum1);
		int num2 = Integer.parseInt(strNum2);
		
		int result = num1 + num2;
		System.out.println(num1 + "+" + num2 + "=" + result);
		
	}

}
