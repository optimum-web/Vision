import React from 'react';
import ReactDOM from 'react-dom';
import * as d3 from "d3";
import FormControl from 'react-bootstrap/lib/FormControl';
import FormGroup from 'react-bootstrap/lib/FormGroup';
import ControlLabel from 'react-bootstrap/lib/ControlLabel';
import Button from 'react-bootstrap/lib/Button';

var UserInvite = React.createClass({
    getInitialState: function () {
        return {
            email: '',
            name: ''
        }
    },
    handleChange: function (event, index, value) {
        var state = {};
        state[event.target.name] = event.target.value;
        this.setState(state);
    },
    componentDidMount: function () { 
        var _self = this;
    },
    
    invite: function() {
        var data= {'email': this.state.email,
                   'name': this.state.name};
        $.authorizedAjax({
            url: '/api/v1.0/invite_user/',
            type: 'POST',
            dataType: 'json',
            contentType: 'application/json',
            data: JSON.stringify(data),
            success: function () {
                console.log("was sent")
                alert("Invitation was sent")
            }.bind(this),
            error: function () {
                alert("Error")
            }.bind(this)
        })
    },

    render: function () {
        var _self = this;
        return (
            <div>
                <h2>User Invite</h2>

                <FormGroup >
                    <ControlLabel>Name</ControlLabel>
                    <span className="text-danger"> *</span>
                    <FormControl
                        type="text"
                        placeholder="Name"
                        name="name"
                        value={this.state.name}
                        data-len="50"
                        onChange={this.handleChange}
                        required
                    />
                </FormGroup>
                <FormGroup >
                    <ControlLabel>E-mail</ControlLabel>
                    <span className="text-danger"> *</span>
                    <FormControl
                        type="text"
                        placeholder="E-mail"
                        name="email"
                        value={this.state.email}
                        data-len="50"
                        onChange={this.handleChange}
                        required
                    />
                </FormGroup>
                <Button bsStyle="success" type="button" onClick={this.invite}>Invite</Button>
            </div>
        );
    }
});

export default UserInvite;
