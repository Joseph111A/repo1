package trabajos_clase;

public class datos_numericos {

    public static void main(String[] args){

        byte entero1 = 127; // 8 bits y va de 128 a -127

        short entero2 = 32767;// 16 bist y va de 32768 a -32767
        int entero3 = 2147483647; // 32 bits y va de 2147483648 a -2147483647
        long entero4 = 9223372036854775807L; // 64 bits y va de 9223372036854775808 a -9223372036854775807

        float decimal1 = 3.4028235E38f; // 32 bits
        double decimal2 = 1.7976931348623157E308; // 64 bits
        
        char caracter = 'a'; // 16 bits

        boolean verdadero = true; // 1 bit
        boolean falso = false; // 1 bit


        System.out.println("El valor de entero1 es: " + entero1);
        System.out.println("El valor de entero2 es: " + entero2);
        System.out.println("El valor de entero3 es: " + entero3);
        System.out.println("El valor de entero4 es: " + entero4);
        System.out.println("El valor de decimal1 es: " + decimal1);
        System.out.println("El valor de decimal2 es: " + decimal2);
        System.out.println("El valor de caracter es: " + caracter);
        System.out.println("El valor de verdadero es: " + verdadero);
        System.out.println("El valor de falso es: " + falso);
    }
}
