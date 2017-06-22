var defaultStyle = {
  'Point': [new ol.style.Style({
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
  })],
  'LineString': [new ol.style.Style({
    stroke: new ol.style.Stroke({
      color: '#f00',
      width: 3
    })
  })],
  'Polygon': [new ol.style.Style({
    fill: new ol.style.Fill({
      color: 'rgba(0,255,255,0.5)'
    }),
    stroke: new ol.style.Stroke({
      color: '#0ff',
      width: 1
    })
  })],
  'MultiPoint': [new ol.style.Style({
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
  })],
  'MultiLineString': [new ol.style.Style({
    stroke: new ol.style.Stroke({
      color: '#0f0',
      width: 3
    })
  })],
  'MultiPolygon': [new ol.style.Style({
    fill: new ol.style.Fill({
      color: 'rgba(0,0,255,0.5)'
    }),
    stroke: new ol.style.Stroke({
      color: '#00f',
      width: 1
    })
  })]
};

var styleFunction = function(feature, resolution) {
  var featureStyleFunction = feature.getStyleFunction();
  if (featureStyleFunction) {
    return featureStyleFunction.call(feature, resolution);
  } else {
    return defaultStyle[feature.getGeometry().getType()];
  }
};

var dragAndDropInteraction = new ol.interaction.DragAndDrop({
  formatConstructors: [
    ol.format.GPX,
    ol.format.GeoJSON,
    ol.format.IGC,
    ol.format.KML,
    ol.format.TopoJSON
  ]
});

var map = new ol.Map({
  interactions: ol.interaction.defaults().extend([dragAndDropInteraction]),
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
    center: [0, 0],
    zoom: 2
  })
});



dragAndDropInteraction.on('addfeatures', function(event) {
  var vectorSource = new ol.source.Vector({
    features: event.features,
    projection: event.projection
  });
  map.getLayers().push(new ol.layer.Image({
    source: new ol.source.ImageVector({
      source: vectorSource,
      style: styleFunction
    })
  }));
  var view = map.getView();
  view.fitExtent(
      vectorSource.getExtent(), /** @type {ol.Size} */ (map.getSize()));
});

var displayFeatureInfo = function(pixel) {
  var features = [];
  map.forEachFeatureAtPixel(pixel, function(feature, layer) {
    features.push(feature);
  });
  if (features.length > 0) {
    var info = [];
    var i, ii;
    for (i = 0, ii = features.length; i < ii; ++i) {
      info.push(features[i].get('name'));
    }
    document.getElementById('info').innerHTML = info.join(', ') || '&nbsp';
  } else {
    document.getElementById('info').innerHTML = '&nbsp;';
  }
};

map.on('pointermove', function(evt) {
  if (evt.dragging) {
    return;
  }
  var pixel = map.getEventPixel(evt.originalEvent);
  displayFeatureInfo(pixel);
});

map.on('click', function(evt) {
  displayFeatureInfo(evt.pixel);
});
