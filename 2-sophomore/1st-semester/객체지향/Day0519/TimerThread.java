package Day0519;

public class TimerThread extends Thread{

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
			}
			
			if(n == 10) {
				return;
			}
			
		}
	}
	
	public static void main(String[] args) {
		// TODO Auto-generated method stub
		TimerThread th = new TimerThread();
		
		th.start();	
	}
}
