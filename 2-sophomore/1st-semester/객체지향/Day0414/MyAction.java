package Day0414;

import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;

import javax.swing.JButton;

public class MyAction implements ActionListener{

	@Override
	public void actionPerformed(ActionEvent e) {
		// TODO Auto-generated method stub
		JButton b = (JButton) e.getSource();
		
		// b.getText() == "Action"
		if (b.getText().equals("Action")){
			b.setText("액션");
		}
		// 다시 "Action" 단어로 변경
		else {
			b.setText("Action");
		}
		
	}
	
}
