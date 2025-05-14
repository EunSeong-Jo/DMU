package Day0512;

import java.awt.FlowLayout;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;

import javax.swing.JFrame;
import javax.swing.JLabel;
import javax.swing.JTextArea;
import javax.swing.JTextField;

public class JTextAreaEx extends JFrame{
	
	public JTextAreaEx() {
		// TODO Auto-generated constructor stub
		setTitle("JTextArea exam");
		setDefaultCloseOperation(EXIT_ON_CLOSE);
		
		setLayout(new FlowLayout());
		
		add(new JLabel("fill out and press <Enter>"));

		JTextField tf = new JTextField(20);
		JTextArea ta = new JTextArea(7, 20);
		
		add(tf);
		add(ta);
		
		tf.addActionListener(new ActionListener() {
			
			@Override
			public void actionPerformed(ActionEvent e) {
				// TODO Auto-generated method stub
				ta.append(tf.getText() + "\n");
				tf.setText("");
			}
		});
		
		setSize(300, 150);
		setVisible(true);
	}
	
	public static void main(String[] args) {
		// TODO Auto-generated method stub
		new JTextAreaEx();
	}

}
