interface D
{
void display();
}

interface E extends D
{
void show();
}

class A
{
void callme()
{
System.out.println("This is in callme method");
}
}

class B extends A implements E
{
public void display()
{
System.out.println("This is in display method");
}
public void show()
{
System.out.println("This is in show method");
}
}

class C extends B
{
void call()
{
System.out.println("This is in call method");
}
}

class interfacedemo
{
public static void main(String args[])
{
C c1=new C(); 
c1.display();
c1.show();
c1.callme();
c1.call();
}
}
