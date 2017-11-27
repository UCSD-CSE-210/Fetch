import React from 'react';
import './WildLifeUploader.css'

class WildLifeUploader extends React.Component {

	constructor(props) {
		super(props);
		this.state = {
			file: null,
			imagePreviewUrl: null,
			submitButton: null,
		};
		this._uploadPhoto = this._uploadPhoto.bind(this);
		this._sendPhotoToServer = this._sendPhotoToServer.bind(this);
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
                            onClick={this._sendPhotoToServer}
                        />
                    </label>,
			});
		};

		reader.readAsDataURL(file);
	}

	_sendPhotoToServer(event) {
		event.preventDefault();
		var formData = new FormData();
		//formData.append('wildlife_id', this.props.trail_id);
		formData.append('image', this.state.file);
		// tested upload_route_image;
		// fetch('http://127.0.0.1:5000/api/upload_wildlife_image', 
		// 	  {method: 'POST', body: formData});
		this.setState({file: null, imagePreviewUrl: null, submitButton: null});
	}

	render() {

		let {imagePreviewUrl} = this.state;
		let imagePreview = null;
		if (imagePreviewUrl) {
			imagePreview = <img className="preview-img" src={imagePreviewUrl} alt=""/>;
		}
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
						<p>For Trail "{this.props.trail_name}" </p>
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
				</div>
			</div>
		);
	}
}

export default WildLifeUploader;