d=create_project_example_Simple(3);
d.x=uint16(257);
d.a_ui16(1)=1;
d.a_ui16(2)=2;
d.a_ui16(3)=3;

f=fopen ("d.bin","w"); write_project_example_Simple(f,d); fclose(f)
f=fopen ("d.bin","r"); d2=read_project_example_Simple(f); fclose(f)

assert(d.n == d2.n)
assert(d.x == d2.x)
assert(d.a_ui16 == d2.a_ui16)

disp("demo.m: all tests passed")
