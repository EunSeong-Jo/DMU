package Day0407;

import java.awt.GridLayout;

//import javax.swing.JButton;
//import javax.swing.JFrame;
//import javax.swing.JLabel;
//import javax.swing.JTextField;
import javax.swing.*;

public class GridLayoutEx extends JFrame{

	GridLayoutEx(){
		setTitle("그리드 레이아웃");
		setDefaultCloseOperation(EXIT_ON_CLOSE);
		
		GridLayout grid = new GridLayout(5, 2);
		grid.setVgap(10);
		
		setLayout(grid);
		
		add(new JLabel("이름"));
		add(new JTextField(""));
		
		add(new JLabel("학번"));
		add(new JTextField(""));
		
		add(new JLabel("학과"));
		add(new JTextField(""));
		
		add(new JLabel("과목"));
		add(new JTextField(""));
		
		add(new JButton("확인"));
		add(new JButton("취소"));
		
		setSize(400, 200);
		setVisible(true);
	}
	
	public static void main(String[] args) {
		// TODO Auto-generated method stub
		new GridLayoutEx();
	}
}
