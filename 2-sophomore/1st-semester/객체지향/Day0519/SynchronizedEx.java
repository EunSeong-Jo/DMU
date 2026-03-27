package Day0519;

import java.util.Iterator;

public class SynchronizedEx {

	public static class SharedBoard {
		private int sum = 0;
		
		synchronized public void add() {
			int n = sum;
			Thread.yield();
			n += 10;
			sum = n;
			
			System.out.println(Thread.currentThread().getName() + ":" + sum);
		}
		public int getSum() {
			return sum;
		}
	}
	
	public static class StudentThread extends Thread {
		private SharedBoard board;
		
		public StudentThread(String name, SharedBoard board) {
			super(name);
			this.board = board;
		}
		
		@Override
		public void run() {
			// TODO Auto-generated method stub
			super.run();
			for(int i = 0; i < 10; i++) {
				board.add();
			}
		}
	}
	
	
	public static void main(String[] args) {
		// TODO Auto-generated method stub
		SharedBoard board = new SharedBoard();
		Thread th1 = new StudentThread("관식", board);
		Thread th2 = new StudentThread("애순", board);
		
		th1.start();
		th2.start();
	}
}
