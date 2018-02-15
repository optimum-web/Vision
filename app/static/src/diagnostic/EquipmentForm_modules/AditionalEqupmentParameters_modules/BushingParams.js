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


var BushingParams = React.createClass({
    getInitialState: function () {
        return {
            'phase_number':'',
            'sealed':'',
            'winding':'',
            'model':'',
            'kw':'',
            'current_rating':'',
            'fluid_volume':'',
            'bushing_manufacturer_h1':'',
            'bushing_manufacturer_h2':'',
            'bushing_manufacturer_h3':'',
            'bushing_manufacturer_hn':'',
            'bushing_manufacturer_x1':'',
            'bushing_manufacturer_x2':'',
            'bushing_manufacturer_x3':'',
            'bushing_manufacturer_xn':'',
            'bushing_manufacturer_t1':'',
            'bushing_manufacturer_t2':'',
            'bushing_manufacturer_t3':'',
            'bushing_manufacturer_tn':'',
            'bushing_manufacturer_q1':'',
            'bushing_manufacturer_q2':'',
            'bushing_manufacturer_q3':'',
            'bushing_manufacturer_qn':'',
            'bushing_type_h':'',
            'bushing_type_hn':'',
            'bushing_type_x':'',
            'bushing_type_xn':'',
            'bushing_type_t':'',
            'bushing_type_tn':'',
            'bushing_type_q':'',
            'bushing_type_qn':'',
            'c1':'',
            'c1pf':'',
            'c2':'',
            'c2pf':'',
            'bil':'',
            'id':'',
            errors: {}

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
                    <div className="col-md-2">
                        <TextField onChange={this.handleChange}
                                   label="Fluid Volume"
                                   name="fluid_volume"
                                   value={this.state.fluid_volume}
                                   errors={errors}
                                   data-type="float"/>
                    </div>
                    <div className="col-md-2">
                        <SelectField
                            source="fluid_type"
                            label="Fluid Type"
                            name="fluid_type_id"
                            value={this.state.fluid_type_id}
                            errors={errors}/>
                    </div>
                    <div className="col-md-2">
                        <TextField onChange={this.handleChange}
                                   label="Voltage"
                                   name="kv"
                                   value={this.state.kv}
                                   errors={errors}
                                   data-type="float"/>
                    </div>
                    <div className="col-md-2">
                        <TextField onChange={this.handleChange}
                                   label="C1"
                                   name="c1"
                                   value={this.state.c1}
                                   errors={errors}
                                   data-type="float"/>
                    </div>
                    <div className="col-md-4">
                        <TextField onChange={this.handleChange}
                                   label="Model"
                                   name="model"
                                   value={this.state.model}
                                   errors={errors}
                                   data-len="50"/>
                    </div>
                </div>

                <div className="row">
                    <div className="col-md-2">
                        <TextField onChange={this.handleChange}
                                   label="C1PF"
                                   name="c1pf"
                                   value={this.state.c1pf}
                                   errors={errors}
                                   data-type="float"/>
                    </div>
                    <div className="col-md-2">
                        <TextField onChange={this.handleChange}
                                   label="C2"
                                   name="c2"
                                   value={this.state.c2}
                                   errors={errors}
                                   data-type="float"/>
                    </div>
                    <div className="col-md-2">
                        <TextField onChange={this.handleChange}
                                   label="C2PF"
                                   name="c2pf"
                                   value={this.state.c2pf}
                                   errors={errors}
                                   data-type="float"/>
                    </div>
                    <div className="col-md-2">
                        <TextField onChange={this.handleChange}
                                   label="Current"
                                   name="current_rating"
                                   value={this.state.current_rating}
                                   errors={errors}
                                   data-type="int"/>
                    </div>
                    <div className="col-md-2">
                        <TextField onChange={this.handleChange}
                                   label="BIL"
                                   name="bil"
                                   value={this.state.bil}
                                   errors={errors}
                                   data-type="int"
                                   data-len="8"/>
                    </div>
                    <div className="col-md-1 ">
                        <Checkbox name="sealed" checked={this.state.sealed} onChange={this.handleChange}><b>Sealed</b></Checkbox>
                    </div>
                </div>
            </div>
        )
    }
});

export default BushingParams;
