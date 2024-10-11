package ch.sec05;

public class advancedforexample {

	public static void main(String[] args) {
		// TODO Auto-generated method stub
		int[] scores = {42,46,74,49,29};
		int sum = 0;
		
		for(int score : scores) {
			sum += score;
		}
		
		System.out.println(sum);
		
		double avg = (double)sum / scores.length;
		System.out.println(avg);
		
	}

}
