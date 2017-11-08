import React, { Component } from 'react';
import logo from './dog.png';
import "./Header.css"

class Header extends Component {
    render() {
        return (
            <div className="Header-header container-fluid text-center">
            	<div>
            		<img src={logo} className="Header-logo" alt="logo" />
                	<h1 id="fetch"><b>Fetch</b></h1>
            	</div>
                <p>Help your dog find the best trail</p>
            </div>
        );
    }
}

export default Header;
