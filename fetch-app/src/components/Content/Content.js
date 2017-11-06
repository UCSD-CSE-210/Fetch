import React from 'react';
import "./Content.css"
import SearchBar from './SearchBar'
import PostsRender from './PostsRender'

class Content extends React.Component {

    constructor(props) {
      super(props);
      this.state = {
          postsRender: null,
      };
      this.fillServerResult = this.fillServerResult.bind(this);
    }

    fillServerResult(data) {
        this.setState({postsRender: null});
        this.setState({postsRender : <PostsRender items = {data}/>});
    }

    render() {
        return (
            <div>
                <div className="container-fluid" id="searchBar">
                    <SearchBar callback = {this.fillServerResult}/>
                </div>
                <div id="posts">
                    {this.state.postsRender}
                </div>
            </div>
        );
    }

}

export default Content;
