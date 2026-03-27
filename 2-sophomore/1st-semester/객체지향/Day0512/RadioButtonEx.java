package Day0512;

import java.awt.BorderLayout;
import java.awt.Color;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.util.Iterator;

import javax.swing.ButtonGroup;
import javax.swing.ImageIcon;
import javax.swing.JFrame;
import javax.swing.JLabel;
import javax.swing.JPanel;
import javax.swing.JRadioButton;

public class RadioButtonEx extends JFrame{

	JRadioButton[] radio = new JRadioButton[3];
	
	String[] text = {"apple", "pear", "cherry"};

	ImageIcon[] img = {
			new ImageIcon("C:\\Users\\asus\\eclipse-workspace\\OOP\\src\\Day0512\\apple.png"),
			new ImageIcon("C:\\Users\\asus\\eclipse-workspace\\OOP\\src\\Day0512\\pear.jpg"),
			new ImageIcon("C:\\Users\\asus\\eclipse-workspace\\OOP\\src\\Day0512\\cherry.jpg")
	};
	
	private JLabel imgLabel = new JLabel();
	
	public RadioButtonEx() {
		// TODO Auto-generated constructor stub
		setTitle("radio button");
		setDefaultCloseOperation(EXIT_ON_CLOSE);
		
		JPanel rdPan1 = new JPanel();
		rdPan1.setBackground(Color.gray);
		
		ButtonGroup btnGroup = new ButtonGroup();
		
		for (int i = 0; i < radio.length; i++) {
			radio[i] =  new JRadioButton(text[i]);
			
			btnGroup.add(radio[i]);
			rdPan1.add(radio[i]);
			
			radio[i].addActionListener(new ActionListener() {
				
				@Override
				public void actionPerformed(ActionEvent e) {
					// TODO Auto-generated method stub
					if (radio[0].isSelected()) {
						imgLabel.setIcon(img[0]);
					} else if (radio[1].isSelected()) {
						imgLabel.setIcon(img[1]);
					} else if (radio[2].isSelected()) {
						imgLabel.setIcon(img[2]);
					}
				}
			});
		}
		
		radio[2].setSelected(true);
		imgLabel.setIcon(img[2]);
		
		add(rdPan1, BorderLayout.NORTH);
		add(imgLabel, BorderLayout.CENTER);
		
		setSize(500, 500);
		setVisible(true);
	}
	
	public static void main(String[] args) {
		// TODO Auto-generated method stub
		new RadioButtonEx();
	}

}
