import React from 'react';
import FormControl from 'react-bootstrap/lib/FormControl';
import FormGroup from 'react-bootstrap/lib/FormGroup';
import Checkbox from 'react-bootstrap/lib/Checkbox';
import ControlLabel from 'react-bootstrap/lib/ControlLabel';
import {findDOMNode} from 'react-dom';
import {hashHistory} from 'react-router';
import {Link} from 'react-router';
import OverlayTrigger from 'react-bootstrap/lib/OverlayTrigger';
import Tooltip from 'react-bootstrap/lib/Tooltip';
import HelpBlock from 'react-bootstrap/lib/HelpBlock';


const TextField = React.createClass({
    _onChange: function (e) {
        this.props.onChange(e);
    },
    render: function () {
        let tooltip = <Tooltip id={this.props.label}>{this.props.label}</Tooltip>;
        var label = (this.props.label != null) ? this.props.label : "";
        var name = (this.props.name != null) ? this.props.name : "";
        var type = (this.props["data-type"] != null) ? this.props["data-type"]: undefined;
        var len = (this.props["data-len"] != null) ? this.props["data-len"]: undefined;
        var validationState = (this.props.errors[name]) ? 'error' : null;
        var error = this.props.errors[name];
        var value = (this.props["value"] != null) ? this.props["value"]: "";
        return (
            <OverlayTrigger overlay={tooltip} placement="top">
                <FormGroup validationState={validationState}>
                    <ControlLabel>{label}</ControlLabel>
                    <FormControl type="text"
                                 placeholder={label}
                                 name={name}
                                 data-type={type}
                                 data-len={len}
                                 onChange={this._onChange}
                                 value={value}
                    />
                    <HelpBlock className="warning">{error}</HelpBlock>
                    <FormControl.Feedback />
                </FormGroup>
            </OverlayTrigger>
        );
    }
});

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
                             name={this.props.name}
                >
                    <option>{this.props.label}</option>);
                    {menuItems}
                </FormControl>
                <HelpBlock className="warning">{error}</HelpBlock>
            </FormGroup>
        );
    }
});


var BreakerParams = React.createClass({

    getInitialState: function () {
        return {
            'fluid_type_id':'',
            'fluid_level_id':'',
            'interrupting_medium_id':'',
            'breaker_mechanism_id':'',
            'phase_number':'',
            'kv':'',
            'kvar':'',
            'sealed':'',
            'welded_cover':'',
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
                    <div className="col-md-3">
                        <SelectField
                            source="fluid_type"
                            label="Fluid Type"
                            name="fluid_type_id"
                            value={this.state.fluid_type_id}
                            errors={errors}/>
                    </div>
                    <div className="col-md-3">
                        <SelectField
                            source="fluid_level"
                            label="Fluid Level"
                            name="fluid_level_id"
                            value={this.state.fluid_level_id}
                            errors={errors}/>
                    </div>
                    <div className="col-md-3">
                        <SelectField
                            source="interrupting_medium"
                            label="Interrupting Medium"
                            name="interrupting_medium_id"
                            value={this.state.interrupting_medium_id}
                            errors={errors}/>
                    </div>
                    <div className="col-md-3">
                        <SelectField
                            source="breaker_mechanism"
                            label="Breaker Mechanism"
                            name="breaker_mechanism_id"
                            value={this.state.breaker_mechanism_id}
                            errors={errors}/>
                    </div>
                </div>

                <div className="row">
                    <div className="col-md-3">
                        <TextField onChange={this.handleChange}
                                   label="Curent Rating"
                                   name="current_rating"
                                   value={this.state.current_rating ? this.state.current_rating : ""}
                                   errors={errors}
                                   data-type="int"
                                   data-len="6"/>
                    </div>
                    <div className="col-md-1 ">
                        <Checkbox name="open" checked={this.state.open} onChange={this.handleChange}><b>Open</b></Checkbox>
                    </div>
                </div>
            </div>
        )
    }
});


export default BreakerParams;