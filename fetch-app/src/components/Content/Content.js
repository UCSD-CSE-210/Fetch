import React, { Component } from 'react';
import "./Content.css"

class Content extends Component {
    constructor(){
        super();
        this.state = {dogs:[]};
    }

    componentDidMount(){
        this.refreshDogImage();
    }

    refreshDogImage(){
        var image = [];
        for (var i = 0; i < 4; i++){
            fetch("https://dog.ceo/api/breed/retriever/golden/images/random")
                .then(data => data.json())
                .then(data => {
                    image.push(data);
                    this.setState({dogs:image})
                });
        }
    }

    render() {
        console.log(this.state.dogs);
        return (
            <div className="Content container-fluid">
                <div className="row">
                    {
                        this.state.dogs.map(dog => (
                            <div className="col-md-3" key={dog.message}>
                                <img className="img-responsive" src= {dog.message} style={{width:100 + "%"}}/>
                            </div>
                        ))
                    }
                </div>
            </div>
        );
    }
}

export default Content;
