package lab2;

import java.util.Scanner;

public class Task3 {
    public static void main(String[] args) {
        Scanner scan = new Scanner(System.in);
        int numba = scan.nextInt();
        String reversed_numba = "";
        while (numba > 0)
        {
            reversed_numba += String.valueOf(numba % 10);
            numba /= 10;
        }
        System.out.println(reversed_numba);
    }
}
