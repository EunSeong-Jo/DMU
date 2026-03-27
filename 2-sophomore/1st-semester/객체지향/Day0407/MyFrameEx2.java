package Day0407;

import java.awt.Color;
import java.awt.FlowLayout;

// import javax.swing.JButton;
// import javax.swing.JFrame;
import javax.swing.*;

// 메인 프로그래밍 방식
public class MyFrameEx2 extends JFrame {

	MyFrameEx2() {
		// super("문자열 타입 타이틀");
		// this 생략 가능
		this.setTitle("문자열 타입 타이틀");
		this.setDefaultCloseOperation(EXIT_ON_CLOSE);
		
		this.setLayout(new FlowLayout());
		
		JButton btn1 = new JButton("확인");
		this.add(btn1);
		btn1.setBackground(Color.GRAY);
		
		this.add(new JButton("취소"));
		this.add(new JButton("삭제"));
		
		this.setSize(300, 200);
		this.setVisible(true);
	}
	
	public static void main(String[] args) {
		// TODO Auto-generated method stub
		// MyFrameEx2 jf2 = new MyFrameEx2();
		
		new MyFrameEx2();
	}

}
