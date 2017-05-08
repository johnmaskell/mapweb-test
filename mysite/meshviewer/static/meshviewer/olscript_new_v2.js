      function transform(extent) {
        return ol.proj.transformExtent(extent, 'EPSG:4326', 'EPSG:3857');
      }


      var defaultStyle = {
        'Point': new ol.style.Style({
          image: new ol.style.Circle({
            fill: new ol.style.Fill({
              color: 'rgba(255,255,0,0.5)'
            }),
            radius: 5,
            stroke: new ol.style.Stroke({
              color: '#ff0',
              width: 1
            })
          })
        }),
        'LineString': new ol.style.Style({
          stroke: new ol.style.Stroke({
            color: '#f00',
            width: 3
          })
        }),
        'Polygon': new ol.style.Style({
          fill: new ol.style.Fill({
            color: 'rgba(0,255,255,0.5)'
          }),
          stroke: new ol.style.Stroke({
            color: '#0ff',
            width: 1
          })
        }),
        'MultiPoint': new ol.style.Style({
          image: new ol.style.Circle({
            fill: new ol.style.Fill({
              color: 'rgba(255,0,255,0.5)'
            }),
            radius: 5,
            stroke: new ol.style.Stroke({
              color: '#f0f',
              width: 1
            })
          })
        }),
        'MultiLineString': new ol.style.Style({
          stroke: new ol.style.Stroke({
            color: '#0f0',
            width: 3
          })
        }),
        'MultiPolygon': new ol.style.Style({
          fill: new ol.style.Fill({
            color: 'rgba(0,0,255,0.5)'
          }),
          stroke: new ol.style.Stroke({
            color: '#00f',
            width: 1
          })
        })
      };

      var styleFunction = function(feature, resolution) {
        var featureStyleFunction = feature.getStyleFunction();
        if (featureStyleFunction) {
          return featureStyleFunction.call(feature, resolution);
        } else {
          return defaultStyle[feature.getGeometry().getType()];
        }
      };

     
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
          center: [0,0],
          zoom: 2
        })
      });

     
     
     var vectorSource =  new ol.source.Vector({
                 
         url: 'https://api.myjson.com/bins/u5fsn',         
         format: new ol.format.GeoJSON()     
     }) 
        
     
     

        map.addLayer(new ol.layer.Vector({
        source: vectorSource
         
        }));
setTimeout(function() {
var extent = vectorSource.getExtent();
var newExtent = transform(extent)
console.log(extent[0]);

/*map.getView().fitExtent(newExtent,map.getSize());*/
        map.getView().setCenter([extent[0], extent[1]])
        map.getView().setZoom(14)



},2000);
