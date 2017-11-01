import React, { Component } from 'react';
import "./Content.css"
import PostsRender from './PostsRender'
import SearchResult from './SearchResult'

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
            <body>
              <div id="posts">
                <PostsRender />
              </div>
            </body>
            <div className="Content container-fluid">
                <SearchResult />
            </div>
        );
    }
}

export default Content;
