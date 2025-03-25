package HW1;

public class Penguin extends Animal implements AnimalBehavior {
    public Penguin(String name, int age) {
        super(name, age);
    }

    @Override
    public String getSpecies() {
        return "펭귄";
    }

    @Override
    public void makeSound() {
        System.out.println(name + "가 꽥꽥거립니다!");
    }

    @Override
    public void move() {
        System.out.println(name + "가 뒤뚱뒤뚱 걷습니다.");
    }
    
    @Override
    public void hunt() {
    	if (Math.random() > 0.6) {
    		System.out.println(name + "가 사냥에 성공했습니다.");
    	}
    	else {
    		System.out.println(name + "가 사냥에 실패했습니다.");
    	}
    }
}
