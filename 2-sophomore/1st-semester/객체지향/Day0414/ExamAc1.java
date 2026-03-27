package Day0414;

import java.awt.FlowLayout;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;

import javax.swing.JButton;
import javax.swing.JFrame;

public class ExamAc1 extends JFrame{

	public ExamAc1() {
		setTitle("Action 이벤트 리스너 예제");
		setDefaultCloseOperation(EXIT_ON_CLOSE);
		setSize(300, 200);
		setVisible(true);
		
		setLayout(new FlowLayout());
		
//		add(new JButton("확인").addActionListener(new ActionListener() {
//			@Override
//			public void actionPerformed(ActionEvent e) {
//				// TODO Auto-generated method stub
//				System.out.println("확인 버튼 클릭");
//			}
//		}));
		
		JButton btnOk = new JButton("확인");
		add(btnOk);
		btnOk.addActionListener(new ActionListener() {
			
			@Override
			public void actionPerformed(ActionEvent e) {
				// TODO Auto-generated method stub
				System.out.println("확인 버튼 클릭");
				System.out.println(e);
			}
		});
		
		
		JButton btnCancel = new JButton("취소");
		add(btnCancel);
		btnCancel.addActionListener(new ActionListener() {
			
			@Override
			public void actionPerformed(ActionEvent e) {
				// TODO Auto-generated method stub
				System.out.println("취소 버튼 클릭");
				System.out.println(e);
			}
		});
	
	}
	
	public static void main(String[] args) {
		// TODO Auto-generated method stub
		new ExamAc1();
	}
}
