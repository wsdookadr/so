y=45;
for (i=[1:8]){
    z = y*i;
    difference(){
        rotate([0,0,z]) translate([57,0,-5]) cube(center = true,[5,10,10]);
        rotate([90,90,z]) translate([6,0,-60]) cylinder(5,2,2);  
    }
    
}
// This is a reference, translate([6,0,-60]) is correct position
rotate([90,90,z]) translate([16,0,-60]) cylinder(5,2,2);
