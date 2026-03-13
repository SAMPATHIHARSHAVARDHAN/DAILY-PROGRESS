import java.util.*;
public class Collection1
{
  public static void main(String[] args)
  {
	  
  List<String> list = new ArrayList<String>();
  list.add("Red");
  list.add("Green");
  list.add("Orange");
  list.add("White");
  list.add("Black");
  //Print Entire List
  System.out.println(list);
  //Print Entire List using for Loop
  for (String element : list)
  {
    System.out.println(element);
  }
  //Insert Elements Existing list in specified Position
  list.add(0, "Pink");
  list.add(6, "Yellow");
  System.out.println(list);
  //get the specified position elements
  System.out.println(list.get(0));
  System.out.println(list.get(6));
  //Updating the existing Element with specified position
  list.set(0, "YellowPink");
  System.out.println(list);
  //Remove element in specified position
  list.remove(0);
  System.out.println(list);

  //Search the Specified Element
  if (list.contains("Red")) 
  {
    System.out.println("Found the element");
  } 
  else 
  {
    System.out.println("There is no such element");
  }
	   Collections.sort(list);
	    System.out.println(list);
      Collections.reverse(list);
  	   System.out.println(list);

 }
}
