
public class Prime {

	public Prime() {
	}
	
	// public boolean isPrime(int n) {
	// 	boolean prime = true;
	// 	int i = n-1;
	// 	while (prime) {
	// 		prime = (n % i) != 0;
	// 		i--;
	// 	}
		
	// 	return prime;
	// }
	
	public boolean isPrime(int n) {
		return n % 2 != 0;
	}
	
	public static void main(String[] args) {
		Prime p = new Prime();
		// p.isPrime(5);
		System.out.print(p.isPrime(0));
	}
}