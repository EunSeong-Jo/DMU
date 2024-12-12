package ch.sec06;

public class car2 {
	
	private int speed;
	private boolean stop;
	
	public int getSpeed() {
		return speed;
	}
	
	public boolean isStop() {
		return stop;
	}
	
	public void setSpeed(int speed) {
		if(speed <= 0) {
			this.speed = 0;
			return;
		}
		else {
			this.speed = speed;
			this.stop = false;
		}
	}
	
	public void setStop(boolean stop) {
		this.stop = stop;
		if (stop == true)
			this.speed = 0;
	}

}
