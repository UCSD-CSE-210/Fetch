import React, { Component } from 'react';
import logo from './dog.png';
import "./Header.css"
import SearchBar from './SearchBar'

class Header extends Component {
    render() {
        return (
          <div class="Header-header container-fluid text-center">
            <img src={logo} className="Header-logo" alt="logo" />
            <h1 id="fetch"><b>Fetch</b></h1>
            <p>Help your dog find the best trail</p>
            <div id="searchBar">
                <SearchBar />
            </div>
          </div>
        );
    }
}

export default Header;
