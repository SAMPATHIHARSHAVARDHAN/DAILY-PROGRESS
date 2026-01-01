class A
{
int l,b; 
A()
{
l=10;
 b=20;
}
A(int u,int v)
{
l=u; 
b=v;
}
int area()
{
return l*b;
}
}
class overconstructdemo
{
public static void main(String args[])
{
A a1=new A(); 
int r1=a1.area();
System.out.println("The area is: "+r1);
A a2=new A(30,40);
int r2=a2.area();
System.out.println("The area is: "+r2);
}
}
