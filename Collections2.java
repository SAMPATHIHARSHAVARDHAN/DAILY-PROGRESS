//Write a Java program to copy one array list into another.
import java.util.*;
  public class Collections2 {
  public static void main(String[] args) {
  List<String> list1 = new ArrayList<String>();
  list1.add("1");
  list1.add("2");
  list1.add("3");
  list1.add("4");
  System.out.println("List1: " + list1);
  List<String> list2 = new ArrayList<String>();
  list2.add("A");
  list2.add("B");
  list2.add("C");
  list2.add("D");
  System.out.println("List2: " + list2);
  // Copy List2 to List1
  Collections.copy(list1, list2);
  System.out.println("Copy List2 to List1 \nAfter copy:");
  System.out.println("List1: " + list1);
  System.out.println("List2: " + list2);
 }
}
