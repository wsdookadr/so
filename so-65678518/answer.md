I liked this image of a groove I found here. The groove is L x G in dimensions. 

[![enter image description here][1]][1]

First of all I've written down a cross-section and I've labeled the important dimensions:

[![enter image description here][2]][2]

On the left, the groove sits in the interior side of the cylinder cross-section. On the right, the groove sits on the exterior of the cylinder cross-section.


Now we're able to use [`rotate_extrude`](https://en.wikibooks.org/wiki/OpenSCAD_User_Manual/2D_to_3D_Extrusion#Rotate_Extrude) in order to generate the solid with the require groove on it.

I'll add the code for the `interior_groove` here:

```
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
```

This is the result of the code when we draw two types of grooves, one on the interior (left) and one on the exterior (right):

[![enter image description here][3]][3]


All the code used for this [can be found here](https://github.com/wsdookadr/so/tree/master/so-65678518).



  [1]: https://i.stack.imgur.com/aNngt.png
  [2]: https://i.stack.imgur.com/e97vB.jpg
  [3]: https://i.stack.imgur.com/w2Fog.png
