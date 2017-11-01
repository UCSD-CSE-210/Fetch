import React, { Component } from 'react';
import "./Content.css"
import mapImg from './GoogleMapTA.jpg';


class SearchResult extends Component {
    render() {
        return (
            <div className="row">
                <div className="col-sm-3">
                    <img className="img-responsive" src={mapImg} style={{width:100 + "%"}}/>
                </div>

                <div className="col-sm-6">
                    This is more information about the route
                </div>

                <div className="col-sm-3">
                    <img className="img-responsive" src="https://dog.ceo/api/img/eskimo/n02109961_7861.jpg" style={{width:100 + "%"}}/>
                </div>
            </div>
        );
    }
}

export default SearchResult;
