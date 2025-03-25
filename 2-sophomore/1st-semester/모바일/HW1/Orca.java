package HW1;

public class Orca extends Animal implements AnimalBehavior {
    public Orca(String name, int age) {
        super(name, age);
    }

    @Override
    public String getSpecies() {
        return "범고래";
    }

    @Override
    public void makeSound() {
        System.out.println(name + "가 끽끽 소리를 냅니다!");
    }

    @Override
    public void move() {
        System.out.println(name + "가 빠르게 헤엄칩니다.");
    }
    
    @Override
    public void hunt() {
    	if (Math.random() > 0.2) {
    		System.out.println(name + "가 사냥에 성공했습니다.");
    	}
    	else {
    		System.out.println(name + "가 사냥에 실패했습니다.");
    	}
    }
}
