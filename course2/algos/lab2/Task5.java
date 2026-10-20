package lab2;

import java.util.Scanner;

public class Task5
{
    public static void main(String[] args)
    {
        Scanner scan = new Scanner(System.in);
        boolean needsExit = false;

        while (!needsExit)
        {
            printMenu();
            int choice = getValidIntChoice(scan);

            switch (choice)
            {
                case 1:
                    performCalculations(scan);
                    break;
                case 2:
                    printProgramInfo();
                    break;
                case 3:
                    printDeveloperInfo();
                    break;
                case 4:
                    System.out.println("Выход из программы...");
                    needsExit = true;
                    break;
            }
        }
    }

    private static void printMenu()
    {
        System.out.println("-----МЕНЮ-----");
        System.out.println("1. Выполнить расчёт");
        System.out.println("2. Информация о программе");
        System.out.println("3. Информация о разработчике");
        System.out.println("4. Выход");
    }

    private static int getValidIntChoice(Scanner scan)
    {
        while (true)
        {
            if (scan.hasNextInt())
            {
                int choice = scan.nextInt();
                if (choice >= 1 && choice <= 4)
                {
                    return choice;
                }
                else
                {
                    System.out.println("Ошибка! Введите число от 1 до 4");
                }
            }
            else
            {
                System.out.println("Ошибка! Введите целое число");
                scan.next();
            }
        }
    }
    // не оч хотелось для ввода начислений и месяцов
    // отдельную функцию писать поэтому вот strictlyPositive специально для этого
    private static double getValidDouble(Scanner scan, String prompt, boolean strictlyPositive)
    {
        System.out.println(prompt);
        while (true)
        {
            if (scan.hasNextDouble())
            {
                double value = scan.nextDouble();
                if (value <= 0 && strictlyPositive)
                {
                    System.out.println("Значение должно быть положительным!");
                }
                else if (!strictlyPositive && value < 0)
                {
                    System.out.println("Значение не должно быть отрицательным!");
                }
                else
                {
                    return value;
                }
            }
            else
            {
                System.out.println("Ошибка! Введите число");
                scan.next();
            }
        }
    }

    private static void printProgramInfo()
    {
        System.out.println("-----Информация о программе-----");
        System.out.println("Вычисляет сложные проценты по формуле:");
        System.out.println("A = P * (1 + r / n) ^ (n * t), где");
        System.out.println("P - начальная сумма");
        System.out.println("r - годовая процентная ставка в виде десятичной дроби");
        System.out.println("n - количество начислений процентов в год");
        System.out.println("t - общий срок вклада в годах");
    }

    private static void printDeveloperInfo()
    {
        System.out.println("-----Информация о разработчике-----");
        System.out.println("Выполнено ЕБ из 911!!");
    }

    // по задаче возвращать ничего не требовалось поэтому я просто войд с принтом бахнул
    private static void performCalculations(Scanner scan)
    {
        double P = getValidDouble(scan, "Введите начальную сумму вклада", false);
        double r = getValidDouble(scan, "Введите годовой процент (в десятичном виде)", false);
        double n = getValidDouble(scan, "Введите количество начислений в год", true);
        double t = getValidDouble(scan, "Введите срок вклада в годах", true);

        double A = P * Math.pow((1 + r / n), (n * t));

        System.out.println("Ваши накопления через " + t + " лет будут равны " + A);
    }
}


