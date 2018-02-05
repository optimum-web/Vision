import React from 'react';
import injectTapEventPlugin from "react-tap-event-plugin";
import {BootstrapTable, TableHeaderColumn} from 'react-bootstrap-table';
import FormControl from 'react-bootstrap/lib/FormControl';
import FormGroup from 'react-bootstrap/lib/FormGroup';
import ControlLabel from 'react-bootstrap/lib/ControlLabel';
import Button from 'react-bootstrap/lib/Button';
import Checkbox from 'react-bootstrap/lib/Checkbox';
import DateTimeField from 'react-bootstrap-datetimepicker/lib/DateTimeField'
import Panel from 'react-bootstrap/lib/Panel';
import Modal from 'react-bootstrap/lib/Modal';
import NewManufacturerForm from './EquipmentForm_modules/NewManufacturerForm';
import NewLocationForm from './EquipmentForm_modules/NewLocationForm';
import NewNormForm from './EquipmentForm_modules/NewNormForm';
import NewEquipmentTypeForm from './EquipmentForm_modules/NewEquipmentTypeForm';
import CreatedByForm from './CampaignForm_modules/NewUserForm';
import HelpBlock from 'react-bootstrap/lib/HelpBlock';
import {NotificationContainer, NotificationManager} from 'react-notifications';
import {DATETIMEPICKER_FORMAT} from './appConstants.js';

import AirBreakerParams from './EquipmentForm_modules/AditionalEqupmentParameters_modules/AirBreakerParams';
import BushingParams  from './EquipmentForm_modules/AditionalEqupmentParameters_modules/BushingParams';
import CapacitorParams from './EquipmentForm_modules/AditionalEqupmentParameters_modules/CapacitorParams';
import BreakerParams from './EquipmentForm_modules/AditionalEqupmentParameters_modules/BreakerParams';
import PowerSourceParams from './EquipmentForm_modules/AditionalEqupmentParameters_modules/PowerSourceParams';
import CableParams from './EquipmentForm_modules/AditionalEqupmentParameters_modules/CableParams';
import SwitchGearParams from './EquipmentForm_modules/AditionalEqupmentParameters_modules/SwitchGearParams';
import InductionMachineParams from './EquipmentForm_modules/AditionalEqupmentParameters_modules/InductionMachineParams';
import SyncroMachineParams from './EquipmentForm_modules/AditionalEqupmentParameters_modules/SyncroMachineParams';
import TapChangerParams from './EquipmentForm_modules/AditionalEqupmentParameters_modules/TapChangerParams';
import RectifierParams from './EquipmentForm_modules/AditionalEqupmentParameters_modules/RectifierParams';
import TransformerParams from './EquipmentForm_modules/AditionalEqupmentParameters_modules/TransformerParams';
import TankParams from './EquipmentForm_modules/AditionalEqupmentParameters_modules/TankParams';
import SwitchParams from './EquipmentForm_modules/AditionalEqupmentParameters_modules/SwitchParams';
import InductanceParams from './EquipmentForm_modules/AditionalEqupmentParameters_modules/InductanceParams';
import GasSensorParams from './EquipmentForm_modules/AditionalEqupmentParameters_modules/GasSensorParams';

import NewNormFuranForm from './Norm_modules/NewNormFuranForm';
import NewNormGasForm from './Norm_modules/NewNormGasForm';
import NewNormIsolationForm from './Norm_modules/NewNormIsolationForm';
import NewNormPhysicForm from './Norm_modules/NewNormPhysicForm';
import NewNormParticlesForm from './Norm_modules/NewNormParticlesForm';

import {findDOMNode} from 'react-dom';
injectTapEventPlugin();

var options = [];
var items = [];

var first_year = 1900;
var current_date = new Date();
var current_year = current_date.getFullYear();
var year_array = [];
year_array.push(first_year);
while (first_year != current_year) {
    first_year++;
    year_array.push(first_year.toString());
}


var EquipmentTypeSelectField = React.createClass({

    handleChange: function (event, index, value) {
        this.setState({
            value: event.target.value

        });
    },

    getInitialState: function () {
        return {
            items: [],
            isVisible: false
        };
    },

    isVisible: function () {
        return this.state.isVisible;
    },

    componentDidMount: function () {
        this.serverRequest = $.authorizedGet(this.props.source, function (result) {

            items = (result['result']);
            this.setState({
                items: items
            });
        }.bind(this), 'json');

    },

    componentWillUnmount: function () {
        this.serverRequest.abort();
    },

    setVisible: function () {
        this.state.isVisible = true;
    },

    render: function () {
        var menuItems = [];
        for (var key in this.state.items) {
            menuItems.push(<option key={this.state.items[key].id}
                                   value={this.state.items[key].id}
                                   accessKey={this.state.items[key].table_name}
            >{`${this.state.items[key].name}`}</option>);

        }
        return (
            <div>
                <FormGroup controlId="formControlsSelect1"
                           validationState={this.props.errors.equipment_type_id ? 'error' : null}>
                    <FormControl
                        componentClass="select"
                        name="equipment_type_id"
                        placeholder="Equipment type"
                        onChange={this.handleChange}
                        required={this.props.required}
                        disabled={this.props.readonly}
                        value={this.props.value}>
                        <option value="">Choose equipment type{this.props.required ? " *" : ""}</option>
                        {menuItems}
                    </FormControl>
                    <HelpBlock className="warning">{this.props.errors.equipment_type_id}</HelpBlock>
                </FormGroup>
            </div>
        );
    }
});


var EquipmentSelectField = React.createClass({

    getInitialState: function () {
        return {
            items: []
        };
    },

    handleChange: function (event, index, value) {

        this.setState({
            value: event.target.value
        })
    },

    componentDidMount: function () {
        this.serverRequest = $.authorizedGet(this.props.source, function (result) {
            var items = (result['result']);
            this.setState({
                items: items
            });
        }.bind(this), 'json');
    },

    componentWillUnmount: function () {
        this.serverRequest.abort();
    },

    removeSelect: function () {
        this.props.removeSelect(this.props.index);
    },

    getSelected: function () {
        return this.state.selected || this.state.value;
    },

    setSelected: function (selected) {
        this.setState({
            selected: selected
        })
    },

    render: function () {
        var menuItems = [];
        for (var key in this.state.items) {
            menuItems.push(
                <option key={this.state.items[key].id}
                        value={this.state.items[key].id}>
                    {`${this.state.items[key].name} ${this.state.items[key].serial}`}
                </option>
            );
        }

        return (
            <div>
                <FormGroup validationState={this.props.errors.equipment_id ? 'error' : null}>
                    <FormControl
                        componentClass="select"
                        placeholder="Select equipment in upstream"
                        name="equipment_id"
                        onChange={this.handleChange}
                        value={this.props.value}>
                        <option value="">Choose equipment in upstream</option>
                        {menuItems}
                    </FormControl>
                    <HelpBlock className="warning">{this.props.errors.equipment_id}</HelpBlock>
                </FormGroup>
            </div>
        );
    }
});


var ManufacturerSelectField = React.createClass({

    handleChange: function (event, index, value) {
        this.setState({
            value: event.target.value
        })
    },

    getInitialState: function () {
        return {
            items: [],
            isVisible: false
        };
    },

    isVisible: function () {
        return this.state.isVisible;
    },

    componentDidMount: function () {
        this.serverRequest = $.authorizedGet(this.props.source, function (result) {

            items = (result['result']);
            this.setState({
                items: items
            });
        }.bind(this), 'json');
    },

    componentWillUnmount: function () {
        this.serverRequest.abort();
    },

    setVisible: function () {
        this.state.isVisible = true;
    },

    render: function () {
        var menuItems = [];
        for (var key in this.state.items) {
            menuItems.push(<option key={this.state.items[key].id}
                                   value={this.state.items[key].id}>{`${this.state.items[key].name}`}</option>);
        }
        return (
            <div>
                <FormGroup controlId="formControlsSelect2"
                           validationState={this.props.errors.manufacturer_id ? 'error' : null}>
                    <ControlLabel>Manufacturer</ControlLabel>
                    <FormControl
                        name="manufacturer_id"
                        componentClass="select"
                        placeholder="Manufacturer"
                        onChange={this.handleChange}
                        value={this.props.value}>
                        <option value="">Choose manufacturer</option>
                        {menuItems}
                    </FormControl>
                    <HelpBlock className="warning">{this.props.errors.manufacturer_id}</HelpBlock>
                </FormGroup>
            </div>
        );
    }
});


var LocationSelectField = React.createClass({

    handleChange: function (event, index, value) {
        this.setState({
            value: event.target.value,
        })

    },

    getInitialState: function () {
        return {
            items: [],
            isVisible: false
        };
    },

    isVisible: function () {
        return this.state.isVisible;
    },

    componentDidMount: function () {
        this.serverRequest = $.authorizedGet(this.props.source, function (result) {

            items = (result['result']);
            this.setState({
                items: items
            });
        }.bind(this), 'json');
    },

    componentWillUnmount: function () {
        this.serverRequest.abort();
    },

    setVisible: function () {
        this.state.isVisible = true;
    },

    render: function () {
        var menuItems = [];
        for (var key in this.state.items) {
            menuItems.push(<option key={this.state.items[key].id}
                                   value={this.state.items[key].id}>{`${this.state.items[key].name}`}</option>);
        }

        return (
            <div>
                <FormGroup controlId="formControlsSelect3"
                           validationState={this.props.errors.location_id ? 'error' : null}>
                    <ControlLabel>Select location</ControlLabel>
                    <FormControl
                        name="location_id"
                        componentClass="select"
                        placeholder="Select location"
                        onChange={this.handleChange}
                        required={this.props.required}
                        value={this.props.value}>
                        <option value="">Select equipment location{this.props.required ? " *" : ""}</option>
                        {menuItems}
                    </FormControl>
                    <HelpBlock className="warning">{this.props.errors.location_id}</HelpBlock>
                </FormGroup>
            </div>
        );
    }
});



var AssignedToSelectField = React.createClass({

    handleChange: function (event, index, value) {
        this.setState({
            value: event.target.value
        })
    },

    getInitialState: function () {
        return {
            items: [],
            isVisible: false
        };
    },

    isVisible: function () {
        return this.state.isVisible;
    },

    componentDidMount: function () {
        this.serverRequest = $.authorizedGet(this.props.source, function (result) {

            items = (result['result']);
            this.setState({
                items: items
            });
        }.bind(this), 'json');
    },

    componentWillUnmount: function () {
        this.serverRequest.abort();
    },

    setVisible: function () {
        this.state.isVisible = true;
    },

    render: function () {
        var menuItems = [];
        for (var key in this.state.items) {
            menuItems.push(<option value={this.state.items[key].id}
                                   key={this.state.items[key].id}>{`${this.state.items[key].name}`}</option>);
        }

        return (
            <div>
                <FormGroup controlId="formControlsSelect5"
                           validationState={this.props.errors.assigned_to_id ? 'error' : null}>
                    <ControlLabel>Assigned to</ControlLabel>
                    <FormControl
                        componentClass="select"
                        name="assigned_to_id"
                        placeholder="Assigned to"
                        onChange={this.handleChange}
                        required={this.props.required}
                        value={this.props.value}>
                        <option value="">Assign performer{this.props.required ? " *" : ""}</option>
                        {menuItems}
                    </FormControl>
                    <HelpBlock className="warning">{this.props.errors.assigned_to_id}</HelpBlock>
                </FormGroup>
            </div>
        );
    }
});


var NormSelectField = React.createClass({

    //handleChange: function (event, index, value) {
    //    this.setState({
    //        value: event.target.value
    //    })
    //},

    getInitialState: function () {
        return {
            items: [],
            isVisible: false
        };
    },

    isVisible: function () {
        return this.state.isVisible;
    },

    componentDidMount: function () {
        this.serverRequest = $.authorizedGet(this.props.source, function (result) {

            items = (result['result']);
            this.setState({
                items: items
            });
        }.bind(this), 'json');
    },

    componentWillUnmount: function () {
        this.serverRequest.abort();
    },

    setVisible: function () {
        this.state.isVisible = true;
    },

    render: function () {
        var menuItems = [];
        for (var key in this.state.items) {
            var name = this.state.items[key].table_name != 'norm_particles' ? this.state.items[key].table_name : 'particles';
            menuItems.push(<option key={this.state.items[key].id}
                                   className={this.props.errors[name] ? 'text-danger' : ''}
                                   value={this.state.items[key].id}
                                   data-name={name}>{`${this.state.items[key].name}`}</option>);
        }

        return (
            <div>
                <FormGroup controlId="formControlsSelect6"
                           validationState={this.props.errors.norm_id ? 'error' : null}>
                    <ControlLabel>Select norm</ControlLabel>
                    <FormControl
                        name="norm_id"
                        componentClass="select"
                        placeholder="Select norm"
                        onChange={this.props.onChange}
                        required={this.props.required}
                        value={this.props.value}>
                        <option value="">Select norm{this.props.required ? " *" : ""}</option>
                        {menuItems}
                    </FormControl>
                    <HelpBlock className="warning">{this.props.errors.norm_id}</HelpBlock>
                </FormGroup>
            </div>
        );
    }
});

var NormTypeSelectField = React.createClass({
    render: function () {
        return (
            <div>
                <FormGroup controlId="formControlsSelect6"
                           validationState={this.props.errors.norm_type ? 'error' : null}>
                    <ControlLabel>Select norm type</ControlLabel>
                    <FormControl
                        name="norm_type"
                        componentClass="select"
                        placeholder="Select norm type"
                        onChange={this.props.onChange}
                        required={this.props.required}
                        value={this.props.value}>
                        <option value="">Select norm type{this.props.required ? " *" : ""}</option>
                        <option value="standard">Standard</option>
                        <option value="custom">Custom</option>
                    </FormControl>
                    <HelpBlock className="warning">{this.props.errors.norm_type}</HelpBlock>
                </FormGroup>
            </div>
        );
    }
});

var FrequencySelectField = React.createClass({

    handleChange: function (event, index, value) {
        this.setState({
            value: event.target.value
        })

    },

    getInitialState: function () {
        return {
            items: ['25', '50', '60', 'DC'],
            isVisible: false,
            showNewEquipmentTypeForm: false,
            showNewManufacturerForm: false,
            showNewLocationForm: false,
            showAssignToForm: false,
            showNewNormForm: false
        };
    },

    isVisible: function () {
        return this.state.isVisible;
    },

    setVisible: function () {
        this.state.isVisible = true;
    },

    render: function () {
        options = [];
        for (var key in this.state.items) {
            options.push(<option key={this.state.items[key]}
                                 value={this.state.items[key]}>{`${this.state.items[key]}`}</option>);
        }

        return (
            <div>
                <FormGroup controlId="formControlsSelect7"
                           validationState={this.props.errors.frequency ? 'error' : null}>
                    <ControlLabel>Select frequency</ControlLabel>
                    <FormControl componentClass="select"
                                 name="frequency"
                                 placeholder="Select frequency"
                                 onChange={this.handleChange}
                                 value={this.props.value}>
                        <option value="">Choose Frequency</option>
                        {options}
                    </FormControl>
                    <HelpBlock className="warning">{this.props.errors.frequency}</HelpBlock>
                </FormGroup>
            </div>
        );
    }
});


var ManufacturedSelectField = React.createClass({

    handleChange: function (event, index, value) {
        this.setState({
            value: event.target.value
        })
    },

    getInitialState: function () {
        return {
            items: year_array,
            isVisible: false
        };
    },

    isVisible: function () {
        return this.state.isVisible;
    },

    setVisible: function () {
        this.state.isVisible = true;
    },

    render: function () {
        options = [];
        for (var key in this.state.items) {
            options.push(<option key={this.state.items[key]}
                                 value={this.state.items[key]}>{`${this.state.items[key]}`}</option>);
        }

        return (
            <div>
                <FormGroup controlId="formControlsSelect8"
                           validationState={this.props.errors.manufactured ? 'error' : null}>
                    <ControlLabel>Select manufactured date</ControlLabel>
                    <FormControl componentClass="select"
                                 name="manufactured"
                                 placeholder="Select manufactured date"
                                 onChange={this.handleChange}
                                 value={this.props.value}>

                        <option value="">Year manufactured</option>
                        {options}
                    </FormControl>
                    <HelpBlock className="warning">{this.props.errors.manufactured}</HelpBlock>
                </FormGroup>
            </div>
        );
    }
});


var EqAdditionalParams = React.createClass({

    getInitialState: function () {
        return {
            tableName: ''
        }
    },

    render: function () {
        if (typeof this.props.data.option_text == 'undefined') {
            return (<div></div>);
        }
        switch (this.props.data.option_text.text) {
            case 'Air circuit breaker':
                return (<AirBreakerParams errors={this.props.data.errors} equipment_item={this.props.equipment_item} ref="additionalParams"/>);
                break;
            case 'Bushing':
                return (<BushingParams errors={this.props.data.errors} equipment_item={this.props.equipment_item} ref="additionalParams"/>);
                break;
            case 'Capacitor':
                return (<CapacitorParams errors={this.props.data.errors} equipment_item={this.props.equipment_item} ref="additionalParams"/>);
                break;
            case 'Breaker':
                return (<BreakerParams errors={this.props.data.errors} equipment_item={this.props.equipment_item} ref="additionalParams"/>);
                break;
            case 'Power Source':
                return (<PowerSourceParams errors={this.props.data.errors} equipment_item={this.props.equipment_item} ref="additionalParams"/>);
                break;
            case 'Cable':
                return (<CableParams errors={this.props.data.errors} equipment_item={this.props.equipment_item} ref="additionalParams"/>);
                break;
            case 'Switchgear':
                return (<SwitchGearParams errors={this.props.data.errors} equipment_item={this.props.equipment_item} ref="additionalParams"/>);
                break;
            case 'Induction machine':
                return (<InductionMachineParams errors={this.props.data.errors} equipment_item={this.props.equipment_item} ref="additionalParams"/>);
                break;
            case 'Synchronous machine':
                return (<SyncroMachineParams errors={this.props.data.errors} equipment_item={this.props.equipment_item} ref="additionalParams"/>);
                break;
            case 'Tap changer':
                return (<TapChangerParams errors={this.props.data.errors} equipment_item={this.props.equipment_item} ref="additionalParams"/>);
                break;
            case 'Rectifier':
                return (<RectifierParams errors={this.props.data.errors} equipment_item={this.props.equipment_item} ref="additionalParams"/>);
                break;
            case 'Transformer':
                return (<TransformerParams errors={this.props.data.errors} edited={this.props.edited} equipment_item={this.props.equipment_item} ref="additionalParams"/>);
                break;
            case 'Tank':
                return (<TankParams errors={this.props.data.errors} equipment_item={this.props.equipment_item} ref="additionalParams"/>);
                break;
            case 'Switch':
                return (<SwitchParams errors={this.props.data.errors} equipment_item={this.props.equipment_item} ref="additionalParams"/>);
                break;
            case 'Inductance':
                return (<InductanceParams errors={this.props.data.errors} equipment_item={this.props.equipment_item} ref="additionalParams"/>);
                break;
            case 'Gas sensor':
                return (<GasSensorParams errors={this.props.data.errors} equipment_item={this.props.equipment_item} ref="additionalParams"/>);
                break;

            default:
                return null;
        }
    }
});


var NormAdditionalParams = React.createClass({

    getInitialState: function () {
        return {
            errors: {},
            norm_id: '',
            norm_option_text:{},
            norms: {},
            refs: {},
            normsToSave: 0
        }
    },

    onChange: function (e) {
        let state = {};
        let name = e.target[e.target.selectedIndex].getAttribute('data-name')
        state[e.target.name] = e.target.value;
        state['norm_option_text'] = {
            name: name,
            id: e.target.value,
            text: e.target[e.target.selectedIndex].text
        };
        this.setState(state);
    },

    submit: function (equipmentId) {
        if (this.props.data.norm_type == 'custom' && this.state.norm_id) {
            this.setState({normsToSave: Object.keys(this.state.norms).length});
            for (let normName in this.state.norms) {
                this.state.refs[normName]
                    .submit(equipmentId)
                    .done(this.clearForm)
                    .fail(this._onError)
            }
        }
    },

    _onError: function (xhr, ajaxOptions, thrownError) {
        let errors = this.state.errors;
        errors[xhr.normName] = xhr.responseJSON.error;
        this.setState(errors);
        this.state.refs[xhr.normName]._onError(xhr, ajaxOptions, thrownError);
    },

    clearForm: function () {
        // Clear main for after save of the last form
        if (this.state.normsToSave == 1) {
            this.props.clearForm();
        } else {
            let normsToSave = this.state.normsToSave;
            normsToSave--;
            this.setState({normsToSave: normsToSave});
        }
    },

    isValid: function () {
        let isValid = true;
        for (let normName in this.state.norms) {
            if (!this.state.refs[normName].isValid()) {
                isValid = false;
                break;
            }
        }
        return isValid;
    },

    saveNormGlobally: function (norm, state, newErrors) {
        let norms = this.state.norms;
        let errors = this.state.errors;
        let refs = this.state.refs;
        norms[norm] = state;
        if (Object.keys(newErrors).length) {
            errors[norm] = newErrors;
        } else {
            delete errors[norm];
        }
        refs[norm] = this.refs[norm];
        this.setState({norms: norms, errors: errors});
    },

    reload: function() {
        var norm_option_text = this.props.data.norm_option_text;
        this.setState({norm_option_text : norm_option_text , 'errors' : {}})
    },

    render: function () {
        let normSelectField = <NormSelectField
            source="/api/v1.0/norm"
            value={this.state.norm_option_text.id}
            onChange={this.onChange}
            errors={this.state.errors}
            ref="norm_id"
            required/>;

        if (Object.keys(this.state.norm_option_text).length == 0) {
            return (<div className="col-md-4 nopadding">{normSelectField}</div>);
        }

        switch (this.state.norm_option_text.name) {
            case 'norm_furan':
                return (
                    <div>
                        <div className="col-md-12 nopadding">
                            <div className="col-md-4 nopadding">{normSelectField}</div>
                        </div>
                        <div>
                            <NewNormFuranForm
                                ref='norm_furan'
                                data={this.state.norms.norm_furan}
                                errorData={this.state.errors.norm_furan || {}}
                                saveNormGlobally={this.saveNormGlobally}
                                setNormSubformSaved={this.props.setNormSubformSaved}
                                cleanForm={this.props.clearForm} 
                                equipmentId={this.props.data.id} />
                        </div>
                    </div>);
                break;
            case 'norm_gas':
                return (
                    <div>
                        <div className="col-md-12 nopadding">
                            <div className="col-md-4 nopadding">{normSelectField}</div>
                        </div>
                        <div>
                            <NewNormGasForm
                                ref='norm_gas'
                                data={this.state.norms.norm_gas}
                                errorData={this.state.errors.norm_gas || {}}
                                saveNormGlobally={this.saveNormGlobally}
                                setNormSubformSaved={this.props.setNormSubformSaved}
                                cleanForm={this.props.clearForm} 
                                equipmentId={this.props.data.id}/>
                        </div>
                    </div>);
                break;
            case 'norm_isolation':
                return (
                    <div>
                        <div className="col-md-12 nopadding">
                            <div className="col-md-4 nopadding">{normSelectField}</div>
                        </div>
                        <div>
                            <NewNormIsolationForm
                                ref='norm_isolation'
                                data={this.state.norms.norm_isolation}
                                errorData={this.state.errors.norm_isolation || {}}
                                saveNormGlobally={this.saveNormGlobally}
                                setNormSubformSaved={this.props.setNormSubformSaved}
                                cleanForm={this.props.clearForm} 
                                equipmentId={this.props.data.id} />
                        </div>
                    </div>);
                break;
            case 'norm_physic':
                return (
                    <div>
                        <div className="col-md-12 nopadding">
                            <div className="col-md-4 nopadding">{normSelectField}</div>
                        </div>
                        <div>
                            <NewNormPhysicForm
                                ref='norm_physic'
                                data={this.state.norms.norm_physic}
                                errorData={this.state.errors.norm_physic || {}}
                                saveNormGlobally={this.saveNormGlobally}
                                setNormSubformSaved={this.props.setNormSubformSaved}
                                cleanForm={this.props.clearForm} 
                                equipmentId={this.props.data.id}/>
                        </div>
                    </div>);
                break;
            case 'particles':
                return (
                    <div>
                        <div className="col-md-12 nopadding">
                            <div className="col-md-4 nopadding">{normSelectField}</div>
                        </div>
                        <div>
                            <NewNormParticlesForm
                                ref='particles'
                                data={this.state.norms.particles}
                                errorData={this.state.errors.particles || {}}
                                saveNormGlobally={this.saveNormGlobally}
                                setNormSubformSaved={this.props.setNormSubformSaved}
                                cleanForm={this.props.clearForm} 
                                equipmentId={this.props.data.id} />
                        </div>
                    </div>);
                break;
            default:
                return null;
        }
    }
});

const EquipmentForm = React.createClass({

    getInitialState: function () {

        var response = {
            loading: false,
            errors: {},
            subform: {},
            fields: [
                'equipment_type_id',
                'manufacturer_id',
                'location_id',
                'assigned_to_id',
                'name',
                'serial',
                'equipment_number',
                'frequency',
                'description',
                'comments',
                'nbr_of_tap_change_ltc',
                //'upstream1',  // TODO: Exclude upstream field or let adding multiple upstreams
                'phys_position',
                'tension4',
                'manufactured'
            ],
            changedFields: [],
            option_text: {},
            equipmentId: null,   // Is set when main form is saved
            equipmentSubformSaved: false,
            normSubformSaved: false,
            norm_type: ''
        };

        for (var i = 0; i < response.fields.length; i++) {
            response[response.fields[i]] = "";
        }
        return response;
    },

    loadData: function() {
        var equipment = this.props.equipment;
        equipment.equipment_item = this.props.equipment_item;
        
        $.authorizedGet("/api/v1.0/equipment_type", function (result) {
            var option_text = {};
            items = (result['result']);
            
            for (var key in items){
                if(items[key].id == equipment.equipment_type_id){
                    equipment.option_text = {
                        name: "EquipmentTypeSelectField",
                        id: equipment.equipment_type_id,
                        text: items[key].name};
                }
            }
            equipment.errors = {};
            this.setState(equipment);
            this.refs['EqAdditionalParams'].refs['additionalParams'].load();
            this.refs['normAdditionalParams'].reload();
        }.bind(this), 'json');
        

    },

    _save: function () {
        var fields = {};
        var fields_aditional = {};
        for (var key in this.state){
            if (key != "upstream1" && this.state.fields.indexOf(key) > -1) {
                fields[key] = this.state[key];
            }
            
        }
        for (var key in this.refs['EqAdditionalParams'].refs['additionalParams'].state){
            if (Object.keys(this.refs['EqAdditionalParams'].refs['additionalParams'].getInitialState()).indexOf(key) > -1 && key != "errors") {
                fields_aditional[key] = this.refs['EqAdditionalParams'].refs['additionalParams'].state[key];
            }
            
        }
        
        var subform = this.state.subform;
        var data = {};
        var path = this.state.table_name;

        for (var i = 0; i < fields.length; i++) {
            var key = fields[i];
            var value = this.state[key];
            if (value == "") {
                value = null;
            }
            data[key] = value;
        }

        var that = this
            , xhr;

        if (this.state.id){
            xhr = $.authorizedAjax({
                url: '/api/v1.0/equipment/' + that.state.id,
                type: 'POST',
                dataType: 'json',
                contentType: 'application/json',
                data: JSON.stringify(fields),
                success: function (data) {
                    that._saveSubform(fields_aditional, that.state.id, that.state.equipment_type.table_name);
                    that._saveNormAdditionalParams(that.state.id);
                },
                beforeSend: function () {
                    this.setState({loading: true});
                }.bind(this)
            })
        }
        else{
            // If the main form haven't been saved yet
            if (!this.state.equipmentId) {
                xhr = $.authorizedAjax({
                    url: '/api/v1.0/equipment/',
                    type: 'POST',
                    dataType: 'json',
                    contentType: 'application/json',
                    data: JSON.stringify(fields),
                    success: function (data) {
                        that.setState({equipmentId: data['result']});
                        that._saveSubform(subform, data['result'], path);
                        that._saveNormAdditionalParams(data['result']);
                    },
                    beforeSend: function () {
                        this.setState({loading: true});
                    }.bind(this)
                })
            } else {
                // Save only subform (for instance, when saving subform for the first time, API returned errors)
                if (!this.state.equipmentSubformSaved) {
                    xhr = this._saveSubform(subform, this.state.equipmentId, path);
                }
                if (!this.state.normSubformSaved) {
                    xhr = this._saveNormAdditionalParams(this.state.equipmentId);
                }
            }
        }
        return xhr;
    },

    _saveNormAdditionalParams(equipmentId) {
        if (this.state.norm_type == 'custom') {
            this._getNormAdditionalParamsForm().submit(equipmentId);
        } else if (this.state.norm_type == 'standard') {
            this.saveStandardNorm(equipmentId);
        }
    },

    _getNormAdditionalParamsForm(){
        return this.refs.normAdditionalParams;
    },

    saveStandardNorm: function (equipmentId) {
        $.authorizedAjax({
            url: '/api/v1.0/equipment/' + equipmentId + '/norm/',
            type: 'POST',
            dataType: 'json',
            contentType: 'application/json'
        });
    },

    _saveSubform(subform, equipmentId, path){
        var that = this;
        if (Object.keys(subform).length != 0) {
            delete subform.norm_type;
            delete subform.norm_id;
            subform['equipment_id'] = equipmentId;
            for (var field in subform) {
                if (subform[field] == "") {
                    subform[field] = null;
                }
            }
            if (subform.id){
                var id = subform.id;
                delete subform.id;
            }
            else
                var id = "";
            return $.authorizedAjax({
                url: '/api/v1.0/' + path + '/' + id,
                type: 'POST',
                dataType: 'json',
                contentType: 'application/json',
                data: JSON.stringify(subform),
                success: that._onSuccess,
                error: that._onError,
                always: that.hideLoading
            });
        } else {
            this._onSuccess();
        }
    },

    _onSubmit: function (e) {
        e.preventDefault();
        if (!this.isValid() || (this.state.norm_type == 'custom' && !this._getNormAdditionalParamsForm().isValid())) {
            NotificationManager.error('Please correct the errors');
            return;
        }

        this._clearErrors();
        var xhr = this._save();
        if (xhr) {
            xhr.fail(this._onError)
                .always(this.hideLoading)
        }
    },

    hideLoading: function () {
        this.setState({loading: false});
    },

    setNormSubformSaved: function () {
        this.setState({normSubformSaved: true});
    },

    _onSuccess: function (data) {
        // Clean the form
        this.setState({equipmentSubformSaved: true});
        if (this.state.norm_type == 'standard') {
            //this.setState(this.getInitialState());
        }
        NotificationManager.success('Equipment has been successfully saved');
    },

    _onError: function (data) {
        var message = "Failed to create";
        var res = data.responseJSON;
        if (res.message) {
            message = data.responseJSON.message;
        }
        if (res.error) {
            // We get list of errors
            if (data.status >= 500) {
                message = res.error.join(". ");
            } else if (res.error instanceof Object) {
                // We get object of errors with field names as key
                for (var field in res.error) {
                    var errorMessage = res.error[field];
                    if (Array.isArray(errorMessage)) {
                        errorMessage = errorMessage.join(". ");
                    }
                    res.error[field] = errorMessage;
                }
                this.setState({
                    errors: res.error
                });
            } else {
                message = res.error;
            }
        }
        NotificationManager.error(message);
    },

    _clearErrors: function () {
        this.setState({errors: {}});
    },

    clearForm: function () {
        //this.setState(this.getInitialState());
    },

    _onChange: function (e) {
        var form = {};
        var subform = this.state.subform;

        if (e.target.type == 'select-one' && e.target.name === 'equipment_type_id') {
            if (typeof e.target.options[e.target.selectedIndex].accessKey != 'undefined') {
                form['table_name'] = e.target.options[e.target.selectedIndex].accessKey;
            }
        }

        if (this.state.fields.indexOf(e.target.name) == -1) {
            if (e.target.type == 'checkbox') {
                subform[e.target.name] = e.target.checked;
            } else if (e.target.type == 'radio') {
                subform[e.target.name] = e.target.value;
            } else if (e.target.type == 'select-one') {
                subform[e.target.name] = e.target.value;
            } else {
                subform[e.target.name] = e.target.value;
            }
            this.setState({subform: subform});
        } else if (e.target.name === 'equipment_type_id') {
            subform = {};
            this.setState({
                subform: subform
            });
        }

        if (e.target.type == 'checkbox') {
            form[e.target.name] = e.target.checked;
        } else if (e.target.type == 'radio') {
            form[e.target.name] = e.target.value;
        } else if (e.target.type == 'select-one') {
            form[e.target.name] = e.target.value;
        } else {
            form[e.target.name] = e.target.value;
        }

        if (e.target.name == 'equipment_type_id') {
            form['option_text'] = {
                name: e.target.name,
                id: e.target.value,
                text: e.target[e.target.selectedIndex].text
            }
        } else if (e.target.name == 'norm_id') {
            form.normSubformSaved = false;
        }


        // TODO: Exclude upstream field or let adding multiple upstreams
        // Manage change of base form fields only
        if (e.target.name != "upstream1" && this.state.fields.indexOf(e.target.name) > -1) {
            form.changedFields = this.state.changedFields.concat([e.target.name]);
        }
        var errors = this._validate(e);
        form = this._updateFieldErrors(e.target.name, form, errors);
        this.setState(form);
    },

    _validate: function (e) {
        var errors = [];
        var error;
        error = this._validateFieldType(e.target.value, e.target.getAttribute("data-type"));
        if (error) {
            errors.push(error);
        }
        error = this._validateFieldLength(e.target.value, e.target.getAttribute("data-len"));
        if (error) {
            errors.push(error);
        }
        error = this._validateFieldChoice(e.target.value, e.target.getAttribute("data-choice"));
        if (error) {
            errors.push(error);
        }
        return errors;
    },

    _validateFieldType: function (value, type) {
        var error = "";
        if (type != undefined && value) {
            var typePatterns = {
                "float": /^(-|\+?)[0-9]+(\.)?[0-9]*$/,
                "int": /^(-|\+)?(0|[1-9]\d*)$/,
                "text": /(\w|\W)+$/
            };
            if (!typePatterns[type].test(value)) {
                error = "Invalid " + type + " value";
            }
        }
        return error;
    },

    _validateFieldLength: function (value, length) {
        var error = "";
        if (value && length) {
            if (value.length > length) {
                error = "Value should be maximum " + length + " characters long"
            }
        }
        return error;
    },

    _validateFieldChoice: function (value, validChoice) {
        var error = "";
        validChoice = (typeof validChoice == "string") ? validChoice.split(",") : null;
        if (Array.isArray(validChoice) && validChoice.indexOf(value) == -1) {
            error = "Not a valid choice. Value should be one of the following: " + validChoice.join(", ");
        }
        return error;
    },

    _updateFieldErrors: function (fieldName, state, errors) {
        // Clear existing errors related to the current field as it has been edited
        state.errors = this.state.errors;
        delete state.errors[fieldName];

        // Update errors with new ones, if present
        if (Object.keys(errors).length) {
            state.errors[fieldName] = errors.join(". ");
        }
        return state;
    },

    isValid: function () {
        return (Object.keys(this.state.errors).length <= 0);
    },

    _formGroupClass: function (field) {
        var className = "form-group ";
        if (field) {
            className += " has-error"
        }
        return className;
    },

    closeNewEquipmentTypeForm: function () {
        this.setState({
            showNewEquipmentTypeForm: false
        })
    },

    closeNewManufacturerForm: function () {
        this.setState({
            showNewManufacturerForm: false
        })
    },

    closeNewLocationForm: function () {
        this.setState({
            showNewLocationForm: false
        })
    },

    closeAssignToForm: function () {
        this.setState({
            showAssignToForm: false,
        })
    },

    closeNewNormForm: function () {
        this.setState({
            showNewNormForm: false
        })
    },

    onNewButtonClick: function (e) {
        if (e.target.id === 'eq_type') {
            this.setState({
                showNewEquipmentTypeForm: true,
                showNewManufacturerForm: false,
                showNewLocationForm: false,
                showAssignToForm: false,
                showNewNormForm: false
            })
        }
        else if (e.target.id === 'manufac') {
            this.setState({
                showNewEquipmentTypeForm: false,
                showNewManufacturerForm: true,
                showNewLocationForm: false,
                showAssignToForm: false,
                showNewNormForm: false
            })
        }
        else if (e.target.id === 'location') {
            this.setState({
                showNewEquipmentTypeForm: false,
                showNewManufacturerForm: false,
                showNewLocationForm: true,
                showAssignToForm: false,
                showNewNormForm: false
            })
        }
        else if (e.target.id === 'assign_to') {
            this.setState({
                showNewEquipmentTypeForm: false,
                showNewManufacturerForm: false,
                showNewLocationForm: false,
                showAssignToForm: true,
                showNewNormForm: false
            })
        }
        else if (e.target.id === 'norm') {
            this.setState({
                showNewEquipmentTypeForm: false,
                showNewManufacturerForm: false,
                showNewLocationForm: false,
                showAssignToForm: false,
                showNewNormForm: true
            })
        }
    },

    onCreate: function (response, fieldName) {
        var state = {};
        state[fieldName] = response.result;
        state.changedFields = this.state.changedFields.concat([fieldName]);
        this.setState(state);
        this.refs[fieldName].componentDidMount();
    },

    _setDateTimeFieldDate(timestamp, fieldName){
        var state = {};
        // If date is not valid (for example, date is deleted) string "Invalid date" is received
        if (timestamp == "Invalid date"){
            timestamp = null;
        } else if (timestamp){
            // It is UNIX timestamp in milliseconds if dateTimeField was empty on load
            // Format date here instead of specifying format in DateTimeField,
            // because error is raised when format is specified, but date is null/undefined/empty string.
            if (/^\d+$/.test(timestamp)){
                timestamp = parseInt(timestamp);
                timestamp = moment(timestamp).toISOString();
            }
            state[fieldName] = timestamp;    // Already formatted to ISO string
        }
        this.setState(state);
    },

    getNormType: function () {
        return this.state.norm_type;
    },

    getEquipmentType: function () {
        return this.state.equipment_type_id;
    },
    set_location:function(location_id){
        this.setState({"location_id": location_id});
    },

    render: function () {
        // Do not set dateTime property if date is null/undefined/empty string, calendar will be broken
        return (
            <div className="form-container">
                <form id="eqtype_form" ref="eqtype_form" onSubmit={this._onSubmit} onChange={this._onChange}>
                    <div>
                        <Panel header={(this.props.action == 'edit' ? "Edit Equipment": "Add Equipment")}>
                            <div className="row">
                                <div className={(this.props.action == 'edit' ? 'col-lg-12' : 'col-lg-11')}>
                                    <EquipmentTypeSelectField
                                        source="/api/v1.0/equipment_type"
                                        value={this.state.equipment_type_id}
                                        errors={this.state.errors}
                                        ref="equipment_type_id"
                                        readonly={(this.props.action == 'edit' )}
                                        required
                                    />
                                </div>
                                <div className={"col-md-1" + (this.props.action == 'edit' ? " collapse": "")}>
                                    <a id="eq_type"
                                       className="btn btn-primary"
                                       onClick={this.onNewButtonClick}
                                    >New</a>
                                </div>
                            </div>
                            
                            <div className="row">
                                <div className={(this.props.action == 'edit' ? 'col-lg-12' : 'col-lg-11')}>
                                    <ManufacturerSelectField
                                        source="/api/v1.0/manufacturer"
                                        value={this.state.manufacturer_id}
                                        errors={this.state.errors}
                                        ref="manufacturer_id"
                                    />
                                </div>
                                <div className={"col-md-1" + (this.props.action == 'edit' ? " collapse": "")}>
                                    <a id="manufac"
                                       className="btn btn-primary"
                                       onClick={this.onNewButtonClick}
                                    >New</a>
                                </div>
                            </div>

                            <div className="row">
                                <div className={(this.props.action == 'edit' ? 'col-lg-12' : 'col-lg-11')}>
                                    <LocationSelectField
                                        source="/api/v1.0/location"
                                        value={this.state.location_id}
                                        errors={this.state.errors}
                                        ref="location_id"
                                        required/>
                                </div>
                                <div className={"col-md-1" + (this.props.action == 'edit' ? " collapse": "")}>
                                    <a id="location"
                                       className="btn btn-primary"
                                       onClick={this.onNewButtonClick}
                                    >New</a>
                                </div>
                            </div>

                            <div className="row">
                                <div className={(this.props.action == 'edit' ? 'col-lg-12' : 'col-lg-11')}>
                                    <AssignedToSelectField
                                        source="/api/v1.0/assigned_to"
                                        value={this.state.assigned_to_id}
                                        errors={this.state.errors}
                                        ref="assigned_to_id"
                                        required
                                    />
                                </div>
                                <div className={"col-md-1" + (this.props.action == 'edit' ? " collapse": "")}>
                                    <a id="assign_to"
                                       className="btn btn-primary"
                                       onClick={this.onNewButtonClick}
                                    >New</a>
                                </div>
                            </div>

                            <div className="row">
                                <div className={(this.props.action == 'edit' ? 'col-lg-12' : 'col-lg-11')}>
                                    <NormTypeSelectField
                                        onChange={this._onChange}
                                        value={this.state.norm_type}
                                        errors={this.state.errors}
                                        ref="norm_type"
                                        required
                                    />
                                </div>
                            </div>
                            <div className="row">
                                {
                                    this.state.norm_type == 'custom' ?
                                        <div className="col-md-12">
                                            <NormAdditionalParams
                                                ref='normAdditionalParams'
                                                clearForm={this.clearForm}
                                                getNormType={this.getNormType}
                                                getEquipmentType={this.getEquipmentType}
                                                setNormSubformSaved={this.setNormSubformSaved}
                                                data={this.state}/>
                                        </div>
                                    : null
                                }
                            </div>
                            <FormGroup controlId="inputNameField"
                                       validationState={this.state.errors.name ? 'error' : null}>
                                <ControlLabel>Equipment Name</ControlLabel>
                                <span className="text-danger"> *</span>
                                <FormControl type="text"
                                             placeholder="Equipment Name"
                                             name="name"
                                             required
                                             data-len="50"
                                             value={this.state.name ? this.state.name : ""}
                                />
                                <HelpBlock className="warning">{this.state.errors.name}</HelpBlock>
                                <FormControl.Feedback />
                            </FormGroup>

                            <FormGroup validationState={this.state.errors.equipment_number ? 'error' : null}>
                                <ControlLabel>Equipment Number</ControlLabel>
                                <span className="text-danger"> *</span>
                                <FormControl
                                    type="text"
                                    placeholder="Equipment number"
                                    name="equipment_number"
                                    value={this.state.equipment_number ? this.state.equipment_number : ""}
                                    data-len="50"
                                    required
                                />
                                <HelpBlock className="warning">{this.state.errors.equipment_number}</HelpBlock>
                                <FormControl.Feedback />
                            </FormGroup>

                            <FormGroup controlId="inputSerialField"
                                       validationState={this.state.errors.serial ? 'error' : null}>
                                <ControlLabel>Serial number</ControlLabel>
                                <FormControl type="text"
                                             name="serial"
                                             placeholder="Serial number"
                                             ref="serial"
                                             data-len="50"
                                             value={this.state.serial ? this.state.serial : ""}
                                />
                                <HelpBlock className="warning">{this.state.errors.serial}</HelpBlock>
                                <FormControl.Feedback />
                            </FormGroup>
                            <div className="row">
                                <div className="col-lg-5">
                                    <FrequencySelectField name="frequency"
                                                          title="Frequency"
                                                          ref="frequency"
                                                          value={this.state.frequency}
                                                          errors={this.state.errors}
                                    />
                                </div>
                            </div>
                            <div className="row">
                                <div className="col-lg-5">
                                    <ManufacturedSelectField title="Manufactured"
                                                             id="manufactured"
                                                             value={this.state.manufactured}
                                                             errors={this.state.errors}
                                    />
                                </div>
                            </div>
                            <div className="row">
                                <div className="col-lg-12">
                                    <FormGroup controlId="descriptionTextarea"
                                               validationState={this.state.errors.description ? 'error' : null}>
                                        <ControlLabel>Description</ControlLabel>
                                        <span className="text-danger"> *</span>
                                        <FormControl componentClass="textarea"
                                                     name="description"
                                                     placeholder="Description"
                                                     ref="description"
                                                     value={this.state.description ? this.state.description : ""}
                                                     required
                                        />
                                        <HelpBlock className="warning">{this.state.errors.description}</HelpBlock>
                                        <FormControl.Feedback />
                                    </FormGroup>
                                </div>
                            </div>

                            <div className="row">
                                <div className="col-lg-12">
                                    <FormGroup controlId="commentsTextarea"
                                               validationState={this.state.errors.comments ? 'error' : null}>
                                        <ControlLabel>Comments</ControlLabel>
                                        <FormControl componentClass="textarea"
                                                     name="comments"
                                                     placeholder="Comments"
                                                     ref="comments"
                                                     value={this.state.comments ? this.state.comments : ""}
                                        />
                                        <HelpBlock className="warning">{this.state.errors.comments}</HelpBlock>
                                        <FormControl.Feedback />
                                    </FormGroup>
                                </div>
                            </div>
                            <div className="row">
                                <div className="col-lg-12">
                                    <FormGroup controlId="tapChangesTextarea" ref="nr_taps"
                                               validationState={this.state.errors.nbr_of_tap_change_ltc ? 'error' : null}>
                                        <ControlLabel>Nbr of Tap Changes LTC</ControlLabel>
                                        <span className="text-danger"> *</span>
                                        <FormControl type="text"
                                                     name="nbr_of_tap_change_ltc"
                                                     placeholder="Tap changes"
                                                     ref="nr_taps"
                                                     value={this.state.nbr_of_tap_change_ltc ? this.state.nbr_of_tap_change_ltc : ""}
                                                     data-type="int"
                                                     required
                                        />
                                        <HelpBlock
                                            className="warning">{this.state.errors.nbr_of_tap_change_ltc}</HelpBlock>
                                        <FormControl.Feedback />
                                    </FormGroup>
                                </div>
                            </div>
                            <div className="row">
                                <div className="col-lg-12">
                                    <FormGroup controlId="physPositionInput"
                                               validationState={this.state.errors.phys_position ? 'error' : null}>
                                        <ControlLabel>Physical Position</ControlLabel>
                                        <span className="text-danger"> *</span>
                                        <FormControl type="text"
                                                     placeholder="Physical position"
                                                     ref="phys_position"
                                                     name="phys_position"
                                                     value={this.state.phys_position ? this.state.phys_position : ""}
                                                     data-type="int"
                                                     required
                                        />
                                        <HelpBlock className="warning">{this.state.errors.phys_position}</HelpBlock>
                                        <FormControl.Feedback />
                                    </FormGroup>

                                </div>
                            </div>

                            <div className="row">
                                <div className="col-lg-12">
                                    <FormGroup controlId="tensionInput"
                                               validationState={this.state.errors.tension4 ? 'error' : null}>
                                        <ControlLabel>Tension</ControlLabel>
                                        <span className="text-danger"> *</span>
                                        <FormControl type="text"
                                                     name="tension4"
                                                     placeholder="Tension"
                                                     ref="tension4"
                                                     value={this.state.tension4 ? this.state.tension4 : ""}
                                                     data-type="float"
                                                     required
                                        />
                                        <HelpBlock className="warning">{this.state.errors.tension4}</HelpBlock>
                                        <FormControl.Feedback />
                                    </FormGroup>
                                </div>
                            </div>
                            <div className="row">
                                <div className={(this.props.action == 'edit' ? 'col-lg-12' : 'col-lg-11')}>
                                    <EqAdditionalParams
                                        data={this.state}
                                        edited={(this.state.subform && Object.keys(this.state.subform).length > 0) ? true : false}
                                        equipment_item={this.state.equipment_item}
                                        ref="EqAdditionalParams"
                                        />
                                </div>
                            </div>
                            <div className="row">
                                <div className="col-md-12">
                                    <Button bsStyle="success" type="submit" className="pull-right">Save</Button>
                                    <Button bsStyle="danger"
                                            onClick={this.handleClose}
                                            className="pull-right margin-right-xs">Cancel</Button>
                                </div>
                            </div>
                        </Panel>
                    </div>
                </form>

                <Modal show={this.state.showNewEquipmentTypeForm}>
                    <Modal.Header>
                        <Modal.Title>New Equipment Type</Modal.Title>
                    </Modal.Header>
                    <Modal.Body>
                        <NewEquipmentTypeForm data={this.props.data}
                                              handleClose={this.closeNewEquipmentTypeForm}
                                              onCreate={this.onCreate}
                                              fieldName="equipment_type_id"/>
                    </Modal.Body>
                </Modal>

                <Modal show={this.state.showNewManufacturerForm}>
                    <Modal.Header>
                        <Modal.Title>New Manufacturer</Modal.Title>
                    </Modal.Header>
                    <Modal.Body>
                        <NewManufacturerForm data={this.props.data}
                                             handleClose={this.closeNewManufacturerForm}
                                             onCreate={this.onCreate}
                                             fieldName="manufacturer_id"/>
                    </Modal.Body>
                </Modal>

                <Modal show={this.state.showNewLocationForm}>
                    <Modal.Header>
                        <Modal.Title>New Location</Modal.Title>
                    </Modal.Header>
                    <Modal.Body>
                        <NewLocationForm data={this.props.data}
                                         handleClose={this.closeNewLocationForm}
                                         onCreate={this.onCreate}
                                         fieldName="location_id"/>
                    </Modal.Body>
                </Modal>

                <Modal show={this.state.showAssignToForm}>
                    <Modal.Header>
                        <Modal.Title>New User Profile</Modal.Title>
                    </Modal.Header>
                    <Modal.Body>
                        <CreatedByForm data={this.props.data}
                                       handleClose={this.closeAssignToForm}
                                       onCreate={this.onCreate}
                                       fieldName="assigned_to_id"/>
                    </Modal.Body>
                </Modal>

                <Modal show={this.state.showNewNormForm}>
                    <Modal.Header>
                        <Modal.Title>New Norm</Modal.Title>
                    </Modal.Header>
                    <Modal.Body>
                        <NewNormForm data={this.props.data}
                                     handleClose={this.closeNewNormForm}
                                     onCreate={this.onCreate}
                                     fieldName="norm_id"/>
                    </Modal.Body>
                </Modal>
            </div>
        );
    }
});

export default EquipmentForm;
