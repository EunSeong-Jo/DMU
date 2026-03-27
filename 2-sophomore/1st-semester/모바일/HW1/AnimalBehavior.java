package HW1;

// 모든 동물들의 필수적이고 공통된 동작들을 정의하기 위해 인터페이스를 사용
// 다중 상속이 가능하여 소리, 이동 외의 다른 동작을 다른 인터페이스에서 추가적으로 상속 받을 수 있음
public interface AnimalBehavior {
    
	// 인터페이스이기 때문에 메소드만 정의하고 동작은 구현하지 않음
	void makeSound(); // 동물의 소리 출력
    void move(); // 동물의 이동 방식 출력
    
    // 나만의 메소드
    void hunt();
}
