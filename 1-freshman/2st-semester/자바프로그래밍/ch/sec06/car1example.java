package ch.sec06;

public class car1example {

	public static void main(String[] args) {
		// TODO Auto-generated method stub
		car1 car5 = new car1("차차");
		System.out.println("car5 company : " + car5.company);
		System.out.println("car5 model : " + car5.model);
		System.out.println("car5 color : " + car5.color);
		System.out.println("car5 maxSpeed : " + car5.maxSpeed + "\n");
		
		car1 car6 = new car1("자가용", "흰색");
		System.out.println("car6 company : " + car6.company);
		System.out.println("car6 model : " + car6.model);
		System.out.println("car6 color : " + car6.color);
		System.out.println("car6 maxSpeed : " + car6.maxSpeed + "\n");
		
		car1 car7 = new car1("택시", "주황", 300);
		System.out.println("car7 company : " + car7.company);
		System.out.println("car7 model : " + car7.model);
		System.out.println("car7 color : " + car7.color);
		System.out.println("car7 maxSpeed : " + car7.maxSpeed);
	}

}
