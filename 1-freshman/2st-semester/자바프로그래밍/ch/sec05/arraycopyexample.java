package ch.sec05;

public class arraycopyexample {

	public static void main(String[] args) {
		// TODO Auto-generated method stub
		String[] oldStrArray = {"java", "array", "copy"};
		String[] newStrArray = new String[5];
		
		System.arraycopy(oldStrArray, 0, newStrArray, 0, oldStrArray.length);

		for(int i = 0; newStrArray.length > i; i++) {
			System.out.print(newStrArray[i] + ", ");
		}
		
	}

}
