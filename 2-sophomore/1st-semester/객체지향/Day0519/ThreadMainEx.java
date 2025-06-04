package Day0519;

public class ThreadMainEx {

	public static void main(String[] args) {
		// TODO Auto-generated method stub
		long id = Thread.currentThread().getId();
		
		String name = Thread.currentThread().getName();
		
		int priority = Thread.currentThread().getPriority();
		
		Thread.State s = Thread.currentThread().getState();
		
		System.out.println("name(이름) = " + name);
		System.out.println("id(아이디) = " + id);
		System.out.println("priority(우선순위 값) = " + priority);
		System.out.println("state(상태) = " + s);
	}

}
