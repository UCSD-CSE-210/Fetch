import React from 'react';
import "./Post.css";
import geoViewport from '@mapbox/geo-viewport'
import WildLifeUploader from './WildLifeUploader'
import DogPictureUploader from './DogPictureUploader'
import Lightbox from 'react-image-lightbox';
import Weatherbox from './Weatherbox';
import Config from '../../Config'

class Post extends React.Component {

    constructor(props) {
        super(props);
        var images = [];
        this.props.value.images.forEach(
            item => {
                images.push(Config.backendServerURL + item.image_url);
            }
        );
        this.state = {
            mapURL : "http://placehold.it/400x20undefined1",
            modal : null,
            photoIndex: 0,
            isOpen: false,
            images: images,
            likeCount: this.props.value.like_count,
            canLike: this.props.value.can_like,
            likeAble: this.props.value.can_like,
            wildlifeWarning: null,
            showWildlifeImages: false,
            wildlifeImages: [],
            wildlifePhotoIndex: 0,
        }
        this.token = "pk.eyJ1IjoiZGNoZW4wMDUiLCJhIjoiY2o5aTQza3o2Mzd4OTMzbGc5ZGVxOGdjcyJ9.RweudrPAlw6K5vNijRoK5Q";
        this._submitWildlife = this._submitWildlife.bind(this);
        this._submitDogPicture= this._submitDogPicture.bind(this);
        this._like = this._like.bind(this);
        this.closeModal = this.closeModal.bind(this);
        this._renderWildlife = this._renderWildlife.bind(this);
    }

    componentDidMount() {
        this._renderMap();
        this._renderWildlife();
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
        this.setState({mapURL : "https://api.mapbox.com/styles/v1/mapbox/streets-v10/static/" +
            'geojson(' + encodeURIComponent(JSON.stringify(geojson)) + ')/' +
            `${viewpoint}/500x300?` +
            `access_token=${this.token}`});
    }

    _renderWildlife(){
        var info = this.props.value;
        if (this.props.shouldShow.wildlife) {
            fetch(Config.backendServerURL + `/api/wildlife?route=${info.id}`)
                .then(data => data.json())
                .then(data => {
                    let wildlifeImages = [];
                    data.results.forEach(
                        (item, index) => {
                            if (item.images) {
                                item.images.forEach(
                                    imgItem => {
                                        wildlifeImages.push(Config.backendServerURL + imgItem.image_url);
                                    }
                                )
                            }
                        }
                    );

                    if (data.results && data.results.length > 0) {
                        this.setState(
                            {
                                wildlifeWarning:
                                <div>
                                    <img className="img-responsive wildlife-icon"
                                         src={require("./wildlifeWarning.svg")}
                                         alt="wildlife warning sign"
                                         onClick={() => {
                                            this.setState({showWildlifeImages: true})
                                        }}/>
                                </div>
                            }
                        );
                        this.setState({wildlifeImages: wildlifeImages});
                    }
                });
        }
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

    _like(event){
        event.preventDefault();
        var thumbsUp = document.getElementById("like_id" + this.props.value.id);

        if (!this.state.canLike) {
            return;
        }else if(this.state.likeAble){
            this.setState({likeCount: this.state.likeCount + 1});
            this.setState({likeAble: !this.state.likeAble});
            console.log(thumbsUp);
            var formData = new FormData();
            formData.append('route_id', this.props.value.id);
            fetch(Config.backendServerURL + '/api/route_like',
                {
                    credentials: "same-origin", method: "POST", body: formData
                }
            );
            thumbsUp.classList.add("liked");
        }else if(!this.state.likeAble){
            this.setState({likeCount: this.state.likeCount - 1});
            this.setState({likeAble: !this.state.likeAble});
            thumbsUp.classList.remove("liked");
        }
    }

    _yesOrNo(boolValue) {
        return (boolValue)? 'Yes' : 'No';
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
                    <h3 className='col-5'><b>{info.name}</b></h3>
                    <div className='col-3 wildlife-box'>
                        {this.state.wildlifeWarning}
                    </div>
                    <Weatherbox className='col-4' weatherInfo={info.weather}/>
                </div>
                <div className="row">
                    <div className="col-sm-4">
                        <div>
                            <p>
                                Address: {info.address}<br/>
                                Shade: {this._yesOrNo(info.is_shade)}<br/>
                                Garbage can: {this._yesOrNo(info.is_garbage_can)}<br/>
                                Parking lot: {this._yesOrNo(info.has_parking_lot)}<br/>
                                Poop bag: {this._yesOrNo(info.is_poop_bag)}<br/>
                                Water: {this._yesOrNo(info.is_water)}<br/>
                                Distance: {this._displayDistance(info.distance)}<br/>
                                Surface: {info.surface}<br/>
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
                        {this.state.showWildlifeImages &&
                            <Lightbox className="post-img"
                                mainSrc={this.state.wildlifeImages[this.state.wildlifePhotoIndex]}
                                nextSrc={this.state.wildlifeImages[(this.state.wildlifePhotoIndex + 1) % this.state.wildlifeImages.length]}
                                prevSrc={this.state.wildlifeImages[(this.state.wildlifePhotoIndex + this.state.wildlifeImages.length - 1)
                                                                    % this.state.wildlifeImages.length]}

                                onCloseRequest={() => this.setState({ showWildlifeImages: false })}
                                onMovePrevRequest={() => this.setState({
                                    wildlifePhotoIndex: (this.state.wildlifePhotoIndex + this.state.wildlifeImages.length - 1) % this.state.wildlifeImages.length,
                                })}
                                onMoveNextRequest={() => this.setState({
                                    wildlifePhotoIndex: (this.state.wildlifePhotoIndex + 1) % this.state.wildlifeImages.length,
                                })}
                            />
                        }
                    </div>

                    <div className="col-sm-8">
                        <div className="post-img">
                            <img className='map img-responsive' alt="trail map" src={this.state.mapURL}/>
                            <div className="like-box">
                                {(this.state.canLike) &&
                                    <span id={"like_id" + info.id} className="fa fa-thumbs-up fa-2x" onClick={this._like}></span>}
                                {!(this.state.canLike) &&
                                    <span className="fa fa-thumbs-up fa-2x unclickable"></span>
                                }
                                <p>{this.state.likeCount}</p>
                            </div>
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
