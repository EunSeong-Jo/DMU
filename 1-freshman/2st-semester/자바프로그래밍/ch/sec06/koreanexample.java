package ch.sec06;

public class koreanexample {

	public static void main(String[] args) {
		// TODO Auto-generated method stub

		korean k1 = new korean("ppp", "010-12-34");
		
		System.out.println("nation : " + k1.nation);
		System.out.println("name : " + k1.name);
		System.out.println("phoneNum : " + k1.phoneNum + "\n");
		
		korean k2 = new korean("kkk", "010-56-78");

		System.out.println("nation2 : " + k2.nation);
		System.out.println("name2 : " + k2.name);
		System.out.println("phoneNum2 : " + k2.phoneNum);
		
	}

}
