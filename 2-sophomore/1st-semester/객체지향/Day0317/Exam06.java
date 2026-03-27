package Day0317;

public class Exam06 {
	
	public static void main(String[] args) {
		// TODO Auto-generated method stub
		try {
			int num1 = 100, num2 = 0;
			System.out.println(num1 / num2);
		} catch (Exception e) {
			// TODO: handle exception
			// StackTrace : 스텍 구조
			e.printStackTrace();
			System.out.println("오류 발생");
		}
		
	}

}
