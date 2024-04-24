const addressInput = document.getElementById("address-input");
async function initMap() {
    await ymaps3.ready;
    const {geocode} = await ymaps.ready();

    const {YMap, YMapDefaultSchemeLayer, YMapListener} = ymaps3;

    const clickHandler = async(object, event) => {
        if (object?.type !== 'hotspot') {
            return;
        }

        const [long, lat] = event.coordinates;
        const addressGeocode = await geocode([lat, long])
        const address = addressGeocode.geoObjects.get(0).properties.get('text');

        if (addressInput !== null) {
            addressInput.value = address;
        }
    };

    const mapListener = new YMapListener({
        layer: 'any', onClick: clickHandler
    });

    const map = new YMap(
        document.getElementById('app'),
        {
            location: {
                center: [82.920430, 55.030204],
                zoom: 10
            }
        }
    );

    map.addChild(new YMapDefaultSchemeLayer());
    map.addChild(mapListener);
}

initMap();