package Day0512;

import java.awt.FlowLayout;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;

import javax.swing.JComboBox;
import javax.swing.JFrame;

public class JComboBoxEx extends JFrame{

	private String[] fruits = {"apple", "banana", "kiwi", "mango", "pear"};
	
	public JComboBoxEx() {
		// TODO Auto-generated constructor stub
		setTitle("ComboBox exam");
		setDefaultCloseOperation(EXIT_ON_CLOSE);
		
		setLayout(new FlowLayout());
		
		JComboBox<String> strCombo = new JComboBox<String>(fruits);
		
		strCombo.addActionListener(new ActionListener() {
			
			@Override
			public void actionPerformed(ActionEvent e) {
				// TODO Auto-generated method stub
				// int idx = strCombo.getSelectedIndex();
				// System.out.println(fruits[idx] + ", " + idx);
				System.out.println(strCombo.getSelectedItem() + ", " + strCombo.getSelectedIndex());
			}
		});
		
		add(strCombo);
		
		setSize(300, 300);
		setVisible(true);
	}
	
	
	public static void main(String[] args) {
		// TODO Auto-generated method stub
		new JComboBoxEx();
	}

}
