package Day0324;

public interface IAnimal {

	// 추상 메소드
	// abstract void eat();
	void eat();
	
}

class ICat implements IAnimal {
	
	@Override
	public void eat() {
		System.out.println("i like fish");
	}
}

class ITiger extends Animal implements IAnimal {
	
	@Override
	public void eat() {
		System.out.println("i like pig");
	}
	
	@Override
	void move() {
		System.out.println("4발로 이동한다");
	}
}

