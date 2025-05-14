package Day0421;

import java.awt.FlowLayout;
import java.awt.GridLayout;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;

import javax.swing.JButton;
import javax.swing.JFrame;
import javax.swing.JLabel;
import javax.swing.JPasswordField;
import javax.swing.JTextField;

public class HW2 extends JFrame{

	public HW2() {
		// TODO Auto-generated constructor stub
		setTitle("LOGIN FORM");
		setDefaultCloseOperation(EXIT_ON_CLOSE);
		setSize(500, 200);
		
		setLayout(new GridLayout(3, 2));
		
		add(new JLabel("이메일"));
		JTextField txt1 = new JTextField();
		add(txt1);
		
		add(new JLabel("비밀번호"));
		JPasswordField txt2 = new JPasswordField();
		add(txt2);
		
		JButton btnL = new JButton("로그인");
		add(btnL);
		btnL.addActionListener(new ActionListener() {
			@Override
			public void actionPerformed(ActionEvent e) {
				// TODO Auto-generated method stub
				String useremail = txt1.getText().toString();
				String userpass = txt2.getText().toString();
				
				if (useremail.equals("hong@google.com") && userpass.equals("1234")) {
					System.out.println("이메일 : " + useremail + "\n" + 
										"비밀번호 : " + userpass + "\n" + 
										"는 로그인되었습니다.");
				}
				else {
					System.out.println("이메일과 비밀번호를 다시 입력하십시오");
				}
			}
		});
	
		JButton btnC = new JButton("취소");
		add(btnC);
		btnC.addActionListener(new ActionListener() {
			@Override
			public void actionPerformed(ActionEvent e) {
				// TODO Auto-generated method stub
				txt1.setText("");
				txt2.setText("");
			}
		});
		
		setVisible(true);	
	}
	
	public static void main(String[] args) {
		// TODO Auto-generated method stub
		new HW2();
	}

}
