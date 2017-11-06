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
        var info = this.props.value;
        var mapURL = "https://api.mapbox.com/styles/v1/mapbox/streets-v10/static/" +
                     'geojson(' + encodeURIComponent(JSON.stringify(info.geojson)) + ')/' +
                     `${info.viewpoint}/500x300?` +
                     `access_token=${this.token}`;
        return (
            <div className="post-card container">
                <h3><b>{info.title}</b></h3>
                <h5>
                    <span className="opacity">{info.date}</span>
                        <span className="ratings">
                            <b>Ratings  </b>
                        <span className="tag">{info.ratings}</span>
                    </span>
                </h5>

                <div className="row">
                    <div className="col-sm-4">
                        <div>
                            <p>{info.description}</p>
                        </div>
                        <div className="post-img">
                            <img className="map img-responsive" src={this.state.imgs} alt="dog img on trail"/>
                        </div>
                    </div>

                    <div className="col-sm-8">
                        <div className="post-img">
                            <img className='map img-responsive' alt="trail map" src={mapURL}/>
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
