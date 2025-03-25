package HW1;

public class Snake extends Animal implements AnimalBehavior {
    public Snake(String name, int age) {
        super(name, age);
    }

    @Override
    public String getSpecies() {
        return "뱀";
    }

    @Override
    public void makeSound() {
        System.out.println(name + "가 스스스 소리를 냅니다!");
    }

    @Override
    public void move() {
        System.out.println(name + "가 기어갑니다.");
    }
    
    @Override
    public void hunt() {
    	if (Math.random() > 0.5) {
    		System.out.println(name + "가 사냥에 성공했습니다.");
    	}
    	else {
    		System.out.println(name + "가 사냥에 실패했습니다.");
    	}
    }
}
