package ch.sec03;

public class bitlogicexample {

	public static void main(String[] args) {
		// TODO Auto-generated method stub
		System.out.println("45 & 25 = " + (45 & 25));
		System.out.println("45 | 25 = " + (45 | 25));
		System.out.println("45 ^ 25 = " + (45 ^ 25));
		System.out.println("~45 = " + (~45));
		
		byte receivedata = -120;
		
		// -120 & 255
		int unsignedint1 = receivedata & 255;
		System.out.println(unsignedint1);
		
		// -120
		int unsignedint2 = Byte.toUnsignedInt(receivedata);
		System.out.println(unsignedint2);
		
		// -128 ~ 127 범위 외에 있는 136 치환
		int test = 136;
		byte btest = (byte)test;
		System.out.println(btest);
	}

}