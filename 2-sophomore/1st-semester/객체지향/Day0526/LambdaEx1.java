package Day0526;

interface MyFunction {
	int calc(int x, int y);
}

public class LambdaEx1 {

	public static void main(String[] args) {
		// TODO Auto-generated method stub
		MyFunction add = (x, y) -> x + y;
		MyFunction minus = (x, y) -> x - y;
		MyFunction gop = (x, y) -> x * y;
		MyFunction na = (x, y) -> x / y;
		MyFunction mod = (x, y) -> x % y;
		
		System.out.println(add.calc(5, 2));
		System.out.println(minus.calc(5, 2));
		System.out.println(gop.calc(5, 2));
		System.out.println(na.calc(5, 2));
		System.out.println(mod.calc(5, 2));
		
	}

}
