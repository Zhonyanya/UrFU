package lab2;

import java.util.Scanner;

public class Task2 {
    public static void main(String[] args) {
        int factorial = 1;
        Scanner scan = new Scanner(System.in);
        int n = scan.nextInt();
        for (int i = 1; i <= n; i++) {
            factorial *= i;
        }
        System.out.println(factorial);
    }
}
