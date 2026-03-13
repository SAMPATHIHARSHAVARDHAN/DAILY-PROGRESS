//Write a Java program to shuffle elements in a array list.
import java.util.*;
  public class Collections3 {
  public static void main(String[] args)
  {
  List<String> list = new ArrayList<String>();
  list.add("Red");
  list.add("Green");
  list.add("Orange");
  list.add("White");
  list.add("Black");
  System.out.println("List before shuffling:\n" + list);
  Collections.shuffle(list);
  System.out.println("List after shuffling:\n" + list);
 }
}
