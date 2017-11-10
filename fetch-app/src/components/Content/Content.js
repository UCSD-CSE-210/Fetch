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

    fillServerResult(data, shouldShow) {
      if (data != null && data.length > 0) {
        this.setState({postsRender: null});
        this.setState({postsRender : <PostsRender items = {data} 
                                                  shouldShow = {shouldShow}/>});
      }
      else {
        this.setState({postsRender: <p>Oops... Cannot find; Will have more route in the future</p>});
      }
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
