package Day0317;

public class Exam07 {

	public static void main(String[] args) {
		// TODO Auto-generated method stub

		Car myCar1 = new Car();
		System.out.println(myCar1.getColor() + ", " + myCar1.getSpeed());
		
		Car myCar2 = new Car("흰색", 10);

		Car myCar3 = new Car("검정", 222);
		
		Car anyCar1 = new Car("빨강", -99);
		
		Car youCar1 = new Car("파랑", 50);
		
		System.out.println(anyCar1.getColor() + ", " + anyCar1.getSpeed());
		
		anyCar1.upSpeed(300);
		
		System.out.println(anyCar1.getColor() + ", " + anyCar1.getSpeed());

		System.out.println("생산된 차 개수(정적 필드) : " + Car.carCount);
		System.out.println("생산된 차 개수(정적 메소드) : " + Car.currentCarCount());
		System.out.println("최고 속도 : " + Car.MAXSPEED);
		
		System.out.println("파이 값 : " + Math.PI);
		System.out.println("3 ^ 5 : " + Math.pow(3, 5));
		
	}

}
