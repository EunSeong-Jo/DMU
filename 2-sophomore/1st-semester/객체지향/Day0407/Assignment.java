package Day0407;

import java.awt.GridLayout;

//import javax.swing.JButton;
//import javax.swing.JFrame;
//import javax.swing.JLabel;
//import javax.swing.JPasswordField;
//import javax.swing.JTextField;
import javax.swing.*;

public class Assignment extends JFrame{

	public Assignment() {
		// TODO Auto-generated constructor stub
		setTitle("로그인");
		setDefaultCloseOperation(EXIT_ON_CLOSE);
		
		GridLayout grid = new GridLayout(3, 2);
		grid.setVgap(10);
		
		setLayout(grid);
		
		add(new JLabel("사용자"));
		add(new JTextField());
		
		add(new JLabel("비밀번호"));
		add(new JPasswordField());
	
		add(new JButton("로그인"));
		add(new JButton("취소"));
		
		setSize(500, 200);
		setVisible(true);
	}
	
	public static void main(String[] args) {
		// TODO Auto-generated method stub
		new Assignment();
	}
}
