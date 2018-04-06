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
        var choice = (this.props["data-choice"] != null) ? this.props["data-choice"]: undefined;
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
                                 data-choice={choice}
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
    handleChange: function (e) {
        this.props.onChange(e);
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
        var required = this.props.required ? this.props.required : null;
        var menuItems = [];
        if (name == "gassensor_id"){
            menuItems.push(<option key="0" value="0">None</option>);
        }
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
                             required={required}
                >
                    <option value="">{required ? this.props.label + " *" : this.props.label}</option>);
                    {menuItems}
                </FormControl>
                <HelpBlock className="warning">{error}</HelpBlock>
            </FormGroup>
        );
    }
});

var StandartSelectField = React.createClass({
    handleChange: function (e) {
        this.props.onChange(e);
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
        var required = this.props.required ? this.props.required : null;
        var menuItems = [];
        
        for (var key in this.props.values) {
            menuItems.push(<option key={this.props.values[key]}
                                   value={this.props.values[key]}>{`${this.props.values[key]}`}</option>);
        }
        return (
            <FormGroup validationState={validationState}>
                <ControlLabel>{label}</ControlLabel>
                <FormControl componentClass="select"
                             onChange={this.handleChange}
                             value={value}
                             name={name}
                             required={required}
                >
                    <option value="">{required ? this.props.label + " *" : this.props.label}</option>);
                    {menuItems}
                </FormControl>
                <HelpBlock className="warning">{error}</HelpBlock>
            </FormGroup>
        );
    }
});

var WindingField = React.createClass({
    handleChange: function (e) {
        this.props.onChange(e);
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
        var items = [];
        items.push("Alumminum")
        items.push("Copper")
        this.setState({"items" : items})
    },
    componentWillUnmount: function () {
        
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
        var required = this.props.required ? this.props.required : null;
        var menuItems = [];
        
        for (var key in this.state.items) {
            menuItems.push(<option key={this.state.items[key]}
                                   value={this.state.items[key]}>{`${this.state.items[key]}`}</option>);
        }
        return (
            <FormGroup validationState={validationState}>
                <ControlLabel>{label}</ControlLabel>
                <FormControl componentClass="select"
                             onChange={this.handleChange}
                             value={value}
                             name={name}
                             required={required}
                >
                    {menuItems}
                </FormControl>
                <HelpBlock className="warning">{error}</HelpBlock>
            </FormGroup>
        );
    }
});

var BushSerialSelectField = React.createClass({
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
                                   value={this.state.items[key].id}>{`${this.state.items[key].name}`}</option>);
        }
        return (
            <FormGroup validationState={validationState}>
                <FormControl componentClass="select"
                             onChange={this.handleChange}
                             defaultValue={value}
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

var TransformerParams = React.createClass({

    getInitialState: function () {
        // return {
        //     'phase_number':'', 'threephase':'', 'fluid_volume':'', 'fluid_type_id':'',
        //         'fluid_level_id':'', 'gassensor_id':'', 'bushing_serial1_id':'', 'bushing_serial2_id':'',
        //         'bushing_serial3_id':'', 'bushing_serial4_id':'', 'bushing_serial5_id':'', 'bushing_serial6_id':'',
        //         'bushing_serial7_id':'', 'bushing_serial8_id':'', 'bushing_serial9_id':'', 'bushing_serial10_id':'',
        //         'bushing_serial11_id':'', 'bushing_serial12_id':'', 'mvaforced11':'', 'mvaforced12':'', 'mvaforced13':'',
        //         'mvaforced14':'', 'imp_base1':'', 'imp_base2':'', 'impbasedmva3':'', 'impbasedmva4':'', 'mvaforced21':'', 'mvaforced22':'',
        //         'mvaforced23':'', 'mvaforced24':'', 'mvaactual':'', 'mvaractual':'',
        //         'mwreserve':'', 'mvareserve':'', 'mwultime':'', 'mvarultime':'',
        //         'ratio_tag1':'', 'ratio_tag2':'', 'ratio_tag3':'', 'ratio_tag4':'',
        //         'static_shield1':'', 'static_shield2':'', 'ratio_tag5':'', 'ratio_tag6':'',
        //         'ratio_tag7':'', 'ratio_tag8':'', 'static_shield3':'', 'static_shield4':'',
        //         'bushing_neutral1':'', 'bushing_neutral2':'', 'bushing_neutral3':'', 'bushing_neutral4':'',
        //         'windings':'', 'winding_metal1':'', 'winding_metal2':'', 'winding_metal3':'', 'winding_metal4':'', 'primary_winding_connection':'', 'secondary_winding_connection':'',
        //         'tertiary_winding_connection':'', 'quaternary_winding_connection':'', 'based_transformer_power':'', 'autotransformer':'',
        //         'bil1':'', 'bil2':'', 'ltc1':'', 'ltc2':'',
        //         'first_cooling_stage_power':'', 'second_cooling_stage_power':'',
        //         'bil3':'', 'bil4':'', 'ltc3':'', 'third_cooling_stage_power':'',
        //         'temperature_rise':'', 'cooling_rating':'', 'primary_tension':'', 'secondary_tension':'',
        //         'tertiary_tension':'', 'impedance1':'', 'impedance2':'', 'impedance3':'', 'impedance4':'',
        //         'formula_ratio1':'', 'formula_ratio2':'', 'formula_ratio3':'',
        //         'sealed':'', 'welded_cover':'','id':'',
        //     'errors': {}

        // }
        return {
            "windings":'', "phase_number":'', "static_shield1":'',"static_shield2":'',"cooling_type":'',"cooling_stages":'',
            "fluid_volume":'',"temperature_rise":'',"conservator_type":'',"welded_cover":'',"primary_tension":'',"secondary_tension":'',
            "tertiary_tension":'',"fourth_tension":'',"mvaforced11":'',"mvaforced12":'',"mvaforced13":'',"mvaforced14":'',
            "imp_base1":'',"imp_base2":'',"imp_base3":'',"imp_base4":'',
            "bil1":'',"bil2":'',"bil3":'',"bil4":'', "winding_metal1":'',"winding_metal2":'',"winding_metal3":'',"winding_metal4":'',
            "primary_winding_connection":'',"secondary_winding_connection":'',"tertiary_winding_connection":'',
            "quaternary_winding_connection":'',"bushing_neutral1":'',"bushing_neutral2":'',"bushing_neutral3":'',
            "bushing_neutral4":'',"ltc2":'',"ltc3":'',"ltc1":'','autotransformer':'','id':'',
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
                        <StandartSelectField onChange={this.handleChange}
                                   label="Nbr of Windings"
                                   name="windings"
                                   value={this.state.windings}
                                   errors={errors}
                                   values={[1,2,3,4]}/>
                    </div>

                    <div className="col-md-3">
                        <StandartSelectField onChange={this.handleChange}
                                   label="Nbr of Phases"
                                   name="phase_number"
                                   value={this.state.phase_number}
                                   errors={errors}
                                   values={[1,3,6]}/>
                    </div>
                    <div className="col-md-3">
                        <Checkbox name="static_shield1" checked={this.state.static_shield1} onChange={this.handleChange}><b>Static Shield 1</b></Checkbox>
                    </div>
                    <div className="col-md-3">
                        <Checkbox name="static_shield2" checked={this.state.static_shield2} onChange={this.handleChange}><b>Static Shield 2</b></Checkbox>
                    </div>
                </div>
                <div className="row">
                    <div className="col-md-3">
                        <StandartSelectField
                                label="Cooling type"
                                value={this.state.cooling_type}
                                errors={errors}
                                name="cooling_type"
                                onChange={this.handleChange}
                                values={['ONAN','ONAF','OFAF','ONAN/ONAF', 'ONWF','OFWF']}
                                />
                    </div>

                    <div className="col-md-3">
                        <StandartSelectField onChange={this.handleChange}
                                   label="Cooling stages"
                                   name="cooling_stages"
                                   value={this.state.cooling_stages}
                                   errors={errors}
                                   values={[1,2,3,4]}/>
                    </div>
                    <div className="col-md-3">
                        <TextField onChange={this.handleChange}
                                   label="Fluid Volume"
                                   name="fluid_volume"
                                   value={this.state.fluid_volume}
                                   errors={errors}
                                   data-type="float"/>
                    </div>

                </div>
                <div className="row"> 
                    <div className="col-md-3">
                        <Checkbox name="autotransformer" checked={this.state.autotransformer} onChange={this.handleChange}><b>Autotransformer</b></Checkbox>
                    </div>
                    <div className="col-md-3">
                        <TextField onChange={this.handleChange}
                                   label="Temperature Rise"
                                   name="temperature_rise"
                                   value={this.state.temperature_rise}
                                   errors={errors}
                                   data-type="int"/>
                    </div>
                    <div className="col-md-3">
                        <StandartSelectField onChange={this.handleChange}
                                   label="Conservator type"
                                   name="conservator_type"
                                   value={this.state.conservator_type}
                                   errors={errors}
                                   values={['Open - no dessicant', 'Open - Dessicant', 'Conservator - no dessicant', 'Conservator - dessicant', 'Conservator with membrane', 'Sealed']}/>
                    </div>
                    <div className="col-md-3">
                        <Checkbox name="welded_cover" checked={this.state.welded_cover} onChange={this.handleChange}><b>Welded Cover</b></Checkbox>
                    </div>
                </div>   
                <div className="row">
                    <div className="col-md-3">
                        <TextField onChange={this.handleChange}
                                   label="Voltage 1 (kV)"
                                   name="primary_tension"
                                   value={this.state.primary_tension}
                                   errors={errors}
                                   data-type="float"/>
                    </div>
                    <div className="col-md-3">
                        <TextField onChange={this.handleChange}
                                   label="Voltage 2 (kV)"
                                   name="secondary_tension"
                                   value={this.state.secondary_tension}
                                   errors={errors}
                                   data-type="float"/>
                    </div>
                    <div className="col-md-3">
                        <TextField onChange={this.handleChange}
                                   label="Voltage 3 (kV)"
                                   name="tertiary_tension"
                                   value={this.state.tertiary_tension}
                                   errors={errors}
                                   data-type="float"/>
                    </div>  
                    <div className="col-md-3">
                        <TextField onChange={this.handleChange}
                                   label="Voltage 4 (kV)"
                                   name="fourth_tension"
                                   value={this.state.fourth_tension}
                                   errors={errors}
                                   data-type="float"/>
                    </div>  
                </div>  
                <div className="row">
                    <div className="col-md-3">
                        <TextField onChange={this.handleChange}
                                   label="MVA 1 (MVA)"
                                   name="mvaforced11"
                                   value={this.state.mvaforced11}
                                   errors={errors}
                                   data-type="float"/>
                    </div>
                    <div className="col-md-3">
                        <TextField onChange={this.handleChange}
                                   label="MVA 2 (MVA)"
                                   name="mvaforced12"
                                   value={this.state.mvaforced12}
                                   errors={errors}
                                   data-type="float"/>
                    </div>
                    <div className="col-md-3">
                        <TextField onChange={this.handleChange}
                                   label="MVA 3 (MVA)"
                                   name="mvaforced13"
                                   value={this.state.mvaforced13}
                                   errors={errors}
                                   data-type="float"/>
                    </div>  
                    <div className="col-md-3">
                        <TextField onChange={this.handleChange}
                                   label="MVA 4 (MVA)"
                                   name="mvaforced14"
                                   value={this.state.mvaforced14}
                                   errors={errors}
                                   data-type="float"/>
                    </div>  
                </div>  
                <div className="row">    
                    <div className="col-md-3">
                        <TextField onChange={this.handleChange}
                                   label="Base Impedance 1 (%)"
                                   name="imp_base1"
                                   value={this.state.imp_base1}
                                   errors={errors}
                                   data-type="float"/>
                    </div>
                    <div className="col-md-3">
                        <TextField onChange={this.handleChange}
                                   label="Base Impedance 2 (%)"
                                   name="imp_base2"
                                   value={this.state.imp_base2}
                                   errors={errors}
                                   data-type="float"/>
                    </div>
                    <div className="col-md-3">
                        <TextField onChange={this.handleChange}
                                   label="Base Impedance 3 (%)"
                                   name="imp_base3"
                                   value={this.state.imp_base3}
                                   errors={errors}
                                   data-type="float"/>
                    </div>
                    <div className="col-md-3">
                        <TextField onChange={this.handleChange}
                                   label="Base Impedance 4 (%)"
                                   name="imp_base4"
                                   value={this.state.imp_base4}
                                   errors={errors}
                                   data-type="float"/>
                    </div>
                </div>  
                <div className="row">  
                    <div className="col-md-3">
                        <TextField onChange={this.handleChange}
                                   label="BIL 1 (kV)"
                                   name="bil1"
                                   value={this.state.bil1}
                                   errors={errors}
                                   data-type="float"/>
                    </div>
                    <div className="col-md-3">
                        <TextField onChange={this.handleChange}
                                   label="BIL 2 (kV)"
                                   name="bil2"
                                   value={this.state.bil2}
                                   errors={errors}
                                   data-type="float"/>
                    </div>
                    <div className="col-md-3">
                        <TextField onChange={this.handleChange}
                                   label="BIL 3 (kV)"
                                   name="bil3"
                                   value={this.state.bil3}
                                   errors={errors}
                                   data-type="float"/>
                    </div>
                    <div className="col-md-3">
                        <TextField onChange={this.handleChange}
                                   label="BIL 4 (kV)"
                                   name="bil4"
                                   value={this.state.bil4}
                                   errors={errors}
                                   data-type="float"/>
                    </div>
                </div>  
                <div className="row">    
                    <div className="col-md-3">
                        <WindingField onChange={this.handleChange}
                                   label="Winding metal 1"
                                   name="winding_metal1"
                                   value={this.state.winding_metal1}
                                   errors={errors}/>
                    </div>
                    <div className="col-md-3">
                        <WindingField onChange={this.handleChange}
                                   label="Winding metal 2"
                                   name="winding_metal2"
                                   value={this.state.winding_metal2}
                                   errors={errors}/>
                    </div>
                    <div className="col-md-3">
                        <WindingField onChange={this.handleChange}
                                   label="Winding metal 3"
                                   name="winding_metal3"
                                   value={this.state.winding_metal3}
                                   errors={errors}/>
                    </div>
                    <div className="col-md-3">
                        <WindingField onChange={this.handleChange}
                                   label="Winding metal 4"
                                   name="winding_metal4"
                                   value={this.state.winding_metal4}
                                   errors={errors}/>
                    </div>
                </div>  
                <div className="row">    
                    <div className="col-md-3">
                        <StandartSelectField onChange={this.handleChange}
                                   label="Connection 1"
                                   name="primary_winding_connection"
                                   value={this.state.primary_winding_connection}
                                   errors={errors}
                                   values={['Delta', 'Wye', 'ZigZag', 'T (Scott)']}
                                   />
                    </div>
                    <div className="col-md-3">
                    <StandartSelectField onChange={this.handleChange}
                                   label="Connection 2"
                                   name="secondary_winding_connection"
                                   value={this.state.secondary_winding_connection}
                                   errors={errors}
                                   values={['Delta', 'Wye', 'ZigZag', 'T (Scott)']}/>
                    </div>
                    <div className="col-md-3">
                    <StandartSelectField onChange={this.handleChange}
                                   label="Connection 3"
                                   name="tertiary_winding_connection"
                                   value={this.state.tertiary_winding_connection}
                                   errors={errors}
                                   values={['Delta', 'Wye', 'ZigZag', 'T (Scott)']}/>
                    </div>
                    <div className="col-md-3">
                    <StandartSelectField onChange={this.handleChange}
                                   label="Connection 4"
                                   name="quaternary_winding_connection"
                                   value={this.state.quaternary_winding_connection}
                                   errors={errors}
                                   values={['Delta', 'Wye', 'ZigZag', 'T (Scott)']}/>
                    </div>
                </div>  
                <div className="row">
                    <div className="col-md-3">
                        <TextField onChange={this.handleChange}
                                   label="Bushing Neutral 1"
                                   name="bushing_neutral1"
                                   value={this.state.bushing_neutral1}
                                   errors={errors}
                                   data-type="float"/>
                    </div>
                    <div className="col-md-3">
                        <TextField onChange={this.handleChange}
                                   label="Bushing Neutral 2"
                                   name="bushing_neutral2"
                                   value={this.state.bushing_neutral2}
                                   errors={errors}
                                   data-type="float"/>
                    </div>
                    <div className="col-md-3">
                        <TextField onChange={this.handleChange}
                                   label="Bushing Neutral 3"
                                   name="bushing_neutral3"
                                   value={this.state.bushing_neutral3}
                                   errors={errors}
                                   data-type="float"/>
                    </div>
                    <div className="col-md-3">
                        <TextField onChange={this.handleChange}
                                   label="Bushing Neutral 4"
                                   name="bushing_neutral4"
                                   value={this.state.bushing_neutral4}
                                   errors={errors}
                                   data-type="float"/>
                    </div>
                    
                </div>  
                <div className="row">
                    <div className="col-md-3">
                        <TextField onChange={this.handleChange}
                                   label="DETC Tap Nbr"
                                   name="ltc2"
                                   value={this.state.ltc2}
                                   errors={errors}
                                   data-type="float"/>
                    </div>
                    <div className="col-md-3">
                        <TextField onChange={this.handleChange}
                                   label="NLTC Tap NBR"
                                   name="ltc3"
                                   value={this.state.ltc3}
                                   errors={errors}
                                   data-type="float"/>
                    </div>
                    <div className="col-md-3">
                        <TextField onChange={this.handleChange}
                                   label="OLTC Tap Nbr"
                                   name="ltc1"
                                   value={this.state.ltc1}
                                   errors={errors}
                                   data-type="float"/>
                    </div>
                    
                </div>  
                  
                {/*
                <div className="row">    
                    
                    <div className="col-md-2">
                        <SelectField
                            source="fluid_type"
                            label="Fluid Type"
                            value={this.state.fluid_type_id}
                            errors={errors}
                            name="fluid_type_id"
                            required={(this.props.edited)}/>
                    </div>
                   <div className="col-md-2">
                        <SelectField
                            source="fluid_level"
                            label="Fluid Level"
                            value={this.state.fluid_level_id}
                            errors={errors}
                            name="fluid_level_id"/>
                    </div>
                    <div className="col-md-2">
                        <SelectField onChange={this.handleChange}
                            source="gas_sensor"
                            label="Gas Sensor"
                            value={this.state.gassensor_id}
                            errors={errors}
                            name="gassensor_id"
                            required={(this.props.edited)}/>
                    </div>
                </div>
                <div className="row">
                    <div className="col-md-2">
                        <BushSerialSelectField
                            source="bushing"
                            label="Bushing Serial 1"
                            value={this.state.bushing_serial1_id}
                            errors={errors}
                            name="bushing_serial1_id"/>
                    </div>
                    <div className="col-md-2">
                        <BushSerialSelectField
                            source="bushing"
                            label="Bushing Serial 2"
                            value={this.state.bushing_serial2_id}
                            errors={errors}
                            name="bushing_serial2_id"/>
                    </div>
                    <div className="col-md-2">
                        <BushSerialSelectField
                            source="bushing"
                            label="Bushing Serial 3"
                            value={this.state.bushing_serial3_id}
                            errors={errors}
                            name="bushing_serial3_id"/>
                    </div>
                    <div className="col-md-2">
                        <BushSerialSelectField
                            source="bushing"
                            label="Bushing Serial 4"
                            value={this.state.bushing_serial4}
                            errors={errors}
                            name="bushing_serial4_id"/>
                    </div>
                    <div className="col-md-2">
                        <BushSerialSelectField
                            source="bushing"
                            label="Bushing Serial 5"
                            value={this.state.bushing_serial5_id}
                            errors={errors}
                            name="bushing_serial5_id"/>
                    </div>
                    <div className="col-md-2">
                        <BushSerialSelectField
                            source="bushing"
                            label="Bushing Serial 1"
                            value={this.state.bushing_serial6_id}
                            errors={errors}
                            name="bushing_serial6_id"/>
                    </div>
                </div>
                <div className="row">
                    <div className="col-md-2">
                        <BushSerialSelectField
                            source="bushing"
                            label="Bushing Serial 7"
                            value={this.state.bushing_serial7}
                            errors={errors}
                            name="bushing_serial7_id"/>
                    </div>
                    <div className="col-md-2">
                        <BushSerialSelectField
                            source="bushing"
                            label="Bushing Serial 8"
                            value={this.state.bushing_serial8_id}
                            errors={errors}
                            name="bushing_serial8_id"/>
                    </div>
                    <div className="col-md-2">
                        <BushSerialSelectField
                            source="bushing"
                            label="Bushing Serial 9"
                            value={this.state.bushing_serial9_id}
                            errors={errors}
                            name="bushing_serial9_id"/>
                    </div>
                    <div className="col-md-2">
                        <BushSerialSelectField
                            source="bushing"
                            label="Bushing Serial 10"
                            value={this.state.bushing_serial10_id}
                            errors={errors}
                            name="bushing_serial10_id"/>
                    </div>
                    <div className="col-md-2">
                        <BushSerialSelectField
                            source="bushing"
                            label="Bushing Serial 11"
                            value={this.state.bushing_serial11_id}
                            errors={errors}
                            name="bushing_serial11_id"/>
                    </div>
                    <div className="col-md-2">
                        <BushSerialSelectField
                            source="bushing"
                            label="Bushing Serial 12"
                            value={this.state.bushing_serial12_id}
                            errors={errors}
                            name="bushing_serial12_id"/>
                    </div>
                </div>
                <div className="row">
                    <div className="col-md-2">
                        <TextField onChange={this.handleChange}
                                   label="Mva Forced 11"
                                   name="mvaforced11"
                                   value={this.state.mvaforced11}
                                   errors={errors}
                                   data-type="float"/>
                    </div>
                    <div className="col-md-2">
                        <TextField onChange={this.handleChange}
                                   label="Mva Forced 12"
                                   name="mvaforced12"
                                   value={this.state.mvaforced12}
                                   errors={errors}
                                   data-type="float"/>
                    </div>
                    <div className="col-md-2">
                        <TextField onChange={this.handleChange}
                                   label="Mva Forced 13"
                                   name="mvaforced13"
                                   value={this.state.mvaforced13}
                                   errors={errors}
                                   data-type="float"/>
                    </div>
                    <div className="col-md-2">
                        <TextField onChange={this.handleChange}
                                   label="Mva Forced 14"
                                   name="mvaforced14"
                                   value={this.state.mvaforced14}
                                   errors={errors}
                                   data-type="float"/>
                    </div>
                    
                </div>
                <div className="row">
                    <div className="col-md-2">
                        <TextField onChange={this.handleChange}
                                   label="Mva Forced 21"
                                   name="mvaforced21"
                                   value={this.state.mvaforced21}
                                   errors={errors}
                                   data-type="float"/>
                    </div>
                    <div className="col-md-2">
                        <TextField onChange={this.handleChange}
                                   label="Mva Forced 22"
                                   name="mvaforced22"
                                   value={this.state.mvaforced22}
                                   errors={errors}
                                   data-type="float"/>
                    </div>
                    <div className="col-md-2">
                        <TextField onChange={this.handleChange}
                                   label="Mva Forced 23"
                                   name="mvaforced23"
                                   value={this.state.mvaforced23}
                                   errors={errors}
                                   data-type="float"/>
                    </div>
                    <div className="col-md-2">
                        <TextField onChange={this.handleChange}
                                   label="Mva Forced 24"
                                   name="mvaforced24"
                                   value={this.state.mvaforced24}
                                   errors={errors}
                                   data-type="float"/>
                    </div>
                    
                </div>
                <div className="row">
                    <div className="col-md-2">
                        <TextField onChange={this.handleChange}
                                   label="Mva Actual"
                                   name="mvaactual"
                                   value={this.state.mvaactual}
                                   errors={errors}
                                   data-type="float"/>
                    </div>
                    <div className="col-md-2">
                        <TextField onChange={this.handleChange}
                                   label="MVAr Actual"
                                   name="mvaractual"
                                   value={this.state.mvaractual}
                                   errors={errors}
                                   data-type="float"/>
                    </div>
                    <div className="col-md-2">
                        <TextField onChange={this.handleChange}
                                   label="Reserve Me"
                                   name="mwreserve"
                                   value={this.state.mwreserve}
                                   errors={errors}
                                   data-type="float"/>
                    </div>
                    <div className="col-md-2">
                        <TextField onChange={this.handleChange}
                                   label="Reserve Mva"
                                   name="mvarreserve"
                                   value={this.state.mvarreserve}
                                   errors={errors}
                                   data-type="float"/>
                    </div>
                    <div className="col-md-2">
                        <TextField onChange={this.handleChange}
                                   label="Ultime Me"
                                   name="mwultime"
                                   value={this.state.mwultime}
                                   errors={errors}
                                   data-type="float"/>
                    </div>
                    <div className="col-md-2">
                        <TextField onChange={this.handleChange}
                                   label="Ultime MVAr"
                                   name="mvarultime"
                                   value={this.state.mvarultime}
                                   errors={errors}
                                   data-type="float"/>
                    </div>
                </div>
                <div className="row">
                    <div className="col-md-2">
                        <TextField onChange={this.handleChange}
                                   label="Ratio Tag 1"
                                   name="ratio_tag1"
                                   value={this.state.ratio_tag1}
                                   errors={errors}
                                   data-len="20"/>
                    </div>
                    <div className="col-md-2">
                        <TextField onChange={this.handleChange}
                                   label="Ratio Tag 2"
                                   name="ratio_tag2"
                                   value={this.state.ratio_tag2}
                                   errors={errors}
                                   data-len="20"/>
                    </div>
                    <div className="col-md-2">
                        <TextField onChange={this.handleChange}
                                   label="Ratio Tag 3"
                                   name="ratio_tag3"
                                   value={this.state.ratio_tag3}
                                   errors={errors}
                                   data-len="20"/>
                    </div>
                    <div className="col-md-2">
                        <TextField onChange={this.handleChange}
                                   label="Ratio Tag 4"
                                   name="ratio_tag4"
                                   value={this.state.ratio_tag4}
                                   errors={errors}
                                   data-len="20"/>
                    </div>

                    
                </div>
                <div className="row">
                    <div className="col-md-2">
                        <TextField onChange={this.handleChange}
                                   label="Ratio Tag 5"
                                   name="ratio_tag5"
                                   value={this.state.ratio_tag5}
                                   errors={errors}
                                   data-len="20"/>
                    </div>
                    <div className="col-md-2">
                        <TextField onChange={this.handleChange}
                                   label="Ratio Tag 6"
                                   name="ratio_tag6"
                                   value={this.state.ratio_tag6}
                                   errors={errors}
                                   data-len="20"/>
                    </div>
                    <div className="col-md-2">
                        <TextField onChange={this.handleChange}
                                   label="Ratio Tag 7"
                                   name="ratio_tag7"
                                   value={this.state.ratio_tag7}
                                   errors={errors}
                                   data-len="20"/>
                    </div>
                    <div className="col-md-2">
                        <TextField onChange={this.handleChange}
                                   label="Ratio Tag 8"
                                   name="ratio_tag8"
                                   value={this.state.ratio_tag8}
                                   errors={errors}
                                   data-len="20"/>
                    </div>
                    <div className="col-md-2">
                        <Checkbox name="static_shield3" checked={this.state.static_shield3} onChange={this.handleChange}><b>Static Shield 3</b></Checkbox>
                    </div>
                    <div className="col-md-2">
                        <TextField onChange={this.handleChange}
                                   label="Static Shield 4"
                                   name="static_shield4"
                                   value={this.state.static_shield4}
                                   errors={errors}
                                   data-type="float"/>
                    </div>
                </div>
                <div className="row">
                    
                    <div className="col-md-2">
                        <TextField onChange={this.handleChange}
                                   label="Based Power"
                                   name="based_transformer_power"
                                   value={this.state.based_transformer_power}
                                   errors={errors}
                                   data-type="float"/>
                    </div>
                    
                </div>
                <div className="row">
                    
                    <div className="col-md-2">
                        <TextField onChange={this.handleChange}
                                   label="First Cooling Stage Power"
                                   name="first_cooling_stage_power"
                                   value={this.state.first_cooling_stage_power}
                                   errors={errors}
                                   data-type="float"/>
                    </div>
                    <div className="col-md-2">
                        <TextField onChange={this.handleChange}
                                   label="Second Cooling Stage Power"
                                   name="second_cooling_stage_power"
                                   value={this.state.second_cooling_stage_power}
                                   errors={errors}
                                   data-type="float"/>
                    </div>
                </div>
                <div className="row">
                    
                    <div className="col-md-2">
                        <TextField onChange={this.handleChange}
                                   label="LTC 3"
                                   name="ltc3"
                                   value={this.state.ltc3}
                                   errors={errors}
                                   data-type="float"/>
                    </div>
                    <div className="col-md-2">
                        <TextField onChange={this.handleChange}
                                   label="Third colling stage power"
                                   name="third_cooling_stage_power"
                                   value={this.state.third_cooling_stage_power}
                                   errors={errors}
                                   data-type="float"/>
                    </div>
                    
                    <div className="col-md-2">
                        <TextField onChange={this.handleChange}
                                   label="Cooling Rating"
                                   name="cooling_rating"
                                   value={this.state.cooling_rating}
                                   errors={errors}
                                   data-type="int"/>
                    </div>
                </div>
                <div className="row">
                    
                    <div className="col-md-2">
                        <TextField onChange={this.handleChange}
                                   label="Impedance 1"
                                   name="impedance1"
                                   value={this.state.impedance1}
                                   errors={errors}
                                   data-type="float"/>
                    </div>
                    <div className="col-md-2">
                        <TextField onChange={this.handleChange}
                                   label="Impedance 2"
                                   name="impedance2"
                                   value={this.state.impedance2}
                                   errors={errors}
                                   data-type="float"/>
                    </div>
                    <div className="col-md-2">
                        <TextField onChange={this.handleChange}
                                   label="Impedance 3"
                                   name="impedance3"
                                   value={this.state.impedance3}
                                   errors={errors}
                                   data-type="float"/>
                    </div>
                </div>
                <div className="row">
                    <div className="col-md-2">
                        <TextField onChange={this.handleChange}
                                   label="Formula Ratio 1"
                                   name="formula_ratio"
                                   value={this.state.formula_ratio}
                                   errors={errors}
                                   data-type="int"/>
                    </div>
                    <div className="col-md-2">
                        <TextField onChange={this.handleChange}
                                   label="Formula Ratio 2"
                                   name="formula_ratio2"
                                   value={this.state.formula_ratio2}
                                   errors={errors}
                                   data-type="int"/>
                    </div>
                    <div className="col-md-2">
                        <TextField onChange={this.handleChange}
                                   label="Formula Ratio 3"
                                   name="formula_ratio3"
                                   value={this.state.formula_ratio3}
                                   errors={errors}
                                   data-type="float"/>
                    </div>
                    <div className="col-md-2 ">
                        <Checkbox name="sealed" checked={this.state.sealed} onChange={this.handleChange}><b>Sealed</b></Checkbox>
                    </div>
                    
                    <div className="col-md-2">
                        <TextField onChange={this.handleChange}
                                   label="Impedance 4"
                                   name="impedance4"
                                   value={this.state.impedance4}
                                   errors={errors}
                                   data-type="float"/>
                    </div>
                </div>
                 */}
            </div>
        )
    }
});


export default TransformerParams;