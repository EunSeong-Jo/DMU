package Day0324;

// color, speed가 private이기 때문에 직접 접근이 불가능함
import Day0317.Car;

public class Automobile extends Car{
	
	private int seatNum;
	
	public Automobile(){ }
	
	public Automobile(String color, int speed, int seatNum){
		super(color, speed);
		this.seatNum = seatNum;
	}
	
	@Override
	public int upSpeed(int value){
		speed = speed + value;
		if(speed > 300) {
			speed = 300;
		}
		return speed;
	}

	public int getSeatNum() {
		return seatNum;
	}

	public void setSeatNum(int seatNum) {
		this.seatNum = seatNum;
	}

}
