package Day0421;

public class Student {

	// 1. 속성
	// private = 캡슐화 (시험)
	private String name, stuId, dept, subj;
	
	// 2. 생성자
	public Student() {
		// TODO Auto-generated constructor stub
	}
	
	// 생성 설정 (시험)
	Student(String name, String stuId, String dept, String subj){
		this.name = name;
		this.stuId = stuId;
		this.dept = dept;
		this.subj = subj;
	}

	// 3. 메소드
	// getter, setter 작성 (시험)
	public String getName() {
		return name;
	}

	public void setName(String name) {
		this.name = name;
	}

	public String getStuId() {
		return stuId;
	}

	public void setStuId(String stuId) {
		this.stuId = stuId;
	}

	public String getDept() {
		return dept;
	}

	public void setDept(String dept) {
		this.dept = dept;
	}

	public String getSubj() {
		return subj;
	}

	public void setSubj(String subj) {
		this.subj = subj;
	}

	@Override
	public String toString() {
		return "이름 : " + name + ", 학번 : " + stuId + ", 학과 : " + dept + ", 과목 : " + subj;
	}
	
}
