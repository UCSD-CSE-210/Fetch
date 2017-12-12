import React from 'react';
import './WildLifeUploader.css';
import Config from '../../Config';
import Surfacebox from './Surfacebox';

class WildLifeUploader extends React.Component {

	constructor(props) {
		super(props);
		this.state = {
			file: null,
			imagePreviewUrl: null,
			submitButton: null,
			wildlifeItems: [],
			wildlifeId: {},
		};
		this._uploadPhoto = this._uploadPhoto.bind(this);
		this._sendPhotoToServer = this._sendPhotoToServer.bind(this);
		this._getGPSThenSendPhotoToServer = this._getGPSThenSendPhotoToServer.bind(this);
		this._geoError = this._geoError.bind(this);
		this.toggleSurfacebox = this.toggleSurfacebox.bind(this);
		this.wildlifetype = '';
	}

	componentDidMount() {
		var wildlifeId = {};
		var wildlifeItems = [];

	    fetch(Config.backendServerURL + '/api/wildlifetype?')
                .then(data => data.json())
                .then(data => {
                	if (data.results) {
                		data.results.forEach(
                			item => {
                				wildlifeId[item.name] = item.id;
								wildlifeItems.push(item.name);
                			}
                		);
						this.setState({
							wildlifeId: wildlifeId,
							wildlifeItems: wildlifeItems,
						});
                	}
                });
    }

	toggleSurfacebox(label) {
        this.wildlifetype = label;
    }

	_uploadPhoto(event) {
		event.preventDefault();

		let reader = new FileReader();
		let file = event.target.files[0];

		reader.onload = () => {
			this.setState({
				file: file,
				imagePreviewUrl: reader.result,
				submitButton:
					<label className="btn  btn-primary col-sm-12 post-btn">
                    	Upload
                        <input
                            style={{"display": "none"}}
                            onClick={this._getGPSThenSendPhotoToServer}
                        />
                    </label>,
			});
		};

		reader.readAsDataURL(file);
	}

	_getGPSThenSendPhotoToServer(event) {
		event.preventDefault();
        if (navigator.geolocation) {
            navigator.geolocation.getCurrentPosition(this._sendPhotoToServer, this._geoError);
            return;
        }
        alert("Sorry! We cannot get your location from your browser");
	}

	_sendPhotoToServer(position) {
		if (!this.wildlifetype || !this.state.wildlifeId[this.wildlifetype]) {
			alert("Please select a wildlife type");
			return;
		}
		var formData = new FormData();
		formData.append('wildlife_type_id', this.state.wildlifeId[this.wildlifetype]);
		formData.append('route_id', this.props.trail_id);
		formData.append('latitude', position.coords.latitude);
		formData.append('longitude', position.coords.longitude);
		formData.append('wildlife_image', this.state.file);
		fetch(Config.backendServerURL + '/api/upload_wildlife_image',
			  {method: 'POST', body: formData});
		this.setState({file: null, imagePreviewUrl: null, submitButton: null});
	}

    _geoError(error) {
        switch(error.code) {
            case error.PERMISSION_DENIED:
                console.log("User denied the request for Geolocation.");
                alert("Please enable your GPS!. We need your location to uploud wildlife images");
                break;
            case error.POSITION_UNAVAILABLE:
                console.log("Location information is unavailable.");
                alert("Sorry! We cannot get your location from your browser");
                break;
            case error.TIMEOUT:
                console.log("The request to get user location timed out.");
                alert("Sorry! We cannot get your location from your browser");
                break;
            default:
                console.log("An unknown error occurred.");
                alert("Sorry! We cannot get your location from your browser");
                break;
        }
    }

	render() {

		let {imagePreviewUrl} = this.state;
		let imagePreview = null;
		if (imagePreviewUrl) {
			imagePreview = <img className="preview-img" src={imagePreviewUrl} alt=""/>;
		}
		var surfaceboxes = this.state.wildlifeItems.map(
            label => <Surfacebox
                        label = {label}
                        callback = {this.toggleSurfacebox}
                        key = {label}
                     />
        );
		return (
			<div className="modal-dialog">
				<div className="modal-content">
					<div className="modal-header">
						<h4 className="modal-title">Upload Picture of Wildlife</h4>
						<button type="button"
								className="close"
                            	onClick={this.props.closeModal}>
                        	&times;
                        </button>
                    </div>
                    <div className="modal-body">
						<p>For Trail "{this.props.trail_name}"</p>
						<p>Please select a wildlife type: </p>
						<div className='wildlifebox'>
		                    {surfaceboxes}
		                </div>
						<label className="btn  btn-primary col-sm-12 post-btn">
                    		Select a photo
                        	<input
                            	style={{"display": "none"}}
                            	type="file"
                            	accept="image/*"
                            	onChange={this._uploadPhoto}
                        	/>
                    	</label>
                    	<div className="preview">
                    		{imagePreview}
                    	</div>
                    	{this.state.submitButton}
                    </div>
                    <div className="modal-footer">
                    	<button type="button"
                    			className="btn btn-default"
                    			onClick={this.props.closeModal}>
                    		Close
                    	</button>
                    </div>
				</div>
			</div>
		);
	}
}

export default WildLifeUploader;
