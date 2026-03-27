package Day0324;

public class Exam09 {

	public static void main(String[] args) {
		// TODO Auto-generated method stub
		
		Automobile pros = new Automobile();
		System.out.println(pros.getColor() + ", " + pros.getSpeed() + ", "
		+ pros.getSeatNum());
		
		Automobile benz = new Automobile("흰색", 5, 2);
		System.out.println(benz.getColor() + ", " + benz.getSpeed() + ", "
				+ benz.getSeatNum());
	
		Automobile iuAuto = new Automobile("빨강", 0, 4);
		System.out.println(iuAuto.getColor() + ", " + iuAuto.getSpeed() + ", "
				+ iuAuto.getSeatNum());
		
		iuAuto.upSpeed(400);
		System.out.println(iuAuto.getColor() + ", " + iuAuto.getSpeed() + ", "
				+ iuAuto.getSeatNum());
	}

}
