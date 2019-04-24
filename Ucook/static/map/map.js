"use strict";


var map = null;
var infowindow = null;
var markers = [];


// Default to downtown Toronto
var defaultPosition = {
  coords: {
    latitude: 43.6722780,
    longitude: -79.3745125
  }
};

var dummyAddresses = [

    { "owner": "dummy",
     "address1" : "3913 Nantasket Street",
     "address2" : "11",
     "postCode" : "15207",
     "city" : "Pittsburgh",
     "state" : "Pennsylvania" },

    {"owner": "dummy1",
     "address1" : "5030 Centre Avenue",
     "address2" : "961",
     "postCode" : "15213",
     "city" : "Pittsburgh",
     "state" : "Pennsylvania" },

    {"owner": "dummy2",
    "address1" : "4716 Ellsworth Avenue",
    "address2" : "11",
    "postCode" : "15213",
    "city" : "Pittsburgh",
    "state" : "Pennsylvania" },

    {"owner": "dummy3",
    "address1" : "2 Bayard Road",
    "address2" : "23",
    "postCode" : "15213",
    "city" : "Pittsburgh",
    "state" : "Pennsylvania" },

    {"owner": "dummy4",
    "address1" : "5000 Forbes Avenue",
    "address2" : "11",
    "postCode" : "15213",
    "city" : "Pittsburgh",
    "state" : "Pennsylvania" },

]

var geoSearch = function(data, map, infoWindow, position, term) {

    var geocoder = new google.maps.Geocoder();

    for (var i = 0; i < data.length; i++) {

        var rawAddr = data[i];
        var addr = getConcatAddress(rawAddr);

        geocoder.geocode( { 'address': addr }, function(results, status) {

            if (status == google.maps.GeocoderStatus.OK) {
                var latitude = results[0].geometry.location.lat();
                var longitude = results[0].geometry.location.lng();
                position = {
                  coords: {
                    latitude: latitude,
                    longitude: longitude,
                  }
                };

//                console.log(position.coords.latitude);
//                console.log(position.coords.longitude);

                var marker = new google.maps.Marker({
                    id: i,
                    title: rawAddr.owner,
                    url:"https://google.com",
                    position: {
                        lat: position.coords.latitude,
                        lng: position.coords.longitude,
                    },
                    map: map,
                });
                markers.push(marker);

                google.maps.event.addListener(marker, 'click', (function (marker, key) {
                    return function () {
                        var content = '<div><a target="_blank" href="' + marker.url + '">' + marker.title + '</ a></div>';
                        infowindow.setContent(content);
                        infowindow.open(map, marker);
                    };
                })(marker, i));

            }

        });

    }

};

var getConcatAddress = function(addr) {
    var concatAddr = addr['address1'] + ", " + addr['city'] + ", " + addr['state'];
    return concatAddr;
}

var populateMap = function (geoPosition, term) {

  $('#geolocation').hide();

  infowindow = new google.maps.InfoWindow({
    content: "hello"
  });

  var position = geoPosition;
  if (!position) {
    position = defaultPosition;
  }

  map = new google.maps.Map(document.getElementById('map'), {
    center: {
      lat: position.coords.latitude,
      lng: position.coords.longitude
    },
    zoom: 16
  });

  // Make info window for marker show up above marker
  var windowOptions = {
    pixelOffset: {
      height: -32,
      width: 0
    }
  };

  // yelpSearch(map, infowindow, position);
  geoSearch(dummyAddresses, map, infowindow, position);

};


var geolocationFail = function() {
  populateMap(defaultPosition);
};


var initMap = function() {
  if (navigator.geolocation) {
    var location_timeout = setTimeout(geolocationFail, 5000);

    navigator.geolocation.getCurrentPosition(function(position) {
      clearTimeout(location_timeout);
      populateMap(position);
    }, function (error) {
        clearTimeout(location_timeout);
        geolocationFail();
    });
  } else {
    // Fallback for no geolocation
    geolocationFail();
  }
};


var clearMarkers = function(markers) {
  for (var i=0; i<markers.length; i++) {
    markers[i].setMap(null);
  }
  markers = [];
};


$('#id_search_form').on('submit', function(event) {
  event.preventDefault();
  // clearMarkers(markers);
  var center = map.getCenter();
  var position = {
    coords: {
      latitude: center.lat(),
      longitude: center.lng()
    }
  };

  // yelpSearch(map, infowindow, position, $('#id_term').val());
  geoSearch(dummyAddresses, map, infowindow, position, $('#id_term').val());

});