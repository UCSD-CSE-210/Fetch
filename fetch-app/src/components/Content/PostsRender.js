import React from 'react';
import "./PostsRender.css";
import Post from './Post';

class PostsRender extends React.Component {

    constructor(props) {
        super(props);
        this.state = {
            items : [],
        };
        this.lastScrollY = 0;
        this.handleScroll = this.handleScroll.bind(this);
    }

    componentDidMount() {
        setInterval(this.handleScroll, 200);
        this.setState({items: this.state.items.concat(this.props.items)});
    }

    isScrolling() {
        const {scrollTop} = document.body;;
        const {clientHeight, scrollHeight} = document.getElementById('posts');
        return scrollTop + clientHeight + 40 >= scrollHeight;
    }

    handleScroll(e, force) {
        if (!force && this.lastScrollY === window.scrollY) {
            return;
        }
        else {
            this.lastScrollY = window.scrollY;
        }
        if (this.isScrolling()) {
            // if (this.state.items.length >= 10)
            //     return;
            // fetch("http://192.168.1.65:4000/search")
            //     .then(data => data.json())
            //     .then(data => {
            //         this.setState({items : this.state.items.concat(data)});
            //     });
        }
    }

    render() {
        let lis = [];
        this.state.items.forEach((item, index) => {
            lis.push(
                <div className="col-xs-12 col-lg-6 col-xl-4" key={index.toString()}>
                    <Post value={item}/>
                </div>
            );
        });
        return (
            <div className="row">
                {lis}
            </div>
        );
    }
}

export default PostsRender;
