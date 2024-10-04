package ch.sec07;

public class multidimensionalarraybyvaluelist {

	public static void main(String[] args) {
		// TODO Auto-generated method stub
		int[][] scores = {{80, 90, 100}, {60, 70}};
		
		System.out.println("1차원 배열 길이 : " + scores.length);
		System.out.println("2차원 배열 길이1 : " + scores[0].length);
		System.out.println("2차원 배열 길이2 : " + scores[1].length);
		
		System.out.println("scores[0][2] : " + scores[0][2]);
		System.out.println("scores[1][1] : " + scores[1][1]);
	
		int class1Sum = 0;
		for(int i = 0; i < scores[0].length; i++)
			class1Sum += scores[0][i];
		
		double class1Avg = (double)class1Sum / scores[0].length;
		System.out.println("1번 배열 평균 : " + class1Avg);
		
		// --------------------------------
		
		int class2Sum = 0;
		for(int i = 0; i < scores[1].length; i++)
			class2Sum += scores[1][i];
		
		double class2Avg = (double)class2Sum / scores[1].length;
		System.out.println("2번 배열 평균 : " + class2Avg);	
	}

}
