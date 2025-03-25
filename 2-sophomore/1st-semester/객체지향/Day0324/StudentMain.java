package Day0324;

public class StudentMain {

	public static void main(String[] args) {
		// TODO Auto-generated method stub

		Student s1 = new Student("김", "구로", "010-1234-5678", "20250324", "인소과");
		Student s2 = new Student("이", "구로", "010-5678-1234", "24032025", "인소과");
		
		s1.print();
		System.out.println();
		s2.print();
		
	}

}
