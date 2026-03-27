package ch.sec07;

public class phone {
	
	public String model;
	public String color;
	
	public void bell() {
		System.out.println("bellllll");
	}
	
	public void sendVoice(String message) {
		System.out.println("me : " + message);
	}
	
	public void receiveVoice(String message) {
		System.out.println("you : " + message);
	}
	
	public void hangUp() {
		System.out.println("cut phone call");
	}
}
