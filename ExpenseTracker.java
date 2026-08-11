import javax.swing.*;
import java.awt.Font;
public class ExpenseTracker
{
    public static void main(String[] args)
    {
        //Base part of GUI
        JFrame frame=new JFrame("Expense Tracker");
        frame.setSize(600,400);
        frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        frame.setLayout(null);
        //Heading
        JLabel head_label=new JLabel("EXPENSE TRACKER");
        head_label.setFont(new Font("Arial",Font.BOLD,20));
        head_label.setBounds(100,30,250,20);
        //Amount
        JLabel label1=new JLabel("Amount:");
        label1.setBounds(30,90,150,20);
        JTextField textField1=new JTextField();
        textField1.setBounds(100,90,150,20);
        //category
        JLabel label2=new JLabel("Category:");
        label2.setBounds(30,120,150,20);
        String [] options={"Food","Travel","Shopping","Education","Entertainment","Others"};
        JComboBox box=new JComboBox<>(options);
        box.setBounds(100,120,150,20);
        //Description
        JLabel label3=new JLabel("Description:");
        label3.setBounds(30,150,150,20);
        JTextField textField3=new JTextField();
        textField3.setBounds(100,150,150,20);
        //Date
        JLabel label4=new JLabel("Date:");
        label4.setBounds(30,180,150,20);
        JTextField textField4=new JTextField();
        textField4.setBounds(100,180,150,20);
        //Button
        JButton button=new JButton("ADD EXPENSE");
        button.setBounds(100,250,150,20);

        JLabel label_1=new JLabel();
        label_1.setBounds(360,90,150,20);

        JLabel label_2=new JLabel();
        label_2.setBounds(360,120,150,20);

        JLabel label_3=new JLabel();
        label_3.setBounds(360,150,150,20);

        JLabel label_4=new JLabel();
        label_4.setBounds(360,180,150,20);
        //working
        button.addActionListener(e->{
           double amt=Double.parseDouble(textField1.getText());
           label_1.setText("Amount: "+amt);
           String cat=(String)box.getSelectedItem();
           label_2.setText("Category: "+cat);
           String des=textField3.getText();
           label_3.setText("Description: "+des);
           String dat=textField4.getText();
           label_4.setText("Date: "+dat);
        });
        //Object calling
        frame.add(head_label);
        frame.add(label1);
        frame.add(textField1);
        frame.add(label2);
        frame.add(box);
        frame.add(label3);
        frame.add(textField3);
        frame.add(label4);
        frame.add(textField4);
        frame.add(button);
        frame.add(label_1);
        frame.add(label_2);
        frame.add(label_3);
        frame.add(label_4);
        //Visibility
        frame.setVisible(true);
    }
}