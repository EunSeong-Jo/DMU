package HW1;

// extends : 클래스 상속
// implements : 인터페이스 구현
public class Lion extends Animal implements AnimalBehavior {
    
	// 자식 클래스가 만들어질 때는 먼저 부모 클래스의 생성자가 실행되어야함
	public Lion(String name, int age) {
		// Lion 클래스에서 부모 클래스 Animal에 있는 생성자 호출하여 실행
        super(name, age);
    }

    @Override
    public String getSpecies() {
        return "사자";
    }

    @Override
    public void makeSound() {
        System.out.println(name + "가 으르렁거립니다!");
    }

    @Override
    public void move() {
        System.out.println(name + "가 초원을 달립니다.");
    }
    
    @Override
    public void hunt() {
    	// 사자는 70%확률로 사냥에 성공함
    	if (Math.random() > 0.3) {
    		System.out.println(name + "가 사냥에 성공했습니다.");
    	}
    	else {
    		System.out.println(name + "가 사냥에 실패했습니다.");
    	}
    }
}
