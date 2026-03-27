package ch.sec07;

public class instanceofexample {

	public static void personInfo(person person) {
		// TODO Auto-generated method stub

		System.out.println("name : " + person.name);
		person.walk();
		
		if(person instanceof student student) {
			System.out.println("studentNo : " + student.studentNo);
			student.study();
		}
		
	}
	
	public static void main(String[] args) {

		person p1 = new person("aaa");
		personInfo(p1);
		
		System.out.println();
		
		person p2 = new student("bbb", 10);
		personInfo(p2);
	}
}
