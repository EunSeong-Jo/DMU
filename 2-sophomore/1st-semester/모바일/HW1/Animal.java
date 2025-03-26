package HW1;

// 공통된 기능(makeSound, move)을 가진 클래스이지만, 
// 일부 기능(getSpecies)은 자식 클래스에서 구현해야 하기 때문에(구현을 강제함) 추상 클래스 설정
public abstract class Animal {
	/*
	 * |   접근제어자  | 같은 클래스 | 같은 패키지 | 자식 클래스(상속) | 외부 클래스 |
	 * |   `public`  |  ✅ 가능  |  ✅ 가능   |    ✅ 가능     |  ✅ 가능   |
	 * | `protected` |  ✅ 가능  |  ✅ 가능   |    ✅ 가능     |  ❌ 불가능 |
	 * |  `private`  |  ✅ 가능  |  ❌ 불가능  |    ❌ 불가능   |  ❌ 불가능 |
	 */
	// protected를 사용해서 같은 패지키 내에서 편하게 사용 가능
	protected String name;
    protected int age;
    
    def(a, b)

    // Animal 메소드를 설정해서 이름과 나이를 리턴
    public Animal(String name, int age) {
        this.name = name;
        this.age = age;
    }
    
    // 동물의 종에 대한 추상 메소드 설정
    public abstract String getSpecies(); 

    // 출력 포멧 설정
    public void displayInfo() {
        System.out.println("이름 : " + name + ", 나이 : " + age + ", 종 : " + getSpecies());
    }
}
