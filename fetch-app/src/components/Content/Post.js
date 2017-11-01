import React, { Component } from 'react';
import "./Post.css"

class Post extends React.Component {

  render() {
    var info = this.props.value;
    return (
      <div class="post-card">
         <div class="container">
           <h3><b>{info.title}</b></h3>
           <h5><span class="opacity">{info.date}</span>
              <span class="ratings">
                <b>Ratings  </b> <span class="tag">{info.ratings}</span>
              </span>
           </h5>
         </div>
         <div class="post-imgs">
          <img class="post" src="http://placehold.it/400x20undefined1" alt=""/>
         </div>
         <div class="container">
           <p>{info.description}</p>
         </div>
       </div>
    );
  }
}

export default Post;
