package ch.sec05;

import java.util.Arrays;

public class arraycopybyforexample {

	public static void main(String[] args) {
		// TODO Auto-generated method stub
		int[] oldIntArray = {1,2,3};
		int[] newIntArray = new int[5];
		
		// 주소값 출력
		System.out.println(newIntArray);
		// 배열값 출력
		System.out.println(Arrays.toString(newIntArray));
		// 인덱스 지정은 출력
		System.out.println(newIntArray[3]);
		
		for(int i = 0; oldIntArray.length > i; i++) {
			newIntArray[i] = oldIntArray[i];
		}
		
		for(int i = 0; newIntArray.length > i; i++) {
			System.out.print(newIntArray[i] + ", ");
		}
		
	}

}
