package Day0519;

public class TimerRunnable extends Thread{

	int n = 0;
	
	@Override
	public void run() {
		// TODO Auto-generated method stub
		super.run();
		
		while (true) {
			System.out.println(n);
			n++;
			
			try {
				sleep(1000);
			} catch (InterruptedException e) {
				// TODO Auto-generated catch block
				e.printStackTrace();
				return;
			}
		}
	}
	
	public static void main(String[] args) {
		// TODO Auto-generated method stub
		Thread th = new Thread(new TimerRunnable());
		th.start();
	}

}
