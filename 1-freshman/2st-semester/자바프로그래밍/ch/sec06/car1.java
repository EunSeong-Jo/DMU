package ch.sec06;

public class car1 {
	
	String company = "현대";
	String color;
	String model;
	int maxSpeed;
	
	car1(String model){
		this(model, "검정색", 200);
	}
	
	car1(String model, String color){
		this(model, color, 200);
	}
	
	car1(String model, String color, int maxSpeed){
		// this(model, color, maxSpeed);
		this.model = model;
		this.color = color;
		this.maxSpeed = maxSpeed;
	}
}
