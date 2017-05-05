/**
 * Define a namespace for the application.
 */
window.app = {};
var app = window.app;

var wxo = 132672;
var wyo = 6770392;
var lxo = -356688;
var lyo = 7271513;

/**
 * @constructor
 * @extends {ol.interaction.Pointer}
 */
app.Drag = function() {   
  ol.interaction.Pointer.call(this, {
    handleDownEvent: app.Drag.prototype.handleDownEvent,
    handleDragEvent: app.Drag.prototype.handleDragEvent,
    handleMoveEvent: app.Drag.prototype.handleMoveEvent,
    handleUpEvent: app.Drag.prototype.handleUpEvent
  });

  /**
   * @type {ol.Pixel}
   * @private
   */
  this.coordinate_ = null;

  /**
   * @type {string|undefined}
   * @private
   */
  this.cursor_ = 'pointer';

  /**
   * @type {ol.Feature}
   * @private
   */
  this.feature_ = null;

  /**
   * @type {string|undefined}
   * @private
   */
  this.previousCursor_ = undefined;

};
ol.inherits(app.Drag, ol.interaction.Pointer);


/**
 * @param {ol.MapBrowserEvent} evt Map browser event.
 * @return {boolean} `true` to start the drag sequence.
 */
app.Drag.prototype.handleDownEvent = function(evt) {
  var map = evt.map;

  var feature = map.forEachFeatureAtPixel(evt.pixel,
      function(feature, layer) {
        return feature;
      });
  
  if (feature) {
    this.coordinate_ = evt.coordinate;
    this.feature_ = feature;
  }

  if (!!feature) {
      if (feature.a != 'staticFeature') {
          return !!feature;
      }
  }
};

/**
 * @param {ol.MapBrowserEvent} evt Map browser event.
 */
app.Drag.prototype.handleDragEvent = function(evt) {
  var map = evt.map;

  var feature = map.forEachFeatureAtPixel(evt.pixel,
      function(feature, layer) {
        return feature;
      });

  var deltaX = evt.coordinate[0] - this.coordinate_[0];
  var deltaY = evt.coordinate[1] - this.coordinate_[1];

  var geometry = /** @type {ol.geom.SimpleGeometry} */
      (this.feature_.getGeometry());
  geometry.translate(deltaX, deltaY);

  this.coordinate_[0] = evt.coordinate[0];
  this.coordinate_[1] = evt.coordinate[1];

  var myPoly = (feature.getGeometry().getExtent());
  console.log(myPoly)  
  var sPoly = String(Math.round(myPoly[0])) + "," + String(Math.round(myPoly[1]));
  document.getElementById("id_myCoords").value = sPoly;
};

/**
 * @param {ol.MapBrowserEvent} evt Event.
 */
app.Drag.prototype.handleMoveEvent = function(evt) {
  if (this.cursor_) {
    var map = evt.map;
    var feature = map.forEachFeatureAtPixel(evt.pixel,
        function(feature, layer) {
          return feature;
        });
    var element = evt.map.getTargetElement();
    if (feature && feature.a != 'staticFeature') {
      if (element.style.cursor != this.cursor_) {
        this.previousCursor_ = element.style.cursor;
        element.style.cursor = this.cursor_;
      }
    } else if (this.previousCursor_ !== undefined) {
      element.style.cursor = this.previousCursor_;
      this.previousCursor_ = undefined;
    }
  }
};


/**
 * @param {ol.MapBrowserEvent} evt Map browser event.
 * @return {boolean} `false` to stop the drag sequence.
 */
app.Drag.prototype.handleUpEvent = function(evt) {
  this.coordinate_ = null;
  this.feature_ = null;
  return false;
};


var polygonFeature = new ol.Feature({
        id: 'draggableFeature',
        geometry: new ol.geom.Polygon([[[-267476, 7011741], [-267476, 7021741],
        [-257476, 7021741], [-257476, 7011741], [-267476, 7011741]]])
 });
polygonFeature.setId('draggableFeature');

var myPoly = (polygonFeature.getGeometry());

console.log((myPoly.B)[0])
console.log((myPoly.B)[1]) 
 
var sPoly = String(Math.round((myPoly.B)[0])) + "," + String(Math.round((myPoly.B)[1]));
console.log(sPoly);

window.onload = function() {
document.getElementById("id_myCoords").value = sPoly;
}

      var map = new ol.Map({
          
          interactions: ol.interaction.defaults().extend([new app.Drag()]),
          layers: [
      new ol.layer.Tile({
      
      source: new ol.source.BingMaps({
        imagerySet: 'Aerial',
        key: 'AqsdQig9tg_VpEvg4FeANtFrqqhmB4XMlbHGO_Ji_-6gf0ihTqU0-np2dU-95G3f'
      })
    }),
    new ol.layer.Vector({
      source: new ol.source.Vector({
        features: [polygonFeature]
      }),
       style: new ol.style.Style({
        stroke: new ol.style.Stroke({
          width: 3,
          color: [255, 0, 0, 1]
        }),
        fill: new ol.style.Fill({
          color: [0, 0, 255, 0.3]
        })
      })
    })
  ],
        target: 'map',
        view: new ol.View({
          center: [-267476.8584784027, 7011741.11645388],
          zoom: 8
        })
      });


var staticpolygonFeature = new ol.Feature({
        id: 'staticFeature',
        geometry: new ol.geom.Polygon([[[lxo, lyo], [lxo, lyo+10000],
        [lxo+10000, lyo+10000], [lxo+10000, lyo], [lxo, lyo]]])
 });
 // this is what set's the ID:
 staticpolygonFeature.setId('staticFeature');

var staticpolygonFeatureii = new ol.Feature({
        id: 'staticFeature',
        geometry: new ol.geom.Polygon([[[wxo, wyo], [wxo, wyo+10000],
        [wxo+10000, wyo+10000], [wxo+10000, wyo], [wxo, wyo]]])
 });
 // this is what set's the ID:
 staticpolygonFeatureii.setId('staticFeature');

var vector_layer = new ol.layer.Vector({
  source: new ol.source.Vector({
    features: [staticpolygonFeature]
  }),
       style: new ol.style.Style({
        stroke: new ol.style.Stroke({
          width: 3,
          color: [255, 255, 0, 1]
        }),
        fill: new ol.style.Fill({
          color: [0, 0, 0, 0.3]
        })
      })
})
var vector_layer_ii = new ol.layer.Vector({
  source: new ol.source.Vector({
    features: [staticpolygonFeatureii]
  }),
       style: new ol.style.Style({
        stroke: new ol.style.Stroke({
          width: 3,
          color: [255, 255, 0, 1]
        }),
        fill: new ol.style.Fill({
          color: [0, 0, 0, 0.3]
        })
      })
})
map.addLayer(vector_layer);
map.addLayer(vector_layer_ii);





