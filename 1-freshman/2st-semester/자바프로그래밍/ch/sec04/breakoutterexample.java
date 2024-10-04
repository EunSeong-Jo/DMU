package ch.sec04;

public class breakoutterexample {

	public static void main(String[] args) {
		// TODO Auto-generated method stub
		out: for(char upper = 'A'; upper <= 'Z'; upper++) {
			for(char lower = 'a'; lower <= 'z'; lower++) {
				System.out.println(upper + "-" + lower);
				if(lower == 'g') {
					break out;
				}
			}
		}
		System.out.println("exit");
	}

}
