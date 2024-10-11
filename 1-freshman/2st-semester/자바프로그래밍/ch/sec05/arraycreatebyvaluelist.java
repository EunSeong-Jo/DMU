package ch.sec05;

public class arraycreatebyvaluelist {

	public static void main(String[] args) {
		// TODO Auto-generated method stub

		String[] season = {"spring", "summer", "fall", "winter"};
		
		System.out.println("season[0] : " + season[0]);
		System.out.println("season[1] : " + season[1]);
		System.out.println("season[2] : " + season[2]);
		System.out.println("season[3] : " + season[3]);
		
		season[1] = "여름";
		System.out.println("season[1] : " + season[1]);
		
		int[] scores = {83, 90, 87};
		int sum = 0;
		
		for(int i = 0; i < 3; i++)
			sum += scores[i];
		
		System.out.println("합 : " + sum);
		double avg = (double)sum / 3;
		System.out.println("평균 : " + avg);
	}

}
