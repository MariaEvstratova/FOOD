async function initMap() {
    await ymaps3.ready;

    const {YMap, YMapDefaultSchemeLayer} = ymaps3;

    // const clickHandler = (object) => {
    //     if (object?.type === 'hotspot') {
    //         console.log('Clicked on hotspot!');
    //     }
    // };
    //
    // const mapListener = new YMapListener({
    //     layer: 'any', onClick: clickHandler
    // });

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
    // map.addChild(new mapListener());
    // map.addChild(new YMapListener());
}

initMap();