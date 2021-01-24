y=45;
for (i=[1:8]){
    z = y*i;    
    rotate([0,0,z]) translate([57,0,-5])
    difference() {
        cube(center=true,[5,10,10]);
        rotate([0,90,0]) translate([0,0,-5]) cylinder(r=2,h=10,$fn=100) ;
    }
}

