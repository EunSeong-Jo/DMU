package Day0414;

import java.awt.FlowLayout;
import java.awt.event.ActionListener;

import javax.swing.JButton;
import javax.swing.JFrame;

import Day0407.MyFrameEx1;

public class IndepClassListener extends JFrame{

	public IndepClassListener() {
		setTitle("Action 이벤트 리스너 예제");
		setDefaultCloseOperation(EXIT_ON_CLOSE);
		setSize(300, 200);
		setVisible(true);
		
		setLayout(new FlowLayout());
		JButton btn = new JButton("Action");
		add(btn);
		
		MyAction MA = new MyAction();
		
		btn.addActionListener(MA);
		
	}
	
	public static void main(String[] args) {
		// TODO Auto-generated method stub
		new IndepClassListener();
	}
}
