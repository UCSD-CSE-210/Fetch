import React, { Component } from 'react';
import "./Content.css"

class Content extends Component {
    render() {
        const placeHolder = "http://via.placeholder.com/350x350";
        return (
            <div className="Content container-fluid">
                <div className="row">
                    <div className="col-md-3">
                        <img className="img-responsive" src= {placeHolder} style={{width:100 + "%"}}/>
                    </div>

                    <div className="col-md-3">
                        <img className="img-responsive" src= {placeHolder} style={{width:100 + "%"}}/>
                    </div>

                    <div className="col-md-3">
                        <img className="img-responsive" src= {placeHolder} style={{width:100 + "%"}}/>
                    </div>

                    <div className="col-md-3">
                        <img className="img-responsive" src= {placeHolder} style={{width:100 + "%"}}/>
                    </div>
                </div>
            </div>
        );
    }
}

export default Content;
