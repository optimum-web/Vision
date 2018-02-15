import React from 'react';
import FormControl from 'react-bootstrap/lib/FormControl';
import FormGroup from 'react-bootstrap/lib/FormGroup';
import ControlLabel from 'react-bootstrap/lib/ControlLabel';
import {findDOMNode} from 'react-dom';
import {hashHistory} from 'react-router';
import {Link} from 'react-router';
import Checkbox from 'react-bootstrap/lib/Checkbox';
import OverlayTrigger from 'react-bootstrap/lib/OverlayTrigger';
import Tooltip from 'react-bootstrap/lib/Tooltip';
import HelpBlock from 'react-bootstrap/lib/HelpBlock';


var SelectField = React.createClass({
    handleChange: function (event, index, value) {
        this.setState({
            value: event.target.value
        });
    },
    getInitialState: function () {
        return {
            items: [],
            isVisible: false,
            value: -1
        };
    },
    isVisible: function () {
        return this.state.isVisible;
    },
    componentDidMount: function () {
        var source = '/api/v1.0/' + this.props.source + '/';
        this.serverRequest = $.authorizedGet(source, function (result) {
            this.setState({items: (result['result'])});
        }.bind(this), 'json');
    },
    componentWillUnmount: function () {
        this.serverRequest.abort();
    },
    setVisible: function () {
        this.state.isVisible = true;
    },
    render: function () {
        var label = (this.props.label != null) ? this.props.label : "";
        var value = (this.props.value != null) ? this.props.value : "";
        var name = (this.props.name != null) ? this.props.name : "";
        var validationState = (this.props.errors[name]) ? 'error' : null;
        var error = this.props.errors[name];
        var menuItems = [];
        for (var key in this.state.items) {
            menuItems.push(<option key={this.state.items[key].id}
                                   value={this.state.items[key].id}>{`${this.state.items[key].name ? this.state.items[key].name : this.state.items[key].model}`}</option>);
        }
        return (
            <FormGroup validationState={validationState}>
                <ControlLabel>{label}</ControlLabel>
                <FormControl componentClass="select"
                             onChange={this.handleChange}
                             value={value}
                             name={name}
                >
                    <option>{this.props.label}</option>);
                    {menuItems}
                </FormControl>
                <HelpBlock className="warning">{error}</HelpBlock>
            </FormGroup>
        );
    }
});


var TankParams = React.createClass({
    getInitialState: function () {
        return {
            'sealed': '',
            'welded_cover': '',
            'id':'',
            'errors': {}
        }
    },

    handleChange: function(e){
        var state = this.state;
        if (e.target.type == "checkbox"){
            state[e.target.name] = e.target.checked;
        }
        else
            state[e.target.name] = e.target.value;
        this.setState(state);
    },

    load:function() {
        this.setState(this.props.equipment_item)
    },

    render: function () {
        var errors = (Object.keys(this.state.errors).length) ? this.state.errors : this.props.errors;
        return (
            <div>
                <div className="row">
                    <div className="col-md-4">
                        <SelectField
                            source="fluid_type"
                            label="Fluid Type"
                            name="fluid_type_id"
                            value={this.state.fluid_type_id}
                            errors={errors}/>
                    </div>
                    <div className="col-md-4">
                        <SelectField
                            source="fluid_level"
                            label="Fluid Level"
                            name="fluid_level_id"
                            value={this.state.fluid_level_id}
                            errors={errors}/>
                    </div>
                    <div className="col-md-2">
                        <Checkbox name="welded_cover" checked={this.state.welded_cover} onChange={this.handleChange}><b>Welded Cover</b></Checkbox>
                    </div>
                </div>
            </div>
        )
    }
});


export default TankParams;