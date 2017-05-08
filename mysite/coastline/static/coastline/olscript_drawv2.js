
var raster = new ol.layer.Tile({
        source: new ol.source.OSM()
      });

      var map = new ol.Map({
          layers: [
    new ol.layer.Tile({
      source: new ol.source.BingMaps({
        imagerySet: 'Aerial',
        key: 'AqsdQig9tg_VpEvg4FeANtFrqqhmB4XMlbHGO_Ji_-6gf0ihTqU0-np2dU-95G3f'
      })
    })
  ],
        target: 'map',
        view: new ol.View({
          center: [-267476.8584784027, 7011741.11645388],
          zoom: 6
        })
      });







      var features = new ol.Collection();
      var featureOverlay = new ol.layer.Vector({
        source: new ol.source.Vector({features: features}),
        style: new ol.style.Style({
          fill: new ol.style.Fill({
            color: 'rgba(255, 255, 255, 0.2)'
          }),

          stroke: new ol.style.Stroke({
            color: '#ffcc33',
            width: 2
          }),
          image: new ol.style.Circle({
            radius: 7,
            fill: new ol.style.Fill({
              color: '#ffcc33'
            })
          })
        })
      });
      featureOverlay.setMap(map);




      var modify = new ol.interaction.Modify({
        features: features,
        // the SHIFT key must be pressed to delete vertices, so
        // that new vertices can be drawn at the same position
        // of existing vertices
        deleteCondition: function(event) {
          return ol.events.condition.shiftKeyOnly(event) &&
              ol.events.condition.singleClick(event);
        }
      });
      map.addInteraction(modify);

      var draw; // global so we can remove it later
      /**var typeSelect = document.getElementById('type');**/
      
      var typeSelect;
      
      console.log(typeSelect);       

      /**console.log(typeSelect.value);**/

      function addInteraction() {
        draw = new ol.interaction.Draw({
          features: features,
          
          type: /** @type {ol.geom.GeometryType} */ ('Polygon')
        });
        map.addInteraction(draw);
      }




      addInteraction();

var myPoly = [0,0,0,0]

var testData = 4;


draw.on('drawend',function(e){
myPoly = (e.feature.getGeometry().getExtent());
console.log(myPoly)
var sPoly = String(Math.round(myPoly[0])) + "," + String(Math.round(myPoly[1]));

console.log(sPoly);
document.getElementById("xmin").value = myPoly[0];
});













