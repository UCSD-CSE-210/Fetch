import React, { Component } from 'react';
import logo from './dog.png';
import "./Header.css"

class Header extends Component {
    render() {
        return (
            <header className="Header-header container-fluid">
                <img src={logo} className="Header-logo" alt="logo" />
                <h1 className="Header-title">Welcome to Fetch</h1>
                
                <form action="">
                  <div class="form-group">
                    <label for="exampleInputEmail1">Email address</label>
                    <input type="search" class="form-control" id="searchBar" placeholder="Search"/>
                  </div>
                  <div class="form-check">
                      <label class="form-check-label">
                        <input class="form-check-input" type="checkbox" value=""/>
                        Water
                      </label>
                  </div>
                    <div class="form-check">
                      <label class="form-check-label">
                        <input class="form-check-input" type="checkbox" value=""/>
                        Poop Bag
                      </label>
                    </div>
                    <div class="form-check">
                      <label class="form-check-label">
                        <input class="form-check-input" type="checkbox" value=""/>
                        Wild life
                      </label>
                    </div>
                    <button type="submit" class="btn btn-primary">Submit</button>
                </form>
            </header>
        );
    }
}

export default Header;
