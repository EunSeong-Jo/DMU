package Day0326;

public class User {
    private String name;
    private int age;

    public User(String name, int age) {
        this.name = name;
        this.age = age;
    }

    // 사용자 정보를 문자열로 반환
    @Override
    public String toString() {
        return "이름: " + name + ", 나이: " + age;
    }
}
