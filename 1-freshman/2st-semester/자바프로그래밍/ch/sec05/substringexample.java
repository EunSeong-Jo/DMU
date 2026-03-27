package ch.sec05;

public class substringexample {

	public static void main(String[] args) {
		// TODO Auto-generated method stub
		String ssn = "12345-67890";
		
		String fNum = ssn.substring(0, 5);
		System.out.println(fNum);
		
		String sNum = ssn.substring(6);
		System.out.println(sNum);
		
	}

}
