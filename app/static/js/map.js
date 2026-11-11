/* =========================================
   MEDIRESCUE - MAP FUNCTIONALITY
   Leaflet.js + OpenStreetMap
   ========================================= */

document.addEventListener("DOMContentLoaded", function () {

    // Check whether the map container exists
    const mapElement = document.getElementById("map");

    if (!mapElement) {
        return;
    }

    // Check whether Leaflet is loaded
    if (typeof L === "undefined") {
        console.error("Leaflet.js is not loaded.");
        return;
    }

    // Default map location: Asansol
    const defaultLatitude = 23.6889;
    const defaultLongitude = 86.9661;

    // Create the map
    const map = L.map("map").setView(
        [defaultLatitude, defaultLongitude],
        13
    );

    // Load OpenStreetMap tiles
    L.tileLayer(
        "https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png",
        {
            attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors',
            maxZoom: 19
        }
    ).addTo(map);

    // Create pickup marker
    let pickupMarker = L.marker([
        defaultLatitude,
        defaultLongitude
    ]).addTo(map);

    pickupMarker.bindPopup("Default pickup location").openPopup();

    // Get pickup coordinate inputs
    const latitudeInput = document.querySelector(
        'input[name="pickup_latitude"]'
    );

    const longitudeInput = document.querySelector(
        'input[name="pickup_longitude"]'
    );

    // Update pickup location when user clicks the map
    map.on("click", function (event) {

        const latitude = event.latlng.lat;
        const longitude = event.latlng.lng;

        // Move marker
        pickupMarker.setLatLng([latitude, longitude]);

        pickupMarker
            .bindPopup("Selected pickup location")
            .openPopup();

        // Update form coordinates
        if (latitudeInput) {
            latitudeInput.value = latitude.toFixed(6);
        }

        if (longitudeInput) {
            longitudeInput.value = longitude.toFixed(6);
        }

        console.log("Pickup coordinates:", latitude, longitude);
    });

    // Get current location using browser permission
    const locationButton = document.getElementById("get-location");

    if (locationButton && navigator.geolocation) {

        locationButton.addEventListener("click", function () {

            navigator.geolocation.getCurrentPosition(

                function (position) {

                    const latitude = position.coords.latitude;
                    const longitude = position.coords.longitude;

                    map.setView([latitude, longitude], 16);

                    pickupMarker.setLatLng([
                        latitude,
                        longitude
                    ]);

                    pickupMarker
                        .bindPopup("Your current location")
                        .openPopup();

                    if (latitudeInput) {
                        latitudeInput.value = latitude.toFixed(6);
                    }

                    if (longitudeInput) {
                        longitudeInput.value = longitude.toFixed(6);
                    }
                },

                function () {
                    alert("Unable to access your location. Please allow location permission.");
                }
            );

        });
    }

});