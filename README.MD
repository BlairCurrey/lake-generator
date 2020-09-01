This repository is for a procedural heightmap generator. I currently have the 'mapGen' program configured to generates lakes.

![A generated lake](/map44366.png)

It makes a heightmap using different layers of [perlin noise](https://github.com/caseman/noise) (and optionally, manually made PNG files) and then converts each pixel to a color according to the range it falls in.
