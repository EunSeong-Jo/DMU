package Day0407;

import java.awt.BorderLayout;
import java.awt.FlowLayout;

import javax.swing.JButton;
import javax.swing.JFrame;

public class BorderLayoutEx extends JFrame{

	BorderLayoutEx(){
		setTitle("보더 레이아웃");
		setDefaultCloseOperation(EXIT_ON_CLOSE);
		
		// 너비 간격 30, 높이 간격 20
		// setLayout(new BorderLayout(30, 20));
		setLayout(new BorderLayout());
		
		add(new JButton("add"), BorderLayout.NORTH);
		add(new JButton("sub"), BorderLayout.SOUTH);
		add(new JButton("mul"), BorderLayout.EAST);
		add(new JButton("div"), BorderLayout.WEST);
		add(new JButton("Calculate"), BorderLayout.CENTER);
		
		setSize(300, 200);
		setVisible(true);
	}
	
	public static void main(String[] args) {
		// TODO Auto-generated method stub
		new BorderLayoutEx();
	}
}
