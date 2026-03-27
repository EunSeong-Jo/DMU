package ch.sec07;

public class smartphoneexample {

	public static void main(String[] args) {

		smartphone myPhone = new smartphone("갤럭시", "검은색");
		
		System.out.println("모델 : " + myPhone.model);
		System.out.println("색상 : " + myPhone.color);
		
		System.out.println("와이파이 상태: " + myPhone.wifi);
		
		myPhone.bell();
		myPhone.sendVoice("hello");
		myPhone.receiveVoice("hi my name is ...");
		myPhone.sendVoice("hi");
		myPhone.hangUp();

		myPhone.setWifi(true);
		myPhone.internet();
	}
}
