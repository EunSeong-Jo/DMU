package Day0512;

import java.awt.Container;
import java.awt.FlowLayout;

import javax.swing.Icon;
import javax.swing.ImageIcon;
import javax.swing.JFrame;
import javax.swing.JLabel;
import javax.swing.SwingConstants;

public class LabelEx extends JFrame{

	public LabelEx() {
		// TODO Auto-generated constructor stub
		
		setTitle("레이블 예제");
		setDefaultCloseOperation(EXIT_ON_CLOSE);
		
		setLayout(new FlowLayout());
		
		Container c = getContentPane();
		
		JLabel textLabel = new JLabel("동양미래대 아이콘");
		
		ImageIcon img = new ImageIcon("C:\\Users\\asus\\eclipse-workspace\\OOP\\src\\Day0512\\동양미래대.png");
		JLabel imgLabel = new JLabel(img);
		
		ImageIcon img2 = new ImageIcon("C:\\Users\\asus\\eclipse-workspace\\OOP\\src\\Day0512\\폰.png");
		JLabel btnLabel = new JLabel("버튼 내부 아이콘", img2, SwingConstants.CENTER);
		
		c.add(textLabel);
		c.add(imgLabel);
		c.add(btnLabel);
		
		setSize(350, 600);
		setVisible(true);
	}
	
	
	public static void main(String[] args) {
		// TODO Auto-generated method stub
		new LabelEx();
	}
}
