package Day0317;
// 클래스
public class Car {
	// 필드
	// private String color;
	// private int speed;
	protected String color;
	protected int speed;
	
	static int carCount = 0;
	
	final static int MAXSPEED = 200;
	final static int MINSPEED = 0;
	
	static int currentCarCount() {
		return carCount;
	}
	
	// 생성자
	public Car(){ } // 기본 생성자
	
	public Car(String color, int speed){
		this.color = color;
		this.speed = speed;
		
		carCount++;
	}
	
	// 메소드
	public int upSpeed(int value){
		speed = speed + value;
		if(speed > 200) {
			speed = 200;
		}
		return speed;
	}
	
	int downSpeed(int value) {
		speed = speed - value;
		if(speed < 0) {
			speed = 0;
		}
		return speed;
	}
	
	public String getColor() {
		return color;
	}
	public void setColor(String color) {
		this.color = color;
	}
	public int getSpeed() {
		return speed;
	}
	public void setSpeed(int speed) {
		this.speed = speed;
	}
	
}
