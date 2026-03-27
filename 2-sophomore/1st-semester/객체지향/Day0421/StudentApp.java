package Day0421;

import java.awt.GridLayout;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.FileNotFoundException;
import java.io.FileReader;
import java.io.FileWriter;
import java.io.IOException;
import java.util.ArrayList;

import javax.swing.JButton;
import javax.swing.JFrame;
import javax.swing.JLabel;
import javax.swing.JTextField;

// extends JFrame (시험)
public class StudentApp extends JFrame{
	
	ArrayList<Student> studentList = new ArrayList<Student>();
	// 생성자 이름 = 클래스 이름 (시험)
	public StudentApp() {
		// TODO Auto-generated constructor stub
		// setTitle과 같은 기본 설정 (시험)
		setTitle("GridLayout Sample");
		setDefaultCloseOperation(EXIT_ON_CLOSE);
		setSize(600, 400);
		
		GridLayout grid = new GridLayout(6, 2);
		grid.setVgap(10);
		
		// 기본 레이아웃(border layout)이 아닌 그리드 레이아웃 설정 (시험)
		setLayout(grid);
		
		// JLable, JButton과 같은 문법 + 대소문자
		add(new JLabel("이름"));
		JTextField inName = new JTextField();
		add(inName);
		
		add(new JLabel("학번"));
		JTextField inStrId = new JTextField();
		add(inStrId);
		
		add(new JLabel("학과"));
		JTextField inDept = new JTextField();
		add(inDept);
		
		add(new JLabel("과목"));
		JTextField inSubj = new JTextField();
		add(inSubj);
		
		JButton btnIn = new JButton("입력");
		add(btnIn);
		// addActionListener, ActionListener, ActionEvent(시험)
		btnIn.addActionListener(new ActionListener() {
			
			@Override
			public void actionPerformed(ActionEvent e) {
				// TODO Auto-generated method stub
				String strName = inName.getText().toString();
				String strStuId = inStrId.getText().toString();
				String strDept = inDept.getText().toString();
				String strSubj = inSubj.getText().toString();
				
				studentList.add(new Student(strName, strStuId, strDept, strSubj));
				System.out.println(strName + " 입력 완료");
			}
		});
		
		
		JButton btnCancel = new JButton("취소");
		add(btnCancel);
		btnCancel.addActionListener(new ActionListener() {
			
			@Override
			public void actionPerformed(ActionEvent e) {
				// TODO Auto-generated method stub
				inName.setText("");
				inStrId.setText("");
				inDept.setText("");
				inSubj.setText("");
			}
		});
		
		JButton btnSave = new JButton("조회 및 파일저장");
		add(btnSave);
		btnSave.addActionListener(new ActionListener() {
			
			@Override
			public void actionPerformed(ActionEvent e) {
				// TODO Auto-generated method stub
				try {
					FileWriter fileOut = new FileWriter("C:\\Users\\asus\\eclipse-workspace\\OOP\\src\\Day0421\\학번.txt");
					// FileWriter fileOut = new FileWriter("C:\\Users\\asus\\eclipse-workspace\\OOP\\src\\Day0421\\학번.csv");
					
					for (Student stu : studentList) {
						fileOut.write(stu.toString() + "\n");
						// fileOut.write(stu.getName()  + "," + stu.getStuId() + "," + stu.getDept() + "," + stu.getSubj() + "\n");
						System.out.println(stu);
					}
					
					fileOut.close();
					System.out.println("저장 완료");
				} catch (IOException e1) {
					// TODO Auto-generated catch block
					e1.printStackTrace();
				}
			
			}
		});
		
		JButton btnSearch = new JButton("이름으로 검색");
		add(btnSearch);
		btnSearch.addActionListener(new ActionListener() {
			
			@Override
			public void actionPerformed(ActionEvent e) {
				// TODO Auto-generated method stub
				String searchName = inName.getText().toString();
				
				for (Student stu : studentList) {
					if (stu.getName().equals(searchName)) {
						inName.setText(stu.getName());
						inStrId.setText(stu.getStuId());
						inDept.setText(stu.getDept());
						inSubj.setText(stu.getSubj());
						System.out.println("입력된 이름을 찾았습니다.");
					}
					else {
						System.out.println("입력된 이름을 찾지 못했습니다.");
					}
				}
			}
		});
		
		setVisible(true);
	}
	
	public static void main(String[] args) {
		// TODO Auto-generated method stub
		new StudentApp();
	}

}
