import React, { Component } from 'react';
import logo from './dog.png';
import "./Header.css"

class Header extends Component {
    render() {
        return (
            <header className="Header-header container-fluid">
                <img src={logo} className="Header-logo" alt="logo" />
                <h1 className="Header-title">Welcome to Fetch</h1>
                <div className="btn-group">
                    <button type="button" className="btn btn-header">Sign Up</button>
                    <button type="button" className="btn btn-header">Sign In</button>
                    <button type="button" className="btn btn-header">Help</button>
                </div>
            </header>
        );
    }
}

export default Header;
