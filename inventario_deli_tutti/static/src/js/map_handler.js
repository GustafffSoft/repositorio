odoo.define('inventario_deli_tutti.map_handler', function (require) {
    "use strict";
    var core = require('web.core');
    var rpc = require('web.rpc');

    core.bus.on('web_client_ready', null, function () {
        if (document.getElementById('map')) {
            var map = L.map('map').setView([19.432608, -99.133209], 13); // Latitud y longitud inicial
            L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
                maxZoom: 18
            }).addTo(map);

            var marker = L.marker([19.432608, -99.133209], {
                draggable: true
            }).addTo(map);

            marker.on('dragend', function (e) {
                var position = marker.getLatLng();
                rpc.query({
                    model: 'produccion.pedidos.especiales',
                    method: 'write',
                    args: [[record_id], {'latitud': position.lat, 'longitud': position.lng}],
                }).then(function (result) {
                    // Manejar el resultado
                });
            });
        }
    });
});
