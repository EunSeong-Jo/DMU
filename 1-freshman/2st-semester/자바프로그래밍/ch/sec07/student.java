package ch.sec07;

public class student extends person{

	public int studentNo;
	
	public student(String name, int studentNo) {
		super(name);
		this.studentNo = studentNo;
	}
	
	public void study() {
		System.out.println("study.");
	}
}
