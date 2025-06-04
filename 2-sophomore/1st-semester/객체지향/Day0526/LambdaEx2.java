package Day0526;

interface MyFunction2 {
	int calc(int x);
}

public class LambdaEx2 {

	public static void main(String[] args) {
		// TODO Auto-generated method stub
		MyFunction2 square = x -> x * x;
		
		System.out.println(square.calc(5));
		
	}

}
