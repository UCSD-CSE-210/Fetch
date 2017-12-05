import React from 'react';
import "./Post.css";
import geoViewport from '@mapbox/geo-viewport'
import WildLifeUploader from './WildLifeUploader'
import DogPictureUploader from './DogPictureUploader'
import Lightbox from 'react-image-lightbox';
import Weatherbox from './Weatherbox';

class Post extends React.Component {

    constructor(props) {
        super(props);
        this.state = {
            imgs : "http://placehold.it/400x20undefined1",
            mapURL : "http://placehold.it/400x20undefined1",
            wildlifeInfo : "",
            modal : null,
            photoIndex: 0,
            isOpen: false,
            images: [],
        }
        this.token = "pk.eyJ1IjoiZGNoZW4wMDUiLCJhIjoiY2o5aTQza3o2Mzd4OTMzbGc5ZGVxOGdjcyJ9.RweudrPAlw6K5vNijRoK5Q";
        this._submitWildlife = this._submitWildlife.bind(this);
        this._submitDogPicture= this._submitDogPicture.bind(this);
        this.closeModal = this.closeModal.bind(this);
    }

    _renderMap() {
        //auto zoom level
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
        var viewpoint = `${center.center[0]},${center.center[1]},${center.zoom - 1.5}`;

        //wildlife
        if (this.props.shouldShow.wildlife) {
            fetch(`http://localhost:5000/api/wildlife?route=${info.id}`)
                .then(data => data.json())
                .then(data => {
                    let wildlife = []
                    data.results.forEach(
                        (item, index) => {
                            wildlife.push(<div> {item.wildlifetype.name} <br/> </div>);
                        }
                    );
                    if (data.results && data.results.length > 0) {
                        this.setState({wildlifeInfo:  <div> Wildlife: <br/>
                                                          {wildlife}
                                                      </div>
                                                });
                    }
                });           
        }
        this.setState({mapURL : "https://api.mapbox.com/styles/v1/mapbox/streets-v10/static/" +
            'geojson(' + encodeURIComponent(JSON.stringify(geojson)) + ')/' +
            `${viewpoint}/500x300?` +
            `access_token=${this.token}`});
    }

    componentDidMount() {
        fetch("https://dog.ceo/api/breed/retriever/golden/images/random")
            .then(data => data.json())
            .then(data => {
                this.setState({imgs: data.message,
                               images: this.state.images.concat([data.message])});
                console.log(this.state.images);
            });
        this._renderMap();
    }

    _yesOrNo(boolValue) {
        return (boolValue)? 'Yes' : 'No';
    }

    _submitWildlife(event) {
        event.preventDefault();
        this.setState({modal: <WildLifeUploader 
                                trail_id = {this.props.value.id}
                                trail_name = {this.props.value.name}
                                closeModal = {this.closeModal}
                                />});
    }

    _submitDogPicture(event) {
        event.preventDefault();
        this.setState({modal: <DogPictureUploader 
                                trail_id = {this.props.value.id}
                                trail_name = {this.props.value.name}
                                closeModal = {this.closeModal}
                                />});
    }

    closeModal(event) {
        event.preventDefault();
        this.setState({modal: null});
    }


    _displayDistance(distance) {
        if (!distance)
            return "Unknown";
        distance = Math.round(distance * 100)/100;
        if (!distance)
            distance = "< 0.005"
        return distance + " miles";
    }

    render() {
        const {
            photoIndex,
            isOpen,
            images,
        } = this.state;
        var info = this.props.value;
        return (
            <div className="post-card container">
                <div className='row'>
                    <h3 className='col-9'><b>{info.name}</b></h3>
                    <Weatherbox className='col-3'/>
                </div>
                <div className="row">
                    <div className="col-sm-4">
                        <div>
                            <p>
                                Address: {info.address}<br/>
                                Shade: {this._yesOrNo(info.is_shade)}<br/>
                                Garbage can: {this._yesOrNo(info.is_garbage_can)}<br/>
                                Water: {this._yesOrNo(info.is_water)}<br/>
                                distance: {this._displayDistance(info.distance)}
                                {this.state.wildlifeInfo}
                            </p>
                        </div>
                        <div className="post-img">
                            <img
                                src={images[0]}
                                className="map img-responsive"
                                alt="dog img on trail"
                                onClick={() => this.setState({isOpen: true})}
                            />
                        </div>
                        {isOpen &&
                            <Lightbox className="post-img"
                                mainSrc={images[photoIndex]}
                                nextSrc={images[(photoIndex + 1) % images.length]}
                                prevSrc={images[(photoIndex + images.length - 1) % images.length]}
         
                                onCloseRequest={() => this.setState({ isOpen: false })}
                                onMovePrevRequest={() => this.setState({
                                    photoIndex: (photoIndex + images.length - 1) % images.length,
                                })}
                                onMoveNextRequest={() => this.setState({
                                    photoIndex: (photoIndex + 1) % images.length,
                                })}
                            />
                        }
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
                                    onClick={this._submitWildlife}
                                />
                            </label>
                            <label className="btn  btn-primary col-sm-12 post-btn">
                                Capture pictures of dogs
                                <input
                                    style={{"display": "none"}}
                                    onClick={this._submitDogPicture}
                                />
                            </label>
                        </div>
                    </div>
                </div>
                <div className="post-modal">
                    {this.state.modal}
                </div>
            </div>
        );
    }

}

export default Post;
