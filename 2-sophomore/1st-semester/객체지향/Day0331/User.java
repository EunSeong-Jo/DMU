package Day0331;

public class User {
	// 속성
    private String name;
    private int age;

    // 생성자
    User(){}
    User(String name, int age) {
    	this.name = name;
    	this.age = age;
    }

    // 메소드
	@Override
	public String toString() {
		return "이름=" + name + ", 나이=" + age;
	}

	public String getName() {
		return name;
	}

	public void setName(String name) {
		this.name = name;
	}

	public int getAge() {
		return age;
	}

	public void setAge(int age) {
		this.age = age;
	}
    
}
