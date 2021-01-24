module interior_groove(alpha=360) {
    L0=2;
    L=2;
    L1=0.7;
    G=2;
    G1=6;
    G2=2;

    rotate_extrude(angle=alpha, $fn=80)
    // mirror([-1,0,0]) translate([-(L0+L+L1+L0),0,0])
    polygon(points=[
    [L0,0],
    [L0,G1],
    [L0+L,G1],
    [L0+L,G+G1],
    [L0,G+G1],
    [L0,G+G1+G2],
    [L0+L+L1,G+G1+G2],
    [L0+L+L1,0]
    ]);
}

module exterior_groove(alpha=360) {
    L0=2;
    L=2;
    L1=0.7;
    G=2;
    G1=6;
    G2=2;

    rotate_extrude(angle=alpha, $fn=80)
    polygon(points=[
    [L0,0],
    [L0,G1+G+G2],
    [L0+L1+L,G1+G+G2],
    [L0+L1+L,G+G1],
    [L0+L1,G+G1],
    [L0+L1,G1],
    [L0+L1+L,G1],
    [L0+L1+L,0]
    ]);
}


interior_groove(alpha=230);
translate([10,0,0]) exterior_groove(alpha=230);





