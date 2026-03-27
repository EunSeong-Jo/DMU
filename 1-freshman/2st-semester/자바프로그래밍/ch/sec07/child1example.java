package ch.sec07;

public class child1example {

	public static void main(String[] args) {
		// TODO Auto-generated method stub

		parent1 parent = new child1();
		
		parent.field1 = "data1";
		parent.method1();
		parent.method2();
		
		child1 child = (child1)parent;

		child.field2 = "yyy";
		child.method3();
	}

}
