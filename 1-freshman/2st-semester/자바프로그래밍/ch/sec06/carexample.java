package ch.sec06;

public class carexample {

	public static void main(String[] args) {
		// TODO Auto-generated method stub
		car myCar = new car();
		
		System.out.println("start : " + myCar.start);
		System.out.println("company : " + myCar.company);
		System.out.println("model : " + myCar.model);
		System.out.println("color : " + myCar.color);
		System.out.println("maxSpeed : " + myCar.maxSpeed);
		System.out.println("speed : " + myCar.speed);
		
		myCar.speed = 999;
		System.out.println("speed : " + myCar.speed);
	}

}
