This repository is for a procedural heightmap generator. I currently have the 'mapGen' program configured to generates lakes.

<img src="https://raw.githubusercontent.com/BlairCurrey/Lunkers/master/maps/map44366.png" alt="map44366.png" width="683" height="341">

It makes a heightmap using different layers of perlin noise (and optionally, manually made PNG files) and then converts each pixel to a color according to the range it falls in. 

The 'Lunkers' file blits the map.png to screen with the boat as well as a "minimap." This is just a quick mock-up UI for an idea I have for a fishing game/simulator.

<img src="https://raw.githubusercontent.com/BlairCurrey/Lunkers/master/lunkersUI.png" alt="lunkersUI.png text" width="640" height="360">

