import React from 'react';
import "./Content.css"
import PostsRender from './PostsRender'

class Content extends React.Component {

    render() {
        return (
            <div id="posts">
                <PostsRender />
            </div>
        );
    }

}

export default Content;
