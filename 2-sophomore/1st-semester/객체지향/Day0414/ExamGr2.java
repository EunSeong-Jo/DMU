package Day0414;

import java.awt.GridLayout;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;

import javax.swing.JButton;
import javax.swing.JFrame;
import javax.swing.JLabel;
import javax.swing.JPasswordField;
import javax.swing.JTextField;

public class ExamGr2 extends JFrame{

	public ExamGr2() {
		// TODO Auto-generated constructor stub
		setTitle("로그인 폼");
		setDefaultCloseOperation(EXIT_ON_CLOSE);
		setSize(400, 300);
		setVisible(true);
		
		setLayout(new GridLayout(3, 2));
		
		JLabel lab1 = new JLabel("아이디");
		add(lab1);
		
		JTextField text1 = new JTextField();
		add(text1);
		
		JLabel lab2 = new JLabel("비밀번호");
		add(lab2);
		
		JPasswordField pass1 = new JPasswordField();
		add(pass1);
		
		JButton btn1 = new JButton("로그인");
		add(btn1);
		btn1.addActionListener(new ActionListener() {
			@Override
			public void actionPerformed(ActionEvent e) {
				// TODO Auto-generated method stub
				String strId = text1.getText();
				String strPw = pass1.getText();
				
				// &&
				if (strId.equals("dongyang") & strPw.equals("1234")) {
					System.out.println("로그인 완료");
				}
				else {
					System.out.println("오류");
				}
			}
		});
		
		JButton btn2 = new JButton("취소");
		add(btn2);
		btn2.addActionListener(new ActionListener() {
			@Override
			public void actionPerformed(ActionEvent e) {
				// TODO Auto-generated method stub
				text1.setText("");
				pass1.setText("");
			}
		});
	}
	
	
	public static void main(String[] args) {
		// TODO Auto-generated method stub
		new ExamGr2();
	}

}
