package Day0414;

import java.awt.GridLayout;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;

import javax.swing.JButton;
import javax.swing.JFrame;
import javax.swing.JLabel;

public class ExamGr1 extends JFrame{

	public ExamGr1() {
		// TODO Auto-generated constructor stub
		setTitle("레이블 예제");
		setDefaultCloseOperation(EXIT_ON_CLOSE);
		setSize(500, 400);
		setVisible(true);
		
//		GridLayout grid = new GridLayout(3, 1);
//		setLayout(grid);
		setLayout(new GridLayout(3, 1));
		
		JLabel lab1 = new JLabel("기본 텍스트");
		add(lab1);
		
		JButton btnHi = new JButton("안녕");
		add(btnHi);
		btnHi.addActionListener(new ActionListener() {
			@Override
			public void actionPerformed(ActionEvent e) {
				// TODO Auto-generated method stub
				lab1.setText("안녕하세요");
			}
		});
		
		
		JButton btnBi = new JButton("잘가");
		add(btnBi);
		btnBi.addActionListener(new ActionListener() {
			@Override
			public void actionPerformed(ActionEvent e) {
				// TODO Auto-generated method stub
				lab1.setText("잘가세요");
			}
		});
	}
	
	
	public static void main(String[] args) {
		// TODO Auto-generated method stub
		new ExamGr1();
	}

}
