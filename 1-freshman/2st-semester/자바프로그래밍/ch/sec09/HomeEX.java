package ch.sec09;

public class HomeEX {

	public static void main(String[] args) {
		// TODO Auto-generated method stub
		Home home = new Home();
		
		home.use1();
		
		home.use2();
		
		home.use3(new RC(){
			@Override
			public void turnOn() {
				System.out.println("turn on hit");
			}
			@Override
			public void turnOff() {
				System.out.println("turn off hit");
			}
		});
	}
}
