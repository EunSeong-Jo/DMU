package ch.sec05;

public class lengthexample {

	public static void main(String[] args) {
		// TODO Auto-generated method stub

		String ssn = "123456789";
		int len = ssn.length();
		
		
		if(len == 13)
			System.out.println("13자리");
		else
			System.out.println("13자리 아님");
		
	}

}
