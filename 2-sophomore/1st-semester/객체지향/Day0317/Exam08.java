package Day0317;

public class Exam08 {

	public static void main(String[] args) {
		// TODO Auto-generated method stub

		Student me = new Student("김길동", 251234, 20);
		System.out.println(me.getName() + ", " + me.getStuId() + ", " + me.getAge());
		
		Student you = new Student("이길동", 255678, 25);
		System.out.println(you.getName() + ", " + you.getStuId() + ", " + you.getAge());
		
		System.out.println("학생 수 : " + Student.studentCount);
	}

}
