package Day0519;

import java.awt.Color;
import java.awt.Container;
import java.awt.FlowLayout;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;

import javax.swing.JButton;
import javax.swing.JFrame;
import javax.swing.JLabel;
import javax.swing.JSlider;
import javax.swing.event.ChangeEvent;
import javax.swing.event.ChangeListener;

public class SliderChangeEx extends JFrame{

	private JLabel colorLabel;
	private JSlider[] sl = new JSlider[3];
	
	public SliderChangeEx() {
		setTitle("슬라이더 ChangeEvent");
		setDefaultCloseOperation(EXIT_ON_CLOSE);
		
		Container c = getContentPane();
		c.setLayout(new FlowLayout());
		colorLabel = new JLabel("슬라이더 예제");
		
		for(int i = 0; i <sl.length; i++) {
			sl[i] = new JSlider(JSlider.HORIZONTAL, 0, 255, 128);
			sl[i].setPaintLabels(true);
			sl[i].setPaintTicks(true);
			sl[i].setPaintTrack(true);
			sl[i].setMajorTickSpacing(50);
			sl[i].setMinorTickSpacing(10);
//			sl[i].addChangeListener(new MyChangeListener());
			c.add(sl[i]);
		}
		
		sl[0].setForeground(Color.red);
		sl[1].setForeground(Color.green);
		sl[2].setForeground(Color.blue);
		
		int r = sl[0].getValue();
		int g = sl[1].getValue();
		int b = sl[2].getValue();
		
		colorLabel.setOpaque(true);
		colorLabel.setBackground(new Color(r, g, b));
		
		JButton btn = new JButton("확인");
		
		btn.addActionListener(new ActionListener() {
			@Override
			public void actionPerformed(ActionEvent e) {
				// TODO Auto-generated method stub
				int r = sl[0].getValue();
				int g = sl[1].getValue();
				int b = sl[2].getValue();
				
				colorLabel.setBackground(new Color(r, g, b)) ;
			}
		});
		
		c.add(colorLabel);
		c.add(btn);
		
		setSize(300, 250);
		setVisible(true);
	}

//	public class MyChangeListener implements ChangeListener{
//		public void stateChanged(ChangeEvent e) {
//			int r = sl[0].getValue();
//			int g = sl[1].getValue();
//			int b = sl[2].getValue();
//			colorLabel.setBackground(new Color(r, g, b));
//		}
//	}
	
	public static void main(String[] args) {
		// TODO Auto-generated method stub
		new SliderChangeEx();
	}

}
