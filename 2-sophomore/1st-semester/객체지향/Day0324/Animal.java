package Day0324;

abstract public class Animal {

	protected String name;
	
	Animal(){}
	
	Animal(String name){
		this.name = name;
	}

	abstract void move();
	
	public String getName() {
		return name;
	}

	public void setName(String name) {
		this.name = name;
	}
	
	
	public static class Eagle extends Animal{
	
		// 속성
		private String home;
	
		// 생성자
		Eagle(){}
	
		Eagle(String name, String home){
			super(name);
			this.home = home;
		}

		// 메소드
		public String getHome() {
			return home;
		}

		public void setHome(String home) {
			this.home = home;
		}
		
		@Override
		void move() {
			System.out.println("날아간다.");
		}
		
	}
	
	
	public static class Tiger extends Animal{
		
		private int age;
	
		Tiger(){}
	
		Tiger(String name, int age){
			super(name);
			this.age = age;
		}
		

		public int getAge() {
			return age;
		}

		public void setAge(int age) {
			this.age = age;
		}

		@Override
		void move() {
			System.out.print("걸어간다.");
		}
		
	}
	
	
}
