package ch.sec09;

public class Home {

	private RC rc = new RC() {
		@Override
		public void turnOn() {
			System.out.println("turn on tv.");
		}
		
		@Override
		public void turnOff() {
			System.out.println("turn off tv.");
		}
	};
	
	public void use1() {
		rc.turnOn();
		rc.turnOff();
	}
	
	public void use2() {
		RC rc = new RC() {
			@Override
			public void turnOn() {
				System.out.println("turn on aircone");
			}
			@Override
			public void turnOff() {
				System.out.println("turn off aircone");
			}
		};
		rc.turnOn();
		rc.turnOff();
	}
	
	public void use3(RC rc) {
		rc.turnOn();
		rc.turnOff();
	}
}
