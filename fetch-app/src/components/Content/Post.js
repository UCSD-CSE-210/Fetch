import React from 'react';
import "./Post.css";
import geoViewport from '@mapbox/geo-viewport'

class Post extends React.Component {

    constructor(props) {
        super(props);
        this.state = {
            imgs : "http://placehold.it/400x20undefined1",
            mapURL : "http://placehold.it/400x20undefined1",
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
        var info = this.props.value;
        let path = [];
        info.coodinates.forEach((items, index) => {
            path.push([items.longitude, items.latitude]);
        });
        var geojson = {
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
        var minX = path[0][0], maxX = path[0][0], minY = path[0][1], maxY = path[0][1];
        for (var i = 1; i < path.length; i++) {
            minX = Math.min(minX, path[i][0]);
            maxX = Math.max(maxX, path[i][0]);
            minY = Math.min(minY, path[i][1]);
            maxY = Math.max(maxY, path[i][1]);
        }
        var center = geoViewport.viewport([
                minX, minY, maxX, maxY
            ], [500, 300]);
        console.log(minX);console.log(maxX);console.log(minY);console.log(maxY);
        var viewpoint = `${center.center[0]},${center.center[1]},${center.zoom - 1.5}`;
        //console.log(path);
        this.setState({mapURL : "https://api.mapbox.com/styles/v1/mapbox/streets-v10/static/" +
                'geojson(' + encodeURIComponent(JSON.stringify(geojson)) + ')/' +
                `${viewpoint}/500x300?` +
                `access_token=${this.token}`});
    }

    render() {
        var info = this.props.value;

                //future work
                // <h5>
                //     <span className="opacity">{info.date}</span>
                //         <span className="ratings">
                //             <b>Ratings  </b>
                //         <span className="tag">{info.ratings}</span>
                //     </span>
                // </h5>
        return (
            <div className="post-card container">
                <h3><b>{info.name}</b></h3>


                <div className="row">
                    <div className="col-sm-4">
                        <div>
                            <p>{info.address}</p>
                        </div>
                        <div className="post-img">
                            <img className="map img-responsive" src={this.state.imgs} alt="dog img on trail"/>
                        </div>
                    </div>

                    <div className="col-sm-8">
                        <div className="post-img">
                            <img className='map img-responsive' alt="trail map" src={this.state.mapURL}/>
                        </div>
                        <div>
                            <label className="btn  btn-primary col-sm-12 post-btn">
                                Upload pictures of wildlife
                                <input
                                    style={{"display": "none"}}
                                    type="file"
                                    accept="image/*"
                                />
                            </label>
                            <label className="btn  btn-primary col-sm-12 post-btn">
                                Capture pictures of dogs
                                <input
                                    style={{"display": "none"}}
                                    type="file"
                                    accept="image/*"
                                />
                            </label>
                        </div>
                    </div>
                </div>
            </div>
        );
    }

}

export default Post;
