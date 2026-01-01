abstractclassshape
{
abstractdoublearea();
}
classrectangleextendsshape
{
doublel=12.5,b=2.5;doublearea()
{
returnl*b;
}
}
classtriangleextendsshape
{
doubleb=4.2,h=6.5;doublearea()
{
return0.5*b*h;
}
}
classsquareextends shape
{
double s=6.5;doublearea()
{
return4*s;
}
}
class Hapedemo
{
publicstaticvoidmain(String[]args)
{
rectangler1=newrectangle();
triangle t1=new triangle();
squares1=newsquare();
System.out.println("Theareaofrectangleis:"+r1.area());
System.out.println("The area of triangle is: "+t1.area());
System.out.println("Theareaofsquareis:"+s1.area());
}
}
