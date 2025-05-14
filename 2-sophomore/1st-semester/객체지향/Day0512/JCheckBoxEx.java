package Day0512;

import java.awt.FlowLayout;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;

import javax.swing.JCheckBox;
import javax.swing.JFrame;
import javax.swing.JLabel;

public class JCheckBoxEx extends JFrame{

	private String[] name = {"apple", "pear", "cherry"};
	private int[] prices = {100, 500, 20000};
	
	int sum = 0;
	
	public JCheckBoxEx() {
		// TODO Auto-generated constructor stub
		setTitle("checkbox & actionevent");
		setDefaultCloseOperation(EXIT_ON_CLOSE);
	
		this.setLayout(new FlowLayout());
		this.add(new JLabel("| apple : 100$ | pear : 500$ | cherry : 20000$ |"));

		JLabel sumLabel = new JLabel("now 0$");
		JCheckBox cbApple = new JCheckBox("apple");
		JCheckBox cbPear = new JCheckBox("pear");
		JCheckBox cbCherry = new JCheckBox("cherry");
		
		cbApple.addActionListener(new ActionListener() {
			
			@Override
			public void actionPerformed(ActionEvent e) {
				// TODO Auto-generated method stub
				if(cbApple.isSelected()) {
					sum += prices[0];
				} else {
					sum -= prices[0];
				}
				
				sumLabel.setText("now " + sum + "$");
			}
		});
		
		
		add(cbApple);
		add(cbPear);
		add(cbCherry);
		
		add(sumLabel);
		
		setSize(500, 500);
		setVisible(true);
	}
	
	
	public static void main(String[] args) {
		// TODO Auto-generated method stub
		new JCheckBoxEx();
	}

}
