package ch.sec03;

public class bitshiftexample2 {

	public static void main(String[] args) {
		// TODO Auto-generated method stub
		int value = 772;
		byte byte1 = (byte)(value >>> 24);
		int int1 = byte1 & 255;
		
		System.out.println(int1);
		
		byte byte2 = (byte)(value >>> 16);
		int int2 = Byte.toUnsignedInt(byte2);
		
		System.out.println(int2);
		
		byte byte3 = (byte)(value >>> 8);
		int int3 = byte3 & 255;
		
		System.out.println(int3);
		
		byte byte4 = (byte)value;
		int int4 = Byte.toUnsignedInt(byte4);
		
		System.out.println(int4);
	}

}
