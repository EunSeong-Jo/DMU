package HW1;

public class Zoo {
    public static void main(String[] args) {
        
    	// 같은 패키지 내에 있기 때문에 import를 하지 않아도 사용 가능함
    	// 다른 패키지에 있는 클래스는 import가 필요함
    	// 인터페이스도 타입으로 선언 가능
    	// 배열 내의 객체들은 인터페이스를 implements한 클래스여야 함
    	AnimalBehavior[] animals = {
            new Lion("심바", 5),
            new Penguin("펭수", 3),
            new Snake("아나콘다", 2),
            new Orca("소피아", 60)
        };
        
        for (AnimalBehavior animal : animals) {
            
        	// animal 변수가 Animal 클래스 타입이라면...
        	if (animal instanceof Animal) {
        		// animal은 animals의 값을 받아오고, animals는 AnimalBehavior 타입이기 때문에
        		// displayInfo를 받아올 수 있는 Animal 클래스로 강제 형변환
                ((Animal) animal).displayInfo();

        	}
            
        	// 강제로 형변환이 이루어진 if문이 끝났음으로 다시 AnimalBehavior 타입으로 돌아옴
        	animal.makeSound();
            animal.move();
            
            animal.hunt();
            System.out.println();
        }
    }
}

