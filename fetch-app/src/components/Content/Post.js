import React from 'react';
import "./Post.css"

class Post extends React.Component {

    constructor(props) {
        super(props);
        this.state = {
            imgs : "http://placehold.it/400x20undefined1",
        }
        this.ourToken = "pk.eyJ1IjoiZGNoZW4wMDUiLCJhIjoiY2o5aTQza3o2Mzd4OTMzbGc5ZGVxOGdjcyJ9.RweudrPAlw6K5vNijRoK5Q";
        this.token="pk.eyJ1IjoicGV0cnVzanZyIiwiYSI6IkJuWjZqbTgifQ._rWDJ27Qq-wCl-l8flkbVQ";
    }

    componentDidMount() {
        fetch("https://dog.ceo/api/breed/retriever/golden/images/random")
            .then(data => data.json())
            .then(data => {
                this.setState({imgs: data.message})
            });
    }

    render() {
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
        var mapURL = "https://api.mapbox.com/styles/v1/mapbox/streets-v10/static/" +
                     'geojson(' + encodeURIComponent(JSON.stringify(g)) + ')/' +
                     "-117.234104275703,32.8817946493596,13.67/500x300@2x?" +
                     `access_token=${this.token}`;
        var info = this.props.value;
        return (
            <div className="post-card">
                <div className="container">
                    <h3><b>{info.title}</b></h3>
                    <h5><span className="opacity">{info.date}</span>
                        <span className="ratings">
                            <b>Ratings  </b>
                            <span className="tag">{info.ratings}</span>
                        </span>
                    </h5>
                </div>
                <div className="post-imgs">
                    <img className='map' src={mapURL}/>
                </div>
                <div className="container">
                    <p>{info.description}</p>
                </div>
            </div>
        );
    }

}

export default Post;
