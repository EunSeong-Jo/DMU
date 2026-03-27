package ch.sec05;

public class arraycreatebyvaluelist2 {

	public static void main(String[] args) {
		// TODO Auto-generated method stub

		int[] scores;
		int sum1 = 0;
		
		scores = new int[] {80, 90, 100};
		
		for(int i = 0; i < 3; i++)
			sum1 += scores[i];
		
		System.out.println("합" + sum1);
		
		printItem(new int[] {81, 91, 101});
	}
	public static void printItem(int[] scores1) {
		for(int i = 0; i < 3; i++)
			System.out.println("score[" + i + "] : " + scores1[i]);
	}

}
