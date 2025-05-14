package Day0414;

import java.awt.GridLayout;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;

import javax.swing.JButton;
import javax.swing.JFrame;
import javax.swing.JLabel;
import javax.swing.JTextField;

public class ExamGr3 extends JFrame{

	public ExamGr3() {
		// TODO Auto-generated constructor stub
		setTitle("그리드 레이아웃 로그인");
		setDefaultCloseOperation(EXIT_ON_CLOSE);
		setSize(500, 300);
		
		setLayout(new GridLayout(5, 2));
		
		add(new JLabel("이름"));
		JTextField text1 = new JTextField();
		add(text1);
		
		add(new JLabel("학번"));
		JTextField text2 = new JTextField();
		add(text2);
		
		add(new JLabel("학과"));
		JTextField text3 = new JTextField();
		add(text3);
		
		add(new JLabel("과목"));
		JTextField text4 = new JTextField();
		add(text4);
		
		JButton btnOk = new JButton("확인");
		add(btnOk);
		btnOk.addActionListener(new ActionListener() {
			@Override
			public void actionPerformed(ActionEvent e) {
				// TODO Auto-generated method stub
				String strName = text1.getText();
				String strNum = text2.getText();
				String strSub = text3.getText();
				String strCla = text4.getText();
				
				System.out.println("이름 : " + strName + ", " + 
									"학번 : " + strNum + ", " + 
									"학과 : " + strSub + ", " + 
									"과목 : " + strCla + " 확인이 되었습니다!!!");
			}
		});
		
		JButton btnCancel = new JButton("취소");
		add(btnCancel);
		btnCancel.addActionListener(new ActionListener() {
			@Override
			public void actionPerformed(ActionEvent e) {
				// TODO Auto-generated method stub
				text1.setText("");
				text2.setText("");
				text3.setText("");
				text4.setText("");
			}
		});
		
		setVisible(true);
	}
	
	
	
	public static void main(String[] args) {
		// TODO Auto-generated method stub
		new ExamGr3();
	}

}
