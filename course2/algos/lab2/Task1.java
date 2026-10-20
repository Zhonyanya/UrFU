package lab2;

import java.util.Scanner;

public class Task1 {
    public static void main(String[] args)
    {
        Scanner scan = new Scanner(System.in);
        int n = scan.nextInt();
        double summation = 0;
        for (int i = 1; i <= n; i++) {
            double term = 1 / Math.sqrt(i);
            summation += term;
        }
        System.out.println(summation);
    }
}
