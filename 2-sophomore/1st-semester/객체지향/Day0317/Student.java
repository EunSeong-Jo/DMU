package Day0317;

public class Student {
	
	private String name;
	private int stuId;
	private int age;
	
	static int studentCount = 0;
	
	// 상속 시 사용
	Student(){}
	
	Student(String name, int stuId, int age){
		this.name = name;
		this.stuId = stuId;
		this.age = age;
		
		studentCount++;
	}

	public String getName() {
		return name;
	}

	public void setName(String name) {
		this.name = name;
	}

	public int getStuId() {
		return stuId;
	}

	public void setStuId(int stuId) {
		this.stuId = stuId;
	}

	public int getAge() {
		return age;
	}

	public void setAge(int age) {
		this.age = age;
	}

}
