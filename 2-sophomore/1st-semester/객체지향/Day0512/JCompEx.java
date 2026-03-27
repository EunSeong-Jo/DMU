package Day0512;

import java.awt.Color;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;

import javax.swing.JButton;
import javax.swing.JFrame;
import javax.swing.JPanel;

public class JCompEx extends JFrame{

	public JCompEx() {
		// TODO Auto-generated constructor stub
		this.setTitle("JComponent 공통 메소드 예제");
		this.setDefaultCloseOperation(EXIT_ON_CLOSE);
		
		JPanel pan1 = new JPanel();
		
		JButton btn1 = new JButton("글자색 / 바탕색 설정");
		JButton btn2 = new JButton("비활성 버튼");
		JButton btn3 = new JButton("X , Y 좌표 버튼");
		
		btn3.addActionListener(new ActionListener() {
			
			@Override
			public void actionPerformed(ActionEvent e) {
				// TODO Auto-generated method stub
				// String loc = pan1.getLocation().toString();
				
				System.out.println(btn3.getX() + ", " + btn3.getY());
				
			}

		});
		
		
		pan1.add(btn1);
		pan1.add(btn2);
		pan1.add(btn3);
		
		btn1.setBackground(Color.yellow);
		btn1.setForeground(Color.magenta);
		btn2.setEnabled(false);
		
		this.add(pan1);
		
		this.setSize(300, 300);
		this.setVisible(true);
	}
	
	
	public static void main(String[] args) {
		// TODO Auto-generated method stub
		new JCompEx();
		
	}

}
