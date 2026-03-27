package Day0526;

// 설계도
import java.time.LocalDateTime;

public class Addr {
	// 필드
	private String name;				// 이름
	private String tel;					// 전화번호
	private String com;					// 회사명
	private LocalDateTime createDate;   // 입력시간
	
	// 생성자 2개
	public Addr() {
		// TODO Auto-generated constructor stub
	}
	
	public Addr(String name, String tel, String com, LocalDateTime createDate) {
		super();
		this.name = name;
		this.tel = tel;
		this.com = com;
		this.createDate = createDate;
	}

	// 메소드 getter, setter, toString() 
	public String getName() {
		return name;
	}

	public void setName(String name) {
		this.name = name;
	}

	public String getTel() {
		return tel;
	}

	public void setTel(String tel) {
		this.tel = tel;
	}

	public String getCom() {
		return com;
	}

	public void setCom(String com) {
		this.com = com;
	}

	public LocalDateTime getCreateDate() {
		return createDate;
	}

	public void setCreateDate(LocalDateTime createDate) {
		this.createDate = createDate;
	}

	@Override
	public String toString() {
		return "name=" + name + ", phone=" + tel + ", companyName=" + com + ", createDate=" + createDate;
	}
	
}
