package ch.sec05;

public class splitexample {

	public static void main(String[] args) {
		// TODO Auto-generated method stub

		String board = "1 , 자바 , 참조타입 , 조";
		
		
		String[] tokens = board.split(",");
		
		System.out.println("번호 : " + tokens[0]);
		System.out.println("제목 : " + tokens[1]);
		System.out.println("내용 : " + tokens[2]);
		System.out.println("나 : " + tokens[3]);
		
		for(int i = 0; i < tokens.length; i++)
			System.out.println(tokens[i]);
		
	}

}
