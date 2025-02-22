package trabajos_clase;
import javax.swing.*;
import java.awt.*;

    

//creado la prinera interfaz (Windows of java )
public class clase_1 {
    public static void main(String[] args) {
      //como se hace una instancia 
        Ventana ventana = new Ventana();
        ventana.setVisible(true);
        ventana.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        lamina lamina = new lamina();
        ventana.add(lamina);
        
    }

}
class Ventana extends JFrame{
    public Ventana(){//costructor del objeto
        setSize(500,500);//tamaño de la ventana
        setLocation(520,190);//ubicacion de la ventana
        setBounds(520,190,500,500);//ubicacion y tamaño de la ventana

        setTitle("es gaayy");//titulo de la ventana
        
    }

}
    
class lamina extends JPanel{
    public void paintComponent(Graphics g){
        super.paintComponent(g);
        g.drawString("Una pagina para andres", 100, 100);//texto en la ventana
    }
}//redimecionar la ventana
//