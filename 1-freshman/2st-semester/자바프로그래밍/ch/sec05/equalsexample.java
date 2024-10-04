package ch.sec05;

public class equalsexample {

	public static void main(String[] args) {
		// TODO Auto-generated method stub

		String strVar1 = "홍";
		String strVar2 = "홍";

		if(strVar1 == strVar2)
			System.out.println("같은 주소");
		else
			System.out.println("다른 주소");
		
		if(strVar1.equals(strVar2))
			System.out.println("같은 문자열");
		
		// ----------------------------------
		
		String strVar3 = new String("홍");
		String strVar4 = new String("홍");
		
		if(strVar3 == strVar4)
			System.out.println("같은 주소");
		else
			System.out.println("다른 주소");
		
		if(strVar3.equals(strVar4))
			System.out.println("같은 문자열");
	}

}
