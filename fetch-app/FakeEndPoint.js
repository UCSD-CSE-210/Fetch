const express = require('express')
const app = express()

var path = [
            [
                -117.233954071999,
                32.8820469288637
            ],
            [
                -117.234104275703,
                32.8817946493596
            ],
            [
                -117.234104275703,
                32.8809927561667
            ],
            [
                -117.235563397408,
                32.8809927561667
            ],
            [
                -117.237580418587,
                32.879307855821
            ],
            [
                -117.237569689751,
                32.8791907225207
            ],
            [
                -117.238685488701,
                32.8781455262187
            ],
            [
                -117.238827645779,
                32.8781365158522
            ],
            [
                -117.238913476467,
                32.8775508400632
            ],
            [
                -117.239235341549,
                32.8776184182363
            ]
        ];

var g = {
            "type": "Feature",
            "geometry": {
                "type": "LineString",
                "coordinates": path,
            },
            "properties": {
                "stroke":"blue",
                "stroke-width":"3",
            },
        };

var fakeData = {results: [
    
    {
        name : 'Trail',
        date : 'November 1 2017',
        ratings : '4.8',
        geojson : g,
        viewpoint : "-117.234104275703,32.8817946493596,13.67",
        imgs: 'https://dog.ceo/api/img/retriever-golden/n02099601_3007.jpg',
        description : 'this is just some random description of a trail this is just some random description of a trail this is just some random description of a trail'
    },
    {
        name : 'Trail',
        date : 'November 1 2017',
        ratings : '4.8',
        geojson : g,
        viewpoint : "-117.234104275703,32.8817946493596,13.67",
        imgs: 'https://dog.ceo/api/img/retriever-golden/n02099601_3007.jpg',
        description : 'this is just some random description of a trail this is just some random description of a trail this is just some random description of a trail'
    }
]
}

app.get('/api/route', function(req, res){
    console.log(req.query);
    res.setHeader('Access-Control-Allow-Origin', '*');
    res.send(JSON.stringify(fakeData));
})

app.listen(5000, () => console.log('Example app listening on port 5000!'))
