import React from 'react';
import DateTimeField from 'react-bootstrap-datetimepicker/lib/DateTimeField';
import FormControl from 'react-bootstrap/lib/FormControl';
import FormGroup from 'react-bootstrap/lib/FormGroup';
import ControlLabel from 'react-bootstrap/lib/ControlLabel';
import Checkbox from 'react-bootstrap/lib/Checkbox';
import Button from 'react-bootstrap/lib/Button';
import NewBushingTestForm from './TestTypeResultForm_modules/NewBushingTestForm';
import WindingTestForm from './TestTypeResultForm_modules/WindingTestForm';
import NewInsulationResistanceTestForm from './TestTypeResultForm_modules/NewInsulationResistanceTestForm';
import VisualTestForm from './TestTypeResultForm_modules/VisualTestForm';
import NewWindingResistanceTestForm from './TestTypeResultForm_modules/NewWindingResistanceTestForm';
import PolymerisationDegreeTestForm from './TestTypeResultForm_modules/PolymerisationDegreeTestForm';
import NewTransformerTestForm from './TestTypeResultForm_modules/NewTransformerTestForm';
import NewDissolvedGasForm from './TestTypeResultForm_modules/NewDissolvedGasTestForm';
import WaterTestForm from './TestTypeResultForm_modules/WaterTestForm';
import NewFuranTestForm from './TestTypeResultForm_modules/NewFuranTestForm';
import NewInhibitorTestForm from './TestTypeResultForm_modules/NewInhibitorTestForm';
import NewPcbTestForm from './TestTypeResultForm_modules/NewPcbTestForm';
import NewFluidTestForm from './TestTypeResultForm_modules/NewFluidTestForm';
import NewParticleTestForm from './TestTypeResultForm_modules/NewParticleTestForm';
import MetalsInOilTestForm from './TestTypeResultForm_modules/MetalsInOilTestForm';
import NewRecommendationForm from './NewTestForm_modules/NewRecommendationForm';
import TestTypeSelectField from './NewTestForm_modules/TestTypeSelectField';
import TestRecommendationList from './TestRecommendationList';
import RepairNotesList from './RepairNotesList';
import TestDiagnosisList from './TestDiagnosisList';
import NewDiagnosisForm from './NewDiagnosisForm';
import {NotificationContainer, NotificationManager} from 'react-notifications';
import {DATETIMEPICKER_FORMAT} from './appConstants.js';
import OverlayTrigger from 'react-bootstrap/lib/OverlayTrigger';
import Tooltip from 'react-bootstrap/lib/Tooltip';
import HelpBlock from 'react-bootstrap/lib/HelpBlock';
import {findDOMNode} from 'react-dom';
import ReactDOM from 'react-dom';
import {EQUIPMENT_STATUS} from './appConstants.js';


var SelectField = React.createClass({
    getInitialState: function () {
        return {
            items: [],
            isVisible: false,
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
        var name = (this.props.name != null) ? this.props.name : "";
        var value = (this.props.value != null) ? this.props.value : "";
        var menuItems = [];
        for (var key in this.state.items) {
            menuItems.push(<option key={this.state.items[key].id}
                                   value={this.state.items[key].id}>{`${this.state.items[key].name}`}</option>);
        }
        return (
            <FormGroup>
                <FormControl componentClass="select"
                             onChange={this.props.onChange}
                             name={name}
                             value={value}
                             disabled={this.props.disabled}
                >
                    <option>{label}</option>
                    {menuItems}
                    <FormControl.Feedback />
                </FormControl>
            </FormGroup>
        );
    }
});

var StatusSelectField = React.createClass({
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

    },
    componentWillUnmount: function () {
    },
    setVisible: function () {
        this.state.isVisible = true;
    },
    render: function () {
        var label = (this.props.label != null) ? this.props.label : "";
        var name = (this.props.name != null) ? this.props.name : "";
        var value = (this.props.value != null) ? this.props.value : "";
        var menuItems = [];
        for (var key in EQUIPMENT_STATUS) {
            menuItems.push(<option key={EQUIPMENT_STATUS[key].id}
                                   value={EQUIPMENT_STATUS[key].id}>{`${EQUIPMENT_STATUS[key].name}`}</option>);
        }

        return (
            <FormGroup>
                <ControlLabel>{label}</ControlLabel>
                <FormControl componentClass="select"
                             onChange={this.props.onChange}
                             name={name}
                             value={value}>
                    <option key={null} value={null}></option>
                    {menuItems}
                    <FormControl.Feedback />
                </FormControl>
            </FormGroup>
        );
    }
});

var SyringeNumberSelectField = React.createClass({

    getInitialState: function () {
        return {
            items: [],
            isVisible: false,
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
        var name = (this.props.name != null) ? this.props.name : "";
        var value = (this.props.value != null) ? this.props.value : "";
        var menuItems = [];
        for (var key in this.state.items) {
            menuItems.push(<option key={this.state.items[key].id}
                                   value={this.state.items[key].id}>{`${this.state.items[key].serial}`}</option>);
        }


        return (
            <FormGroup>
                <ControlLabel>{label}</ControlLabel>
                <FormControl componentClass="select"
                             onChange={this.props.onChange}
                             name={name}
                             value={value}
                             disabled={this.props.disabled}
                >
                    <option key={null} value={null}></option>
                    {menuItems}
                    <FormControl.Feedback />
                </FormControl>
            </FormGroup>
        );
    }
});

const DateTimeFieldWithLabel = React.createClass({
    _onChange: function (timestamp) {
        this.props.onDateTimeFieldChange(timestamp, this.props.name);
    },
    render: function () {
        var label = (this.props.label != null) ? this.props.label : "Please select a date";
        var name = (this.props.name != null) ? this.props.name : "";
        // Do not set dateTime property if date is null/undefined/empty string, calendar will be broken
        var dateValue = this.props.value;
        dateValue = (dateValue) ? {
            dateTime: dateValue,
            format: DATETIMEPICKER_FORMAT
        } : {defaultText: label};

        return (
            <div className="datetimepicker input-group date">
                <DateTimeField name={name}
                               onChange={this._onChange}
                               {...dateValue}
                               inputProps={{disabled: this.props.readOnly}}
                />
            </div>
        );
    }
});

const TextField = React.createClass({
    render: function () {
        var label = (this.props.label != null) ? this.props.label : "";
        var name = (this.props.name != null) ? this.props.name : "";
        var value = (this.props.value != null) ? this.props.value : "";
        var className = (this.props.className != null) ? this.props.className : "";
        return (
            <FormGroup className={className}>
                <ControlLabel>{label}</ControlLabel>
                <FormControl type="text"
                             placeholder={label}
                             name={name}
                             value={value}
                             onChange={this.props.onChange}
                             disabled={this.props.disabled}
                />
                <FormControl.Feedback />
            </FormGroup>
        );
    }
});

const TextArea = React.createClass({
    render: function () {
        let tooltip = <Tooltip id={this.props.label}>{this.props.label}</Tooltip>;
        var label = (this.props.label != null) ? this.props.label : "";
        var name = (this.props.name != null) ? this.props.name : "";
        var value = (this.props.value != null) ? this.props.value : "";
        var error = this.props.errors[name];
        return (
            <OverlayTrigger overlay={tooltip} placement="top">
                <FormGroup>
                    <FormControl componentClass="textarea"
                                 placeholder={label}
                                 name={name}
                                 value={value}
                                 onChange={this.props.onChange}
								 required={this.props.required}
                    />
                    <HelpBlock className="warning">{error}</HelpBlock>
                    <FormControl.Feedback />
                </FormGroup>
            </OverlayTrigger>
        );
    }
});

var EquipmentTestIdentificationForm = React.createClass({
    getInitialState: function () {
        return {
            loading: false,
            errors: {}
        }
    },
    render: function () {
        var data = (this.props.data != null) ? this.props.data : {};
        return (
            <div className="form-container">
                <div className="row">
                    <div className="col-md-4">
                        <SelectField source="test_type"
                                     label="Test type"
                                     name='test_type_id'
                                     value={data.test_type_id}
                                     disabled/>
                    </div>

                    <div className="col-md-3 col-md-offset-2">
                        <SelectField source="user"
                                     label="Performed By"
                                     name='performed_by_id'
                                     value={data.performed_by_id}
                                     disabled/>
                    </div>
                    <div className="col-md-2 nopadding padding-right-xs">
                        <TextField label="Fluid Temperature (&#8451;)"
                                   name='temperature'
                                   value={data.temperature}
                                   onChange={this.props.onChange}
                                   />
                    </div>
                </div>
                <div className="row">
                    <div className="col-md-2">
                        <SelectField source="insulation"
                                     label="Insulating Fluid"
                                     name='fluid_type_id'
                                     value={data.fluid_type_id}
                                     onChange={this.props.onChange}
                        />
                    </div>
                    <div className="col-md-2">
                        <SelectField source="contract"
                                     label="Lab contract &#8470;"
                                     name='lab_contract_id'
                                     value={data.lab_contract_id}
                                     disabled/>
                    </div>
                    <div className="col-md-3 col-md-offset-2">
                        <SelectField source="test_status"
                                     label="Status"
                                     name='test_status_id'
                                     value={data.test_status_id}
                        />
                    </div>
                    <div className="col-md-2 nopadding padding-right-xs">
                        <TextField label="Load (Mva)"
                                   value={data.charge}
                                   name="charge"
                                   onChange={this.props.onChange}
                                   />
                    </div>
                </div>
                <div className="row">
                    <div className="col-md-3 ">
                        <SelectField source="sampling_point"
                                     label="Sampling point"
                                     name='sampling_point_id'
                                     value={data.sampling_point_id}
                                     disabled
                        />
                    </div>
                    <div className="col-md-3">
                        <SyringeNumberSelectField source="syringe"
                                                  label="Syringe &#8470; / Jar &#8470;"
                                                  name='seringe_num'
                                                  value={data.seringe_num}
                                                  onChange={this.props.onChange}
                        />
                    </div>
                    <div className="col-md-3" key={data.date_analyse}>
                        <DateTimeFieldWithLabel label="Lab Analysis Date"
                                                name='date_analyse'
                                                value={data.date_analyse}
                                                onChange={this.props.onChange}
                                                onDateTimeFieldChange={this.props.onDateTimeFieldChange}
                        />
                    </div>
                    <div className="col-md-3 nopadding padding-right-xs">
                        <SelectField source="lab"
                                     label="Lab./On-line analyser"
                                     name='lab_id'
                                     value={data.lab_id}
                                     onChange={this.props.onChange}
                                     />
                    </div>
                </div>
                <div className="row">
                    <div className="col-md-3">
                        <SelectField source="equipment"
                                     label="Equipment"
                                     name='equipment_id'
                                     value={data.equipment_id}
                                     disabled/>
                    </div>
                    <div className="col-md-3">
                        <SelectField source="test_reason"
                                     label="Test reason"
                                     name='test_reason_id'
                                     value={data.test_reason_id}
                                     disabled/>
                    </div>
                    <div className="col-md-3">
                        <TextField label="Analysis Number"
                                   value={data.analysis_number}
                                   name="test_number"
                                   disabled/>
                    </div>
                </div>
            </div>
        );
    }
});

var EquipmentTestRepairForm = React.createClass({
    getInitialState: function () {
        return {
            loading: false,
            errors: {},
            formEdited: false
        }
    },

    _onChange: function (e) {
        var state = {formEdited: true};
        state[e.target.name] = e.target.value;
        this.setState(state);
        this.props.onChange(e);
    },

    is_valid: function () {
        var errors = [];
        if (this.state.formEdited && !this.state.repair_test_type_id) {
             errors.push("Test Repair notes Tab: Test type is required.");
        }
        return errors;
    },

    render: function () {
        var data = (this.props.data != null) ? this.props.data : {};
        return (
            <div className="tab_row">
                <div className="col-md-12">
                    <RepairNotesList testResultId={this.props.data.id}
                                     testTypeId={this.props.data.test_type_id}
                                     ref="testRepairNotesList"/>
                </div>
                <div className="col-md-6">
                        <TextArea label="Repair description"
                                  name='description'
                                  value={data.description}
                                  onChange={this._onChange}
                                  errors={this.state.errors}/>
                </div>
                <div className="col-md-6">
                        <TextArea label="Remark"
                                  name='remark'
                                  value={data.remark}
                                  onChange={this._onChange}
                                  errors={this.state.errors}/>
                </div>
                <div className="col-md-12">
                        <TextArea label="Sample"
                                  name='sample'
                                  value={data.sample}
                                  onChange={this._onChange}
                                  errors={this.state.errors}/>
                </div>
                <div className="col-md-4">
                    <TestTypeSelectField key={this.props.data.selected_subtests}
                                         selectedSubtests={this.props.data.selected_subtests}
                                         testType={this.props.data.test_type}
                                         handleChange={this._onChange}
                                         name="repair_test_type_id"
                                         errors={this.state.errors}
                                         required={this.state.formEdited}/>
                </div>
                <div className="col-md-8" key={data.date_created}>
                    <DateTimeFieldWithLabel label="Please select repair date"
                                            name='date_created'
                                            value={data.date_created}
                                            onChange={this._onChange}
                                            onDateTimeFieldChange={this.props.onDateTimeFieldChange}
                                            readOnly/>
                </div>
            </div>
        );
    }
});

var EquipmentTestDiagnosisForm = React.createClass({
    getInitialState: function () {
        return {
            loading: false,
            showNewRecommendationForm: false,
            recommendationPreselected: false,
            recommendation_id: null,
            formEdited: false,
            errors: {}
        }
    },

    componentDidMount: function () {
        this.serverRequest = $.authorizedGet(this.props.source, function (result) {
            var items = (result['result']);
            this.setState({
                items: items
            });

        }.bind(this), 'json');
    },

    closeNewRecommendationForm: function () {
        this.setState({showNewRecommendationForm: false})
    },

    updatePredefinedRecommendations: function (recommendationId, testTypeId, recommendationType) {
        var state = {showNewRecommendationForm: false};

        if (recommendationType == "predefined") {
            // Reload select field with predefined recommendations and
            // change the value in the global state
            this.props.setStateData({
                recommendation_id: recommendationId,
                recommendation_test_type_id: testTypeId
            });
            state.recommendation_id = recommendationId;
            state.recommendationPreselected = true;
        } else if (recommendationType == "test") {
            state.recommendation_id = "";
            // Reload Recommendation list
            this.refs.testRecommendationList.reloadList(this.props.data.id, this.props.data.test_type_id);
        }
        this.setState(state);
    },

    _onChange: function (e) {
        var OTHER_RECOMENDATION_TEXT = "Other recommendations (specify)";

        // Open new recommendation form, if needed
        if (e.target.name == "recommendation_id") { 
            var state = {};
            // Change value in this form's state to be able to select
            state.recommendation_id = e.target.value;
            // Change the value in the global state to save it from there
            this.props.onChange(e);

            if (e.target.selectedOptions.length && e.target.selectedOptions[0].text == OTHER_RECOMENDATION_TEXT){
                state.formEdited = false;
                // No special method for opening NewRecommendationForm in order not to set state twice
                state.showNewRecommendationForm = true;
                this.props.data.recommendation_id = null;
            } else {
                state.formEdited = true;
                this.closeNewRecommendationForm();
            }
            state.recommendationPreselected = false;
        }
        this.setState(state);
    },

    handleTestTypeChange: function (e) {
        this.setState({recommendation_test_type_id: e.target.value});
        this.props.onChange(e);
    },

    is_valid: function () {
        var errors = [];
        if (this.state.formEdited && !this.state.recommendation_test_type_id) {
             errors.push("Recommendation notes Tab: Test type is required.");
        }
        return errors;
    },

    render: function () {
        return (
                <div className="tab_row">
                    <div className="col-lg-12">
                        <TestRecommendationList testResultId={this.props.data.id}
                                                testTypeId={this.props.data.test_type_id}
                                                ref="testRecommendationList"/>
                    </div>

                    <div className="col-lg-8 nopadding">
                        <SelectField source="recommendation"
                                     label="Predefined recommendation"
                                     name='recommendation_id'
                                     value={this.state.recommendation_id}
                                     key={this.state.recommendation_id}
                                     onChange={this._onChange}
                                     ref="recommendation"
                        />
                    </div>
                    {this.state.showNewRecommendationForm ?
                        <div className="col-lg-12 nopadding">
                            <NewRecommendationForm testResultId={this.props.data.id}
                                                   recommendationId={this.state.recommendation_id}
                                                   selectedSubtests={this.props.data.selected_subtests}
                                                   testType={this.props.data.test_type}
                                                   handleClose={this.closeNewRecommendationForm}
                                                   onSuccess={this.updatePredefinedRecommendations}/>
                        </div>
                        : null
                    }
                    {!this.state.showNewRecommendationForm && !this.state.recommendationPreselected ?
                        <div className="col-lg-4">
                            <TestTypeSelectField key={this.props.data.selected_subtests}
                                                 selectedSubtests={this.props.data.selected_subtests}
                                                 testType={this.props.data.test_type}
                                                 handleChange={this.handleTestTypeChange}
                                                 name="recommendation_test_type_id"
                                                 errors={this.state.errors}
                                                 required={this.state.formEdited}/>
                        </div>
                        : null
                    }
                </div>
        )
    }
});

var EquipmentTestEqDiagnosisForm = React.createClass({
    getInitialState: function () {
        return {
            loading: false,
            diagnosis_id: null,
            diagnosisPreselected: false,
            formEdited: false,
            errors: {}
        }
    },

    componentDidMount: function () {
        this.serverRequest = $.authorizedGet(this.props.source, function (result) {
            var items = (result['result']);
            this.setState({
                items: items
            });
        }.bind(this), 'json');
    },

    _closeNewDiagnosisForm: function () {
        this.setState({
            diagnosis_id: null
        })
    },

    updatePredefinedDiagnosis: function (id, testTypeId, diagnosisType) {
        this.props.setStateData({diagnosis_id: id, diagnosis_test_type_id: testTypeId});
        var state = {diagnosis_id: id, diagnosisPreselected: true};
        if (diagnosisType == "test") {
            this.refs.diagnosisList.reloadList(this.props.data.id, this.props.data.test_type_id);
            state.diagnosis_id = "";
            state.diagnosisPreselected = false;
        }
        this.setState(state);
    },

    _onChange: function (e) {
        var OTHER_DIAGNOSIS_ID = 3;
        var formEdited = true;
        var state = {};
        if (e.target.value == OTHER_DIAGNOSIS_ID) {
            formEdited = false;
            this.props.data.diagnosis_id = null;
        }

        state[e.target.name] = e.target.value;
        if (e.target.name == 'diagnosis_id') {
            state.diagnosisPreselected = false;
            state.formEdited = formEdited;
            // Change the value in the global state to save it from there
            this.props.onChange(e);
        }
        this.setState(state);
    },

    is_valid: function () {
        var errors = [];
        if (this.state.formEdited && !this.state.diagnosis_test_type_id) {
             errors.push("Diagnosis Tab: Test type is required.");
        }
        return errors;
    },

    render: function () {
        var OTHER_DIAGNOSIS_ID = 3;

        return (
            <div method="post" action="#" onChange={this._onChange}>
                <div className="tab_row">
                    <div className="col-md-12">
                        <TestDiagnosisList testResultId={this.props.data.id}
                                           testTypeId={this.props.data.test_type_id}
                                           diagnosisId={this.state.diagnosis_id}
                                           ref="diagnosisList"/>
                    </div>
                    <div className="col-md-8 nopadding padding-right-xs">
                        <SelectField source="diagnosis"
                                     label="Predefined diagnosis"
                                     name='diagnosis_id'
                                     ref="diagnosis"
                                     value={this.state.diagnosis_id}
                                     key={this.state.diagnosis_id}
                                     onChange={this._onChange}
                            />
                    </div>
                    {parseInt(this.state.diagnosis_id) === OTHER_DIAGNOSIS_ID ?
                        <div className="col-md-12 nopadding">
                            <NewDiagnosisForm testResultId={this.props.data.id}
                                              diagnosisId={this.state.diagnosis_id}
                                              selectedSubtests={this.props.data.selected_subtests}
                                              testType={this.props.data.test_type}
                                              handleClose={this._closeNewDiagnosisForm}
                                              onSuccess={this.updatePredefinedDiagnosis}
                                />
                        </div>
                        : null
                    }
                    {parseInt(this.state.diagnosis_id) !== OTHER_DIAGNOSIS_ID && !this.state.diagnosisPreselected ?
                        <div className="col-md-4">
                            <TestTypeSelectField key={this.props.data.selected_subtests}
                                                 selectedSubtests={this.props.data.selected_subtests}
                                                 testType={this.props.data.test_type}
                                                 handleChange={this.props.onChange}
                                                 name="diagnosis_test_type_id"
                                                 errors={this.state.errors}
                                                 required={this.state.formEdited}
                                                 ref="diagnosisTestTypeId"/>
                        </div>
                        : null
                    }
                </div>
            </div>
        );
    }
});

var TestValuesForm = React.createClass({
    render: function () {
        if (this.props.testType == null) {
            return (<div></div>);
        }
        var tableName = this.props.testType.test_table_name;
        switch (tableName) {
            case "bushing_test":
                return (<NewBushingTestForm testResultId={this.props.testResultId}
                                            tableName={tableName}/>);
            case "winding_test":
                return (<WindingTestForm testResultId={this.props.testResultId}
                                         tableName={tableName}/>);
            case "insulation_resistance_test":
                return (<NewInsulationResistanceTestForm testResultId={this.props.testResultId}
                                                         tableName={tableName}/>);
            case "visual_inspection_test":
                return (<VisualTestForm testResultId={this.props.testResultId}
                                        tableName={tableName}/>);
            case "winding_resistance_test":
                return (<NewWindingResistanceTestForm testResultId={this.props.testResultId}
                                                      tableName={tableName}/>);
            case "polymerisation_degree_test":
                return (<PolymerisationDegreeTestForm testResultId={this.props.testResultId}
                                                      tableName={tableName}/>);
            case "transformer_turn_ratio_test":
                return (<NewTransformerTestForm testResultId={this.props.testResultId}
                                                tableName={tableName}/>);
            case "dissolved_gas_test":
                return (<NewDissolvedGasForm testResultId={this.props.testResultId}
                                             tableName={tableName}/>);
            case "water_test":
                return (<WaterTestForm testResultId={this.props.testResultId}
                                       tableName={tableName}/>);
            case "furan_test":
                return (<NewFuranTestForm testResultId={this.props.testResultId}
                                          tableName={tableName}/>);
            case "inhibitor_test":
                return (<NewInhibitorTestForm testResultId={this.props.testResultId}
                                              tableName={tableName}/>);
            case "pcb_test":
                return (<NewPcbTestForm testResultId={this.props.testResultId}
                                        tableName={tableName}/>);
            case "fluid_test":
                return (<NewFluidTestForm testResultId={this.props.testResultId}
                                          tableName={tableName}/>);
            case "particle_test":
                return (<NewParticleTestForm testResultId={this.props.testResultId}
                                             tableName={tableName}/>);
            case "metals_in_oil_test":
                return (<MetalsInOilTestForm testResultId={this.props.testResultId}
                                             tableName={tableName}/>);
            default:
                return (<div></div>);
        }
    }
});

var EquipmentTestForm = React.createClass({
    getInitialState: function () {
        return {
            loading: false,
            csrf_token: 'not set',
            fields: ['test_type_id', 'test_reason_id',
                'status_id', 'temperature', 'lab_contract_id',
                'sampling_point_id', 'equipment_id', 'lab_id',
                'fluid_type_id', 'date_analyse', 'test_status_id'],
            testRecommendationFields: ['recommendation_id', 'recommendation_test_type_id'],
            testRepairNotesFields: ['description', 'remark', 'sample', 'date_created', 'repair_test_type_id'],
            testDiagnosisFields: ['diagnosis_notes', 'diagnosis_id', 'diagnosis_test_type_id'],
            errors: {},
            data: null,
            campaignIndicator: "",
            equipmentStatusChanged: false   // Reset this flag not to save same equipment status twice
        }
    },

    _save: function () {
        var errors = this._validateSubforms();
        if (errors.length) {
            for (var i = 0; i < errors.length; i++) {
                // Use setTimeout, otherwise only last notification is shown
                setTimeout(function(error){NotificationManager.error(error, null, 5000, null, true)}, 100, errors[i]);
            }
            return false;
        }

        this._saveTestRecommendation();
        this._saveRepairNote();
        this._saveDiagnosis();
        this._saveEquipmentStatus();
        var fields = this.state.fields;
        var data = {};
        var url = '/api/v1.0/test_result/';
        var type = 'POST';
        for (var i = 0; i < fields.length; i++) {
            var key = fields[i];
            data[key] = this.state.data[key];
        }
        if ('id' in this.state.data) {
            url += this.state.data['id'];
        }

        return $.authorizedAjax({
            url: url,
            type: type,
            dataType: 'json',
            contentType: 'application/json',
            data: JSON.stringify(data),
            beforeSend: function () {
                this.setState({loading: true});
            }.bind(this)
        })
    },

    _validateSubforms: function () {
        var errors = [];
        errors.push(...this.refs.diagnosisForm.is_valid());
        errors.push(...this.refs.recommedationForm.is_valid());
        errors.push(...this.refs.repairNotesForm.is_valid());
        return errors;
    },

    _saveTestRecommendation: function () {
        var fields = this.state.testRecommendationFields;
        var data = {};
        var url = '/api/v1.0/test_recommendation/';
        var type = 'POST';
        for (var i = 0; i < fields.length; i++) {
            var key = fields[i];
            if (this.state.data[key]) {
                data[key] = this.state.data[key];
            }
        }

        if (Object.keys(data).length) {
            // There are several fields with the name test_type_id - differ them somehow
            data.test_type_id = data.recommendation_test_type_id;
            delete data.recommendation_test_type_id;
            data.test_result_id = this.state.data['id'];
            $.authorizedAjax({
                url: url,
                type: type,
                dataType: 'json',
                contentType: 'application/json',
                data: JSON.stringify(data),
                beforeSend: function () {
                },
                success: function () {
                    NotificationManager.success('Test recommendation has been saved successfully');
                },
                error: function () {
                    NotificationManager.error("Sorry an error occurred while saving test recommendation");
                }.bind(this)
            });
        }
    },

    _saveRepairNote: function () {
        var fields = this.state.testRepairNotesFields;
        var data = {};
        var url = '/api/v1.0/test_repair_note/';
        var type = 'POST';
        for (var i = 0; i < fields.length; i++) {
            var key = fields[i];
            if (this.state.data[key]) {
                data[key] = this.state.data[key];
            }
        }

        if (Object.keys(data).length) {
            // There are several fields with the name test_type_id - differ them somehow
            data.test_type_id = data.repair_test_type_id;
            delete data.repair_test_type_id;
            data.test_result_id = this.state.data['id'];
            $.authorizedAjax({
                url: url,
                type: type,
                dataType: 'json',
                contentType: 'application/json',
                data: JSON.stringify(data),
                beforeSend: function () {
                },
                success: function () {
                },
                error: function (xhr, status, response) {
                    NotificationManager.error(response.error);
                }.bind(this)
            });
        }
    },

    _saveDiagnosis: function () {
        var fields = this.state.testDiagnosisFields;
        var data = {};
        var url = '/api/v1.0/test_diagnosis/';
        var type = 'POST';
        for (var i = 0; i < fields.length; i++) {
            var key = fields[i];
            if (this.state.data[key]) {
                data[key] = this.state.data[key];
            }
        }
        if (Object.keys(data).length) {
            // There are several fields with the name test_type_id - differ them somehow
            data.test_type_id = data.diagnosis_test_type_id;
            delete data.diagnosis_test_type_id;
            data.test_result_id = this.state.data['id'];
            $.authorizedAjax({
                url: url,
                type: type,
                dataType: 'json',
                contentType: 'application/json',
                data: JSON.stringify(data),
                beforeSend: function () {},
                success: function () {
                    NotificationManager.success('Test diagnosis has been saved successfully');
                },
                error: function (xhr, status, response) {
                    NotificationManager.error(response.error);
                }.bind(this)
            });
        }
    },

    _saveEquipmentStatus: function () {
        if (this.state.equipmentStatusChanged && this.state.data.equipment_status) {
            var that = this;
            // Get node_id from tree endpoint
            $.authorizedAjax({
                url: '/api/v1.0/tree/?equipment_id=' + that.state.data.equipment_id,
                type: "GET",
                dataType: 'json',
                contentType: 'application/json',
                success: function (result) {
                    that._saveEquipmentStatusToTree(result.result);
                },
                error: function () {
                    NotificationManager.error("Sorry an error occurred while getting node Id");
                }.bind(this)
            });
        }
    },

     _saveEquipmentStatusToTree: function (result) {
         // Save status to tree
         var that = this;
         if (result.length) {
             var data = {node_id: result[0].id, status: this.state.data.equipment_status};
             $.authorizedAjax({
                 url: 'tree/status/',
                 type: 'POST',
                 dataType: 'json',
                 contentType: 'application/x-www-form-urlencoded; charset=UTF-8',
                 data: data,
                 success: function (result) {
                     that._saveEquipmentStatusToEquipment(result);
                 },
                 error: function () {
                     NotificationManager.error("Sorry an error occurred while saving equipment status to tree");
                 }.bind(this)
             });
         }
    },

    _saveEquipmentStatusToEquipment: function () {
        // Save status to equipment
        var that = this;
        var data = {status: this.state.data.equipment_status};
        $.authorizedAjax({
            url: '/api/v1.0/equipment/' + that.state.data.equipment_id,
            type: 'POST',
            dataType: 'json',
            contentType: 'application/json',
            data: JSON.stringify(data),
            success: function () {
                NotificationManager.success('Equipment status has been saved successfully');
                that.setState({equipmentStatusChanged: false});
            },
            error: function () {
                NotificationManager.error("Sorry an error occurred while saving equipment status to equipment");
            }.bind(this)
        });
    },

    _onSubmit: function (e) {
        e.preventDefault();
        var errors = this._validate();
        if (Object.keys(errors).length != 0) {
            this.setState({
                errors: errors
            });
            return;
        }
        var xhr = this._save();
        if (xhr) {
            xhr.done(this._onSuccess)
                .fail(this._onError)
                .always(this.hideLoading)
        }
    },

    hideLoading: function () {
        this.setState({loading: false});
    },

    _onSuccess: function (data, status, xhr) {
        // this.refs.eqtype_form.getDOMNode().reset();
        // this.setState(this.getInitialState());
        NotificationManager.success('Saved');
        this.props.updateSource('/api/v1.0/test_result/?equipment_id=' + this.state.data.equipment_id);

        this.reloadSubforms();
        this.resetTestTypeSelectFields();
        this.cleanSubformsState();
    },

    reloadSubforms: function () {
        // Reload Repair Notes list
        this.refs.repairNotesForm.refs.testRepairNotesList.reloadList(this.refs.repairNotesForm.props.data.id);
        this.refs.repairNotesForm.setState(this.refs.repairNotesForm.getInitialState());

        // Reload Recommendation list
        this.refs.recommedationForm.refs.testRecommendationList.reloadList(this.refs.recommedationForm.props.data.id);
        this.refs.recommedationForm.setState(this.refs.recommedationForm.getInitialState());

        // Reload Diagnosis list
        this.refs.diagnosisForm.refs.diagnosisList.reloadList(this.refs.diagnosisForm.props.data.id);
        this.refs.diagnosisForm.setState(this.refs.diagnosisForm.getInitialState());
    },

    cleanSubformsState: function () {
        var stateData = this.state.data;
        var fields = [];
        fields = fields.concat(this.state.testDiagnosisFields)
                       .concat(this.state.testRecommendationFields)
                       .concat(this.state.testRepairNotesFields);

        for (var i = 0; i < fields.length; i++) {
            stateData[fields[i]] = null;
        }
        this.setState({data: stateData});
    },

    resetTestTypeSelectFields: function () {
        document.getElementById('diagnosis_test_type_id').value = "";
        document.getElementById('recommendation_test_type_id').value = "";
        document.getElementById('repair_test_type_id').value = "";
    },

    _onError: function (data) {
        var message = "Failed to create";
        var res = data.responseJSON;
        if (res.message) {
            message = data.responseJSON.message;
        }
        if (res.errors) {
            this.setState({
                errors: res.errors
            });
        }
    },

    _onChange: function (e) {
        var data = (this.state.data != null) ? this.state.data : {};
        if (e.target.type == 'checkbox') {
            data[e.target.name] = e.target.checked || null;
        } else if (e.target.type == 'radio') {
            data[e.target.name] = e.target.value || null;
        } else if (e.target.type == 'select-one') {
            data[e.target.name] = e.target.value || null;
        } else {
            data[e.target.name] = e.target.value || null;
        }

        var status = {data: data};
        if (e.target.name === 'equipment_status') {
            status.equipmentStatusChanged = true;
        }
        this.setState(status);
    },

    _setStateData: function (state) {
        // immutability-helper package might be used instead
        var newData = this.state.data;
        for (var field in state) {
            newData[field] = state[field];
        }
        this.setState({data: newData});
    },

    _validate: function () {
        var errors = {};
        return errors;
    },

    _formGroupClass: function (field) {
        var className = "form-group ";
        if (field) {
            className += " has-error"
        }
        return className;
    },

    componentDidMount: function () {
        this.serverRequest = $.authorizedGet('/api/v1.0/test_result/' + this.props.selectedRowId, this._addDataToStateAndGetIndicator, 'json');
    },

    _addDataToStateAndGetIndicator: function (result) {
        $.authorizedGet('/api/v1.0/campaign/' + result['result'].campaign_id, function (campaignResult){
            var data = result['result'];
            data.equipment_status = result['result'].equipment.status;
            this.setState({
                data: data,
                campaignIndicator: campaignResult['result'].created_by.name})
        }.bind(this), 'json');
    },

    _onDateTimeFieldChange: function (timestamp, fieldName) {
        var stateData = this.state.data;
        // If date is not valid (for example, date is deleted) string "Invalid date" is received
        if (timestamp == "Invalid date") {
            timestamp = null;
        } else if (timestamp) {
            // It is UNIX timestamp in milliseconds if dateTimeField was empty on load
            // Format date here instead of specifying format in DateTimeField,
            // because error is raised when format is specified, but date is null/undefined/empty string.
            if (/^\d+$/.test(timestamp)) {
                timestamp = parseInt(timestamp);
                timestamp = moment(timestamp).toISOString();
            }
            stateData[fieldName] = timestamp;    // Already formatted to ISO string
        }
        this.setState({data: stateData});
    },

    render: function () {
        var data = (this.state.data != null) ? this.state.data : {};
        return (
            <div>
                <input type="hidden" value={this.state.csrf_token}/>
                <div className="maxwidth padding-top-lg margin-bottom-xs">
                    <ul id="tabs" className="nav nav-tabs " data-tabs="tabs">
                        <li className="active"><a href="#tabs-1" data-toggle="tab"> Identification </a></li>
                        <li><a href="#tabs-2" data-toggle="tab"> Test values </a></li>
                        <li><a href="#tabs-3" data-toggle="tab"> Test repair notes </a></li>
                        <li><a href="#tabs-4" data-toggle="tab"> Recommendation notes </a></li>
                        <li><a href="#tabs-5" data-toggle="tab"> Diagnosis </a></li>
                    </ul>
                    <div id="my-tab-content" className="tab-content col-lg-12 nopadding">
                        <div id="tabs-1" role="tabpanel" className="tab-pane active ">
                            <EquipmentTestIdentificationForm data={data}
                                                             onChange={this._onChange}
                                                             onDateTimeFieldChange={this._onDateTimeFieldChange}/>

                            <div className="col-lg-6">
                                <TextField label="Indicator"
                                           value={this.state.campaignIndicator}
                                           name=""
                                           disabled/>
                            </div>
                        </div>
                        <div id="tabs-2" role="tabpanel" className="tab-pane">
                            <TestValuesForm testResultId={this.props.selectedRowId}
                                            testType={data.test_type}/>

                            <div className="col-lg-6">
                                <TextField label="Indicator"
                                           value={this.state.campaignIndicator}
                                           name=""
                                           disabled/>
                            </div>
                        </div>
                        <div id="tabs-3" role="tabpanel" className="tab-pane">
                            <EquipmentTestRepairForm data={data}
                                                     onChange={this._onChange}
                                                     onDateTimeFieldChange={this._onDateTimeFieldChange}
                                                     setStateData={this._setStateData}
                                                     ref="repairNotesForm"/>

                            <div className="col-lg-12">
                                <TextField label="Indicator"
                                           value={this.state.campaignIndicator}
                                           className="col-lg-6"
                                           name=""
                                           disabled/>
                            </div>
                        </div>
                        <div id="tabs-4" role="tabpanel" className="tab-pane">
                            <EquipmentTestDiagnosisForm data={data}
                                                        onChange={this._onChange}
                                                        setStateData={this._setStateData}
                                                        ref="recommedationForm"/>

                            <div className="col-lg-6">
                                <TextField label="Indicator"
                                           value={this.state.campaignIndicator}
                                           name=""
                                           disabled/>
                            </div>
                        </div>
                        <div id="tabs-5" role="tabpanel" className="tab-pane">
                            <EquipmentTestEqDiagnosisForm data={data}
                                                          onChange={this._onChange}
                                                          setStateData={this._setStateData}
                                                          ref="diagnosisForm"/>

                            <div className="col-lg-6">
                                <TextField label="Indicator"
                                           value={this.state.campaignIndicator}
                                           name=""
                                           disabled/>
                            </div>
                            <div className="col-lg-6">
                                <StatusSelectField label="Status"
                                                   value={data.equipment_status}
                                                   onChange={this._onChange}
                                                   name="equipment_status"/>
                            </div>
                        </div>
                    </div>
                </div>
                <div className="row">
                    <div className="col-md-1 pull-right nopadding padding-right-xs">
                        <FormGroup>
                            <Button bsStyle="success"
                                    type="submit"
                                    onClick={this._onSubmit}
                                >Save</Button>
                        </FormGroup>
                    </div>
                    <div className="col-md-1 pull-right ">
                        <FormGroup>
                            <Button bsStyle="danger"
                                    onClick={this.props.handleClose}
                                >Close</Button>
                        </FormGroup>
                    </div>
                </div>
            </div>
        );
    }
});

export default EquipmentTestForm;
