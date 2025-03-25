package Day0324;

import javax.sound.sampled.Control.Type;

interface ClickList {
	void print();
}

public class Exam13 {

	public static void main(String[] args) {
		// TODO Auto-generated method stub

		ClickList object1 = new ClickList() {
			
			@Override
			public void print() {
				// TODO Auto-generated method stub
				System.out.println("클릭 리스트");
			}
		};
		
		object1.print();
		
		int a = Integer.parseInt("100");
		System.out.println(a + 1);
	}

}
