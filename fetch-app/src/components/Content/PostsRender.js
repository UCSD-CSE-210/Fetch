import React, { Component } from 'react';
import "./PostsRender.css"
import Post from './Post'

class PostsRender extends React.Component {

  constructor(props) {
    super(props);
    this.state = {
      items : [
        {
          title : 'Trail 1',
          date : 'November 1 2017',
          ratings : '5.0',
          description : 'this is just some random description of a trail this is just some random description of a trail this is just some random description of a trail'
        },
        {
          title : 'Trail 2',
          date : 'November 1 2017',
          ratings : '4.8',
          description : 'this is just some random description of a trail this is just some random description of a trail this is just some random description of a trail'
        }
      ]
    };
    this.lastScrollY = 0;
    this.handleScroll = this.handleScroll.bind(this);
  }

  componentDidMount() {
    setInterval(this.handleScroll, 500);
  }

  isScrolling() {
    const {scrollTop} = document.body;;
    const {clientHeight, scrollHeight} = document.getElementById('posts');
    return scrollTop + clientHeight + 40 >= scrollHeight;
  }

  handleScroll(e, force) {
    if (!force && this.lastScrollY == window.scrollY) {
      return;
    }
    else {
      this.lastScrollY = window.scrollY;
    }
    if (this.isScrolling()) {
      var data = {
        title : 'Trail',
        date : 'November 1 2017',
        ratings : '4.8',
        description : 'this is just some random description of a trail this is just some random description of a trail this is just some random description of a trail'
      }
      this.setState({items : this.state.items.concat(data)});
    }
  }

  renderSinglePost(info) {
    return <Post value={info}/>;
  }

  render() {
    let lis = [];
    this.state.items.forEach((item, index) => {
      lis.push(
        <div>
            {this.renderSinglePost(item)}
        </div>
      );
    })
    return (
      <div>
        {lis}
      </div>
    );
  }
}

export default PostsRender;
