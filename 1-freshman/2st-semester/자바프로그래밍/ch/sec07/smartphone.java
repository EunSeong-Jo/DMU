package ch.sec07;

public class smartphone extends phone{

	public boolean wifi;
	
	public smartphone(String model, String color) {
		this.model = model;
		this.color = color;
	}	
	
	public void setWifi(boolean wifi) {
		this.wifi = wifi;
		System.out.println("change wifi status");
	}
	
	public void internet() {
		System.out.println("connect internet");
	}
}
