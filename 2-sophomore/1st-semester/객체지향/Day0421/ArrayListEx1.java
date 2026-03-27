package Day0421;

import java.util.ArrayList;

public class ArrayListEx1 {

	public static void main(String[] args) {
		// TODO Auto-generated method stub

		ArrayList<String> nameList = new ArrayList<String>();
		
		nameList.add("홍길동");
		nameList.add("동양미래대");
		nameList.add("OOP");
		nameList.add("100");
		
		for (String name : nameList) {
			System.out.println(name);
		}
		
		// ----------------------------------------------------
		
		ArrayList<Integer> ageList = new ArrayList<Integer>();
		
		ageList.add(23);
		ageList.add(25);
		ageList.add(96);
		ageList.add(100);
		
		for (Integer age : ageList) {
			System.out.println(age);
		}
		
		// ----------------------------------------------------
		
		ArrayList<Student> studentList = new ArrayList<Student>();
		
		Student st1 = new Student("홍길동", "20232678", "인소과", "OOP");
		studentList.add(st1);

		studentList.add(new Student("동미대", "19650001", "없음", "없음"));
		studentList.add(new Student("김박사", "19990101", "컴공과", "객체지향"));
		
		for (Student stu : studentList) {
			System.out.println(stu);
		}
	}

}
