package Day0526;

import java.awt.FlowLayout;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;

import javax.swing.JButton;
import javax.swing.JFrame;
import javax.swing.JLabel;

public class LambdaEx3 extends JFrame{

	public LambdaEx3() {
		// TODO Auto-generated constructor stub
		setTitle("람다 판넬예제");
		setDefaultCloseOperation(EXIT_ON_CLOSE);
		
		setSize(500, 200);
		setVisible(true);
		
		setLayout(new FlowLayout());
		JLabel label1 = new JLabel("아이스크림을 좋아하나요??");
		add(label1);
		
		JButton btnY = new JButton("Yes");
		add(btnY);
		btnY.addActionListener(e -> label1.setText("예, 아이스크림을 좋아합니다."));
		
		JButton btnN = new JButton("No");
		add(btnN);
		btnN.addActionListener(e -> label1.setText("아니오, 아이스크림을 좋아하지 않습니다."));
		
	}
	
	public static void main(String[] args) {
		// TODO Auto-generated method stub
		new LambdaEx3();
	}

}
